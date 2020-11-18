# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter


class HistoryTianqiPipeline:
    """
       同步操作
       """

    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect('localhost', 'root', '123456', 'weather_dazhou',charset="utf8")  # 有中文要存入数据库的话要加charset='utf8'
        # 创建游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # sql语句
        insert_sql = """
           replace into  dazhou(date,temp_max,temp_min,weather,wind) VALUES(%s,%s,%s,%s,%s)
           """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (item['date'], item['temp_max'], item['temp_min'], item['weather'],
                                         item['wind']))
        # 提交，不进行提交无法保存到数据库
        self.conn.commit()


    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
