import requests  # 请求网页
import os  # 用于创建文件夹
from lxml import etree  # 使用其中的xpath

#网络请求头部信息
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.11 Safari/537.36"}

# 第一层，获取公众号全部文章的链接
def start():
    filename = 'url.txt'  # 之前存在本地的公众号源代码
    with open(filename, 'r', encoding='utf-8')as f:
        source = f.read()  # 读取内容
    html_ele = etree.HTML(source)  # xpath常规操作
    hrefs = html_ele.xpath('//div[contains(@data-type,"APPMSG")]/h4/@hrefs')  # 锁定元素位置
        
    num = 0
    for i in hrefs:
        num += 1
        try:
            apply_one(i,num)
            # # 存储文章链接以确定是否成功提取
            # with open("src.txt", 'a') as f:
            #     f.write(i+"\n")
        except:
            continue
        print('第%d篇爬取完毕' % num)


# 第二层，解析单篇文章
def apply_one(url,num):
    response = requests.get(url, headers=headers)
    elements = etree.HTML(response.text)
    data_src = elements.xpath("/html/body/div/div/div/div/div/div/p/img/@data-src")
    print(len(data_src))
    data_src = data_src[2:-1]
    print(len(data_src))
    for src in data_src:
        try:
            download(src,num)  # 下载图片
        except:
            continue


# 第三层下载层
def download(src,num):
    response = requests.get(src, headers=headers)
    name = src.split('/')[-2]  # 截取文件名
    print(name)
    dtype = src.split('=')[-1]  # 截取图片类型
    name += '.'+dtype  # 重构图片名
    folder="pic/t"+str(num)+"/"
    os.makedirs(folder, exist_ok=True)  # 当前目录生成doge文件夹
    with open(folder+name, 'wb')as f:
        f.write(response.content)


if __name__ == '__main__':
    start()
