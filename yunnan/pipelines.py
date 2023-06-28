# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql
class YunnanPipeline:
    def open_spider(self,spider):
        # 创建连接
        self.client = pymysql.connect(
            host="localhost",
            port=3306,
            user="username",
            password="password",
            database="dabatase",
            charset="utf8"
        )
        self.cursor = self.client.cursor()

    def close_spider(self,spider):
        self.cursor.close()
        self.client.close()

    def process_item(self, item, spider):
        tablename = item["tablename"]
        # 创建表
        sql = f'create table {tablename} (guid varchar(40),title varchar(100),publishTime varchar(15),content varchar(20000));'
        try:
            self.cursor.execute(sql)
            # 改动数据后需要通过客户端对象进行提交操作
            self.client.commit()
            print("创建成功")
        except Exception as e:
            print(e)
        # 添加数据
        try:
            inster_sql = f"insert into {tablename} values (%s,%s,%s,%s);"
            self.cursor.execute(inster_sql,(item['guid'],item['title'],item['publishTime'],item['content']))
            # 改动数据后需要通过客户端对象进行提交操作
            self.client.commit()
            print("插入成功")
        except Exception as e:
            print(e)
        return item
