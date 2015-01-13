/**************************************************************************
 *
 *  This file is part of the UGE(Uniform Game Engine).
 *  Copyright (C) by SanPolo Co.Ltd. 
 *  All rights reserved.
 *
 *  See http://uge.spolo.org/ for more information.
 *
 *  SanPolo Co.Ltd
 *  http://uge.spolo.org/  sales@spolo.org uge-support@spolo.org
 *
**************************************************************************/
try{
	
	load('/logic/camera_entity.js');  //运行后加载，在路径是在同级目录下
	load('/logic/camera_effect.js');
	
	load('/logic/player_entity.js');
	load('/logic/player_effect.js');
	
	load('/logic/music_effect.js');
	load('/logic/music_bg.js');
	
	load('/logic/sand_table_effect.js');
	load('/logic/wander_effect.js');
	
	/* added by wangxin 2012-04-06 begin */
	load('/logic/star_entity.js'); 
	/* added by wangxin 2012-04-06 end */
	
	/*added by HouDongqiang 2012-04-12 begin*/
	load('/logic/search_effect.js');
	/* added by HouDongqiang 2012-04-012 end */
	
	/*	added by YueChaoFeng 2012-07-23 begin	*/
	load('/logic/full_view_effect.js');
	/*	added by YueChaoFeng 2012-07-23 begin	*/
	
	/*	added by YueChaoFeng 2012-08-23 begin	*/
	// load('/logic/guides_effect.js');
	/*	added by YueChaoFeng 2012-08-23 begin	*/
	
	/*	added by YueChaoFeng 2012-09-19 begin	*/
	// load('/logic/guides_entity.js');
	// load("/json/json_autorun.js"); 
	/*	added by YueChaoFeng 2012-09-19 begin	*/
	
	// bird fly in sky.
	load('/logic/bird_entity.js');
	load('/logic/bird_effect.js');
	
	//iCamera = Entities.CreateEntity(CAMERA);
	//player = Entities.CreateEntity(PLAYER);
 	//music_bg = Entities.CreateEntity(MUSIC_BG);

	var CreateEntities = function(){
		iCamera = Entities.CreateEntity(CAMERA);
		player = Entities.CreateEntity(PLAYER);
		music_bg = Entities.CreateEntity(MUSIC_BG);
		star = Entities.CreateEntity(STAR); //王鑫添加星星对象(2012-06-12)
		// guides = Entities.CreateEntity(GUIDES);
	}
	
	/* Modified by yuechaofeng begin	*/
	//判断是否为多线程加载
	var pWin = GUI.GUISheet.Get("word");
	var isThreadedLoader = false;
	if(CmdLine.GetOption("thread"))
	{
		isThreadedLoader = true;
	}
	
	if(isThreadedLoader)
	{
		iprint("多线程加载");
		// 多线程加载开始
		Loader.Load({
			stages : 
			[
				{
					name : "shader",
					// 加载时间权重
					weighing : 2, 
					filename : "/art/shaderlib.xml"
				}, 
				{
					name : "sound",
					weighing : 10,
					filename : "/art/soundlib.xml"
				}, 
				{
					name : "texture",
					weighing : 40,
					filename : "/art/materials.xml"
				},
				{
					name : "material",
					weighing : 2,
					filename : "/art/materials.xml"
				},
				{
					name : "meshfact",
					weighing : 40,
					filename : "/art/factorylib.xml"
				},
				{
					name : "meshobj",
					weighing : 2,
					filename : "/art/world.xml"
				}
			],
			onprocessWorldNode : onprocessWorldNode,
			onloadend : onloadend,
			onprogress : onprogress
		});
	}else{
		iprint("普通加载");
		// 在另外一个线程加载场景
		iThreadedLoader = Registry.Get('iThreadedLoader');
		iThreadedLoader.flags = 1;
		iThreadReturn = iThreadedLoader.LoadMapFile('/art/', 'world.xml');
		iThreadReturn.onfinish = function()
		{
			onloadend();
		}
	}
	
	//可以往<world>节点中添加新的节点
	function onprocessWorldNode(node_world)
	{
		var sector_world = node_world.GetChild("sector");
		var meshobjSet = sector_world.GetChildren("meshobj");
		if(!meshobjSet)
		{//没有任何meshObjs需要显示，报错退出！
			System.exitcode = 15;
			System.exitmsg = "no meshobjs in world!!";
			return false;
		}
		console.debug("Finding the mesh which camera sets to.");
	}
	
	//通过这个函数可以获得进度信息
	function onprogress(pe)
	{
		//以滚动条方式显示进度。
		CursesUI.ProgressBar(pe.total, pe.loaded);
		GUI.Windows.Get("hongfangkuai").SetProperty("CurrentProgress",pe.loaded/pe.total);
		GUI.Windows.Get("word").SetProperty("text_theme",parseInt(pe.loaded)+"%");
	}
	/* Modified by yuechaofeng end	*/
	//场景加载结束后调用的处理
	function onloadend()
	{
		pWin.SetProperty("text_theme","100%");
		var chang_word = GUI.Animations.GetAnimation("chang_word");
		if(chang_word){
			GUI.Animations.DestroyAnimationInstance(chang_word);
		}
		
		//为校园图片集创建图片集
		for(var act in JSON_SCHOOL.ui.schoolIntroduce.img.activity)
		{
			var act_name=act.substring(0,act.indexOf("."));
			GUI.Imagesets.CreateImageset(act_name,"/ui/data/image/activity/"+act);
		}
		for (var doc in JSON_SCHOOL.ui.schoolIntroduce.img.docenten)
		{
			var doc_name=doc.substring(0,doc.indexOf("."));
			GUI.Imagesets.CreateImageset(doc_name,"/ui/data/image/docenten/"+doc);
		}
		for (var sce in JSON_SCHOOL.ui.schoolIntroduce.img.scenery)
		{
			var sce_name = sce.substring(0,sce.indexOf("."));
			GUI.Imagesets.CreateImageset(sce_name,"/ui/data/image/scenery/"+sce);
		}
		
		//根据imageset文件创建图片对象
		for (var image in UI_IMAGESET){
			GUI.Imagesets.CreateImagesetFromXml(UI_IMAGESET[image]);
		}
		
		//根据image文件创建图片对象
		for(var index in UI_IMAGE){
			GUI.Imagesets.CreateImageset(index,UI_IMAGE[index]);
		}
		C3D.engine.Prepare();
		
		//创建entities
		CreateEntities();
		pWin.SetProperty("text_colour","FFF50701");
	    cd = Registry.Get('iCollideSystem');
		bVar = cd.InitializeCollision(engine);
		
		var actor = player.pcarray['pcactormove'].QueryInterface("iPcActorMove");
		
		var id = C3D.engine.SubscribeFrame(function(){
			if(!actor.IsMoving())
			{
				player.pcarray['pcmesh'].PerformAction('SetAnimation',['animation','stand'],['cycle',true],['reset', false]);
				// guides.pcarray['pcmesh'].PerformAction('SetAnimation',['animation','stand'],['cycle',true],['reset', false]);
			}
			else
			{
				if (actor.IsMovingForward())
				{
					if(isRunOrWalk){//走
						player.pcarray['pcmesh'].PerformAction('SetAnimation',['animation',"walk"],['cycle',true],['reset', false]);
						// if(player.isGuidesMode){
							// guides.pcarray['pcmesh'].PerformAction('SetAnimation',['animation',"walk"],['cycle',true],['reset', false]);
						// }else{
							// guides.pcarray['pcmesh'].PerformAction('SetAnimation',['animation',"stand"],['cycle',true],['reset', false]);
						// }
					}else{//跑
						player.pcarray['pcmesh'].PerformAction('SetAnimation',['animation',"run"],['cycle',true],['reset', false]);
					}
				}
				else if (actor.IsMovingBackward())
				{
					if(isRunOrWalk){//走
						player.pcarray['pcmesh'].PerformAction('SetAnimation',['animation',"walk"],['cycle',true],['reset', false]);
						// if(player.isGuidesMode){
							// guides.pcarray['pcmesh'].PerformAction('SetAnimation',['animation',"walk"],['cycle',true],['reset', false]);
						// }else{
							// guides.pcarray['pcmesh'].PerformAction('SetAnimation',['animation',"stand"],['cycle',true],['reset', false]);
						// }
					}else{//跑
						player.pcarray['pcmesh'].PerformAction('SetAnimation',['animation',"run"],['cycle',true],['reset', false]);
					}
				}
				else if (actor.IsStrafing())
				{
					if(isRunOrWalk){//走
						player.pcarray['pcmesh'].PerformAction('SetAnimation',['animation',"walk"],['cycle',true],['reset', false]);
						// if(player.isGuidesMode){
							// guides.pcarray['pcmesh'].PerformAction('SetAnimation',['animation',"walk"],['cycle',true],['reset', false]);
						// }else{
							// guides.pcarray['pcmesh'].PerformAction('SetAnimation',['animation',"stand"],['cycle',true],['reset', false]);
						// }
					}else{//跑
						player.pcarray['pcmesh'].PerformAction('SetAnimation',['animation',"run"],['cycle',true],['reset', false]);
					}
				}
			}
		});
		
		// @par3 : 模型在多少米内显示。
		MeshGen.SetMeshGenerate(player.pcarray['pcactormove'],player.pcarray['pcmesh'], 180);
	
		//设置world.xml文件中ambient 和 light数据为light.js中的值
		var sectorList = engine.sectors;
		var sector = sectorList.Get(0);
		//设置环境光的强度
		sector.ambient = ([CONFIG_LIGHT.ambient.r,CONFIG_LIGHT.ambient.g,CONFIG_LIGHT.ambient.b]);
		// 获得lightlist
		var lightlist = sector.lights ;
		// var light = lightlist.Get(0);
		//设置太阳光的强度
		// light.color = ([CONFIG_LIGHT.sun.r,CONFIG_LIGHT.sun.g,CONFIG_LIGHT.sun.b]);
		//创建一个灯光
		var col = new Math3.Color(0.30, 0.30, 0.30);
		var pos = JSON_SCHOOL.roleInitialize.role.position;
		player.light = C3D.engine.CreateLight("Lamp",  [pos.x , pos.y + 15 , pos.z], 150, col , 3);
		// 添加 light 到 lightlist
		lightlist.Add(player.light);
		
		//岳朝凤修改 加载场景时间的统计 2012-6-8
		//获取场景加载结束时的系统时间
		var finishTime = (new Date().getTime() - startTime)/1000;//毫秒转换成秒
		var bootTime = Math.round(finishTime);//取整
		iprint('\n' + "本次加载场景所需时间： " + bootTime + " 秒" + '\n');
		
		Event.Send("superpolo.application.startup");
	}
}catch(e){
	alert(e);
}