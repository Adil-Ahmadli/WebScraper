import scrapy
from productscraper.items import ProductItem
from scrapy_splash import SplashRequest

lua_script = """
function main(splash, args)
    splash:set_custom_headers({
      ["x-custom-header"] = "splash"
    })
    assert(splash:go(args.url))
    assert(splash:wait(5))
    while not splash:select('.product-price-container span.prc-dsc') do
        assert(splash:wait(5))
        print(".")
    end
    return {html = splash:html()}
end
"""

class ProductSpider(scrapy.Spider):
    name = 'product_spider'

    def start_requests(self):
        urls = getattr(self, 'urls', None)
        if urls is not None:
            urls = urls.split(',')
            for url in urls:
                yield SplashRequest(
                        url=url, 
                        callback=self.parse,
                        endpoint="execute",
                        args={ 'wait': 5, "timeout":120, 'lua_source': lua_script, "images":0, "resource_timeout":20},
                        splash_headers={"Connection":"keep-alive"}
                    )

    def parse(self, selector):
        item = ProductItem()

        with open("output.html", "w", encoding="utf-8") as f:
            f.write(selector.css("*").get())
        f.close()

        print("---------------")
        x = selector.css('img[loading="lazy"]::attr(alt)').get()
        value = selector.css(f'img[alt="{x}"]::attr(src)').get()
        print(value)
        print("---------------")

        item['title'] = " ".join(selector.xpath('//h1[@class="pr-new-br"]/span/text()').getall())
        item['price'] = selector.css('.product-price-container span.prc-org::text').get() # it can be none
        item['price_without_discount'] = selector.css('.product-price-container span.prc-dsc::text').get()

        x = selector.css('img[loading="lazy"]::attr(alt)').get()
        item['main_image_url'] = selector.css(f'img[alt="{x}"]::attr(src)').get()

        item['other_image_urls'] = selector.css(f'img[loading="lazy"]:not([alt="{x}"])::attr(src)').getall()
        item['rating_score'] = selector.css('.rating-line-count').get()
        item['review_count'] = selector.css('.total-review-count').get()
    
        yield item
