# coding=utf-8
import os, sys, codecs
import shutil
from xml.dom.minidom import parse

import common
import config
import bucfg


#处理漫游路线的数据格式
def process():

	print '-------------------------------'
	print common.encodeChinese('>> 整理漫游路线数据')
	print ''
	
	# 拷贝 xml到art下的wander下
	if os.path.isdir(bucfg.wanNewDir):
		shutil.rmtree(bucfg.wanNewDir)
	
	shutil.copytree(bucfg.wanDir,bucfg.wanNewDir)
	
	# 直接写json
	createWanderJson()
	print ""
	
#获取从sequences中数据和product下的名字

def createWanderJson():

	count=0		#编写xml
	domString   = "JSON_WANDER= {"
	domString += " \n\t\"wander_route\": {"
	
	for wan in os.listdir(bucfg.wanNewDir):		
		relPath= os.path.join(bucfg.wanNewDir.split("\\")[-1],wan)
		filePath= os.path.join(bucfg.wanNewDir,wan)
		wan_dic=wan.split(".xml")[0]
		
		#区别其他文件
		if wan_dic.find("Camera00") < 0 or filePath.find(".svn") > 0 :
			continue
			
		count+=1
		# 动态添加 <one_manyou_one>
		domString += " \n\t\t\""+dic_[wan_dic]+"\": {"
		domString   += " \n\t\t\t\"sequence_name\": \""+wan.split(".")[0]+" \","
		domString += createNameTag(dic_wander[wan_dic])           #			"sequence_frame" : 1000,
		domString +=createFrame(filePath)

		# 动态添加路径
		domString   += " \n\t\t\t\"file_path\": "
		domString   += "\"/art/"+relPath.replace("\\","/")+"\""	
		
		if count !=4:
			domString   += "\n\t\t\t},"	
		else:
			domString   += "\n\t\t\t}"	
				
	domString   += "\n\t}"	
	domString   += "\n}"	
	common.writeNewFile(bucfg.dataDir+"json_wander.js",domString)	
	print ''
	
	
	

#添加漫游按钮的中英文	
def createNameTag(dir):
	dir=os.path.join(bucfg.prdSeq,dir)
	
	print common.encodeChinese('正在处理的文件：'), dir
	
	domString = ""
	f = open (dir, 'r' )  
	fileList = f.readlines()
	print fileList
	
	if not common.isFileEncodingGBK(dir) :
		print common.encodeChinese('[ERROR] 这个文件的编码有问题，请使用Notepad++转换成ANSI的：\n\t'), dir
		common.exit()
	
	cName=fileList[0].replace("\n","").decode("gbk").encode("utf-8")
	eName=fileList[1].replace("\n","").decode("gbk").encode("utf-8")
	
	domString   += " \n\t\t\t\"chinese_name\": \""+cName+" \","
	#是否有英文名
	if len(fileList)>1:
		domString += " \n\t\t\t\"english_name\": \" "+eName+"\","
	else:
		domString  += " \n\t\t\t\"english_name\": \" \","
		
	domString  += " \n\t\t\t\"sequence_time\": "
	
	#是否又设定了时间
	if len(fileList)>2 :
		if fileList[2].find("\n")>0:
			sequence_time=fileList[2].replace("\n","")+","
		else:
			sequence_time="84000,"	 #按照每秒24帧/s计算现在
	else:
		sequence_time="84000,"	
	
	domString   += sequence_time	
	f.close()
	
	return domString

#添加坐标	
def createFrame(dir):
	domString=""
	
	#打开导出的漫游路线坐标的xml
	seqDom = parse(dir)
	seqNode=seqDom.getElementsByTagName("wander")[0]
	count=0
	#添加坐标和名字标签
	#添加漫游时间
	for node in seqNode.childNodes:
		if "wander" in (node.nodeName):
			count+=1
	#添加帧数
	domString+="\n\t\t\t\"sequence_frame\": "+str(count-1)+","
	return domString
	


#没有swith我就用字典把xml和txt的对应一致
dic_  = {   'wander_Camera001'   : 'one_manyou_one',
		 'wander_Camera002'     : 'one_manyou_two',
		 'wander_Camera003' : 'two_manyou_one',
		 'wander_Camera004'   : 'two_manyou_two'
 }

dic_wander  = {   'wander_Camera001'   : common.encodeChinese('漫游路线一.txt'),
		 'wander_Camera002'     : common.encodeChinese('漫游路线二.txt'),
		 'wander_Camera003' : common.encodeChinese('漫游路线三.txt'),
		 'wander_Camera004'   : common.encodeChinese('漫游路线四.txt')
 }