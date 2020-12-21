# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class ZxcsPipeline:
    def __init__(self):
        self.host = '192.168.1.141'
        self.port = 3307
        self.db = 'Scrapy_DB'
        self.user = 'root'
        self.password = '3813121'

    def open_spider(self, response):
        self.dbcon = pymysql.connect(self.host, self.user, self.password, port=self.port, db=self.db)
        self.cur = self.dbcon.cursor()

    def process_item(self, item, spider):
        # id=item['book_sn']
        # print(id)
        # self.cur.execute("SELECT * FROM zxcsinf WHERE book_sn=%s" %id)
        self.insert_db(item)
        return item

    def insert_db(self, item):
        values = (
            item['book_sn'],
            item['book_name'],
            item['book_author'],
            item['book_class'],
            item['book_size'],
            item['book_time'],
            item['book_image'],
            item['book_url'],
            item['file_urls'],
        )
        sql = 'INSERT INTO zxcsinfo VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cur.execute(sql, values)

    def close_spider(self, spider):
        self.dbcon.commit()
        self.dbcon.close()

