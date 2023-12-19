import scrapy
from productscraper.items import ProductItem
from scrapy_splash import SplashRequest
from urllib.parse import urlencode
 
API_KEY = '9963810e06443673febd6bfb0628d6b0'

def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'apiParams':{ 'autoparse': True, 'retry_404': True }}
    proxy_url = 'https://async.scraperapi.com/jobs' + urlencode(payload)
    return proxy_url

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
#lua_script = quote(lua_script)

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
        print(selector.css('img[loading="lazy"]').getall())
        print("---------------")
        item['title'] = " ".join(selector.xpath('//h1[@class="pr-new-br"]/span/text()').getall())
        item['price'] = selector.css('.product-price-container span.prc-org::text').get() # it can be none
        item['price_without_discount'] = selector.css('.product-price-container span.prc-dsc::text').get()
        item['main_image_url']   = selector.xpath('//div[@class="product-slide focused"]/img').get() ## some has only one phote and different selec
        item['other_image_urls'] = selector.xpath('//div[@class="product-slide"]/img').getall()
        item['rating_score'] = selector.css('.rating-line-count').get()
        item['review_count'] = selector.css('.total-review-count').get()
    
        yield item
