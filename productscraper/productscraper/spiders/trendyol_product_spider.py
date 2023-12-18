import scrapy
from productscraper.items import ProductItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ProductSpider(scrapy.Spider):
    name = 'trendyol_product_spider'

    def __init__(self, *args, **kwargs):
        super(ProductSpider, self).__init__(*args, **kwargs)

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)

    def start_requests(self):
        urls = getattr(self, 'urls', None)
        if urls is not None:
            urls = urls.split(',')
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        rendered_body = self.driver.page_source

        item = ProductItem()
        selector = scrapy.Selector(text=rendered_body)

        item['title'] = " ".join(selector.xpath('//h1[@class="pr-new-br"]/span/text()').getall())
        item['price'] = selector.css('.product-price-container span.prc-org::text').get() # it can be none
        print(item['price'])
        item['price_without_discount'] = selector.css('.product-price-container span.prc-dsc::text').get()

        if item['price'] is None or item['price'] == '':
            item['price'] = item['price_without_discount']

        item['main_image_url']   = selector.xpath('//div[@class="product-slide focused"]/img/@src').get()
        item['other_image_urls'] = selector.xpath('//div[@class="product-slide"]/img/@src').getall()

        item['rating_score'] = selector.css('.rating-line-count::text').get()
        item['review_count'] = selector.css('.total-review-count::text').get()
    
        yield item

    def closed(self, reason):
        self.driver.quit()

# Create a CrawlerProcess and pass the spider
process = scrapy.crawler.CrawlerProcess()
process.crawl(ProductSpider)
process.start()