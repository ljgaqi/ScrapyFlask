import pymysql
import urllib.request

path='d:/py/fengniao/feng/image/'

con=pymysql.connect(host='liaqi.3322.org',user='root',passwd='3813121',port=13307,db='Scrapy_DB')
cur=con.cursor()
curlen=cur.execute("SELECT f_sn,image_urls FROM fengniao")
for cu in cur:
    image_name=cu[0]
    image_urls=cu[1]
    filename='{}{}'.format(path,image_name+'.jpg')
    print(filename+' begin download!')
    urllib.request.urlretrieve(image_urls,filename)

con.close()
