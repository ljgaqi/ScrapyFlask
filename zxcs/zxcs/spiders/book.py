import scrapy
import re
import time
from scrapy.linkextractors import LinkExtractor
from zxcs.items import ZxcsItem

class BookSpider(scrapy.Spider):
    name = 'book'
    start_urls = ['http://www.zxcs.me/sort/55',
                  'http://www.zxcs.me/sort/23',
                  'http://www.zxcs.me/sort/25',
                  'http://www.zxcs.me/sort/26',
                  'http://www.zxcs.me/sort/27',
                  'http://www.zxcs.me/sort/28',
                  'http://www.zxcs.me/sort/29',]
    def parse(self, response):
        le=LinkExtractor(restrict_xpaths=('//*[@id="plist"]/dt/a'))
        links=le.extract_links(response)
        for link in links:
            yield scrapy.Request(url=link.url,callback=self.parse_book_info)
        patten_next_page=next_page_patten = re.compile('</span>  <a href="(.+?)">')
        next_page=patten_next_page.search(response.text).group(1)
        if next_page:
            yield scrapy.Request(url=next_page,callback=self.parse)

    def parse_book_info(self,response):
        item=ZxcsItem()
        item['book_url']=response.url
        item['book_sn']=int(response.url.split("/")[-1])

        patten_book=re.compile('《(.*?)》')
        item['book_name']=patten_book.search(response.text).group(1)
        patten_author=re.compile('作者：(.*?)</a>')
        item['book_author']=patten_author.search(response.text).group(1)

        item['book_class']=response.xpath('//*[@id="ptop"]/a/text()').extract()[1]
        patten_size=re.compile('【TXT大小】：(.*?) MB')
        item['book_size']=float(patten_size.search(response.text).group(1))

        item['book_time']=int(time.strftime('%Y%m%d',time.localtime(time.time())))
        # item['book_text']=response.xpath('//*[@id="content"]/p[3]').extract_first()

        item['book_image']=response.xpath('//*[@id="content"]/a/img/@src').extract_first()

        book_down_urls=response.xpath('//*[@id="content"]/div/div/p/a/@href').extract_first()
        yield scrapy.Request(url=book_down_urls,meta={'item':item},callback=self.parse_book_down)

    def parse_book_down(self,response):
        item=response.meta.get("item")
        item['file_urls']=response.xpath('//*[@class="downfile"]/a/@href').extract_first()
        yield item

