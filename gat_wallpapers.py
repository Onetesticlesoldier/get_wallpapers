# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 23:54:11 2021

@author: 帅比唐尧
"""

import requests      #爬虫
import re            #正则表达式
import os            #文件操作


def get_url(base_url):
    keyword=input("请输入英文关键词:(爬取排行榜请输入toplist)") 
    if keyword=='toplist': 	#获取排行榜的url模板
        base_url=base_url+keyword+'?page='
    else: 					#获取基于关键词的url模板
        base_url=base_url+'search?q='+keyword+'&page='
    return base_url         #返回模板


def get_img_url(base_url):
    header={ 
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74'
    } 									 #模拟浏览器头部，伪装成用户
    img_url_list=[]		 				 #创建一个空列表
    page_num=input("请输入下载页数:(一页24张)") 
    for num in range(1,int(page_num)+1): #循环遍历每页
        new_url=base_url+str(num)  		 #将模板进行拼接得到每页壁纸完整的url(实质:字符串的拼接)
        page_text=requests.get(url=new_url,headers=header).text #获取url源代码
        ex='<a class="preview" href="(.*?)"' 
        img_url_list+=re.findall(ex,page_text,re.S) 	#利用正则表达式从源代码中截取每张壁纸缩略图的url并全部存放在一个列表中 
    return img_url_list					 #返回列表


def download_img(img_url_list):
    header={ 
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74'
    } 											#模拟浏览器头部，伪装成用户
    keyword=input("请再次输入关键词以方便创建文件夹:")
    if not os.path.exists('D:/wallpapers'):     #在D盘目录下创建一个名为wallpapers的文件夹
        os.mkdir('D:/wallpapers')
    path='D:/wallpapers/'+keyword
    if not os.path.exists(path):				#在wallpapers文件夹下创建一个以关键词命名的子文件夹以存放此次下载的所有壁纸
        os.mkdir(path)
    for i in range(len(img_url_list)): 			#循环遍历列表，对每张壁纸缩略图的url进行字符串的增删获得壁纸原图下载的url  注：jpg或png结尾
        x=img_url_list[i].split('/')[-1]  		#获取最后一个斜杠后面的字符串
        a=x[0]+x[1] 							#获取字符串的前两位
        img_url='https://w.wallhaven.cc/full/'+a+'/wallhaven-'+x+'.jpg'  #拼接字符串,先默认jpg结尾
        code=requests.get(url=img_url,headers=header).status_code 
        if code==404:						    #若网页返回值为404，则为png结尾
            img_url='https://w.wallhaven.cc/full/'+a+'/wallhaven-'+x+'.png'
        img_data=requests.get(url=img_url,headers=header,timeout=20).content  #获取壁纸图片的二进制数据,加入timeout限制请求时间
        img_name=img_url.split('-')[-1] 		#生成图片名字
        img_path=path+'/'+img_name			    #生成图片存储路径
        with open(img_path,'wb') as fp:		    #('w':写入,'b':二进制格式)
            fp.write(img_data)
            print(img_name,'下载成功')     		#每张图片下载成功后提示


def main(url):
    base_url=get_url(url) 
    img_url_list=get_img_url(base_url) 
    download_img(img_url_list)

main('https://wallhaven.cc/')

#爬取壁纸时可能会有些慢（受网速影响），需要耐心等待！耐心等待！耐心等待！
