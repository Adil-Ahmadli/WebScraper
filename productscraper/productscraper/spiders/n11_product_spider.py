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
    while not splash:select('.priceDetail .priceContainer') do
        assert(splash:wait(5))
        print(".")
    end
    return {html = splash:html()}
end
"""

class N11ProductSpider(scrapy.Spider):
    name = 'n11_product_spider'

    def __init__(self, *args, **kwargs):
        super(N11ProductSpider, self).__init__(*args, **kwargs)

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

        item['title'] = " ".join(selector.xpath('//h1[@class="proName"]/text()').getall())
        item['price'] = selector.css('.priceDetail .priceContainer .oldPrice::text').get() # it can be none
        
        print("---------------")
        print(item['price'])
        print("---------------")

        item['price_without_discount'] = selector.css('.priceDetail .priceContainer .newPrice ins::text').get()

        if item['price'] is None or item['price'] == '':
            item['price'] = item['price_without_discount']

        item['main_image_url']   = selector.xpath('//div[@id="thumbSlider"]/div[@class="slick-list draggable"]/div[@class="slick-track"]/div[@class="slick-slide slick-current slick-active"]/div/div/img/@src').get()
        # fololwing can be none
        item['other_image_urls'] = selector.xpath('//div[@id="thumbSlider"]/div[@class="slick-list draggable"]/div[@class="slick-track"]/div[@class="slick-slide" or @class="slick-slide slick-active"]/div/div/img/@src/@src').getall() 

        item['rating_score'] = selector.css('.proRatingHolder .ratingScore::text').get() # it can be none
        item['review_count'] = selector.css('.proRatingHolder .ratingText span::text').get() # it can be none
    
        yield item
