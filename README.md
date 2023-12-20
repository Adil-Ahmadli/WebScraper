Please install and activate python virtual environment:
`pip instal virtualenv`
`venv\Scripts\activate`

Install dependencies:
`pip install -r requirements.txt`

Install docker and pull `scrapinghub/splash`.
Then run docker image for scrapy splash with following command:
`docker run -it -p 8050:8050 --rm scrapinghub/splash --max-timeout 3600`

Run spiders:
`scrapy crawl product_spider -a urls='https://www.hepsiburada.com/defunc-true-music-bluetooth-kablosuz-kulaklik-p-HBCV000008RSDH?magaza=Hepsiburada'`


format is like following:
`scrapy crawl product_spider -a urls="url1,url2,url3..."`
`scrapy crawl n11_product_spider -a urls="url1,url2,url3..."`

product_spider and n11_product_spider are for trendyol and n11, respectively.