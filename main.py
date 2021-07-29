# coding=UTF-8
import os  # 用于创建文件夹
import sys
import time
import requests  # 请求网页
import threading
from lxml import etree  # 使用其中的xpath
from alive_progress import alive_bar #引入进度条模块

ver = '2.1'
threads = []
#网络请求头部信息
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.81 Safari/537.36"}

# 第一层，获取公众号全部文章的链接
def start(num):
    if os.path.exists('url.txt'):
        print("加载 url.txt 中...")
    else:
        print("未找到 url.txt ...")
    filename = 'url.txt'  # 之前存在本地的公众号源代码
    with open(filename, 'r', encoding='utf-8')as f:
        source = f.read()  # 读取内容
    html_ele = etree.HTML(source)  # xpath常规操作
    hrefs = html_ele.xpath('//div[contains(@data-type,"APPMSG")]/h4/@hrefs')  # 锁定元素位置
    
    # 存储文章链接以确定是否成功提取  
    if os.path.exists('lnks.txt'):
        print("加载 lnks.txt 中...")
    else:
        print("lnks.txt已生成，此文件用于验证提取链接并用于统计")
        for n in hrefs:
            with open("lnks.txt", 'a') as f:
                f.write(n+"\n")
    try:
        total_sum=-1
        for total_sum, line in enumerate(open(r"lnks.txt",'r')):
            total_sum+=1
    except:
        print("lnks.txt 不存在，你是不是把他删了")

    print("lnks.txt 加载完成")
    print("url.txt 加载完成")

    for i in hrefs:
        num += 1
        try:
            apply_one(i,num)
        except:
            continue
        print('第%d篇爬取完毕' % num)
        print("总进度: "+str(num)+"/"+str(total_sum))


# 第二层，解析单篇文章
def apply_one(url,num):
    response = requests.get(url, headers=headers)
    elements = etree.HTML(response.text)
    data_src = elements.xpath("/html/body/div/div/div/div/div/div/p/img/@data-src")
    #print(len(data_src))
    data_src = data_src[2:-1]
    #print(len(data_src))
    with alive_bar(len(data_src)) as bar:
        for src in data_src:
            try:
                bar()
                t=threading.Thread(target=download,args=(src, num))
                t.setDaemon(True)
                t.start()
                #download(src,num)  # 下载图片
            except:
                continue
            time.sleep(0.1)
        t.join()


# 第三层下载层
def download(src,num):
    response = requests.get(src, headers=headers)
    name = src.split('/')[-2]  # 截取文件名
    dtype = src.split('=')[-1]  # 截取图片类型
    name += '.'+dtype  # 重构图片名
    folder="pic/t"+str(num)+"/"
    # 检测图片名字已存在则跳过
    if os.path.exists(folder+name):
        #print(name+" 已存在.")
        return
    os.makedirs(folder, exist_ok=True)  # 当前目录生成文件夹
    with open(folder+name, 'wb')as f:
        f.write(response.content)


if __name__ == '__main__':
    print("GETWX Version : "+ver)
    status=input('确定开始? [Y/N]')
    if status == 'Y' or status == 'y':
        try: 
            lists = os.listdir('pic')  #列出目录的下所有文件和文件夹保存到lists
            lists.sort(key=lambda fn:os.path.getmtime('pic' + "\\" + fn))  #按时间排序
            dir_new = os.path.join('pic',lists[-1])  #获取最新的文件夹
            #print(dir_new[5:])
            dir_new_no=int(dir_new[5:])
            if os.path.exists(dir_new):
                print("第"+str(dir_new_no)+"篇已存在，将从下一篇继续")
                start(dir_new_no-1)
            else:
                start(0)
        except:
            start(0)
    else:
        sys.exit()