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


try{
	(function(){
	
// ==========================================================================================================
// ===   ��ǰ effect ��ȡ�����Ĺ�������   ===================================================================
// ==========================================================================================================

// ==========================================================================================================
// ======  ���ĵ��¼�  ======================================================================================
// ==========================================================================================================

		/*  music start */
		Event.Subscribe(function(e){
			if(music_bg.state == "stop" || music_bg.state == "close" || music_bg.state == "play"){
				music_bg.state = "play";
				music_bg.pcarray['pcsoundsource'].SetProperty('mode', 'relative');
				music_bg.pcarray['pcsoundsource'].SetProperty('soundname', 'background');
				music_bg.pcarray['pcsoundsource'].SetProperty('volume', 1.5); //��ʼ����
				music_bg.pcarray['pcsoundsource'].Play();
				music_bg.pcarray['pcsoundsource'].SetProperty('loop', true);  /*Ĭ��Ϊѭ��*/
			}
		}, "music.effect.play");

		/*  music stop */
		Event.Subscribe(function(e){
			if(music_bg.state == "play"){
				music_bg.state = "stop";
				music_bg.pcarray['pcsoundsource'].Stop(); 
			}   
		}, "music.effect.stop");
		
		//������������---��ʼ
		var index = 0;
		Event.Subscribe(function(e){
			var guides_sounds = e.guides_music;
			var Volume = e.Volume ;
			if(music_bg.guides_state == "stop" || music_bg.guides_state == "close" || music_bg.guides_state == "play"){
				if(index == 0 ){
					music_bg.guides_state = "play";
					music_bg.pcarray['pcsoundsource'].SetProperty('mode', 'relative');
					music_bg.pcarray['pcsoundsource'].SetProperty('soundname', guides_sounds);
					music_bg.pcarray['pcsoundsource'].SetProperty('volume', Volume); //��ʼ����
					music_bg.pcarray['pcsoundsource'].Play();
					music_bg.pcarray['pcsoundsource'].SetProperty('loop', true);/*Ĭ�ϲ�Ϊѭ��*/
				}
				index++ ; 
			}
		},"music.effect.guides_sounds.play");
		
		//������������---ֹͣ
		Event.Subscribe(function(e){
			if(music_bg.guides_state == "play"){
				if(index > 0 ){
					music_bg.guides_state = "stop";
					music_bg.pcarray['pcsoundsource'].Stop(); 
					index = 0 ;
				}
			}   
		},"music.effect.guides_sounds.stop");
	})();
} catch(e){
	alert(e);
}