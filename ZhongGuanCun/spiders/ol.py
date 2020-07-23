# -*- coding: utf-8 -*-
import scrapy, datetime
from scrapy_redis.spiders import RedisSpider

from ZhongGuanCun.items import ZhongguancunItem


class OlSpider(RedisSpider):
    name = 'ol'
    # allowed_domains = ['detail.zol.com.cn']
    # start_urls = ['http://detail.zol.com.cn/subcategory.html']

    redis_key = 'price'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(OlSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        second_node_list = response.xpath('//*[@class="mod-cate_item"]/ul')

        second_cat_list = [i.xpath('./li[1]/a/text()').get() for i in second_node_list]
        second_cat_url_list = ['http://detail.zol.com.cn' + i.xpath('./li[1]/a/@href').get() for i in second_node_list]
        second_cat_dict = {k: v for k, v in zip(second_cat_list, second_cat_url_list)}

        for s_cat, s_url in second_cat_dict.items():
            print('二级分类：{}'.format(s_cat))
            yield scrapy.Request(url=s_url, callback=self.parse_classify, meta={
                's_cat': s_cat,
                'second_cat_url': s_url
            })

    def parse_classify(self, response):
        s_cat = response.meta['s_cat']
        s_url = response.meta['second_cat_url']
        third_node_list = response.xpath('//div[contains(@class,"mod-cate-box")]/ul/li')
        cat_list = [s_cat + '>' + i.xpath('./h3/a/text()').get() for i in third_node_list]
        third_cat_url_list = ['http://detail.zol.com.cn' + t.xpath('./h3/a/@href').get() for t in third_node_list]
        third_cat_dict = {k: v for k, v in zip(cat_list, third_cat_url_list)}
        for t_cat, t_url in third_cat_dict.items():
            # print('完整分类：{}'.format(t_cat))
            yield scrapy.Request(url=t_url, callback=self.parse_brand, meta={
                'third_cat_url': t_url,
                't_cat': t_cat,
                'second_cat_url': s_url
            })

    def parse_brand(self, response):
        th_cat = response.meta['t_cat']

        brand_node_list = response.xpath('//*[@id="J_ManuFilter"]/div/a[position()>1]')

        brand_name_list = [th_cat + '>' + i.xpath('./text()').get() for i in brand_node_list]
        brand_url_list = ['http://detail.zol.com.cn' + i.xpath('./@href').get() for i in brand_node_list]
        brand_cat_dict = {k: v for k, v in zip(brand_name_list, brand_url_list)}

        for all_cat, url in brand_cat_dict.items():
            # print('产品分类：{}'.format(all_cat))
            yield scrapy.Request(url=url, callback=self.parse_product, meta={
                'second_cat_url': response.meta['second_cat_url'],
                'third_cat_url': response.meta['third_cat_url'],
                'category': all_cat,
                'brand_url': url
            })

    def parse_product(self, response):
        product_node_list = response.xpath('//*[@id="J_PicMode"]/li')
        for product_node in product_node_list:
            item = ZhongguancunItem()
            item['产品分类'] = response.meta['category'].replace(': ','')
            item['对应分类链接'] = response.meta['second_cat_url']
            item['对应二级分类链接'] = response.meta['third_cat_url']
            item['对应品牌分类链接'] = response.meta['brand_url']
            item['产品链接'] = 'http://detail.zol.com.cn' + product_node.xpath('./a[1]/@href').get()
            item['产品名称'] = product_node.xpath('./h3/a/@title').get()
            item['产品参考价'] = product_node.xpath('./div[1]/span[2]/b[2]/text()').get()
            item['产品评分'] = product_node.xpath('./div[2]/span[2]/text()').get()
            item['产品评论量'] = product_node.xpath('./div[2]/a[1]/text()').get()
            item['产品介绍'] = product_node.xpath('./h3/a/span/text()').get()
            item['下载时间'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield item
        # 翻页
        part_url = response.xpath('//*[@class="next"]/@href').get()
        if part_url:
            next_url = 'http://detail.zol.com.cn' + part_url
            yield scrapy.Request(url=next_url, callback=self.parse_product)
