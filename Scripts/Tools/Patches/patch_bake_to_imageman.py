# ------------------------------------------------------------------------------
# Patch Bake to Image Manager
# Modified for Weta: Jens Kafitz // jkafitz@wetafx.co.nz
# ------------------------------------------------------------------------------
# http://mari.ideascale.com
# ------------------------------------------------------------------------------
# 
# Original Author: Sreenivas alapati
# ------------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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


