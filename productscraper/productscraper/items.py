import scrapy


class ProductItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    price_without_discount = scrapy.Field()
    main_image_url = scrapy.Field()
    other_image_urls = scrapy.Field()
    rating_score = scrapy.Field()
    review_count = scrapy.Field()
