# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from scrapy.exceptions import DropItem


class JavbusPipeline(object):
    def __init__(self):
        self.host='192.168.1.141'
        self.port=3307
        self.db='Scrapy_DB'
        self.user='root'
        self.password='3813121'
    def open_spider(self,response):
        self.maria_connect=pymysql.connect(self.host, self.user, self.password, port=self.port, db=self.db)
        self.cur=self.maria_connect.cursor()
    def process_item(self,item,spider):
        self.id=item['jav_sn']
        self.cur.execute("SELECT * FROM jav WHERE jav_sn LIKE '%s'" %(self.id))
        results=self.cur.fetchone()
        if results==None:
            self.insert_db(item)
            self.insert_cili(item)
            return item
        else:
            print(self.id + '已在数据库中，不再下载！')
            raise DropItem()
    def insert_db(self,item):
        info_values=(
            item['jav_sn'],
            item['jav_name'],
            item['jav_time'],
            item['jav_date'],
            item['jav_open_date'],
            item['jav_url'],
            item['image_urls']
        )
        print(item['jav_sn']+'保存到数据库中！')
        main_sql='INSERT INTO jav VALUES (%s,%s,%s,%s,%s,%s,%s)'
        self.cur.execute(main_sql,info_values)
        self.maria_connect.commit()

    def insert_cili(self,item):
        cili_info = item['jav_cili']

        for cili in cili_info:
            cav=(
                cili['fanhao'],
                cili['size'],
                cili['openTime'],
                cili['magnetUrl']
            )
            cili_sql ='INSERT INTO javcili VALUES (%s,%s,%s,%s)'
            self.cur.execute(cili_sql, cav)
            self.maria_connect.commit()

    def close_spider(self,spider):

        self.maria_connect.close()