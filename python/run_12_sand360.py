# coding=utf-8import os,sys,codecsimport shutil# from xml.dom import *from xml.dom import minidomfrom xml.dom.minidom import parseimport commonimport configimport bucfg# 处理360全景沙盘展示# 读取 /src/product/sand360目录下的所有文件夹和文件# 读取 /src/product/position/sand_position_360.xmldef process():		print ''	print '-------------------------------'	print common.encodeChinese('>> 处理 360 全景沙盘')	print ''		# 先判断 /src/product/position/sand_position_360.xml 文件是否存在，	# 如果不存在则不生成这部分数据，	# 对应的 template 中就不会显示这个功能	if not os.path.isfile(bucfg.posSand360):		print common.encodeChinese('没有发现沙盘的数据，跳过处理')		return		# 读取xml文件的内容	try:		f = codecs.open(bucfg.posSand360, "r", "utf8")		sand360xmlString = f.read() 		f.close()	except:		common.ansixml2utf8xml(bucfg.posSand360)		f = codecs.open(bucfg.posSand360, "r", "utf8")		sand360xmlString = f.read() 		f.close()		jsonString = "FLASH_PANORAMA = {"		# 先遍历 /src/product/sand360 目录下的分类目录	sand360Dir = "%ssand360\\"%(bucfg.productDir)	cateList = os.listdir(sand360Dir)	index = 0	for cate in cateList:		if cate.find(".svn")>-1:			continue		cateArr = cate.split("@")		jsonString += "\n\t\""+ str(index) +"\" : {"		jsonString += "\n\t\t\"chinese\": \""+ cateArr[1] +"\"," 		jsonString += "\n\t\t\"english\": \""+ cateArr[2] +"\","		jsonString += "\n\t\t\"genus\" : ["				sand360Files = os.listdir(sand360Dir + cate)		for sand360File in sand360Files:			if sand360File.find(".png")>-1:				continue			if sand360File.find(".svn")>-1:				continue			fileName = sand360File[:-4]			names = fileName.split("@")			# 如果在 sand_position_360.xml 文件中已经定义了这个文件，则添加该数据，否则不添加			if sand360xmlString.find(names[0].decode("gbk")):				jsonString += "\n\t\t\t{"				jsonString += "\n\t\t\t\t\"name\" : {"				jsonString += "\n\t\t\t\t\t\"chinese\" : \""+ names[0] +"\","				jsonString += "\n\t\t\t\t\t\"english\" : \""+ names[1] +"\""				jsonString += "\n\t\t\t\t},"				# 获得360在沙盘中的UI的坐标				jsonString += getPosition(names[0]).decode("gbk").encode("utf8")				# 判断URL是外链接 .txt的文件				# 还是当前目录下的swf文件 .swf的文件				ext = common.getFilenameExt(sand360File)				url = ""				allfilepath = sand360Dir + cate + "\\" + sand360File				if ext ==".swf":					url = names[1].replace(" ","_")					# 将这个 .swf 文件拷贝到 /target/					newfilename = "%sflash360\\360\\%s"%(bucfg.targetDir, url+".swf")					shutil.copyfile( allfilepath , newfilename)					# url 格式化为 "吉利大学 -- 汽车学院%qichexueyuan"  这个格式， title -- chinese % filename					url = common.readFileFirstLine(bucfg.prdInit) + " -- " + names[0] + "%" + url				elif ext == ".txt":					url = common.readFileFirstLine(allfilepath)				jsonString += "\n\t\t\t\t\"url\" : \""+url+"\""				jsonString += "\n\t\t\t},"				# 添加一个空节点，避免一个节点时json自动转数组为对象		jsonString += getEmptyNode()				jsonString += "\n\t\t]"		jsonString += "\n\t},"		index += 1		jsonString += "\n}"		newFilePath = "%sjson\\sand_360.js"%(bucfg.targetDir)	common.writeNewFile(newFilePath, jsonString.decode("gbk").encode("utf8"))	print ''	############################################################################# 根据中文名称取 sand_position_360.xml 中的坐标def getPosition(cname):	jsonString =""		sandDoc = parse( bucfg.posSand360 )			labels = sandDoc.getElementsByTagName("label")	for lab in labels:		if cname.decode("gbk")==lab.getAttribute("id"):			for sub in lab.childNodes:				if sub.nodeType==1:	# 判断xml节点类型如果是 Element					pos = sub.firstChild.nodeValue					posArr = pos[1:-1].split(",")					jsonString += "\n\t\t\t\t\"position_x\" : \""+posArr[0]+"\","					jsonString += "\n\t\t\t\t\"position_y\" : \""+posArr[1]+"\","					jsonString += "\n\t\t\t\t\"position_z\" : \""+posArr[2]+"\","			break	return jsonString############################################################################# 生成一个空节点def getEmptyNode():	jsonString =""	jsonString += "\n\t\t\t{"	jsonString += "\n\t\t\t\t\"name\" : {"	jsonString += "\n\t\t\t\t\t\"chinese\" : \"\","	jsonString += "\n\t\t\t\t\t\"english\" : \"\""	jsonString += "\n\t\t\t\t},"	jsonString += "\n\t\t\t\t\"position_x\" : \"\","	jsonString += "\n\t\t\t\t\"position_y\" : \"\","	jsonString += "\n\t\t\t\t\"position_z\" : \"\","	jsonString += "\n\t\t\t\t\"url\" : \"\""	jsonString += "\n\t\t\t},"	return jsonString'''"0": {		"chinese": "公寓",         "english": "apartment",		"genus" :[			{				"name": {					"chinese": "汇康公寓", 					"english": "HuiKangapartment"				}, 				"position_x": "-81.78631591796875", 				"position_y": "0.18376421928405762", 				"position_z": "23.375259399414062", 				"url": "吉利大学 -- 汽车学院%qichexueyuan"			},			{				"name": {					"chinese": "汇文公寓", 					"english": "HuiWenapartment"				}, 				"position_x": "-81.78631591796875", 				"position_y": "0.18376421928405762", 				"position_z": "23.375259399414062", 				"url": "http://lib.uibe.edu.cn/attchment/web_lib_capture/uibelibrary.html"			}		]		    },'''