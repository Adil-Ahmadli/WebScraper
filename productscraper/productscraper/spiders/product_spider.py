import scrapy
from productscraper.productscraper.items import ProductItem


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
    
        item['title'] = response.css('h1.product-title::text').get()
        item['price'] = response.css('span.price::text').get()
        item['price_without_discount'] = response.css('span.original-price::text').get()
        item['main_image_url'] = response.css('#main-image::attr(src)').get()
        
        other_images = response.css('.other-images img::attr(src)').getall()
        item['other_image_urls'] = other_images
        item['rating_score'] = response.css('.rating-score::text').get()
    
        review_text = response.css('.review-count::text').get()
        item['review_count'] = review_text
    
        yield item
        