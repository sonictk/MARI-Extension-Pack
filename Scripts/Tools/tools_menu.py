# --------------------------------------------------------------------
# Mari Extension Pack GUI Tools
# Copyright (c) 2015 Mari Ideascale. All Rights Reserved.
# --------------------------------------------------------------------
# Written by Jens Kafitz, 2015
# http://mari.ideascale.com
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
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS
# IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
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




# --------------------------------------------------------------------


'''The following adds new functionality to the MARI Gui.
Items are grouped by the standard MARI Menus they appear in such as
CHANNELS,LAYERS,PATCHES etc.

Items are placed within existing Menus (UI_Path) and a copy is placed
in a common Script Menu (script_menu_path)

Shortcut Bindings are available but not necessarily set.'''


# --------------------------------------------------------------------





import mari
import os

tool_menu_version = '2.2'


# Icon Path for custom icons
extPack_icon_path = os.path.join(os.path.dirname(__file__), "Icons")


def createToolsMenu():

######################################################################
# Objects
######################################################################


    #  Export UV Mask

    UI_path = 'MainWindow/Objects'
    script_menu_path = 'MainWindow/Scripts/Objects'

    exportUVMask = mari.actions.create ('Export UV Mask', 'mari.customScripts.exportUVMasks()')
    mari.menus.addAction(exportUVMask, UI_path, 'Ambient Occlusion')
    mari.menus.addAction(exportUVMask, script_menu_path)

    icon_filename = 'EdgeMask.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    exportUVMask.setIconPath(icon_path)


    ###  Menu Separators ###

    mari.menus.addSeparator('MainWindow/Objects','Ambient Occlusion')



######################################################################
# Channels
######################################################################


    ###   Duplicate & Flatten Selected Channels ###

    UI_path = 'MainWindow/&Channels'
    script_menu_path = 'MainWindow/Scripts/Channels'

    DuplicateFlatten = mari.actions.create ('Duplicate && Flatten', 'mari.customScripts.flattenSelectedChannels()')
    mari.menus.addAction(DuplicateFlatten, UI_path, 'Flatten')
    mari.menus.addAction(DuplicateFlatten, script_menu_path)

    icon_filename = 'BakeShader.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    DuplicateFlatten.setIconPath(icon_path)

    # --------------------------------------------------------------------

    ###   Export Custom Channel Selection ###

    # Added twice to main interface to maintain existing logic
    UI_path_A = 'MainWindow/&Channels/Export Flattened'
    UI_path_B = 'MainWindow/&Channels/Export'
    script_menu_path = 'MainWindow/Scripts/Channels/Export'

    ExportSelected = mari.actions.create ('Export Custom Channel Selection', 'mari.customScripts.exportSelectedChannels()')
    mari.menus.addAction(ExportSelected, UI_path_A,'Export Current Channel Flattened')
    mari.menus.addAction(ExportSelected, UI_path_B,'Export Current Channel')
    mari.menus.addAction(ExportSelected, script_menu_path)

    icon_filename = 'ExportImages.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    ExportSelected.setIconPath(icon_path)

    # --------------------------------------------------------------------
    ###   Save Channel Resolution ###

    UI_path = 'MainWindow/&Channels/Resize'
    script_menu_path = 'MainWindow/Scripts/Channels/Template'

    getChannelTemplate = mari.actions.create ('Save Channel Resolution ', 'mari.customScripts.channel_template_get()')

    mari.menus.addAction(getChannelTemplate, UI_path)
    mari.menus.addAction(getChannelTemplate, script_menu_path)

    icon_filename = 'Channel.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    getChannelTemplate.setIconPath(icon_path)

    # --------------------------------------------------------------------

    ###    Load Channel Resolution ###

    UI_path = 'MainWindow/&Channels/Resize'
    script_menu_path = 'MainWindow/Scripts/Channels/Template'

    setChannelTemplate = mari.actions.create ('Load Channel Resolution', 'mari.customScripts.channel_template_set()')

    mari.menus.addAction(setChannelTemplate, UI_path)
    mari.menus.addAction(setChannelTemplate, script_menu_path)

    icon_filename = 'ChannelPresets.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    setChannelTemplate.setIconPath(icon_path)

# --------------------------------------------------------------------

    ###    Create Channel from Resolution ###

    # To avoid Interface bloat this is currently not embedded into the Channel Palette and only accessible via the Script Menu.
    # Ideally we should come up with a way to add this to the "Channel Size" Dropdowns under "Add Channel" / "Quick Channel"

    UI_path = 'MainWindow/&Channels'
    script_menu_path = 'MainWindow/Scripts/Channels/Template'

    newChannelFromTemplate = mari.actions.create ('Create Channel from Resolution', 'mari.customScripts.channel_template_set()')

    # mari.menus.addAction(newChannelFromTemplate, UI_path)
    mari.menus.addAction(newChannelFromTemplate, script_menu_path)

    icon_filename = "AddChannel.png"
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    newChannelFromTemplate.setIconPath(icon_path)



######################################################################
# Layers
######################################################################


    ###  Channel Layer ###

    UI_path = 'MainWindow/&Layers'
    script_menu_path = 'MainWindow/Scripts/Layers'

    chanLayer = mari.actions.create('Add Channel Layer', 'mari.customScripts.ChannelLayerUI_layer()')
    mari.menus.addAction(chanLayer, UI_path, 'Add Adjustment Layer')
    mari.menus.addAction(chanLayer, script_menu_path)

    icon_filename = 'linked.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    chanLayer.setIconPath(icon_path)


    # --------------------------------------------------------------------

    ###  Clone & merge layers ###

    UI_path = 'MainWindow/&Layers/'
    script_menu_path = 'MainWindow/Scripts/Layers'

    MergeDuplicate = mari.actions.create('Clone && Merge Layers', 'mari.customScripts.CloneMerge()')
    mari.menus.addAction(MergeDuplicate, UI_path,'Transfer')
    mari.menus.addAction(MergeDuplicate, script_menu_path)

    icon_filename = 'AddChannel.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    MergeDuplicate.setIconPath(icon_path)
    MergeDuplicate.setShortcut('Ctrl+Shift+E')


    # --------------------------------------------------------------------

    # Removes existing default 'Convert to Paintable' from Interface to be
    # replaced by batch Convert to Paintable (below)

    mari.menus.removeAction('MainWindow/&Layers/Convert To Paintable')

    # --------------------------------------------------------------------

    ### Convert to Paintable (batch) ###

    UI_path = 'MainWindow/&Layers/'
    script_menu_path = 'MainWindow/Scripts/Layers'

    BatchConvertToPaintable = mari.actions.create ('Convert To Paintable', 'mari.customScripts.convertToPaintable()')
    mari.menus.addAction(BatchConvertToPaintable, UI_path,'Sharing')
    mari.menus.addAction(BatchConvertToPaintable, script_menu_path)

    icon_filename = 'Painting.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    BatchConvertToPaintable.setIconPath(icon_path)


    # --------------------------------------------------------------------

    ###  Convert to Paintable Menu Separators ###

    mari.menus.addSeparator(UI_path,'Sharing')
    mari.menus.addSeparator(UI_path,'Convert To Paintable')

    # --------------------------------------------------------------------

    ###  Toggle Layer Visbility ###

    UI_path = 'MainWindow/&Layers/' + u'Visibility + Lock'
    script_menu_path = 'MainWindow/Scripts/Layers/' + u'Visibility + Lock'


    toggleSelVisibility = mari.actions.create('Toggle Selected Visibility', 'mari.customScripts.toggleSelVisibility()')
    mari.menus.addAction(toggleSelVisibility, UI_path, 'Remove Layers')
    mari.menus.addAction(toggleSelVisibility, script_menu_path)

    icon_filename = 'ToggleVisibility.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    toggleSelVisibility.setIconPath(icon_path)


    toggleUnselVisibility = mari.actions.create('Toggle Unselected Visibility', 'mari.customScripts.toggleUnselVisibility()')
    mari.menus.addAction(toggleUnselVisibility, UI_path)
    mari.menus.addAction(toggleUnselVisibility, script_menu_path)

    icon_filename = 'ToggleVisibility.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    toggleUnselVisibility.setIconPath(icon_path)



    # --------------------------------------------------------------------

    ###  Toggle Layer Lock ###

    UI_path = 'MainWindow/&Layers/' + u'Visibility + Lock'
    script_menu_path = 'MainWindow/Scripts/Layers/Visibility + Lock'

    toggleSelLock = mari.actions.create('Toggle Selected Lock', 'mari.customScripts.toggleSelLock()')
    mari.menus.addAction(toggleSelLock, UI_path)
    mari.menus.addAction(toggleSelLock, script_menu_path)

    icon_filename = 'Lock.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    toggleSelLock.setIconPath(icon_path)


    toggleUnselLock = mari.actions.create('Toggle Unselected Lock', 'mari.customScripts.toggleUnselLock()')
    mari.menus.addAction(toggleUnselLock, UI_path)
    mari.menus.addAction(toggleUnselLock, script_menu_path)

    icon_filename = 'Lock.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    toggleUnselLock.setIconPath(icon_path)


    # --------------------------------------------------------------------

    ###  Lock/Visibility Separator Main Interface ###

    mari.menus.addSeparator(UI_path,'Toggle Selected Lock')
    mari.menus.addSeparator('MainWindow/&Layers/','Remove Layers')


    # --------------------------------------------------------------------

    ### Channel Mask ###

    UI_path = 'MainWindow/&Layers/Layer Mask/Add Mask'
    script_menu_path = 'MainWindow/Scripts/Layers/Layer Mask'

    chanMask = mari.actions.create('Add Channel Mask', 'mari.customScripts.ChannelLayerUI_layermask()')
    mari.menus.addAction(chanMask, UI_path)
    mari.menus.addAction(chanMask, script_menu_path)

    icon_filename = 'linked.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    chanMask.setIconPath(icon_path)


    ### Channel Mask Group ###

    UI_path = 'MainWindow/&Layers/Layer Mask/Add Mask'
    script_menu_path = 'MainWindow/Scripts/Layers/Layer Mask'

    chanMaskGrp = mari.actions.create('Add grouped Channel Mask', 'mari.customScripts.ChannelLayerUI_maskgroup()')
    mari.menus.addAction(chanMaskGrp, UI_path)
    mari.menus.addAction(chanMaskGrp, script_menu_path)

    icon_filename = 'NewFolder.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    chanMaskGrp.setIconPath(icon_path)



######################################################################
# Patches
######################################################################


    ###   Patch Bake to Image Manager ###

    UI_path = 'MainWindow/&Patches'
    script_menu_path = 'MainWindow/Scripts/Patches'

    PatchToImageMgr= mari.actions.create('Patch to Image Manager', 'mari.customScripts.patch_bake_to_imageman()')
    mari.menus.addAction(PatchToImageMgr, UI_path,'UV Mask to Image Manager')
    mari.menus.addAction(PatchToImageMgr, script_menu_path)

    icon_filename = 'SaveToImageManager.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    PatchToImageMgr.setIconPath(icon_path)


    # --------------------------------------------------------------------


    ###  Menu Separator ###

    mari.menus.addSeparator(UI_path,'UV Mask to Image Manager')



######################################################################
# Camera
######################################################################


    ###  Quick Unproject Channel to Image Manager ###

    UI_path = 'MainWindow/&Camera'
    script_menu_path = 'MainWindow/Scripts/Camera'

    ChannelToImageMgr = mari.actions.create('Quick Unproject Channel', 'mari.customScripts.unproject_channel_to_imageman()')
    mari.menus.addAction(ChannelToImageMgr, script_menu_path)
    mari.menus.addAction(ChannelToImageMgr, UI_path,'Camera Left')

    icon_filename = 'SaveToImageManager.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    ChannelToImageMgr.setIconPath(icon_path)


    # --------------------------------------------------------------------

    ###   Quick Unproject Layer to Image Manager ###

    UI_path = 'MainWindow/&Camera'
    script_menu_path = 'MainWindow/Scripts/Camera'

    LayerToImageMgr = mari.actions.create('Quick Unproject Layer', 'mari.customScripts.unproject_layer_to_imageman()')
    mari.menus.addAction(LayerToImageMgr, UI_path,'Camera Left')
    mari.menus.addAction(LayerToImageMgr, script_menu_path)

    icon_filename = 'SaveToImageManager.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    LayerToImageMgr.setIconPath(icon_path)


    # --------------------------------------------------------------------

    ###  Camera Menu Separator ###

    UI_path = 'MainWindow/&Camera'
    mari.menus.addSeparator(UI_path,'Camera Left')




######################################################################
# VIEW
######################################################################

    # Screenshot all Channels

    UI_path = 'MainWindow/View'
    script_menu_path = 'MainWindow/Scripts/View'

    screenshotChannels = mari.actions.create('Screenshot All Channels','mari.customScripts.screenshot_all_channels()')
    mari.menus.addAction(screenshotChannels, UI_path, 'Screenshot Settings')
    mari.menus.addAction(screenshotChannels, script_menu_path)

    icon_filename = 'CanvasSnapshot.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    screenshotChannels.setIconPath(icon_path)


######################################################################
# Shading
######################################################################

    #  Disable Viewport Refresh

    script_menu_path = 'MainWindow/Scripts/Shading'
    UI_path = 'MainWindow/&Shading'

    action_viewportDisable = mari.actions.create("Pause Viewport Update", "mari.customScripts.disableViewport()")
    action_viewportDisable.setCheckable(True)

    mari.menus.addAction(action_viewportDisable, script_menu_path)
    mari.menus.addAction(action_viewportDisable, UI_path, 'Toggle Wireframe')

    icon_filename = 'extPack_disableViewport.png'
    icon_path = extPack_icon_path + '/' + icon_filename
    action_viewportDisable.setIconPath(icon_path)
    action_viewportDisable.setShortcut('Ctrl+Space')


    action_viewportDisable.setStatusTip('Pause Viewport Update. This can help speed up operations by not having to wait for the viewport to update.')
    action_viewportDisable.setToolTip('Pause Viewport Update')
    action_viewportDisable.setWhatsThis('Pause Viewport Update. A repackaged toggleShaderCompile action')


    # Adding to default lighting toolbar
    lightingToolbar = mari.app.findToolBar('Lighting')
    isLocked = lightingToolbar.isLocked()
    lightingToolbar.setLocked(False)
    lightingToolbar.addAction('/Mari/Scripts/Pause Viewport Update', [0,0], False)
    lightingToolbar.setLocked(isLocked)

    ###  Menu Separators ###

    mari.menus.addSeparator(UI_path,'Toggle Wireframe')


######################################################################
# Shaders
######################################################################

    #  Sync Shader Selection across multiple Objects

    UI_path_A = 'MainWindow/&Shading'
    UI_path_B = 'Shaders/Panel'
    UI_path_C = 'MriLayerShader/CollectionContext'
    script_menu_path = 'MainWindow/Scripts/Shaders'

    syncObjectShaders = mari.actions.create(
        "Sync Object Shaders", "mari.customScripts.setAllObjectsToShader()"
        )

    syncObjectShaders.setStatusTip('Sync your Shader Selection across all Objects')
    syncObjectShaders.setToolTip('Sync Object Shader Selection')
    syncObjectShaders.setWhatsThis('Sync Object Shader Selection between Objects')

    mari.menus.addAction(syncObjectShaders, UI_path_A, '-Flat')
    mari.menus.addAction(syncObjectShaders, UI_path_B)
    mari.menus.addAction(syncObjectShaders, UI_path_C,'Duplicate Shader')
    mari.menus.addAction(syncObjectShaders, script_menu_path)

    icon_filename = "Shader.png"
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    syncObjectShaders.setIconPath(icon_path)

######################################################################
# Selection Groups
######################################################################

    #  Create Material ID Channel from Selection Groups

    UI_path_B = 'MriGeometrySelectionGroup/Panel'
    script_menu_path = 'MainWindow/Scripts/Selection Groups'
    matIdFromGroup = mari.actions.create("MaterialID from Selection Groups", "mari.customScripts.matIDFromGroup()")

    matIdFromGroup.setStatusTip('Create a MaterialID Channel from Selection Groups')
    matIdFromGroup.setToolTip('Create a MaterialID Channel from Selection Groups')
    matIdFromGroup.setWhatsThis('Create a MaterialID Channel from Selection Groups')

    mari.menus.addAction(matIdFromGroup, UI_path_B)
    mari.menus.addAction(matIdFromGroup, script_menu_path)

    icon_filename = "Shader.png"
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    matIdFromGroup.setIconPath(icon_path)


######################################################################
# Image Manager
######################################################################

    #  Export selected Image Manager Images

    UI_path = 'MriImageManager/ItemContext'
    script_menu_path = 'MainWindow/Scripts/Image Manager'

    exportUVMask = mari.actions.create ('Export Selection', 'mari.customScripts.exportImageManager()')
    mari.menus.addAction(exportUVMask, UI_path)
    mari.menus.addAction(exportUVMask, script_menu_path)

    icon_filename = 'ExtractImage.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    exportUVMask.setIconPath(icon_path)

    ###  Menu Separators ###

    mari.menus.addSeparator(UI_path,'Export Selection')


######################################################################
# ONLINE HELP
######################################################################

    # EXTENSION PACK ONLINE HELP

    UI_path = 'MainWindow/Help'
    script_menu_path = 'MainWindow/Scripts/Help'

    extHelp = mari.actions.create('Extension Pack Online Help','mari.customScripts.open_online_help()')
    mari.menus.addAction(extHelp, UI_path, 'Release Notes')
    mari.menus.addAction(extHelp, script_menu_path)

    icon_filename = 'Help.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + '/' + icon_filename
    extHelp.setIconPath(icon_path)

    ###  Menu Separators ###

    mari.menus.addSeparator(UI_path,'Release Notes')