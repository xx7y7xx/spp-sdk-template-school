# coding=utf-8
# ################################################
# #导入dom模块
# ################################################
from xml.dom import *
from  xml.dom import minidom
from xml.dom.minidom import parse
import os
import shutil
import sys
import codecs
import getopt
import time
import sppbuild

# SPP_HOME = os.environ['SPP_HOME']
# pathProduct = '%s%s' % (SPP_HOME, '\\tools\\template\\school\\product\\')
# pathArt = '%s%s' % (SPP_HOME, '\\tools\\template\\school\\art\\')
# xmlPath = '%s%s'%( pathArt , 'position\\' )   #美术的xml

import common
import config		
import bucfg		# build 所需文件路径列表

#模块功能介绍：
# run_schooljson
#  		rolexml()						# 处理角色初始化位置信息
#  		schoolintroduce()		# 处理校园介绍数据
#  		sandcategory()			# 处理沙盘分类
#  		builddata()					# 处理建筑信息
#  		schoolhelp()				# 处理主菜单帮助信息
#  		minimap()					# 处理小地图
#  run_schoolnewhelp				# 处理新手帮助信息
#  run_schoolnewhelpenglish	# 新手帮助英文信息
#  run_searchdata					# 搜索数据处理
#  run_uisand							# 沙盘的数据
#  run_appendWorldxml			# world.xml中添加节点
#  run_loadbg							# 处理加载界面背景图
#  run_video							# 处理视频集
#  run_nocollision					# 处理无碰撞的模型
#  run_sand360						# 处理沙盘360全景
#  run_schoolroute					# 处理校园介绍中的路线指引
#  run_sequences						# 漫游路线
############################################################
xml2json = ""

##############################################################
# 该模块的入口
def build(tmpDir):
	global xml2json
	sys.path.append(tmpDir)

	import xml2json		#导入数据转换模块
	xml2json = xml2json
	
	# 判断需要的目录及文件是否存在
	if os.path.isdir(bucfg.targetDir):	# 判断 target 目录存在否
		
		# 拷贝 /spp_sdk/template/[templateName]/ 下的所有文件到 target 目录下；如果有临时文件的话，记得处理完了之后要删除掉
		print '-------------------------------'		
		print common.encodeChinese("正在复制模板文件...")
		print ''
		copyTemplate(tmpDir)  #调用拷贝模板函数
		print ''
		print common.encodeChinese("模板文件复制完成。")
		print ''	
		
		### 删除target下的svn目录
		removeSVN()
		
		######################################################################################
		# 这里需要获取 spp_sdk/tools/script/python/的路劲，
		# 扫描并动态加载这个路径下的所有模块，调用每个模块中的 process()
		moduleDir = "%spython"%(tmpDir)
		moduleList = os.listdir(moduleDir)
		moduleArray = [] # 存放以 run_ 开头，扩展名为 .py 的文件
		for module in moduleList:
			if module[-3:]==".py" and module[:4]=="run_":		# 找到文件名以 run_ 开头，扩展名为 .py 的文件
				id = int(module[4:].split("_")[0])
				runModule = module[:-3]							# 取到该文件的 module 名称
				moduleArray.append((id,runModule))
				
		# 排序 这个方法有兴趣可以研究下
		moduleArray.sort(key=lambda x:int(x[0]))
		
		#动态调用process方法
		for module in moduleArray:
			tmpmodule = __import__(module[1])					# 加载这个 module
			tmpmodule.process()									# 调用该 module 中名为 process（）的入口方法来执行编译
			
	else:
		print common.encodeChinese("target 目录不存在，--publish 操作失败！")
		os._exit(0)
	
	###############################################################################################
	###############################################################################################
	##  开始执行数据转换 和 编译
	
	# 遍历 target/json/目录下的所有 xml 文件并转换为javascript json 对象
	# dataDir = "%s\\target\\json\\"%(config.PROJECT_HOME)
	xmlList = os.listdir(bucfg.dataDir)
	for xmlFile in xmlList:
		if xmlFile.find('.svn') < 0 and xmlFile[-4:]=='.xml' and xmlFile.find("map") < 0:	# 过滤掉非 xml 文件
			# 取得文件名
			fileName = xmlFile[:-4]
			# 设置需要转换的文件路径
			inputFile = "%s%s"%(bucfg.dataDir, xmlFile)
			# 设置输出后的文件路径
			outputFile = "%s%s.js"%(bucfg.dataDir, fileName)
			# 执行转换操作
			xml2jsonFile(inputFile , outputFile)

	
	#编写bat
	burnGoPy="%spython\\"%(config.schoolTemDir) #burnGo.py的路径
	rebuildBat ="sppbuild --publish=school " #全部构建
	buildBat ="sppbuild --publish=school --build " #只构建数据	
	rebPacBat ="sppbuild --publish=school  --setup" #全部构建
	buildPacBat ="sppbuild --publish=school --build --setup" #只构建数据
	pacBat="makensis publish\CM.nsi"   #生成单独打包的bat
	cdPacBat ="makensis publish\CD.nsi"   #生成安装版单独打包的bat
	rebuildCD = "sppbuild --publish=school  --setupBurnGo" #全部构建光盘打包
	buildCD = "sppbuild --publish=school --build --setupBurnGo"#只构建数据光盘打包
	if not os.path.exists(config.PROJECT_HOME+"\\手动打包.bat"):
		#chenyang20121229:使用html来书写UI界面，activex来调用。
		#writeBat(rebuildBat,common.encodeChinese("\\全部构建.bat"))
		#writeBat(buildBat,common.encodeChinese("\\只构建数据.bat"))	
		#writeBat(rebPacBat,common.encodeChinese("\\全部构建+打包.bat"))
		#writeBat(buildPacBat,common.encodeChinese("\\只构建数据+打包.bat"))
		#writeBat(rebuildCD,common.encodeChinese("\\全部构建光盘打包.bat"))
		#writeBat(buildCD,common.encodeChinese("\\只构建数据光盘打包.bat"))
		dummy = 1
		
		if len(sppbuild.mergeList)<2:	
			#writeBat(pacBat,common.encodeChinese("\\手动打包.bat"))
			#writeBat(cdPacBat,common.encodeChinese("\\光盘版手动打包.bat"))
			dummy = 1
			
	print ''
	print ''
	print common.encodeChinese('项目模板编译完成！')
	print ''
	print ''
#####################################################################

# 自定义函数

# xml文件转换为json文件
def xml2jsonFile(input, output):
	try:
		# 读取所有的js文件
		txt = xml2json.parse(input , output)
		f = codecs.open(output, "w", "utf8")
		json_intercept = txt[1:-1]
	
		#先替换掉[padding='l:0 t:4 r:0 b:4']
		json_intercept = json_intercept.replace("[padding='l:0 t:4 r:0 b:4']","o__o")

		# 先判断 json_intercept 是否已经执行过替换了，或者是直接写成 json 格式的，不是从xml转换过来的
		# 没有执行过替换的文件都有一个共同的特点，在文件的开头中没有 = 号		
		json_front=json_intercept.split("{")[0]   
		if json_front.find("=")<0:
			json_intercept=SubsetStr(json_intercept) # 读取第一个花括号前的字符，将第引号去掉，冒号替换为等号

		json_intercept = json_intercept.replace("o__o","[padding='l:0 t:4 r:0 b:4']")
		json_intercept = json_intercept.replace('n__n','')
		json_intercept = json_intercept.replace('\"            [','[')
		json_intercept = json_intercept.replace('\"        [','[')
		json_intercept = json_intercept.replace('\"          ','\"')
		json_intercept = json_intercept.replace('\"              ','\"')
		json_intercept = json_intercept.replace('\"[','[')
		json_intercept = json_intercept.replace(']\"',']')
		json_intercept = json_intercept.replace('null,','')
		json_intercept = json_intercept.replace('null','')
		json_intercept = json_intercept.replace('//n','\\n\\\n')
		json_intercept = json_intercept.replace('a_a','&')
		
		#重写文件
		f.write(json_intercept)
		f.close()
		
	except:
		print ''
		print common.encodeChinese(config.ERR702)
		print common.encodeChinese("这有可能是数据文件格式错误导致的，请检查如下文件：")
		print ">>> "+input
		print ">>> "+output
		print ''
		common.pause()
		os._exit(0)

#替换“”：为=		
def SubsetStr(jsString):
	old_str = jsString.split("{")[0]
	new_str=old_str.replace("\"","").replace(":","=")
	other_str=jsString.lstrip(old_str)
	strs=new_str+other_str	
	return strs 


#	#
#@annotation 编写处理刻录的bat 
# #
def writeBat(content,fileName):
	# 生成bat脚本命令
	common.writeNewFile(config.PROJECT_HOME+fileName,content)
	
#拷贝模板文件
def copyTemplate(tmpDir):

	tmpLogicPath = "%stemplate"%(tmpDir)		# /spp_sdk/template/[templateName]/template
	target = "%s\\target"%(config.PROJECT_HOME)	# /[projectName]/target
	
	copyList = [
	"\\art\\fonts",
	"\\art\\models",
	"\\json",
	"\\logic",
	"\\ui",
	"\\flash360",
	"\\run.bat",
	"\\start.js"
	]
	
	for file in copyList:
		cmd = ""
		if file.find('.')<0:
			cmd = "xcopy /E /y /q "+tmpLogicPath+file+" "+target+file+"\\"
			res = os.system(cmd)
			if res == 1:
				print ''
				print common.encodeChinese('你可以尝试这样解决：')
				print common.encodeChinese(">> 系统中缺少xcopy.exe文件，\n>> 请下载  http://192.168.3.78/bak/xcopy.rar  这个文件并解压，\n>> 将xcopy.exe文件放到C:/windows/system32/目录下")
				common.pause()
				os._exit(0)
		else:
			shutil.copyfile(tmpLogicPath+file, target+file)	
	

### --------------------------------------------------------------------------------------	
### 针对svn1.6，删除target下的.svn
def removeSVN():	
	for (p,d,f) in os.walk(bucfg.targetDir):
		if p.find('.svn')>0:
			os.popen('rd /s /q %s'%p)