# coding=utf-8
import os, sys, codecs
import shutil
from xml.dom.minidom import parse

import common
import config
import bucfg

dataDir = "%s\\target\\json\\"%(config.PROJECT_HOME)
#处理漫游路线的数据格式
def process():
	#读取url的txt文件内容
	createUrlJson(bucfg.url)

#编写json文件
def createUrlJson(urlContent):
	#直接编写json文件
	jsonString=""
	jsonString+="URL={"
	jsonString+="\n\t\thome_url:\""+(urlContent[0]).split("\n")[0]+"\"" 
    #判断txt的内存在几个url
	if len(urlContent)>1:
		jsonString+=","
		jsonString+="\t\t"
		jsonString+="\n\t\tvideo_url:\""+(urlContent[1]).split("\n")[0]+"\""
	jsonString+="\n}"
	f=open(dataDir+"url.js","w")
	f.write(jsonString)
		
		
		
# 1	
# URL={
# 2	
        # home_url:"http://www.uibe.edu.cn/";
		
# 3	
        # video_url:"http://www.uibe.edu.cn/uibe_Video/UIBE_info_in_CN/video.html"
# 4	
# }