# --------------------------------------------------------------------
# Mari Extension Pack GUI Tools
# Copyright (c) 2015 Mari Ideascale. All Rights Reserved.
# --------------------------------------------------------------------
# Implementation for MARI Extension Pack: Jens Kafitz
# --------------------------------------------------------------------
# File: tools_menu.py
# Description: The following adds custom scripts to the Mari GUI
# --------------------------------------------------------------------
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
# --------------------------------------------------------------------


######################################################################
# The following adds new functionality to the MARI Gui.
# Items are placed within existing Menus (UI_Path) and a copy is placed
# in a common Script Menu (script_menu_path)
# Shortcut Bindings are available but not necessarily set
######################################################################


import mari


def createToolsMenu():


######################################################################
# Patches
######################################################################

	UI_path = "MainWindow/&Patches"
	script_menu_path = "MainWindow/Scripts/Patches"

# --------------------------------------------------------------------


	###   Patch Bake to Image Manager ### 

	PatchToImageMgr= mari.actions.create('Patch to Image Manager', 'mari.customScripts.patch_bake_to_imageman()')
	mari.menus.addAction(PatchToImageMgr, UI_path,"UV Mask to Image Manager")
	mari.menus.addAction(PatchToImageMgr, script_menu_path)

	icon_filename = "SaveToImageManager.png"
	icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
	PatchToImageMgr.setIconPath(icon_path)
	PatchToImageMgr.setShortcut('')



######################################################################
# Camera
######################################################################

	UI_path = "MainWindow/&Camera"
	script_menu_path = "MainWindow/Scripts/Camera"

# --------------------------------------------------------------------

	###  Quick Unproject Channel to Image Manager ### 

	ChannelToImageMgr = mari.actions.create('Quick Unproject Channel', "mari.customScripts.unproject_channel_to_imageman()")
	mari.menus.addAction(ChannelToImageMgr, script_menu_path)
	mari.menus.addAction(ChannelToImageMgr, UI_path,"Camera Left")

	icon_filename = "SaveToImageManager.png"
	icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
	ChannelToImageMgr.setIconPath(icon_path)
	ChannelToImageMgr.setShortcut('')

# --------------------------------------------------------------------

	###   Quick Unproject Layer to Image Manager ###

	LayerToImageMgr = mari.actions.create('Quick Unproject Layer', "mari.customScripts.unproject_layer_to_imageman()")
	mari.menus.addAction(LayerToImageMgr, UI_path,"Camera Left")
	mari.menus.addAction(LayerToImageMgr, script_menu_path)

	icon_filename = "SaveToImageManager.png"
	icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
	LayerToImageMgr.setIconPath(icon_path)
	LayerToImageMgr.setShortcut('')

# --------------------------------------------------------------------

	###  Quick Unproject Menu Separator ###

	mari.menus.addSeparator(UI_path,"Camera Left")



######################################################################
# Channels
######################################################################

	UI_path = "MainWindow/&Channels"
	script_menu_path = "MainWindow/Scripts/Channels"

# --------------------------------------------------------------------

	###   Export Custom Selection ###

	ExportSelected = mari.actions.create ('Export Custom Selection', 'mari.customScripts.exportSelectedChannels()')
	mari.menus.addAction(ExportSelected, UI_path,"Export")
	mari.menus.addAction(ExportSelected, script_menu_path)
	
	icon_filename = "ExportImages.png"
	icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
	ExportSelected.setIconPath(icon_path)
	ExportSelected.setShortcut('')

# --------------------------------------------------------------------

	###   Duplicate & Flatten Selected ###

	DuplicateFlatten = mari.actions.create ('Duplicate+Flatten', 'mari.customScripts.flattenSelectedChannels()')
	mari.menus.addAction(DuplicateFlatten, UI_path, "Transfer")
	mari.menus.addAction(DuplicateFlatten, script_menu_path)

	icon_filename = "BakeShader.png"
	icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
	DuplicateFlatten.setIconPath(icon_path)
	DuplicateFlatten.setShortcut('')




######################################################################
# Layers
######################################################################

	###  Merge & Duplicate layers ###

	UI_path = "MainWindow/&Layers/"
	script_menu_path = "MainWindow/Scripts/Layers/Layer Selection"

	MergeDuplicate = mari.actions.create('Duplicate+Merge Layers', 'mari.customScripts.MergeDuplicate()')
	mari.menus.addAction(MergeDuplicate, UI_path,"Transfer")
	mari.menus.addAction(MergeDuplicate, script_menu_path)

	icon_filename = "AddChannel.png"
	icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
	MergeDuplicate.setIconPath(icon_path)
	MergeDuplicate.setShortcut('Ctrl+Shift+E')

	
# --------------------------------------------------------------------

	# Removes existing default "Convert to Paintable" from Interface to be 
	# replaced by batch Convert to Paintable (below)

	mari.menus.removeAction("MainWindow/&Layers/Convert To Paintable")

# --------------------------------------------------------------------

	### Convert to Paintable (batch) ### 

	UI_path = "MainWindow/&Layers/"
	script_menu_path = "MainWindow/Scripts/Layers/Layer Selection"

	BatchConvertToPaintable = mari.actions.create ('Convert To Paintable', 'mari.customScripts.convertToPaintable()')
	mari.menus.addAction(BatchConvertToPaintable, UI_path,"Sharing")
	mari.menus.addAction(BatchConvertToPaintable, script_menu_path)

	icon_filename = "Painting.png"
	icon_path = mari.resources.path(mari.resources.ICONS) + "/" + icon_filename
	BatchConvertToPaintable.setIconPath(icon_path)
	BatchConvertToPaintable.setShortcut('')

	

# --------------------------------------------------------------------

	###  Convert to Paintable Menu Separators ###

	mari.menus.addSeparator(UI_path,"Sharing")
	mari.menus.addSeparator(UI_path,"Convert To Paintable")

# --------------------------------------------------------------------

#  Toggle Layer Visibility & Lock

	UI_path = "MainWindow/&Layers/Layer Selection"
	script_menu_path = "MainWindow/Scripts/Layers/Layer Selection"

	toggleSelVisibilityAction = mari.actions.create('Toggle Selected Visibility', 'mari.customScripts.toggleSelVisibility()')
	mari.menus.addAction(toggleSelVisibilityAction, 'MainWindow/Layers/Layer Selection')
	mari.menus.addAction(toggleSelVisibilityAction, 'MainWindow/Scripts/Layers/Layer Selection')
	toggleSelVisibilityAction.setShortcut('')
	
	toggleUnselVisibilityAction = mari.actions.create('Toggle Unselected Visibility', 'mari.customScripts.toggleUnselVisibility()')
	mari.menus.addAction(toggleUnselVisibilityAction, 'MainWindow/Layers/Layer Selection')
	mari.menus.addAction(toggleUnselVisibilityAction, 'MainWindow/Scripts/Layers/Layer Selection')
	toggleUnselVisibilityAction.setShortcut('')
	
	toggleSelLockAction = mari.actions.create('Toggle Selected Lock', 'mari.customScripts.toggleSelLock()')
	mari.menus.addAction(toggleSelLockAction, 'MainWindow/Layers/Layer Selection')
	mari.menus.addAction(toggleSelLockAction, 'MainWindow/Scripts/Layers/Layer Selection')
	toggleSelLockAction.setShortcut('')
	
	toggleUnselLockAction = mari.actions.create('Toggle Unselected Lock', 'mari.customScripts.toggleUnselLock()')
	mari.menus.addAction(toggleUnselLockAction, 'MainWindow/Layers/Layer Selection')
	mari.menus.addAction(toggleUnselLockAction, 'MainWindow/Scripts/Layers/Layer Selection')
	toggleUnselLockAction.setShortcut('')

# --------------------------------------------------------------------

## Layer mask from selection

	selectMaskITEM = mari.actions.create('From Selection', 'mari.customScripts.selectionMask()')
	selectMaskITEM.setIconPath('%s/SelectAll.png' % icon_path)
	selectMaskInvertITEM = mari.actions.create('From Selection(Invert)', 'mari.customScripts.selectionMask_inv()')
	selectMaskInvertITEM.setIconPath('%s/SelectInvert.png' % icon_path)
	
	mari.menus.addAction(selectMaskITEM, 'MainWindow/&Layers/Layer Mask/Add Mask')
	mari.menus.addAction(selectMaskInvertITEM, 'MainWindow/&Layers/Layer Mask/Add Mask')
	mari.menus.addAction(selectMaskITEM, 'MainWindow/Scripts/Layers/Layer Mask')
	mari.menus.addAction(selectMaskInvertITEM, 'MainWindow/Scripts/Layers/Layer Mask')

	selectMaskITEM.setShortcut('')
	selectMaskInvertITEM.setShortcut('')

# --------------------------------------------------------------------

# Channel Layer, Channel Mask + Channel Mask Group

	chanLayer = mari.actions.create('Add Channel Layer', 'mari.customScripts.CLCreate_layer()')
	mari.menus.addAction(chanLayer, 'MainWindow/&Layers', 'Add Adjustment Layer')
	mari.menus.addAction(chanLayer, 'MainWindow/Scripts/Layers/Layer Mask')
	icon_filename = "linked.png"
	chanLayer.setIconPath(icon_path)
	chanLayer.setShortcut('')


	chanLayerMaskITEM = mari.actions.create('Add Channel Mask', 'mari.customScripts.CLCreate_layermask()')
	chanLayerMaskITEM.setIconPath('%s/AddChannel.png' % icon_path)
	
	chanLayerGrpMaskITEM = mari.actions.create('Add Channel Mask (Group)', 'mari.customScripts.CLCreate_maskgroup()')
	chanLayerGrpMaskITEM.setIconPath('%s/NewFolder.png' % icon_path)


	mari.menus.addAction(chanLayerMaskITEM, 'MainWindow/&Layers/Layer Mask/Add Mask')
	mari.menus.addAction(chanLayerMaskITEM, 'MainWindow/Scripts/Layers/Layer Mask')
	mari.menus.addAction(chanLayerGrpMaskITEM, 'MainWindow/&Layers/Layer Mask/Add Mask')
	mari.menus.addAction(chanLayerGrpMaskITEM, 'MainWindow/Scripts/Layers/Layer Mask')


	chanLayerMaskITEM.setShortcut('')
	chanLayerGrpMaskITEM.setShortcut('')


######################################################################
# Object
######################################################################


#  Export UV Mask


	script_menu_path = "MainWindow/Scripts/Object"

	action = mari.actions.create ('Export UV Mask', 'mari.customScripts.exportUVMasks()')
	mari.menus.addAction(action, UI_path)
	mari.menus.addAction(action, script_menu_path)
	action.setShortcut('')



######################################################################
# Review
######################################################################

# Screenshot all Channels

	action = mari.actions.create('Screenshot All Channels','mari.customScripts.screenshot_all_channels()')
	mari.menus.addAction(action, "MainWindow/View")
	mari.menus.addAction(action, "MainWindow/Scripts/Review")
	action.setShortcut('')


