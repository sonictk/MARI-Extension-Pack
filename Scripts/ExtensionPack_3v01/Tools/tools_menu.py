# --------------------------------------------------------------------
# Mari Extension Pack GUI Tools
# Copyright (c) 2015 MARI Extension Pack. All Rights Reserved.
# --------------------------------------------------------------------
# Written by Jens Kafitz, 2015
# http://www.campi3d.com
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


'''

The following adds new functionality to the MARI Gui.
Items are grouped by the standard MARI Menus they appear in such as
CHANNELS,LAYERS,PATCHES etc.

Items are placed within existing Menus (UI_Path) and a copy is placed
in a common Script Menu (script_menu_path)

actionScripts are accessing customScript class defined in __init__ file.

A global extPack_icon_path variable exists for Icons places in the ExtPack Icon Folder.

Please note that Shortcuts should NOT be set as part of the action creation
Shortcuts are defined in bulk at the very end of the function by passing the shortcut
to set and the action path to a shortcut check function that ensures that User
set shortcuts are respected

The very end of the file is reserved for signal connections

'''


# --------------------------------------------------------------------


import mari
import os

tool_menu_version = '3.0'

# Global Icon Path for custom icons
extPack_icon_path = os.path.join(os.path.dirname(__file__), "Icons")



def setShortCutifEmpty(shortcut,actionpath):
    ''' Checks if User assigned Shortcut or shortcut clash exists'''

    try:
        # if a shortcut exists this won't error
        mari.actions.shortcut(actionpath)
        shortcutIsSet = True
    except Exception:
        shortcutIsSet = False
        pass

    if shortcutIsSet == False and mari.actions.shortcutIsInUse(shortcut) == False:
        action = mari.actions.get(actionpath)
        action.setShortcut(shortcut)



def createToolsMenu():
    '''Adds all Extension Pack Elements to UI'''

######################################################################
# FILE
######################################################################


    #  set Project Paths (Paths)

    UI_path = 'MainWindow/File'
    script_menu_path = 'MainWindow/Scripts/File'

    setProjectPath = mari.actions.create ('/Mari/MARI Extension Pack/File/Project Paths', 'mari.customScripts.set_project_paths()')
    mari.actions.addToSet('RequiresProject',setProjectPath)

    mari.menus.addAction(setProjectPath, UI_path, 'Settings')
    mari.menus.addAction(setProjectPath, script_menu_path)

    icon_filename = 'Folder.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    setProjectPath.setIconPath(icon_path)


######################################################################
# Selection
######################################################################



    ###  Isolate Select ###

    UI_path = 'MainWindow/Selection'
    script_menu_path = 'MainWindow/Scripts/Selection'
    context_path = 'Canvas/Context/Visibility'

    isolateSelect = mari.actions.create('/Mari/MARI Extension Pack/Selection/Isolate Selection', 'mari.customScripts.isolateSelect()')
    mari.actions.addToSet('RequiresProject',isolateSelect)

    mari.menus.addAction(isolateSelect, UI_path, 'Hide Unselected')
    mari.menus.addAction(isolateSelect, context_path,'Hide Unselected')
    mari.menus.addAction(isolateSelect, script_menu_path)

    icon_filename = 'ShowAll.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    isolateSelect.setIconPath(icon_path)


######################################################################
# Objects
######################################################################



    ###  Subdivision ###

    UI_path = 'MainWindow/Objects/' + u'Subdivision'
    script_menu_path = 'MainWindow/Scripts/Objects/' + u'Subdivision'
    context_path = 'MriGeoEntity/ItemContext/'  + u'Subdivision'


    setAllToHighestSUBD = mari.actions.create('/Mari/MARI Extension Pack/Objects/Subdivision/Set all to Highest Level', 'mari.customScripts.setAllSUBDToHigh()')
    mari.actions.addToSet('RequiresProject',setAllToHighestSUBD)
    mari.menus.addAction(setAllToHighestSUBD, UI_path, 'Generate')
    mari.menus.addAction(setAllToHighestSUBD, context_path,'Generate')
    mari.menus.addAction(setAllToHighestSUBD, script_menu_path)

    icon_filename = 'lighting_flat.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    setAllToHighestSUBD.setIconPath(icon_path)

    setAllToLowestSUBD = mari.actions.create('/Mari/MARI Extension Pack/Objects/Subdivision/Set all to Lowest Level', 'mari.customScripts.setAllSUBDToLow()')
    mari.actions.addToSet('RequiresProject',setAllToLowestSUBD)
    mari.menus.addAction(setAllToLowestSUBD, UI_path)
    mari.menus.addAction(setAllToLowestSUBD, context_path)
    mari.menus.addAction(setAllToLowestSUBD, script_menu_path)

    icon_filename = 'SinglePane.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    setAllToLowestSUBD.setIconPath(icon_path)


    setAllVisibleToHighestSUBD = mari.actions.create('/Mari/MARI Extension Pack/Objects/Subdivision/Set all Visible to Highest Level', 'mari.customScripts.setVisibleSUBDToHigh()')
    mari.actions.addToSet('RequiresProject',setAllVisibleToHighestSUBD)
    mari.menus.addAction(setAllVisibleToHighestSUBD, UI_path)
    mari.menus.addAction(setAllVisibleToHighestSUBD, context_path)
    mari.menus.addAction(setAllVisibleToHighestSUBD, script_menu_path)

    icon_filename = 'lighting_flat.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    setAllVisibleToHighestSUBD.setIconPath(icon_path)

    setAllVisibleToLowestSUBD = mari.actions.create('/Mari/MARI Extension Pack/Objects/Subdivision/Set all Visible to Lowest Level', 'mari.customScripts.setVisibleSUBDToLow()')
    mari.actions.addToSet('RequiresProject',setAllVisibleToLowestSUBD)
    mari.menus.addAction(setAllVisibleToLowestSUBD, UI_path)
    mari.menus.addAction(setAllVisibleToLowestSUBD, context_path)
    mari.menus.addAction(setAllVisibleToLowestSUBD, script_menu_path)

    icon_filename = 'SinglePane.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    setAllVisibleToLowestSUBD.setIconPath(icon_path)


    ###  Menu Separators ###

    mari.menus.addSeparator(UI_path,'Set all Visible to Highest Level')
    mari.menus.addSeparator(context_path,'Set all Visible to Highest Level')


    #  Export Geometry

    UI_path = 'MainWindow/Objects'
    script_menu_path = 'MainWindow/Scripts/Objects'
    context_path = 'MriGeoEntity/ItemContext'

    exportGeo = mari.actions.create ('/Mari/MARI Extension Pack/Objects/Export Object', 'mari.customScripts.exportGeometry()')
    mari.actions.addToSet('RequiresProject',exportGeo)
    exportGeoLight = mari.actions.create ('Export Object', 'mari.customScripts.exportGeometryLight()')
    mari.actions.addToSet('RequiresProject',exportGeoLight)
    mari.menus.addAction(exportGeo, UI_path, 'Ambient Occlusion')
    mari.menus.addAction(exportGeoLight, context_path,'Remove Object')
    mari.menus.addAction(exportGeo, script_menu_path)

    icon_filename = 'SaveFileAs.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    exportGeo.setIconPath(icon_path)
    exportGeoLight.setIconPath(icon_path)


    #  Export UV Mask

    UI_path = 'MainWindow/Objects'
    script_menu_path = 'MainWindow/Scripts/Objects'
    context_path = 'MriGeoEntity/ItemContext'

    # One launches full interface where you can select multiple objects, the other just works on current object
    exportUVMask = mari.actions.create ('/Mari/MARI Extension Pack/Objects/Export UV Mask', 'mari.customScripts.exportUVMasks()')
    mari.actions.addToSet('RequiresProject',exportUVMask)
    exportUVMaskLight = mari.actions.create ('Export UV Mask', 'mari.customScripts.exportUVMasksLight()')
    mari.actions.addToSet('RequiresProject',exportUVMaskLight)


    mari.menus.addAction(exportUVMask, UI_path, 'Ambient Occlusion')
    mari.menus.addAction(exportUVMaskLight, context_path,'Ambient Occlusion')
    mari.menus.addAction(exportUVMask, script_menu_path)

    icon_filename = 'EdgeMask.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    exportUVMask.setIconPath(icon_path)
    exportUVMaskLight.setIconPath(icon_path)


    ###  Menu Separators ###

    mari.menus.addSeparator(UI_path,'Ambient Occlusion')
    mari.menus.addSeparator(context_path,'Ambient Occlusion')



######################################################################
# Channels
######################################################################


    ###   Duplicate & Flatten Selected Channels ###

    UI_path = 'MainWindow/&Channels'
    script_menu_path = 'MainWindow/Scripts/Channels'

    DuplicateFlatten = mari.actions.create ('/Mari/MARI Extension Pack/Channels/Duplicate && Flatten', 'mari.customScripts.flattenSelectedChannels()')
    mari.actions.addToSet('RequiresProject',DuplicateFlatten)

    mari.menus.addAction(DuplicateFlatten, UI_path, 'Flatten')
    mari.menus.addAction(DuplicateFlatten, script_menu_path)

    icon_filename = 'BakeShader.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    DuplicateFlatten.setIconPath(icon_path)

    # --------------------------------------------------------------------

    ###   Export Custom Channel Selection ###

    # Added twice to main interface to maintain existing logic
    UI_path_A = 'MainWindow/&Channels/Export Flattened'
    UI_path_B = 'MainWindow/&Channels/Export'
    Context_path_A = 'Canvas/Context/Export Flattened'
    Context_path_B = 'Canvas/Context/Export'
    script_menu_path = 'MainWindow/Scripts/Channels/Export'

    ExportSelectedFlattened = mari.actions.create ('/Mari/MARI Extension Pack/Channels/Export Custom Channel Selection', 'mari.customScripts.exportSelectedChannelsFlattened()')
    ExportSelected = mari.actions.create ('Export Custom Channel Selection', 'mari.customScripts.exportSelectedChannels()')
    mari.actions.addToSet('RequiresProject',ExportSelectedFlattened)
    mari.actions.addToSet('RequiresProject',ExportSelected)


    mari.menus.addAction(ExportSelectedFlattened, UI_path_A,'Export All Channels Flattened')
    mari.menus.addAction(ExportSelected, UI_path_B,'Export All Channels')
    mari.menus.addAction(ExportSelectedFlattened, Context_path_A,'Export All Channels Flattened')
    mari.menus.addAction(ExportSelected, Context_path_B,'Export All Channels')
    mari.menus.addAction(ExportSelectedFlattened, script_menu_path)

    icon_filename = 'ExportImages.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    ExportSelected.setIconPath(icon_path)
    ExportSelectedFlattened.setIconPath(icon_path)

    # --------------------------------------------------------------------
    ###   Save Channel Resolution ###

    UI_path = 'MainWindow/&Channels/Resize'
    script_menu_path = 'MainWindow/Scripts/Channels/Template'

    getChannelTemplate = mari.actions.create ('/Mari/MARI Extension Pack/Channels/Resize/Save Channel Resolution ', 'mari.customScripts.channel_template_get()')
    mari.actions.addToSet('RequiresProject',getChannelTemplate)

    mari.menus.addAction(getChannelTemplate, UI_path)
    mari.menus.addAction(getChannelTemplate, script_menu_path)

    icon_filename = 'Channel.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    getChannelTemplate.setIconPath(icon_path)

    # --------------------------------------------------------------------

    ###    Load Channel Resolution ###

    UI_path = 'MainWindow/&Channels/Resize'
    script_menu_path = 'MainWindow/Scripts/Channels/Template'

    setChannelTemplate = mari.actions.create ('/Mari/MARI Extension Pack/Channels/Resize/Load Channel Resolution', 'mari.customScripts.channel_template_set()')
    mari.actions.addToSet('RequiresProject', setChannelTemplate)


    mari.menus.addAction(setChannelTemplate, UI_path)
    mari.menus.addAction(setChannelTemplate, script_menu_path)

    icon_filename = 'ChannelPresets.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    setChannelTemplate.setIconPath(icon_path)

# --------------------------------------------------------------------

    ###    Create Channel from Resolution ###

    # To avoid Interface bloat this is currently not embedded into the Channel Palette and only accessible via the Script Menu.
    # Ideally we should come up with a way to add this to the "Channel Size" Dropdowns under "Add Channel" / "Quick Channel"

    UI_path = 'MainWindow/&Channels'
    script_menu_path = 'MainWindow/Scripts/Channels/Template'

    newChannelFromTemplate = mari.actions.create ('/Mari/MARI Extension Pack/Channels/Resize/Create Channel from Resolution', 'mari.customScripts.channel_template_create()')
    mari.actions.addToSet('RequiresProject',newChannelFromTemplate)


    # mari.menus.addAction(newChannelFromTemplate, UI_path)
    mari.menus.addAction(newChannelFromTemplate, script_menu_path)

    icon_filename = "AddChannel.png"
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    newChannelFromTemplate.setIconPath(icon_path)

# --------------------------------------------------------------------

    ###   Duplicate Channels ###

    UI_path = 'MainWindow/&Channels'
    script_menu_path = 'MainWindow/Scripts/Channels'

    DuplicateChannel = mari.actions.create ('/Mari/MARI Extension Pack/Channels/Duplicate', 'mari.customScripts.duplicate_channel()')
    mari.actions.addToSet('RequiresProject',DuplicateChannel)

    mari.menus.addAction(DuplicateChannel, UI_path, 'Cut')
    mari.menus.addAction(DuplicateChannel, script_menu_path)

    icon_filename = 'DuplicateChannel.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    DuplicateChannel.setIconPath(icon_path)

# --------------------------------------------------------------------

    ###   Pin to Collection ###

    UI_path = 'MainWindow/&Channels/' + u'Pin'
    script_menu_path = 'MainWindow/Scripts/Channels/' + u'Pin'

    # Actions for Saving and managing pins

    quickPinChannel = mari.actions.create('/Mari/MARI Extension Pack/Channels/Pin Channels/Save Quick Pin', 'mari.customScripts.quickPin("channel")')
    pinCollectionChannel = mari.actions.create('/Mari/MARI Extension Pack/Channels/Pin Channels/Pin to Collection', 'mari.customScripts.collectionPin("channel")')

    # Actions for Adding pinned Layers
    mari.actions.addToSet('RequiresProject',quickPinChannel)
    mari.actions.addToSet('RequiresProject',pinCollectionChannel)

    mari.menus.addAction(quickPinChannel,UI_path,'Duplicate')
    mari.menus.addAction(quickPinChannel,script_menu_path)
    mari.menus.addAction(pinCollectionChannel,UI_path)
    mari.menus.addAction(pinCollectionChannel,script_menu_path)

    icon_filename = 'linked.16x16.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    quickPinChannel.setIconPath(icon_path)

    icon_filename = 'script.16x16.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    pinCollectionChannel.setIconPath(icon_path)


######################################################################
# Layers
######################################################################


    ###  Channel Layer ###

    UI_path = 'MainWindow/&Layers'
    script_menu_path = 'MainWindow/Scripts/Layers'

    chanLayer = mari.actions.create('/Mari/MARI Extension Pack/Layers/Add Channel Layer', 'mari.customScripts.ChannelLayerUI_layer()')
    mari.actions.addToSet('RequiresProject',chanLayer)

    mari.menus.addAction(chanLayer, UI_path, 'Add Adjustment Layer')
    mari.menus.addAction(chanLayer, script_menu_path)

    icon_filename = 'Channel.16x16.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    chanLayer.setIconPath(icon_path)


    # --------------------------------------------------------------------

    ###  Clone & merge layers ###

    UI_path = 'MainWindow/&Layers/'
    script_menu_path = 'MainWindow/Scripts/Layers'

    MergeDuplicate = mari.actions.create('/Mari/MARI Extension Pack/Layers/Clone && Merge Layers', 'mari.customScripts.CloneMerge()')
    mari.actions.addToSet('RequiresProject',MergeDuplicate)

    mari.menus.addAction(MergeDuplicate, UI_path,'Transfer')
    mari.menus.addAction(MergeDuplicate, script_menu_path)

    icon_filename = 'AddChannel.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    MergeDuplicate.setIconPath(icon_path)


    # --------------------------------------------------------------------

    # Removes existing default 'Convert to Paintable' from Interface to be
    # replaced by batch Convert to Paintable (below)

    mari.menus.removeAction('MainWindow/&Layers/Convert To Paintable')

    # --------------------------------------------------------------------

    ### Convert to Paintable (batch) ###

    UI_path = 'MainWindow/&Layers/'
    script_menu_path = 'MainWindow/Scripts/Layers'

    BatchConvertToPaintable = mari.actions.create ('/Mari/MARI Extension Pack/Layers/Convert To Paintable', 'mari.customScripts.convertToPaintable()')
    mari.actions.addToSet('RequiresProject',BatchConvertToPaintable)

    mari.menus.addAction(BatchConvertToPaintable, UI_path,'Sharing')
    mari.menus.addAction(BatchConvertToPaintable, script_menu_path)

    icon_filename = 'Painting.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    BatchConvertToPaintable.setIconPath(icon_path)


    # --------------------------------------------------------------------

    ###  Convert to Paintable Menu Separators ###

    mari.menus.addSeparator(UI_path,'Sharing')
    mari.menus.addSeparator(UI_path,'Convert To Paintable')

    # --------------------------------------------------------------------

    ### Pin Layers

    UI_path = 'MainWindow/&Layers/' + u'Pin'
    script_menu_path = 'MainWindow/Scripts/Layers/' + u'Pin'

    # Actions for Saving and managing pins
    quickPinLayer = mari.actions.create('/Mari/MARI Extension Pack/Layers/Pin Layers/Save Quick Pin', 'mari.customScripts.quickPin("layer")')
    pinCollectionLayer = mari.actions.create('/Mari/MARI Extension Pack/Layers/Pin Layers/Pin to Collection', 'mari.customScripts.collectionPin("layer")')
    manageCollections = mari.actions.create('/Mari/MARI Extension Pack/Layers/Pin Layers/Edit Collection Pins', 'mari.customScripts.manageCollectionPins()')

    # Actions for Adding pinned Layers
    quickPinInsert = mari.actions.create('/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/Quick Pin','mari.customScripts.emptyPin()')
    emptyCol = mari.actions.create('/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/No Collection Pins',None)


    mari.actions.addToSet('RequiresProject',quickPinLayer)
    mari.actions.addToSet('RequiresProject',pinCollectionLayer)
    mari.actions.addToSet('RequiresProject',manageCollections)
    mari.actions.addToSet('RequiresProject',quickPinInsert)
    mari.actions.addToSet('RequiresProject',emptyCol)


    mari.menus.addAction(quickPinLayer,UI_path,'Cut')
    mari.menus.addAction(quickPinLayer,script_menu_path)
    mari.menus.addAction(pinCollectionLayer,UI_path)
    mari.menus.addAction(pinCollectionLayer,script_menu_path)
    mari.menus.addAction(manageCollections,UI_path)
    mari.menus.addAction(manageCollections,script_menu_path)


    icon_filename = 'linked.16x16.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    quickPinLayer.setIconPath(icon_path)
    quickPinInsert.setIconPath(icon_path)

    icon_filename = 'script.16x16.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    pinCollectionLayer.setIconPath(icon_path)

    icon_filename = 'Folder.16x16.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    manageCollections.setIconPath(icon_path)

    UI_path = 'MainWindow/&Layers/' + u'Add Pinned Layer'
    mari.menus.addAction(quickPinInsert,UI_path,'Add Adjustment Layer')
    mari.menus.addSeparator(UI_path)
    mari.menus.addAction(emptyCol,UI_path)



    # --------------------------------------------------------------------


    ###  Toggle Layer Visbility ###

    UI_path = 'MainWindow/&Layers/' + u'Visibility + Lock'
    script_menu_path = 'MainWindow/Scripts/Layers/' + u'Visibility + Lock'


    toggleSelVisibility = mari.actions.create('/Mari/MARI Extension Pack/Layers/Visibility + Lock/Toggle Selected Visibility', 'mari.customScripts.toggleSelVisibility()')
    mari.actions.addToSet('RequiresProject',toggleSelVisibility)

    mari.menus.addAction(toggleSelVisibility, UI_path, 'Remove Layers')
    mari.menus.addAction(toggleSelVisibility, script_menu_path)

    icon_filename = 'ToggleVisibility.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    toggleSelVisibility.setIconPath(icon_path)


    toggleUnselVisibility = mari.actions.create('/Mari/MARI Extension Pack/Layers/Visibility + Lock/Toggle Unselected Visibility', 'mari.customScripts.toggleUnselVisibility()')
    mari.actions.addToSet('RequiresProject',toggleUnselVisibility)

    mari.menus.addAction(toggleUnselVisibility, UI_path)
    mari.menus.addAction(toggleUnselVisibility, script_menu_path)

    icon_filename = 'ToggleVisibility.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    toggleUnselVisibility.setIconPath(icon_path)



    # --------------------------------------------------------------------

    ###  Toggle Layer Lock ###

    UI_path = 'MainWindow/&Layers/' + u'Visibility + Lock'
    script_menu_path = 'MainWindow/Scripts/Layers/Visibility + Lock'

    toggleSelLock = mari.actions.create('/Mari/MARI Extension Pack/Layers/Visibility + Lock/Toggle Selected Lock', 'mari.customScripts.toggleSelLock()')
    mari.actions.addToSet('RequiresProject',toggleSelLock)

    mari.menus.addAction(toggleSelLock, UI_path)
    mari.menus.addAction(toggleSelLock, script_menu_path)

    icon_filename = 'Lock.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    toggleSelLock.setIconPath(icon_path)


    toggleUnselLock = mari.actions.create('/Mari/MARI Extension Pack/Layers/Visibility + Lock/Toggle Unselected Lock', 'mari.customScripts.toggleUnselLock()')
    mari.actions.addToSet('RequiresProject',toggleUnselLock)

    mari.menus.addAction(toggleUnselLock, UI_path)
    mari.menus.addAction(toggleUnselLock, script_menu_path)

    icon_filename = 'Lock.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    toggleUnselLock.setIconPath(icon_path)


    # --------------------------------------------------------------------

    ###  Lock/Visibility Separator Main Interface ###

    mari.menus.addSeparator(UI_path,'Toggle Selected Lock')
    mari.menus.addSeparator('MainWindow/&Layers/','Remove Layers')


    # --------------------------------------------------------------------

    ### Channel Mask ###

    UI_path = 'MainWindow/&Layers/Layer Mask/Add Mask'
    script_menu_path = 'MainWindow/Scripts/Layers/Layer Mask'

    chanMask = mari.actions.create('/Mari/MARI Extension Pack/Layers/Add Mask/Add Channel Mask', 'mari.customScripts.ChannelLayerUI_layermask()')
    mari.actions.addToSet('RequiresProject',chanMask)

    mari.menus.addAction(chanMask, UI_path)
    mari.menus.addAction(chanMask, script_menu_path)

    icon_filename = 'Channel.16x16.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    chanMask.setIconPath(icon_path)


    ### Channel Mask Group ###

    UI_path = 'MainWindow/&Layers/Layer Mask/Add Mask'
    script_menu_path = 'MainWindow/Scripts/Layers/Layer Mask'

    chanMaskGrp = mari.actions.create('/Mari/MARI Extension Pack/Layers/Add Mask/Add grouped Channel Mask', 'mari.customScripts.ChannelLayerUI_maskgroup()')
    mari.actions.addToSet('RequiresProject',chanMaskGrp)

    mari.menus.addAction(chanMaskGrp, UI_path)
    mari.menus.addAction(chanMaskGrp, script_menu_path)

    icon_filename = 'NewFolder.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    chanMaskGrp.setIconPath(icon_path)



######################################################################
# Patches
######################################################################


    ###   Patch Bake to Image Manager ###

    UI_path = 'MainWindow/&Patches'
    script_menu_path = 'MainWindow/Scripts/Patches'

    PatchToImageMgr= mari.actions.create('/Mari/MARI Extension Pack/Patches/Patch to Image Manager', 'mari.customScripts.patch_bake_to_imageman()')
    mari.actions.addToSet('RequiresProject',PatchToImageMgr)

    mari.menus.addAction(PatchToImageMgr, UI_path,'UV Mask to Image Manager')
    mari.menus.addAction(PatchToImageMgr, script_menu_path)

    icon_filename = 'SaveToImageManager.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
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

    ChannelToImageMgr = mari.actions.create('/Mari/MARI Extension Pack/Camera/Quick Unproject Channel', 'mari.customScripts.unproject_channel_to_imageman()')
    mari.actions.addToSet('RequiresProject',ChannelToImageMgr)

    mari.menus.addAction(ChannelToImageMgr, script_menu_path)
    mari.menus.addAction(ChannelToImageMgr, UI_path,'Camera Left')

    icon_filename = 'SaveToImageManager.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    ChannelToImageMgr.setIconPath(icon_path)


    # --------------------------------------------------------------------

    ###   Quick Unproject Layer to Image Manager ###

    UI_path = 'MainWindow/&Camera'
    script_menu_path = 'MainWindow/Scripts/Camera'

    LayerToImageMgr = mari.actions.create('/Mari/MARI Extension Pack/Camera/Quick Unproject Layer', 'mari.customScripts.unproject_layer_to_imageman()')
    mari.actions.addToSet('RequiresProject',LayerToImageMgr)

    mari.menus.addAction(LayerToImageMgr, UI_path,'Camera Left')
    mari.menus.addAction(LayerToImageMgr, script_menu_path)

    icon_filename = 'SaveToImageManager.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
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

    screenshotChannels = mari.actions.create('/Mari/MARI Extension Pack/View/Screenshot All Channels','mari.customScripts.screenshot_all_channels()')
    mari.actions.addToSet('RequiresProject',screenshotChannels)

    mari.menus.addAction(screenshotChannels, UI_path, 'Screenshot Settings')
    mari.menus.addAction(screenshotChannels, script_menu_path)

    icon_filename = 'CanvasSnapshot.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    screenshotChannels.setIconPath(icon_path)


######################################################################
# Shading
######################################################################

    #  Disable Viewport Refresh

    script_menu_path = 'MainWindow/Scripts/Shading'
    UI_path = 'MainWindow/&Shading'

    action_viewportDisable = mari.actions.create("/Mari/MARI Extension Pack/Shading/Pause Viewport Update", "mari.customScripts.disableViewport('full')")
    action_viewportDisable.setCheckable(True)
    mari.actions.addToSet('RequiresProject',action_viewportDisable)


    mari.menus.addAction(action_viewportDisable, script_menu_path)
    mari.menus.addAction(action_viewportDisable, UI_path, 'Toggle Wireframe')

    icon_filename = 'extPack_disableViewport.png'
    icon_path = extPack_icon_path + os.sep +  icon_filename
    action_viewportDisable.setIconPath(icon_path)


    action_viewportDisable.setStatusTip('Pause Viewport Update. This can help speed up operations by not having to wait for the viewport to update.')
    action_viewportDisable.setToolTip('Pause Viewport Update')
    action_viewportDisable.setWhatsThis('Pause Viewport Update. A repackaged toggleShaderCompile action')

    # Adding to default lighting toolbar
    lightingToolbar = mari.app.findToolBar('Lighting')
    isLocked = lightingToolbar.isLocked()
    lightingToolbar.setLocked(False)
    lightingToolbar.addAction('/Mari/MARI Extension Pack/Shading/Pause Viewport Update', [0,0], False)
    lightingToolbar.setLocked(isLocked)

    # Hooking up a signal directly to the viewport
    toggleCompileAction = mari.actions.get('/Mari/Canvas/Toggle Shader Compiling')
    mari.utils.connect(toggleCompileAction.triggered,lambda: mari.customScripts.disableViewport('iconOnly'))


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
        "/Mari/MARI Extension Pack/Shaders Palette/Sync Object Shaders", "mari.customScripts.setAllObjectsToShader()"
        )

    mari.actions.addToSet('RequiresProject',syncObjectShaders)


    syncObjectShaders.setStatusTip('Sync your Shader Selection across all Objects')
    syncObjectShaders.setToolTip('Sync Object Shader Selection')
    syncObjectShaders.setWhatsThis('Sync Object Shader Selection between Objects')

    mari.menus.addAction(syncObjectShaders, UI_path_A, '-Flat')
    mari.menus.addAction(syncObjectShaders, UI_path_B)
    mari.menus.addAction(syncObjectShaders, UI_path_C,'Duplicate Shader')
    mari.menus.addAction(syncObjectShaders, script_menu_path)

    icon_filename = "Shader.png"
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    syncObjectShaders.setIconPath(icon_path)

######################################################################
# Selection Groups
######################################################################

    #  Create Material ID Channel from Selection Groups

    UI_path_B = 'MriGeometrySelectionGroup/Panel'
    script_menu_path = 'MainWindow/Scripts/Selection Groups'

    matIdFromGroup = mari.actions.create("/Mari/MARI Extension Pack/Shaders Palette/MaterialID from Selection Groups", "mari.customScripts.matIDFromGroup()")
    mari.actions.addToSet('RequiresProject',matIdFromGroup)


    matIdFromGroup.setStatusTip('Create a MaterialID Channel from Selection Groups')
    matIdFromGroup.setToolTip('Create a MaterialID Channel from Selection Groups')
    matIdFromGroup.setWhatsThis('Create a MaterialID Channel from Selection Groups')

    mari.menus.addAction(matIdFromGroup, UI_path_B)
    mari.menus.addAction(matIdFromGroup, script_menu_path)

    icon_filename = "Shader.png"
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    matIdFromGroup.setIconPath(icon_path)


######################################################################
# Image Manager
######################################################################

    #  Export selected Image Manager Images

    UI_path = 'MriImageManager/ItemContext'
    script_menu_path = 'MainWindow/Scripts/Image Manager'

    exportImageMan = mari.actions.create ('/Mari/MARI Extension Pack/Image Manager/Export Selection', 'mari.customScripts.exportImageManager()')
    mari.actions.addToSet('RequiresProject',exportImageMan)

    mari.menus.addAction(exportImageMan, UI_path)
    mari.menus.addAction(exportImageMan, script_menu_path)

    icon_filename = 'ExtractImage.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    exportImageMan.setIconPath(icon_path)

    ###  Menu Separators ###

    mari.menus.addSeparator(UI_path,'Export Selection')



######################################################################
# ONLINE HELP
######################################################################

    # EXTENSION PACK ONLINE HELP

    UI_path = 'MainWindow/Help'
    script_menu_path = 'MainWindow/Scripts/Help'

    extHelp = mari.actions.create('/Mari/MARI Extension Pack/Help/Extension Pack Online Help','mari.customScripts.open_online_help()')
    mari.menus.addAction(extHelp, UI_path, 'Release Notes')
    mari.menus.addAction(extHelp, script_menu_path)

    icon_filename = 'Help.png'
    icon_path = mari.resources.path(mari.resources.ICONS) + os.sep +  icon_filename
    extHelp.setIconPath(icon_path)

    ###  Menu Separators ###

    mari.menus.addSeparator(UI_path,'Release Notes')


######################################################################
# LOAD USER SHORTCUTS OVERWRITING ANY DEFAULT ONES FOR EXT PACK ACTIONS
######################################################################

    mari.actions.loadUserShortcuts()

    setShortCutifEmpty('Ctrl+1','/Mari/MARI Extension Pack/Selection/Isolate Selection')
    setShortCutifEmpty('Ctrl+Shift+E','/Mari/MARI Extension Pack/Layers/Clone && Merge Layers')
    setShortCutifEmpty('Ctrl+Alt+C','/Mari/MARI Extension Pack/Layers/Pin Layers/Save Quick Pin')
    setShortCutifEmpty('Ctrl+Alt+V','/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/Quick Pin')
    setShortCutifEmpty('Ctrl+Space',"/Mari/MARI Extension Pack/Shading/Pause Viewport Update")


######################################################################
# PROJECT SIGNAL ATTACHMENTS
######################################################################

    # Disable Elements when no project is open, this is done by toggling the 'RequiresProject' set on or off

    if mari.projects.current() is None:
        mari.actions.disableSet('RequiresProject')
    else:
        mari.actions.enableSet('RequiresProject')

    mari.utils.connect(mari.projects.opened, lambda: mari.actions.enableSet('RequiresProject'))
    mari.utils.connect(mari.projects.closed, lambda: mari.actions.disableSet('RequiresProject'))

    # -------------------------------------------------------------------------

    #  Restore Collection Pins when project loaded, clear them if project closed

    mari.utils.connect(mari.projects.opened, lambda: mari.customScripts.restoreProjectPins())
    mari.utils.connect(mari.projects.closed, lambda: mari.customScripts.clearCollectionPins())

    # -------------------------------------------------------------------------

    #  Restore User Set Project Paths on project Load

    mari.utils.connect(mari.projects.opened, lambda: mari.customScripts.restore_project_paths())



######################################################################
# DEBUGGING HELPER
######################################################################

# The following line just makes sure that the RequiresProject set is enabled at all times a project is open.
# This usually happens automatically but when working in python console using mari.utils.reloadAll() out of a project
# after reloading scripts the set isn't enabled.

if mari.projects.current() is not None:
    mari.actions.enableSet('RequiresProject')












