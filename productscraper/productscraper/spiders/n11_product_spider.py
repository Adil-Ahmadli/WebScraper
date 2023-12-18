import scrapy
from productscraper.items import ProductItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class N11ProductSpider(scrapy.Spider):
    name = 'n11_product_spider'

    def __init__(self, *args, **kwargs):
        super(N11ProductSpider, self).__init__(*args, **kwargs)

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

        item['title'] = " ".join(selector.xpath('//h1[@class="proName"]/text()').getall())
        item['price'] = selector.css('.priceDetail .priceContainer .oldPrice::text').get() # it can be none
        print(item['price'])
        item['price_without_discount'] = selector.css('.priceDetail .priceContainer .newPrice ins::text').get()

        if item['price'] is None or item['price'] == '':
            item['price'] = item['price_without_discount']

        item['main_image_url']   = selector.xpath('//div[@id="thumbSlider"]/div[@class="slick-list draggable"]/div[@class="slick-track"]/div[@class="slick-slide slick-current slick-active"]/div/div/img/@src').get()
        # fololwing can be none
        item['other_image_urls'] = selector.xpath('//div[@id="thumbSlider"]/div[@class="slick-list draggable"]/div[@class="slick-track"]/div[@class="slick-slide" or @class="slick-slide slick-active"]/div/div/img/@src/@src').getall() 

        item['rating_score'] = selector.css('.proRatingHolder .ratingScore::text').get() # it can be none
        item['review_count'] = selector.css('.proRatingHolder .ratingText span::text').get() # it can be none
    
        yield item

    def closed(self, reason):
        self.driver.quit()

# Create a CrawlerProcess and pass the spider
process = scrapy.crawler.CrawlerProcess()
process.crawl(N11ProductSpider)
process.start()