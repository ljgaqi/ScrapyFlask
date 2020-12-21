import scrapy
import re
import time
import math
import random
from scrapy.linkextractors import LinkExtractor
from javbus.items import JavbusItem

class JavSpider(scrapy.Spider):
    name = 'jav'
    start_urls = ['https://www.fanbus.in']
    web='https://www.fanbus.in'

    def parse(self, response):
        le=LinkExtractor(restrict_xpaths='//*[@id="waterfall"]')
        links=le.extract_links(response)
        for link in links:
            yield scrapy.Request(url=link.url,callback=self.parse_info)
        nextpage=response.xpath('//*[@id="next"]/@href').extract_first()
        if nextpage:
            nextpage=self.web+nextpage
            yield scrapy.Request(url=nextpage,callback=self.parse)


    def parse_info(self,response):
        item=JavbusItem()
        item['jav_sn']=response.xpath('//*[@class="row movie"]/div/p/span[2]/text()').extract_first()
        item['jav_name']=response.xpath('//*[@class="container"]/h3/text()').extract_first()

        patten_time=re.compile('長度:</span> (.*?)分鐘')
        item['jav_time']=int(patten_time.search(response.text).group(1))
        item['jav_date']=int(time.strftime('%Y%m%d',time.localtime(time.time())))

        patten_open_date=re.compile('發行日期:</span> (.*?)</p')
        item['jav_open_date']=patten_open_date.search(response.text).group(1)
        item['jav_url']=response.url
        item['image_urls']=response.xpath('//*[@class="bigImage"]/@href').extract_first()

        patten_gid=re.compile('var gid = (.*?);')
        gid=patten_gid.search(response.text).group(1)
        uc='0'
        img=item['image_urls']
        magnet_url = "https://www.fanbus.in/ajax/uncledatoolsbyajax.php?gid=" \
                     "{}&lang=zh&img={}&uc=0&floor={}".format(gid, img, math.floor(random.random() * 1000 + 1))
        yield scrapy.Request(magnet_url, meta={'item': item}, callback=self.parse_magnet)

    def parse_magnet(self,response):
        item = response.meta.get("item")
        elements = response.xpath("//tr")
        info = []
        if len(elements)>=1:
            for i in range(len(elements)):
                sourceInfo = {}
                #磁力链接
                mangetUrl = elements[i].xpath("td[1]/a/@href").extract_first()
                sourceInfo["magnetUrl"] = mangetUrl
                # #番号
                fanhao = item['jav_sn']
                sourceInfo["fanhao"] = fanhao

                #视频大小
                size = elements[i].xpath("td[2]/a/text()").extract_first().strip() if  elements[i].xpath("td[2]/a/text()").extract_first() else ""
                sourceInfo["size"] = size
                # #时间
                openTime = elements[i].xpath("td[3]/a/text()").extract_first().strip() if elements[i].xpath("td[3]/a/text()").extract_first() else ""
                sourceInfo["openTime"] = openTime
                info.append(sourceInfo)
        item["jav_cili"] = info
        yield item


