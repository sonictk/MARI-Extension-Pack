import mari




# ------------------------------------------------------------------------------  
import Patches.patch_bake_to_imageman as patch_bake_to_imageman

import Camera.unproject_channel_to_imageman as unproject_channel_to_imageman
import Camera.unproject_layer_to_imageman as unproject_layer_to_imageman

import Layers.channel_mask as channel_mask
import Layers.mask_from_selection as mask_from_selection
import Layers.clone_merge_layers as clone_merge_layers
import Layers.toggle_layer_visibility_lock as toggle_layer_visibility_lock
import Layers.convert_to_paintable as convert_to_paintable

import Channels.export_selected_channels as export_selected_channels
import Channels.flatten_selected_channels as flatten_selected_channels
import Channels.channel_template as channel_template

import Object.export_uv_masks as export_uv_masks

import Review.screenshot_all_channels as screenshot_all_channels
# ------------------------------------------------------------------------------   

class customScripts():

    def patch_bake_to_imageman(self):
        patch_bake_to_imageman.patch_bake_to_imageman()

    def unproject_channel_to_imageman(self):
        unproject_channel_to_imageman.unproject_channel_to_imageman()

    def unproject_layer_to_imageman(self):
        unproject_layer_to_imageman.unproject_layer_to_imageman()

    # ------------------------------------------------------------    

    def exportSelectedChannels(self):
        export_selected_channels.exportSelectedChannels()

    def flattenSelectedChannels(self):
        flatten_selected_channels.flattenSelectedChannels()

    def channel_template_get(self):
        channel_template.getChannelTemplate()

    def channel_template_create(self):
        channel_template.createChannelFromTemplate()

    def channel_template_set(self):
        channel_template.setChannelFromTemplate()

    # ------------------------------------------------------------   

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


    def selectionMask(self):
        mask_from_selection.selectionMask(invert=False)

    def selectionMask_inv(self):
        mask_from_selection.selectionMask(invert=True)

    def CLCreate_layer(self):
        channel_mask.CLCreate("layer").exec_()

    def CLCreate_layermask(self):
        channel_mask.CLCreate("mask").exec_()

    def CLCreate_maskgroup(self):
        channel_mask.CLCreate("maskgroup").exec_()

    def convertToPaintable(self):
        convert_to_paintable.convertToPaintable()

    # --------------------------------------------------------------

    def exportUVMasks(self):
        export_uv_masks.exportUVMasks()

    # --------------------------------------------------------------

    def screenshot_all_channels(self):
        screenshot_all_channels.screenshotAllChannels()


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
print 'Channel Tools added (4): '
print 'Channel Menu: Export Custom Selection'
print 'Channel Menu: Duplicate & Flatten'
print 'Channel Menu: Resize/Save Channel Resolution'
print 'Channel Menu: Resize/Load Channel Resolution'
print '-----------------------------------------'
print 'Layer Tools added (5): '
print 'Layer Menu: Add Channel Layer'
print 'Layer Menu: Layer Mask/Add Mask/Add Channel Mask'
print 'Layer Menu: Layer Mask/Add Mask/Add Channel Mask (Group)'
print 'Layer Menu: Clone & Merge Layers'
print 'Layer Menu: Convert To Paintable (replaces default)'
print '-----------------------------------------'
print 'Patches Tools added (1): '
print 'Patches Menu: Patch to Image Manager'
print '-----------------------------------------'
print 'Camera Tools added (2): '
print 'Camera Menu: Quick Unproject Channel'
print 'Camera Menu: Quick Unproject Layer'
print '-----------------------------------------'
# ------------------------------------------------------------------------------




