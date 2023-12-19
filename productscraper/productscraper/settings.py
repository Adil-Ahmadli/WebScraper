# Scrapy settings for productscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "productscraper"

SPIDER_MODULES = ["productscraper.spiders"]
NEWSPIDER_MODULE = "productscraper.spiders"
CONCURRENT_REQUESTS = 32

FEEDS = {
    'data.json': {'format': 'json', 'overwrite': True},
    'data.csv':  {'format': 'csv',  'overwrite': True},
}
SCRAPEOPS_APT_KEY = '87d36a24-5a54-434c-a8c2-100dc07c9225'
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 5

SCRAPEOPS_PROXY_ENABLED = True

ROTATIING_PROXY_LIST = [
    '72.210.221.223:4145',
    '192.252.214.20:15864',
    '192.252.216.81:4145',
    '142.54.237.34:4145',
    '107.181.168.145:4145',
    '74.119.147.209:4145',
    '72.206.181.123:4145',
    '98.170.57.249:4145',
    '68.71.254.6:4145',
    '142.54.226.214:4145',
    '103.174.81.66:8080'
    "179.53.207.195:8080",
    "34.64.85.78:3128",
    "148.251.192.186:80",
    "14.207.97.109:8080",
    "178.62.229.28:3128",
    "74.96.118.126:80",
    "12.7.109.1:9812",
    "5.149.81.90:8080",
    "161.132.125.244:8080",
    "181.81.245.194:4128",
    "103.48.69.113:82",
    "66.225.254.16:80",
    '115.127.83.142:1234',
    '87.247.251.240:3128',
    '181.13.141.234:80',
    "158.180.16.252:80",
    "82.113.157.122:31280",
    "94.23.1.178:3128",
    "179.189.48.253:8080",
    "64.56.150.102:3128",
    "81.12.40.250:8080",
    "124.198.91.170:29268",
    "154.0.154.113:8080",
    "35.201.24.9:80",
    "51.38.241.250:54321",
    "83.126.54.155:8080",
    "103.108.88.41:8080",
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

SPLASH_URL = "http://localhost:8050"
PROXY_POOL_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'




# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 0.25  # 250 ms of delay
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = True
#REDIRECT_ENABLED = True
#RETRY_ENABLED = True

#DOWNLOADER_HTTP2_ENABLED = True
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "productscraper.middlewares.ProductscraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "productscraper.middlewares.ProductscraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "productscraper.pipelines.ProductscraperPipeline": 300,
    'productscraper.pipelines.ExcelExportPipeline': 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
