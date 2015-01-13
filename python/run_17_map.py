# coding=utf-8
import os, sys, codecs
import shutil

import common
import config
import bucfg
import checkbuild
import run_100_log
import xml2json

#########################################

# 设置需要转换的文件路径
inputFile = "%smaxpos.xml"%(bucfg.positionDir)
# 设置输出后的文件路径
outputFile = "%smap.js"%(bucfg.dataDir)
# 处理小地图
def process():
	try:
		print '-------------------------------'
		print common.encodeChinese('>> 小地图')
		print ''
		# print  outputFile
		# 直接将xml转为js
		txt = xml2json.parse(inputFile , outputFile)
		jsString = txt[1:-1]
		f = codecs.open(outputFile, "w", "utf8")
		# print jsString
		oldTxt=' "maxposition": {'
		newTxt="MINI_MAP= {"    #
		if jsString.find(newTxt) < 0:
			jsString=jsString.replace(oldTxt,newTxt+modMapJs())
			print ""
		#替换 开头    maxposition= {
		f.write(jsString)
		f.close()
	except:
		print outputFile+config.ERR500

# 补充js对象
	# "index" : "1",
	# "data": {
		# "1": {
			# "areaSize" :"{{0,1024},{0,922}}", 
			# "height": "922",
			# "width": "1024"
		# }, 
		# "2": {
			# "areaSize" :"{{0,1536},{0,1383}}", 
			# "height": "1383",
			# "width": "1536"
		# }, 
		# "3": {
			# "areaSize" :"{{0,2048},{0,1844}}", 
			# "height": "1844",
			# "width": "2048"
		# }, 
		# "4": {
			# "areaSize" :"{{0,2560},{0,2305}}", 
			# "height": "2305",
			# "width": "2560"
		# }, 
		# "5": {
			# "areaSize" :"{{0,3072},{0,2766}}", 
			# "height": "2766",
			# "width": "3072"
		# }
	# }
	
#添加对象
def modMapJs():
	mapString = ""
	mapString += '\n\t"index" : "1",'
	mapString += '\n\t"data": {'
	mapString += '	\n\t\t"1": {'
	mapString += '	\n\t\t\t"areaSize" :"{{0,1024},{0,922}}", '
	mapString += '\n\t\t\t"height": "922",'
	mapString += '\n\t\t\t"width": "1024"'
	mapString += '\n\t\t}, '
	mapString += '\n\t\t"2": {'
	mapString += '	\n\t\t\t"areaSize" :"{{0,1536},{0,1383}}", '
	mapString += '\n\t\t\t"height": "1383",'
	mapString += '\n\t\t\t"width": "1536"'
	mapString += '\n\t\t}, '
	mapString += '\n\t\t"3": {'
	mapString += '\n\t\t\t"areaSize" :"{{0,2048},{0,1844}}", '
	mapString += '	\n\t\t\t"height": "1844",'
	mapString += '\n\t\t\t"width": "2048"'
	mapString += '\n\t\t}, '
	mapString += '\n\t\t"4": {'
	mapString += '	\n\t\t\t"areaSize" :"{{0,2560},{0,2305}}", '
	mapString += '	\n\t\t\t"height": "2305",'
	mapString += '\n\t\t\t"width": "2560"'
	mapString += '\n\t\t}, '
	mapString += '\n\t\t"5": {'
	mapString += '	\n\t\t\t"areaSize" :"{{0,3072},{0,2766}}", '
	mapString += '	\n\t\t\t"height": "2766",'
	mapString += '\n\t\t\t"width": "3072"'
	mapString += '\n\t\t}'
	mapString += '\n\t},'
	
	return mapString