import re
import requests
from lxml import etree
import pandas as pd
import os
import numpy as np
from urllib.request import urlretrieve
import time
import random


class Statistic_Yearbook_2021():
    root = os.getcwd()
    url_base = "http://www.stats.gov.cn/tjsj/ndsj/2021/"
    headers = {
        "X-Powered-By": "anyu.qianxin.com",
        "Content-Type": "text/html",
    }   
    
    def __init__(self):
        super(Statistic_Yearbook_2021,self).__init__()
        os.makedirs(os.path.join(self.root,"已下载"),exist_ok=True)
        self.html = self.html_etree_index
        self.urls = self.files_urls
        self.filter_titles()
        self.paths = self.files_save_path
        pass
    
    
    def filter_titles(self):
        df = pd.DataFrame(columns=["url","title"])
        df["url"] = self.files_urls
        df["title"] = self.files_titles_raw

        def rename_jianyaoshuoming(data):
            url = data['url']
            title = data['title']
            if "简要说明" in title:
                url_id = re.findall("\d{2}",str(url))[-1]
                title = url_id + "_简要说明"  
            
            if "主要统计指标解释" in title:
                url_id = re.findall("\d{2}",str(url))[-1]
                title = url_id + "_主要统计指标解释"  
            return title
            
        df["fixed_title"] = df.apply(rename_jianyaoshuoming,axis=1)
        self.files_titles_filtered = df["fixed_title"].tolist()    
    
    
    
    @property
    def rsp_index(self):
        url = "http://www.stats.gov.cn/tjsj/ndsj/2021/left.htm"
        rsp = requests.get(url=url,headers=self.headers)
        rsp.encoding = "gbk"
        return rsp
    
    @property
    def html_etree_index(self):
        rsp = self.rsp_index
        html = etree.HTML(rsp.text)
        return html
    
    @property
    def files_urls(self):
        xpath_links_pattern = '//ul[@id = "foldinglist"]/li/a/@href'
        xpath_links = self.html.xpath(xpath_links_pattern)
        xpath_links = [self.url_base + str(link) for link in xpath_links]
        def filter_urls(url):
            if str(url).endswith(".jpg"):
                url = url.replace(".jpg",".xls")      
            return url
        xpath_links = list(map(filter_urls,xpath_links))
        return xpath_links
    
    @property
    def files_titles_raw(self):
        xpath_titles_pattern = '//ul[@id = "foldinglist"]/li/a/text()'
        xpath_titles = self.html.xpath(xpath_titles_pattern)
        def filter_name(x):
            """过滤文件名,将\/:*?"<>|等字符替换为空"""
            x = re.sub(r"[\/:*?\"<>|]", "", x)
            return x
        xpath_titles = list(map(filter_name,xpath_titles))        
        return xpath_titles
    
    @property
    def files_save_path(self):
        def combine_unit_url(i):
            file_name = self.files_titles_filtered[i]
            file_extension = self.files_urls[i].split(".")[-1]
            return os.path.join(self.root,"已下载",file_name + "." + file_extension)
        return [combine_unit_url(i) for i in range(len(self.files_urls))]
    
    
    def unit_download(self,i):
        total = len(self.paths)
        def unit_download(i):
            url = self.urls[i]
            save_path = self.paths[i]
            urlretrieve(url,save_path)
            print(f"{i+1}/{total}已下载：",self.urls[i],self.files_titles_filtered[i])
        try:
            unit_download(i)
        except Exception as e:
            print(f"failed with : {self.urls[i]},{self.paths[i]}")
        
        