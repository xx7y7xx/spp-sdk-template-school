# coding=utf-8import os,sysimport configimport commonimport bucfgdef process():		print '-------------------------------'	print common.encodeChinese('>> 整理搜索所需数据')	print ''	domString   = "<SEARCH_DATA>"	domString += getCategorys()	domString += "\n</SEARCH_DATA>"	domString=domString.replace("&","a_a")	common.writeNewFile(bucfg.targetDir+"json/ui_search.xml", domString)		print ''# 遍历出所有的 category ; 即，遍历 /src/prodcut/sandTable 下所有的目录# 生成沙盘信息分类def getCategorys():	domString = ""	dirs = os.listdir(bucfg.prdSandTable)	for dir in dirs:		if dir.find(".svn")>-1:			continue		tmplist = dir.split("@")		dirPath = bucfg.prdSandTable+dir		domString += getOneSeed(dirPath)		return domString			# 遍历 /src/product/ui/sandTable/1@...@.../ 目录中的所有文件# 生成某个分类下的具体信息searchdata_num = -1def getOneSeed( dirPath ):	global searchdata_num	domString = ""	dirs = os.listdir(dirPath)	tmpstr = ""	for dir in dirs:		if dir[-4:]==".txt":			fname = dir.split(".")[0]			if dir.find("url")>0:				continue			if tmpstr.find(fname)==-1:				searchdata_num += 1				numstr = str(searchdata_num)				domString += "\n\t<n__n"+numstr+">"				domString += getSeedCnEn(dirPath+"\\"+fname)				domString += "\n\t</n__n"+numstr+">"				tmpstr += fname					return domString# 根据 /src/product/ui/sandTable/1@...@.../中文名.cn.txt 中的“中文名”分别# 读取中文介绍、英文介绍def getSeedCnEn(file):	enFile = file+".en.txt"	cnFile = file+".cn.txt"	domString   = ""	if os.path.isfile(enFile) and os.path.isfile(enFile):		domString += "\n\t\t\t\t<chinese>"		domString += "\n\t\t\t\t\t<name>"+common.readFileFirstLine(cnFile)+"</name>"		domString += "\n\t\t\t\t\t<intro>"		domString += common.readFileExceptFirst(cnFile)		domString += "\n\t\t\t\t\t</intro>"		domString += "\n\t\t\t\t</chinese>"		domString += "\n\t\t\t\t<english>"		domString += "\n\t\t\t\t\t<name>"+common.readFileFirstLine(enFile)+"</name>"		domString += "\n\t\t\t\t\t<intro>"		domString += common.readFileExceptFirst(enFile)		domString += "\n\t\t\t\t\t</intro>"		domString += "\n\t\t\t\t</english>"	else:		print file+".en.txt/.cn.txt    is  not found !"		os._exit(0)	return domString	