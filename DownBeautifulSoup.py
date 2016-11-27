from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import os
import re

"""
使用Python爬虫抓取BeautifulSoup中文文档(http://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/index.html)
"""
download_directory = "beautifulsoup"
base_url = "http://www.crummy.com/software/BeautifulSoup/bs4/doc.zh"


def get_html():
    """
    获取网页BeautifulSoup对象
    :return:BeautifulSoup对象
    """
    global base_url
    html = urlopen(base_url + "/index.html")
    bs_obj = BeautifulSoup(html, "lxml")
    return bs_obj


def download_html():
    """
    下载页面
    """
    global base_url
    urlretrieve(base_url + "/index.html", download_directory + "/" + "index.html")


def download_css(download_directory, bs_obj):
    """
    下载页面所有的css文件
    :param download_directory: 下载文件夹
    :param bs_obj: BeautifulSoup对象
    """
    links = bs_obj.findAll("link", {"rel": "stylesheet"})
    for link in links:
        if link["href"] is not None:
            href = link["href"]
            file_dir = os.path.dirname(download_directory + "/" + href)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            urlretrieve(base_url + "/" + href, download_directory + "/" + href)


def download_javascript(download_directory, bs_obj):
    """
    下载页面所有的javascript文件
    :param download_directory: 下载文件夹
    :param bs_obj: BeautifulSoup对象
    """
    links = bs_obj.findAll("script", {"type": "text/javascript"}, src=True)
    for link in links:
        if link["src"] is not None:
            href = link["src"]
            file_dir = os.path.dirname(download_directory + "/" + href)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            urlretrieve(base_url + "/" + href, download_directory + "/" + href)


download_html()
soup = get_html()
download_css(download_directory, soup)
download_javascript(download_directory, soup)
