/**************************************************************************
 *
 *  This file is part of the UGE(Uniform Game Engine).
 *  Copyright (C) by SanPolo Co.Ltd.
 *  All rights reserved.
 *
 *  See http://uge.spolo.org/ for more information.
 *
 *  SanPolo Co.Ltd
 *  http://uge.spolo.org/   sales@spolo.org uge-support@spolo.org
 *
**************************************************************************/
try {
	MUSIC_BG = {
		name : "music_bg",
		pc : {
			"pcsoundsource" : {},
			"pcmesh" : {
				action : [
					{
						name : "SetMesh",
						param : [
							['name','music_bg']
						]
					},
					{
						name : "SetAnimation",
						param : [
							['animation','stand'],
							['cycle',true]
						]
					}
				]
			},
			"pccommandinput" : {
				action : [
					{
						name : "Bind",
						param : [
							['trigger','ESC'],
							['command','quit']
						]
					}
				]
			}
		},
		event : {
			/*退出场景*/
			"pccommandinput_quit0" : function(){
				System.Quit();
			}
		},
		property : {
			state : "play", //播放状态
			guides_state : "stop" //导游解说词的播放状态,默认不播放 
		},
		subscribe : {
		}
	};
}
catch (e)
{
	alert(e);
}