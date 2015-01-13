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
		Event.Subscribe(function(e){
			//点击进入场景后执行以下代码
			if(player.role_ok == "ok"){
				//根据name获取Box meshobj
				var meshobj = C3D.engine.FindMeshObject('sky');
				//判断Box是否存在，存在执行if语句，不存在执行else语句
				if(meshobj){
					//声明触发距离
					var gap = 10;
					var show = false;
					var flag = true;
					var index = 0;
					while(flag)
					{
						if( typeof(FULL_VIEW_POSITION[index]) == "undefined" )
						{
							flag = false;
						}else{
							//获取人物当前坐标向量
							var pre_posx = e.position.x;
							var pre_posy = e.position.y;
							var pre_posz = e.position.z;
							var pre_pos = new Math3.Vector3(pre_posx,pre_posy,pre_posz);
							// 获取触发进入360全景展示的坐标向量
							var FV_posx = FULL_VIEW_POSITION[index].position.position_x;
							var FV_posy = FULL_VIEW_POSITION[index].position.position_y;
							var FV_posz = FULL_VIEW_POSITION[index].position.position_z;
							var FV_pos = new Math3.Vector3(FV_posx,FV_posy,FV_posz);
							//计算当前坐标向量与触发全景展示的坐标向量差
							var vec_gap = pre_pos.Subtract(FV_pos);
							var len = vec_gap.Length();
							var matName = FULL_VIEW_POSITION[index].matName;
							var materialbox = C3D.engine.FindMaterial(matName);
							//比较向量差和触发距离--满足条件，则发送消息给UI--显示是否进入全景展示提示框
							if(len <= gap && materialbox){
								show = true;
								flag = false;
								player.fview_id = index;
								player.isRegGuides = false;
							}else{
								show = false;
							}
							Event.Send({
								name : "ui.full_view_prompt.display",
								player : player,
								show : show
							});
						}
						index ++;
					}
				}else{
					var show = false;
					Event.Send({
						name : "ui.full_view_prompt.display",
						player : player,
						show : show
					});
				}
			}
		},"player.effect.full_view");

		//动态更换Box贴图
		Event.Subscribe(function(e){
			var id = e.id;
			var matName = "";
			if(player.isRegGuides){
				var id = player.regGui_id;
				matName = REGIONAL_GUIDES_DATA[id].matName;
			}else{
				var id = player.fview_id;
				matName = FULL_VIEW_POSITION[id].matName;
			}
			var materialbox = C3D.engine.FindMaterial(matName);
			C3D.engine.FindMeshObject("sky").meshObject.matWrap = materialbox;
		},"change.sky_box.textures");
		
		//鼠标双击停止旋转
		Event.Subscribe(function(e){
			if(player.isFullView && player.isRotateRight){
				player.pcarray['pcactormove'].PerformAction('RotateRight',['start',false]);
				player.isRotateRight = false;
			}else{
				return;
			}
			//设置摄像机pitch值
			iCamera.pcarray["pcdefaultcamera"].SetProperty("pitch", 0.3020000159740448);
		},"crystalspace.input.mouse.0.button.doubleclick");	})();
}catch(e){
	alert("error:",e);
}