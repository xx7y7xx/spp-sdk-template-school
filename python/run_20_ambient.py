# coding=utf-8

#导入所需模块
######################################
# 系统模块
import os
from xml.dom.minidom import parse

# 自定义模块
import common
import bucfg


########################################
###本文件用于动态加入环境光
######################################

########################################
#模板入口
def process():
	print""
	print common.encodeChinese(">>添加环境光")
	addAmb()
	print"--------------------------------------------"
	
########################
#读取light.xml数据
def addAmb():
	
	#变量定义
	r_a=""
	g_a=""
	b_a=""
	
	lightDoc = parse( bucfg.prdLightXml )       #读取xml
	
	ambient = lightDoc.getElementsByTagName("ambient") #获取节点
	
	if len(ambient)>0:
	
		for node in ambient[0].childNodes:
			if node.nodeName=="r":
				r_a = node.firstChild.nodeValue
			if node.nodeName=="g":
				g_a = node.firstChild.nodeValue
			if node.nodeName=="b":
				b_a = node.firstChild.nodeValue
				
	#编写light.js
	createAmbJs(r_a,g_a,b_a)
	
############################
#编写js文件
def createAmbJs(r,g,b):

	ambString=""
	ambString += 'CONFIG_LIGHT = {'
	ambString += '\n\t"ambient" :{'
	ambString += '\n\t\t"r" : '+r+','
	ambString += '\n\t\t"g" : '+g+','
	ambString += '\n\t\t"b" : '+b
	ambString += '\n\t}'
	ambString += '\n}'
	
	lightPath="%slight.js"%(bucfg.dataDir)      #存放在target/json/light.js
	common.writeNewFile(lightPath,ambString)
	