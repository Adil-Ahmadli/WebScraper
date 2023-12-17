import scrapy
from productscraper.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'product_spider'

    def start_requests(self):
        urls = getattr(self, 'urls', None)
        if urls is not None:
            urls = urls.split(',')
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = ProductItem()
        print(response.xpath('//h1').get())
        item['title'] = response.xpath('//h1[@class="zLHJIGKJ"]/text()[1]').get()
        item['price'] = response.css('MwknKR4m::text').get()
        item['price_without_discount'] = response.css('FteoagkF::text').get()

        if item['price'] is None or item['price'] == '':
            item['price'] = item['price_without_discount']

        item['main_image_url'] = response.xpath('//swiper-container[@class="main-carousel"]/swiper-slide['
                                                '@data-swiper-slide-index="0"]/img/@src').get()
        item['other_image_urls'] = response.xpath('//swiper-container[@class="main-carousel"]/swiper-slide['
                                                  '@data-swiper-slide-index!="0"]/img/@src').getall()

        item['rating_score'] = response.css('.rnUHKhce::text').get()
        item['review_count'] = response.css('.Euo7zJKH span b::text').get()
    
        yield item
