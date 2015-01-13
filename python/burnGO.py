# coding=utf-8

#                                                                本模块负责光盘版安装包的处理
#
#-------------------------------------------------------------------------------------------
import os,shutil,codecs,sys
import common 
import config 

#变量定义
#------------------------------------------------------------------------------------------------
burnGoDir="%s\\Burn_Edition\\"%(config.PROJECT_HOME)
web360="%s\\web360"%(config.PROJECT_HOME)
publishDir = "%s\\publish\\"%(config.PROJECT_HOME)
indexHtml="%s\\index.html"%(web360)
indexHdHtml="%s\\index_hd.html"%(web360)
autorunFile="%s\\autorun.inf"%(publishDir)
proName=config.PROJECT_HOME.split("\\")[-1]

#---------------------------------------------------------------------------------------
#程序入口
def process():

	print common.encodeChinese("刻录版安装包操作------------------")
	
	# 修改index.xml文件的按钮事件 
	ModifyHtml()
	
	# 添加自动运行inf 
	content=""
	content +="[autorun]"
	
	import bucfg
	nameTxt="%s\\setupInfo\\setupName.txt"%(bucfg.productDir)
	proName=common.readFile(nameTxt)
	proName=proName[0:-6]     #去掉最后4个字符
	content +="\nopen="+proName+common.encodeChinese("光盘版.exe")
	common.writeNewFile(autorunFile,content)

	
#----------------------------------------------------------------------------------------------------	
def copySchool():

	if not os.path.exists(web360):
		print"" 
		print common.encodeChinese("操作被终止.......")
		print common.encodeChinese("error！360网站不存在，请先完成360网站的build")
		print "-------------------------------------------"
		
	# 复制360网站 
	print ""
	print common.encodeChinese("正在拷贝web360网站文件........")
	os.system("xcopy  /E/y /q "+web360+" "+pubweb360Dir)
	
	# 复制3D客户端
	# print 
	# print encodeChinese("正在拷贝3D客户端文件.....")
	# os.system("xcopy  /E/y /q "+pubweb360Dir+" "+burnGoDir)


#-------------------------------------------------------------------------------------------------------------------------------------		
#修改index.html		
def ModifyHtml():

	content=common.readFile(indexHtml)
	old_con='onclick="download()"'
	new_con="onclick=\"Run('run.bat')\" "
	
	if content.find("run.bat") < 0:
		content=content.replace(old_con,new_con)
		content=content.replace("</body>",'\t<script type="text/javascript" src="js/run.js"></script>\n</body>')
	print ""
	common.writeNewFile(indexHdHtml,content)
	print ".."


	