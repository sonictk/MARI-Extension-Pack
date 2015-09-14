# --------------------------------------------------------------------
# Mari Extension Tools INIT
# Copyright (c) 2015 MARI Extension Pack. All Rights Reserved.
# --------------------------------------------------------------------
# Written by Jens Kafitz, 2015
# http://www.campi3d.com
# --------------------------------------------------------------------
# File: __init__.py
# Description: The following imports all tools found in the relevant
#              subfolders to be accessible by tools_menu.py
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


import mari

tool_init_version = '3.0'

# ------------------------------------------------------------------------------

# FILE:
import File.extPack_setProjectPaths as set_project_paths

# SELECTION:
import Selection.extPack_isolateSelect as isolateSelect

# PATCHES:
import Patches.extPack_patch_bake_to_imageman as patch_bake_to_imageman

 # CAMERA:
import Camera.extPack_unproject_channel_to_imageman as unproject_channel_to_imageman
import Camera.extPack_unproject_layer_to_imageman as unproject_layer_to_imageman

# LAYERS
import Layers.extPack_channel_layer as channel_layer
import Layers.extPack_clone_merge_layers as clone_merge_layers
import Layers.extPack_toggle_visibility_lock as toggle_layer_visibility_lock
import Layers.extPack_convert_to_paintable as convert_to_paintable
import Layers.extPack_pinnedLayers as pinned_layers


# CHANNELS:
import Channels.extPack_exportSelectedChannels as export_selected_channels
import Channels.extPack_flattenSelectedChannels as flatten_selected_channels
import Channels.extPack_channelTemplate as channel_template
import Channels.extPack_duplicateChannel as duplicate_channel

# SHADERS:
import Shaders.extPack_set_all_current_shader as setAllCurrentShader

# SELECTION GROUPS:
import SelectionGroups.extPack_matIDfromGroup as matIDFromGroup

# OBJECTS:
import Object.extPack_export_uv_masks as export_uv_masks
import Object.extPack_export_geometry as export_geometry
import Object.extPack_setSubdivisionLevels as set_subd_level

# IMAGE MANAGER:
import ImageManager.extPack_export_imageMan_images as exportImageManager

# VIEW:
import View.extPack_screenshot_all_channels as screenshot_all_channels

# SHADING:
import Shading.extPack_disableViewport as disableViewport

# HELP:
import Help.extPack_online_help as onlineHelp

# ------------------------------------------------------------------------------

class customScripts():

    # ------------------------------------------------------------
    # FILE:

    def set_project_paths(self):
        set_project_paths.setProjectPath()

    # ------------------------------------------------------------
    # SELECTION:

    def isolateSelect(self):
        isolateSelect.isolateSelect()

    # ------------------------------------------------------------
    # PATCHES:

    def patch_bake_to_imageman(self):
        patch_bake_to_imageman.patch_bake_to_imageman()

    # ------------------------------------------------------------
    # CAMERA:

    def unproject_channel_to_imageman(self):
        unproject_channel_to_imageman.unproject_channel_to_imageman()

    def unproject_layer_to_imageman(self):
        unproject_layer_to_imageman.unproject_layer_to_imageman()

    # ------------------------------------------------------------
    # CHANNELS:

    def exportSelectedChannelsFlattened(self):
        export_selected_channels.exportSelectedChannels('flattened')

    def exportSelectedChannels(self):
        export_selected_channels.exportSelectedChannels('layered')

    def flattenSelectedChannels(self):
        flatten_selected_channels.flattenSelectedChannels()

    def channel_template_get(self):
        channel_template.getChannelTemplate()

    def channel_template_create(self):
        channel_template.createChannelFromTemplate()

    def channel_template_set(self):
        channel_template.setChannelFromTemplate()

    def duplicate_channel(self):
        duplicate_channel.duplicateChannel()


    # ------------------------------------------------------------
    # LAYERS:

    def CloneMerge(self):
        clone_merge_layers.CloneMergeGUI().exec_()

    def toggleSelVisibility(self):
        toggle_layer_visibility_lock.toggleSelVisibility()

    def toggleUnselVisibility(self):
        toggle_layer_visibility_lock.toggleUnselVisibility()

    def toggleSelLock(self):
        toggle_layer_visibility_lock.toggleSelLock()

    def toggleUnselLock(self):
        toggle_layer_visibility_lock.toggleUnselLock()


    def ChannelLayerUI_layer(self):
        channel_layer.ChannelLayerUI("layer").exec_()

    def ChannelLayerUI_layermask(self):
        channel_layer.ChannelLayerUI("mask").exec_()

    def ChannelLayerUI_maskgroup(self):
        channel_layer.ChannelLayerUI("maskgroup").exec_()

    def convertToPaintable(self):
        convert_to_paintable.convertToPaintable()

    # Pinned Layers:

    def emptyPin(self):
        pinned_layers.emptyQuickPin()

    def quickPin(self):
        pinned_layers.addQuickPin()

    def triggerQuickPin(self,layerName,project_uuid,layer_uuid):
        pinned_layers.triggerQuickPin(layerName,project_uuid,layer_uuid)

    def collectionPin(self,mode):
        pinned_layers.addCollectionPin(mode)

    def triggerCollectionPin(self,layerType,layerName,project_uuid,layer_uuid):
        pinned_layers.triggerCollectionPin(layerType,layerName,project_uuid,layer_uuid)

    # --------------------------------------------------------------
    # SHADERS:

    def setAllObjectsToShader(self):
        setAllCurrentShader.setAllCurrentShader()

    # --------------------------------------------------------------
    # SELECTION GROUPS:

    def matIDFromGroup(self):
        matIDFromGroup.matIDFromSelectionGroup()

    # --------------------------------------------------------------
    # OBJECTS:

    def exportUVMasks(self):
        export_uv_masks.exportUVMasks('full')

    def exportUVMasksLight(self):
        export_uv_masks.exportUVMasks('light')

    def exportGeometry(self):
        export_geometry.exportGEOs('full')

    def exportGeometryLight(self):
        export_geometry.exportGEOs('light')

    def setAllSUBDToHigh(self):
        set_subd_level.setAllToHighest()

    def setAllSUBDToLow(self):
        set_subd_level.setAllToLowest()

    def setVisibleSUBDToHigh(self):
        set_subd_level.setAllVisibleToHighest()

    def setVisibleSUBDToLow(self):
        set_subd_level.setAllVisibleToLowest()


    # --------------------------------------------------------------
    # IMAGE MANAGER:

    def exportImageManager(self):
        exportImageManager.exportSelImgs()


    # --------------------------------------------------------------
    # VIEW:

    def screenshot_all_channels(self):
        screenshot_all_channels.screenshotAllChannels()

    # --------------------------------------------------------------
    # SHADING:

    def disableViewport(self,mode):
        disableViewport.disableViewport(mode)

    # --------------------------------------------------------------
    # HELP:

    def open_online_help(self):
        onlineHelp.openExtPackHelp()

# ------------------------------------------------------------------------------

mari.customScripts = customScripts()

# ------------------------------------------------------------------------------
# This is used to generate the menu inside of Mari

import tools_menu
tools_menu.createToolsMenu()


# ------------------------------------------------------------------------------
# Simple Print out of loaded Python Scripts


print "Loading Tool Additions ..."
print '-----------------------------------------'
print 'Lighting Toolbar Additions (1): '
print 'Shading Menu: Pause Viewport Update'
print '-----------------------------------------'
print 'File Additions (1):'
print 'File Menu: Project Paths'
print '-----------------------------------------'
print 'Selection Additions (1):'
print 'Selection Menu: Isolate Selection'
print '-----------------------------------------'
print 'Object Palette Additions (6): '
print 'Object Menu: Export Geometry'
print 'Object Menu: Export UV Masks'
print 'Object Menu: Subdivision/Set all to Highest Level'
print 'Object Menu: Subdivision/Set all to Lowest Level'
print 'Object Menu: Subdivision/Set all visible to Highest Level'
print 'Object Menu: Subdivision/Set all visible to Lowest Level'
print '-----------------------------------------'
print 'Channel Palette Additions (5): '
print 'Channel Menu: Export Custom Selection'
print 'Channel Menu: Duplicate & Flatten'
print 'Channel Menu: Resize/Save Channel Resolution'
print 'Channel Menu: Resize/Load Channel Resolution'
print 'Channel Menu: Duplicate'
print '-----------------------------------------'
print 'Layer Palette Additions (11): '
print 'Layer Menu: Add Pinned Layer'
print 'Layer Menu: Pin/Save Quick Pin'
print 'Layer Menu: Pin/Pin to Collection'
print 'Layer Menu: Pin/Manage Collection Pins'
print 'Layer Menu: Add Channel Layer'
print 'Layer Menu: Layer Mask/Add Mask/Add Channel Mask'
print 'Layer Menu: Layer Mask/Add Mask/Add Channel Mask (Group)'
print 'Layer Menu: Clone & Merge Layers'
print 'Layer Menu: Convert To Paintable (replaces default)'
print 'Layer Menu: Toggle Visibility selected/unselected'
print 'Layer Menu: Toggle Lock selected/unselected'
print '-----------------------------------------'
print 'Patches Palette Additions (1): '
print 'Patches Menu: Patch to Image Manager'
print '-----------------------------------------'
print 'Shader Palette Additions (1): '
print 'Shader Menu: Sync Object Shaders'
print '-----------------------------------------'
print 'SelectionGroup Palette Additions (1): '
print 'Create MaterialID from Selection Group'
print '-----------------------------------------'
print 'Camera Palette Additions (2): '
print 'Camera Menu: Quick Unproject Channel'
print 'Camera Menu: Quick Unproject Layer'
print '-----------------------------------------'
print 'View Palette Additions (1): '
print 'View Menu: Screenshot All Channels'
print '-----------------------------------------'
print 'Image Manager Palette Additions (1): '
print 'Image Manager: Export Selection'
print '-----------------------------------------'
print 'Help Menu Additions (1): '
print 'Help Menu: Mari Extension Pack Help'
print '-----------------------------------------'
# ------------------------------------------------------------------------------




