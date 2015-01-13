# coding=utf-8
#---------------------------------------------------------------

# 本模块负责将星星贴图的复制到主场景的materials.xml中，为了是避免加载顺序导致的星星的的贴图加载失败。

#-----------------------------------------------------------------
#模块调用
import os, sys, codecs
import shutil

# 自定义
import common
import config
import bucfg
#---------------------------------------------------------------

#变量

#-----------------------------------------------------------------
materialsXml = "%sart\\materials.xml"%(bucfg.targetDir)        #materials.xml路劲定义

# main()
#--------------------------------------------------------------------------------

def process():

	print common.encodeChinese(">>复制星星贴图")
	
	try:	
		xmlString=common.readFile(materialsXml)
		
		if  xmlString.find("star")<0 :                                                      #避免重复添加
		
			xmlString = xmlString.replace("</textures>",addTextures())           #以替换字符的形式添加
			xmlString = xmlString.replace("</materials>",addMaterials())
			common.writeNewFile(materialsXml,xmlString)                               #写入文件
			
	except:
		print sys.exc_info()[0],sys.exc_info()[1] ##一般来说这样就足够了
		print common.encodeChinese("哇，出错了..........")                                    #异常打印
		
#---------------------------------------------------------------------------------	
#拼接texture

def addTextures():
	txtString = ''
	txtString += '\t<texture name=\"star2.png\">' 
	txtString += '\n\t  <file>/art/models/star/textures/star2.png</file>' 
	txtString += '\n\t  <alpha><binary/></alpha>'
	txtString += '\n\t</texture>'
	txtString += '\n\t<texture name=\"star1.png\">'
	txtString += '\n\t  <file>/art/models/star/textures/star1.png</file>' 
	txtString += '\n\t  <alpha><binary/></alpha>'  
	txtString += '\n\t</texture>'
	txtString += '\n</textures>'                                             #不能只顾替换，忘了添加，否则你就完了！！！
	return txtString

#--------------------------------------------------------------------------------------
# 拼接material 

def addMaterials():

	matString=""
	matString +="\t<material name=\"Material_M2_star\">" 
	matString +="\n\t  <texture>star2.png</texture>" 
	matString +="\n\t  <shader type=\"ambient\">ambient</shader>" 
	matString +="\n\t</material>" 
	matString +="\n\t<material name=\"Material_M1_star\">" 
	matString +="\n\t  <texture>star1.png</texture>" 
	matString +="\n\t  <shader type=\"ambient\">ambient</shader>" 
	matString +="\n\t</material> "   
	matString +="\n</materials> "                                             #不能只顾替换，忘了添加，否则你就完了！！！

	return   matString
	
	
# ------------------------------------------------------------------------------------------------	
	# 添加对照

	#texture
	
	# <texture name="star2.png">
      # <file>/art/models/star/textures/star2.png</file>
	   # <alpha><binary/></alpha>
    # </texture>
    # <texture name="star1.png">
      # <file>/art/models/star/textures/star1.png</file>
	   # <alpha><binary/></alpha>
    # </texture>
	
	
	# material
    # <material name="Material_M2_star">
      # <texture>star2.png</texture>
	   # <shader type="ambient">ambient</shader>
    # </material>
    # <material name="Material_M1_star">
      # <texture>star1.png</texture>
	  	# <shader type="ambient">ambient</shader>
    # </material> 