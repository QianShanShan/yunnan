import subprocess

spider_list = ["getZbycList", "ggzy.yn.gov", "getZbggList","getGzsxList","getPbbgList","getZbJgGgList","getContractList"]
for spider in spider_list:
    subprocess.run(['scrapy', 'crawl', spider])