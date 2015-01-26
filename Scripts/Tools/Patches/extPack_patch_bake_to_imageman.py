# ------------------------------------------------------------------------------
# Patch Bake to Image Manager
# ------------------------------------------------------------------------------
# Will Bake+Flatten the selected Patches and place the result in the Image Manager
# ------------------------------------------------------------------------------
# http://mari.ideascale.com
# http://cg-cnu.blogspot.in/
# ------------------------------------------------------------------------------
# Written by Sreenivas Alapati, 2014
# ------------------------------------------------------------------------------
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF HE POSSIBILITY OF SUCH DAMAGE.
# ------------------------------------------------------------------------------

import mari
import os


def patchBake():
	'''Bake the selected patches to image manager'''
	
	if not mari.projects.current():
		mari.utils.message('No project currently open', title = 'Error')
		return

	curGeo = mari.geo.current()
	patchList = list (curGeo.patchList() )
	selPatchList = [patch for patch in patchList if patch.isSelected() ]
	
	if len(selPatchList) == 0:
		mari.utils.meesage('Select atleast one patch', title = 'Error')
		return
	
	if mari.app.version().isWindows():
		path = str(mari.resources.path("MARI_USER_PATH")).replace("\\", "/")
	else:
		path = str( mari.resources.path("MARI_USER_PATH") )	

	curChan = curGeo.currentChannel()
	curChanName = str(curChan.name())
	
	layers = curChan.layerList()
	
	mari.history.startMacro('Patch Bake to Image Manager')
	mari.app.setWaitCursor()
	
	for layer in layers:
		layer.setSelected(True)
	
	copyAction = mari.actions.find('/Mari/Layers/Copy')
	copyAction.trigger()
	
	pasteAction = mari.actions.find('/Mari/Layers/Paste')
	pasteAction.trigger()
	
	curChan.mergeLayers()
	
	curLayer = curChan.currentLayer()
	curImgSet = curLayer.imageSet()
	
	for patch in selPatchList:
		
		uv = patch.uvIndex()
		
		curPatchIndex = str(patch.udim())
		savePath = path + curChanName + '.' + curPatchIndex + '.tif'
		
		patchImg = curImgSet.image(uv, -1)
		patchImg.saveAs(savePath)
	
		mari.images.load(savePath)
		os.remove(savePath)
	
	curChan.removeLayers()
	
	mari.history.stopMacro()
	mari.app.restoreCursor()



def patch_bake_to_imageman():

	patchBake()


