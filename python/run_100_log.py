# coding=utf-8

#导入所需模板
import common
import os
import bucfg
import shutil
import datetime
import time
###################################################

########################################
###本文件用于生成build日志 打印缺失文件等报错信息
######################################
nowTime=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
fileList=[]
message=""

#模板入口
def process():
	print""
	print"------------------------------"
	createLog(fileList)
	# print file
	print"--------------------------------------------"
	
def createLog(fileList):
	#生成log日志
	logStr ="【sppbuild blog】"
	# print fileList.length
	if len(fileList)>0:
		logStr +=common.encodeChinese("缺少以下文件目录，已从模板进行自动拷贝模拟文件，请及时修改真实数据.")
		for file in fileList:
			logStr +="\n"+message
			logStr +="\n"+str(file)
			logStr +="\n--------------------------------------【"+nowTime+"】"
	else:
		logStr +="--------------------------------------"
		logStr +=common.encodeChinese("")
		logStr +="\n---------------------------【"+nowTime+"】"
		
	common.writeNewFile(bucfg.targetDir+"\\blog.txt",logStr)