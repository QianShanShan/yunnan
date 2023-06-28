import scrapy
import json
import re
class GetpbbglistSpider(scrapy.Spider):
    name = "getPbbgList"
    allowed_domains = ["ggzy.yn.gov.cn"]
    start_urls = ["https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getPbbgList"]

    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://ggzy.yn.gov.cn",
            "Pragma": "no-cache",
            "Referer": "https://ggzy.yn.gov.cn/tradeHall/tradeList",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        }

    def start_requests(self):
        '''
        重写请求，添加参数
        :return:
        '''
        for url in self.start_urls:
            # 进行循环确定爬取的页数
            for page in range(1, 10):
                data = {
                    "hildType": "",
                    "cityId": "018",
                    "endTime": "",
                    "industryCode": "",
                    "pageNum": page,
                    "pageSize": 10,
                    "startTime": "",
                    "title": "",
                    "tradeType": "gcjs"
                }
                formdata = json.dumps(data)
                yield scrapy.Request(url=url, method='POST', headers=self.headers, body=formdata, callback=self.parse)

    def parse(self, response):
        data = response.json()
        data_list = data['value']['list']
        for da in data_list:
            # 创建item
            item = {}
            # 获得表名
            item['tablename'] = response.url.split('/')[-1]
            # 获得详情页的guid
            guid = da['guid']
            item['guid'] = guid
            # 获取标题
            item['title'] = da['publicityname']
            # 获取时间
            item['publishTime'] = da['publicitystarttime']
            yield scrapy.Request(
                url=f'https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/findPbbgByGuid?guid={guid}',
                headers=self.headers, callback=self.sec_parse, meta={'item': item})

    def sec_parse(self, response):
        item = response.meta['item']
        data = response.json().get('value')
        # 获取内容
        content = ''.join(re.findall('>(.*?)<', data['publicitycontent']))
        item['content'] = content
        yield item
