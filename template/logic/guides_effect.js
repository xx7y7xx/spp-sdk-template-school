/**************************************************************************
 *  This file is part of the UGE(Uniform Game Engine) of SPP.
 *  Copyright (C) by SanPolo Co.Ltd. 
 *  All rights reserved.
 *  See http://spp.spolo.org/ for more information.
 *
 *  SanPolo Co.Ltd
 *  http://spp.spolo.org/  sales@spolo.org spp-support@spolo.org
**************************************************************************/
try{
	(function(){
		/*	点击导游按钮---判断导游模式----全程导游 or 区域导游	*/
		Event.Subscribe(function(e){
			player.role_ok = "false";
			//根据name获取Box meshobj
			var meshobj = C3D.engine.FindMeshObject('sky');
			//判断Box是否存在，存在执行if语句，不存在执行else语句
			if(meshobj){
				//声明变量
				var vec_Length = 50;
				for(var index in REGIONAL_GUIDES_DATA){
					if( typeof(REGIONAL_GUIDES_DATA[index]) == "undefined" )
					{
						Event.Send({
							name : "ui.entire_journey_guides.display",
							player : player,
							show : true
						});
						break;
					}else{
						//获取人物坐标
						var position = player.pcarray['pcmesh'].position;
						//人物的坐标向量
						var perPos_vec = new Math3.Vector3( position.x , position.y , position.z);
						//从json文件中获取meshobj的坐标
						var meshPosX = REGIONAL_GUIDES_DATA[index].mesh_pos.pos_x;
						var meshPosY = REGIONAL_GUIDES_DATA[index].mesh_pos.pos_y;
						var meshPosZ = REGIONAL_GUIDES_DATA[index].mesh_pos.pos_z;
						//模型的坐标向量
						var meshPos_vec = new Math3.Vector3( meshPosX , meshPosY , meshPosZ);
						//计算当前坐标向量与触发区域导游的坐标向量差
						var vec_Len = perPos_vec.Subtract(meshPos_vec);
						var len = vec_Len.Length();
						var matName = REGIONAL_GUIDES_DATA[index].matName;
						var materialbox = C3D.engine.FindMaterial(matName);
						//满足条件---执行区域导游
						if(len <= vec_Length && materialbox){
							player.regGui_id = index;
							player.isRegGuides = true;
							Event.Send({
								name : "ui.regional_guides.display",
								player : player,
								id : index,
								show : true
							});
							break;
						}else{//不满足条件---执行全程导游
							Event.Send({
								name : "ui.entire_journey_guides.display",
								player : player,
								show : true
							});
						}
					}
				}
			}
		},"player.effect.guides.judgement");
		
		/*	初始化自动寻路环境	*/
		Event.Subscribe(function(e){
			var actor = e.player;
			var posX = e.posX;
			var posY = e.posY;
			var posZ = e.posZ;
			//获得iPcPathFinder和iPcSteer对象
			player.iPcPathFinder = player.pcarray['pcpathfinder'].QueryInterface("iPcPathFinder");
			player.iPcSteer = player.pcarray['pcsteer'].QueryInterface("iPcSteer");
			//获得world.xml文件中的setctor
			var engine = Registry.Get('iEngine');
			var sectorlist = engine.sectors;
			var setctor = sectorlist.Get(0);
			player.iPcPathFinder.SetGraph(celgraph);
			//seek的添加是因为CEL库存在BUG，正常情况下是没有必要添加的
			//seek的点即为初始点的一个临近点
			player.iPcPathFinder.Seek(setctor, [posX,posY,posZ]);
		},"player.effect.graph.init");
		
		/*	导游路线起始点	*/
		Event.Subscribe(function(e){
			var actor = player;
			var posX = e.posX;
			var posY = e.posY;
			var posZ = e.posZ;
			var roty = e.roty;
			//guides快速定位到新生入学路线起始点
			if( posX != undefined && posY != undefined && 
				posZ != undefined && roty != undefined )
			{
				guides.pcarray['pcmesh'].PerformAction('SetVisible',['visible', true]);
				guides.pcarray['pcmesh'].PerformAction(
					'MoveMesh',
					[
						'position',
						[
							posX, 
							posY, 
							posZ
						]
					],
					[
						'rotation',
						[
							0,
							0 - roty,
							0
						]
					]
				);
				guides.pcarray['pclinearmovement'].SetProperty('gravity', 19.6);
				//player快速定位到新生入学路线起始点
				player.pcarray['pcmesh'].PerformAction(
					'MoveMesh',
					[
						'position',
						[
							posX,
							posY,
							posZ
						]
					],
					[
						'rotation',
						[
							0,
							0 - roty,
							0
						]
					]
				);
				player.pcarray['pclinearmovement'].SetProperty('gravity', 19.6);
				player.isStop = false ; 
			}else{
				iprint("将guides和player定位到路线起始点时，坐标信息出现NaN型，请检查！！  ps: guides_effect.js 'player.effect.moveTo.route_guides.start'");
			}
		},"player.effect.moveTo.route_guides.start");
		
		/*	路线导游---事件触发	*/
		Event.Subscribe(function(e){
			var actor = e.player;
			var posX = e.posX;
			var posY = e.posY;
			var posZ = e.posZ;
			var moveSpeed = e.speed;
			var text_content = e.text_content;
			if(!player.iPcSteer || !player.iPcPathFinder){
				alert("初始化自动寻路环境失败！！！");
				return;
			}
			// 复位操作 
			Event.Send({
				name : "effect.camera.change.player0",
				player : player
			});
			//显示导游
			guides.pcarray['pcmesh'].PerformAction('SetVisible',['visible', true]);
			//设置移动速度
			player.pcarray['pcactormove'].PerformAction(
				'SetSpeed',
					['movement', moveSpeed],
					['running',  2],
					['rotation',  2],
					['jumping',   1]
			);
			//设置player可以跨越小型障碍物
			player.pcarray['pclinearmovement'].PerformAction(
				'InitCD',
					['offset',[0, 0.0, 0]],
					['body',[0.5,0.65,0.5]],
					['legs',[0.5,2,0.5]]
			);
			//获取player的Position作为起始点
			var position = player.pcarray['pcmesh'].GetProperty('position');
			//设置下一节点为终点
			var pos_end_num = [posX,posY,posZ];
			actor.iPcSteer.CheckArrivalOn(1);
			//将上次移动的位置作为这次移动的起始位置
			var pos_start_num = [position.x ,position.y , position.z];
			var pos_start = celgraph.GetClosest(pos_start_num);
			var pos_end = celgraph.GetClosest(pos_end_num);
			var ShortPath = celgraph.ShortestPath(pos_start, pos_end, celpath);
			if(ShortPath){
				//开始行走
				player.iPcPathFinder.FollowOneWayPath(celpath);
			}else{
				alert(" 没有找到相关路线 ");
			}
			var id = C3D.engine.SubscribeFrame(function(){
				//获得meshWrapperPlayer
				if(player.sex == "nv"){
					var meshWrapperPlayer = C3D.engine.FindMeshObject('woman');
				}
				if(player.sex == "nan"){
					var meshWrapperPlayer = C3D.engine.FindMeshObject('man');
				}
				//获得meshWrapperGuides
				var meshWrapperGuides = C3D.engine.FindMeshObject("guides");
				//获取iPcActorMove
				var pcactor = player.pcarray['pcactormove'].QueryInterface('iPcActorMove');
				var IsMoving = pcactor.IsMoving();
				if(player.isFirst_Guides){
					IsMoving = true;
					player.isFirst_Guides = false;
				}
				if( IsMoving && meshWrapperPlayer){
					//将meshWrapperPlayer的移动信息赋给meshWrapperGuides
					var mt = meshWrapperPlayer.movable.GetTransform();
					//保持一定的距离，获取人物的位置
					var cur_pos = player.pcarray['pcmesh'].GetProperty("position");
					var x = cur_pos.x + 0.1;
					var z = cur_pos.z + 0.5;
					if(mt){
						var v0 = mt.GetFront();
						var v1 = mt.GetO2TTranslation();
						meshWrapperGuides.movable.SetTransform(mt);
					}
					if(v0){
						x = Number(-1*v0[0].toFixed(3))/Number(v0.Length().toFixed(3));
						z = Number(-2*v0[2].toFixed(3))/Number(v0.Length().toFixed(3));
					}
					if(v1){
						x = Number(x) + Number(v1[0]);
						z = Number(z) + Number(v1[2]);
					}
					//将导游指定到人物的某一位置
					meshWrapperGuides.movable.pos = [x , cur_pos.y, z];
					//使位置调整生效
					meshWrapperGuides.movable.Update();
					//此时两者为run
					player.pcarray['pcmesh'].PerformAction('SetAnimation',['animation','run'],['cycle',true],['reset', false]);
					guides.pcarray['pcmesh'].PerformAction('SetAnimation',['animation','run'],['cycle',true],['reset', false]);
					//屏蔽键盘操作
				    Event.Send({
						name : "player.effect.disable_keybord"
					});
					//屏蔽鼠标操作
					Event.Send({
						name : "player.effect.close_MouseAxis0"
					});
				}else{
					//此时为stand
					player.pcarray['pcmesh'].PerformAction('SetAnimation',['animation','stand'],['cycle',true],['reset', false]);
					guides.pcarray['pcmesh'].PerformAction('SetAnimation',['animation','stand'],['cycle',true],['reset', false]); 
					C3D.engine.UnsubscribeFrame(id);
					//停止旋转
					player.pcarray['pcactormove'].PerformAction('RotateLeft',['start',false]);
					// guides.pcarray['pcactormove'].PerformAction('RotateLeft',['start',false]);
					player.pcarray['pcactormove'].PerformAction('RotateRight',['start',false]);
					// guides.pcarray['pcactormove'].PerformAction('RotateRight',['start',false]);
					// 复位操作 
					Event.Send({
						name : "effect.camera.change.player0", 
						player : player 
					});
					//恢复player的正常跨越状态
					player.pcarray['pclinearmovement'].PerformAction(
						'InitCD',
							['offset',[0, 0.0, 0]],
							['body',[0.5,0.65,0.5]],
							['legs',[0.5,0.4,0.5]] 
					);
					//弹出导游点提示窗体
					Event.Send({
						name : "player.effect.open_guides_point_form",
						text_content : text_content 
					});
					//结束导游时，关闭景点介绍窗口
					if(player.isStop){
						Event.Send({
							name : "player.effect.close_guides_point_form"
						});
						player.isStop = false;
					}
					player.canMouseCtrlMove = false;
				}
			});
		},"player.effect.route_guides.begin");

		/*	加速浏览--事件触发	*/
		Event.Subscribe(function(e){
			var moveSpeed = e.moveSpeed ; 
			player.pcarray['pcactormove'].PerformAction(
				'SetSpeed', 
					['movement', moveSpeed], 
					['running',  2], 
					['rotation',  2], 
					['jumping',   1]
			);
		},"player.effect.accelerate_move");
		
		/*	移动导游到导游初始点 	*/
		Event.Subscribe(function(e){
			var guides_posX = GUIDES_DATA.initPosition.x;
			var guides_posY = GUIDES_DATA.initPosition.y;
			var guides_posZ = GUIDES_DATA.initPosition.z;
			var guides_rotY = GUIDES_DATA.initRotation.y;
			if( guides_posX != undefined && guides_posX != undefined && 
				guides_posX != undefined && guides_rotY != undefined )
			{
				guides.pcarray['pcmesh'].PerformAction('SetVisible',['visible', true]);
				//guides快速定位到历史文化路线起始点
				guides.pcarray['pcmesh'].PerformAction(
					'MoveMesh',
					[
						'position',
						[
							guides_posX, 
							guides_posY, 
							guides_posZ
						]
					],
					[
						'rotation',
						[
							0,
							0 - guides_rotY,
							0
						]
					]
				);
				player.isGuidesMode = false;
			}else{
				iprint("移动导游到导游初始位置时，坐标信息出现NaN型，请检查！！  ps: guides_effect.js 'player.effect.move_guides.initPos'");
			}
		},"player.effect.move_guides.initPos");
		
		/*	结束导游模式 	*/
		Event.Subscribe(function(e){
			var actor = e.player;
			//暂停和停止事件
			actor.pcarray['pcsteer'].Interrupt();
			guides.pcarray['pcmesh'].PerformAction('SetVisible',['visible', true]);
			actor.pcarray['pclinearmovement'].PerformAction(
				'InitCD',
					['offset',[0, 0.0, 0]],
					['body',[0.5,0.65,0.5]],
					['legs',[0.5,0.4,0.5]]
			);
			player.isStop = true ;
			player.isGuidesMode = false;
		},"player.effect.route_guides.stop");
		
		/*	判断人物里导游初始位置间的距离	*/
		Event.Subscribe(function(e){
			if(!player.isGuidesMode && player.role_ok == "ok"){
				var gap = 3;
				//获取guides的位置坐标
				var guiPos_x = GUIDES_DATA.initPosition.x;
				var guiPos_y = GUIDES_DATA.initPosition.y;
				var guiPos_z = GUIDES_DATA.initPosition.z;
				var guiPos_vec = new Math3.Vector3(guiPos_x , guiPos_y , guiPos_z);
				//获取人物的位置坐标
				var perPos = player.pcarray['pcmesh'].position;
				var perPos_vec = new Math3.Vector3(perPos.x , perPos.y , perPos.z);
				//计算人物当前坐标向量与导游初始点的坐标向量差
				var vec_Len = perPos_vec.Subtract(guiPos_vec);
				var len = vec_Len.Length();
				//判断人物与guides间的距离是否小于1
				if(len <= gap){
					//发送消息给ui，显示全程导游提示框
					Event.Send({
						name : "ui.entire_journey_guides.display",
						player : player,
						show : true
					});
				}else{
					//发送消息给ui，不显示全程导游提示框
					Event.Send({
						name : "ui.entire_journey_guides.display",
						player : player,
						show : false
					});
					player.isGuidesMode = false;
				}
			}
		},"player.effect.nearby.guides");
	})();
}catch(e){
	alert("error:",e);
}