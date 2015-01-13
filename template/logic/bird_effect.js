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
			// 获取iSequence，sequence属性封装了Set和Get
			
			var iEngineSequenceManager = C3D.ensequence;
			var iSequenceManager = C3D.seqmanager;
			
			var iSequenceWrapper = iEngineSequenceManager.FindSequenceByName('spp_bird1');
			var iSequence = iSequenceWrapper.sequence;
			
			// RunSequence可以有缺省值
			iSequenceManager.RunSequence(1, iSequence);
		}, "superpolo.application.startup");
	})();
} catch(e){
	alert(e);
}