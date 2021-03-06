# -*- coding: utf-8 -*-

# Scrapy settings for ZhongGuanCun project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ZhongGuanCun'

SPIDER_MODULES = ['ZhongGuanCun.spiders']
NEWSPIDER_MODULE = 'ZhongGuanCun.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'ZhongGuanCun (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 300

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs


DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 300
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'ZhongGuanCun.middlewares.ZhongguancunSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'ZhongGuanCun.middlewares.ZhongguancunDownloaderMiddleware': 543,
    'ZhongGuanCun.middlewares.MyUserAgentMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'ZhongGuanCun.pipelines.ZhongguancunPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 1
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 配置数据库
# mongo:
MONGO_URL = '127.0.0.1:27017'
MONGO_DBNAME = 'WangdamaTest'
MONGO_COLLECTION = '中关村在线IT产品报价信息'

# 实现分布式断点续爬
"""
1，普通爬虫继承RedisSpider爬虫类
2，注释allowed_domains和start_urls
3，重写__init__()方法
4，修改以下配置文件
5，正常启动爬虫(可以多个窗口开启)命令一样scrapy crawl zol 使得爬虫就位
6，启动redis数据库，执行——>lpush或者rpush redis_key 爬取的域名
    eg: lpush zol_it_price http://detail.zol.com.cn/subcategory.html 使得所有节点爬虫真正开启
    程序自动从数据库获取请求
要开启mongo跟redis数据库"""
#  1， redis:
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
#  2，添加以下配置，注释上面的ITEM_PIPELINES
"""
参数说明：
RFPDupeFilter # 指纹去重类
Scheduler # 调度器类
SCHEDULER_PERSIST # 是否持久化请求队列和指纹集合
RedisPipeline # 管道类
"""
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
ITEM_PIPELINES = {
    'ZhongGuanCun.pipelines.ZhongguancunPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}
