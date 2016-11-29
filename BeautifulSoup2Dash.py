import os, sqlite3

import shutil

import re
from bs4 import BeautifulSoup

"""
将抓取的BeautifulSoup中文文档转换为Dash文档(http://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/index.html)
"""


def copy_file(src, doc_name):
    if os.path.exists("dashdoc/" + doc_name):
        shutil.rmtree("dashdoc/" + doc_name)
    shutil.copytree(src, "dashdoc/" + doc_name + "/Contents/Resources/Documents")


def create_xml(doc_name, CFBundleIdentifier, CFBundleName, DocSetPlatformFamily, dashIndexFilePath):
    xml = []
    xml.append(r'<?xml version="1.0" encoding="UTF-8"?>' + '\n')
    xml.append(
        r'<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">' + '\n')
    xml.append(r'<plist version="1.0">' + '\n')
    xml.append(r'<dict>' + '\n')
    xml.append(r'	<key>CFBundleIdentifier</key>' + '\n')
    xml.append(r'	<string>' + CFBundleIdentifier + r'</string>' + '\n')
    xml.append(r'	<key>CFBundleName</key>' + '\n')
    xml.append(r'	<string>' + CFBundleName + r'</string>' + '\n')
    xml.append(r'	<key>DocSetPlatformFamily</key>' + '\n')
    xml.append(r'	<string>' + DocSetPlatformFamily + r'</string>' + '\n')
    xml.append(r'	<key>dashIndexFilePath</key>' + '\n')
    xml.append(r'	<string>' + dashIndexFilePath + r'</string>' + '\n')
    xml.append(r'	<key>isDashDocset</key>' + '\n')
    xml.append(r'	<true/>' + '\n')
    xml.append(r'</dict>' + '\n')
    xml.append(r'</plist>' + '\n')
    xml_str = ''.join(xml)

    file = open("dashdoc/" + doc_name + '/Contents/Info.plist', 'w')
    file.write(xml_str)


def create_db(doc_name, index_html_name):
    conn = sqlite3.connect("dashdoc/" + doc_name + '/Contents/Resources/docSet.dsidx')
    cur = conn.cursor()

    try:
        cur.execute('DROP TABLE searchIndex;')
    except:
        pass
    cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
    cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

    docpath = "dashdoc/" + doc_name + '/Contents/Resources/Documents/'

    page = open(os.path.join(docpath, index_html_name)).read()
    soup = BeautifulSoup(page, "lxml")

    href_link = set()

    for tag in soup.find("div", {"class": "sphinxsidebar"}).findAll("a", href=True):
        name = tag.text.strip()
        name = re.sub("\n+", " ", name)
        name = re.sub(" +", " ", name)
        if re.match("\[[0-9]*\]", name):
            continue
        if name.startswith("http:"):
            continue
        if len(name) > 1:
            path = tag.attrs['href'].strip()
            if path not in href_link:
                href_link.add(path)
                if path != 'index.html':
                    if path.startswith("#"):
                        path = "index.html" + path
                    cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                                (name, 'Keyword', path))
                    print('name: %s, path: %s' % (name, path))

    any = re.compile('.*')
    for tag in soup.find_all('a', {'href': any}):
        name = tag.text.strip()
        name = re.sub("\n+", " ", name)
        name = re.sub(" +", " ", name)
        if re.match("\[[0-9]*\]", name):
            continue
        if name.startswith("http:"):
            continue
        if name.startswith("#"):
            name = "#" + name
        if len(name) > 1:
            path = tag.attrs['href'].strip()
            if path not in href_link:
                href_link.add(path)
                if path != 'index.html':
                    cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                                (name, 'Keyword', path))
                    print('name: %s, path: %s' % (name, path))

    conn.commit()
    conn.close()


copy_file("beautifulsoup", "beautifulsoup_zh.docset")
create_xml("beautifulsoup_zh.docset", "beautifulsoup", "BeautifulSoup_zh", "python",
           "index.html")
create_db("beautifulsoup_zh.docset", "index.html")
