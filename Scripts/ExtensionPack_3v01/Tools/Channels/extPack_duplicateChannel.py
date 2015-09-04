# ------------------------------------------------------------------------------
# Duplicate Channels
# ------------------------------------------------------------------------------
# 'Duplicate Channels' will create a true Duplicate of the selected Channel
# - Channel Layers will be linked to original channel and channel duplication is
#   avoided (other than copy & paste)
# - Internal Sharing of layers from one point of the layerstack to another is kept without referencing original src channel
# - External Sharing of Layers (layers from 2nd channel shared into src channel) is maintained in duplicate channel
#   and links to 2nd channel are restored in duplicate channel
# - Mixed & combined Internal & External Sharing is maintained without referencing original src channel
# ------------------------------------------------------------------------------
# Written by Jens Kafitz, 2015
# ------------------------------------------------------------------------------
# http://www.campi3d.com
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

class layerList():
    """Searches for Layerlists in substacks. Returns Layers and corresponding stacks"""

    def __init__(self):
        curGeo = None
        curChannel = None
        curLayer = None

    def returnTrue(self,layer):
        """Returns True for any object passed to it."""
        return True


    def getLayerList(self,layer_list, stack, criterionFn):
        """Returns a list of all of the layers in the stack that match the given criterion function, including substacks."""
        matchingLayers = []
        tu = ()
        for layer in layer_list:
            if criterionFn(layer):
                tu = stack,layer
                matchingLayers.append(tu)
            if hasattr(layer, 'layerStack') is True and layer.isChannelLayer() is False:
                matchingLayers.extend(self.getLayerList(layer.layerStack().layerList(),layer.layerStack(),criterionFn))
            if layer.hasMaskStack():
                matchingLayers.extend(self.getLayerList(layer.maskStack().layerList(),layer.maskStack(), criterionFn))
            if hasattr(layer, 'hasAdjustmentStack') and layer.hasAdjustmentStack():
                matchingLayers.extend(self.getLayerList(layer.adjustmentStack().layerList(),layer.adjustmentStack(), criterionFn))

        return matchingLayers

# ------------------------------------------------------------------------------

def restoreSharing(mode,layer_duplicate,target_stack,src_uuid,uuid_dict):
    "Creates a correctly linked shared layer to the original channel or layer"

    layer = layer_duplicate

    currentStack = target_stack
    shareType = mode

    channelLayer_name = layer.name()

    _hasMaskStack = False
    _hasMask = False
    _hasAdjStack = False
    layer_maskStack = ()
    layer_mask = ()
    layer_adjStack = ()
    repairedSharing = None


    shared_target = uuid_dict[src_uuid]

    if shareType == "channel":
        # create a new channel layer that is linked to original channel
        repairedSharing = currentStack.createChannelLayer('CHANNELLAYER',shared_target,layer)

        if layer.hasMask() and not layer.hasMaskStack():
            # if original 'wrong' layer had a mask, recreate it on the new one
            _hasMaskStack = False
            _hasMask = True
            _maskEnabled = True
            _maskEnabled =  layer.isMaskEnabled()
            layer_mask = layer.maskImageSet()
            repairedSharing.setMaskImageSet(layer_mask)
            repairedSharing.setMaskEnabled(_maskEnabled)

        if layer.hasMaskStack():
            # if original 'wrong' layer had a mask stack, recreate it on the new one
            _hasMaskStack = True
            _hasMask = False
            _maskEnabled = True
            _maskEnabled =  layer.isMaskEnabled()
            layer_maskStack = layer.maskStack()
            repairedSharing.setMaskStack(layer_maskStack)
            repairedSharing.setMaskEnabled(_maskEnabled)


        if layer.hasAdjustmentStack():
            # if original 'wrong' layer had an adjustment stack, recreate it on the new one
            _hasAdjStack = True
            _hasActiveAdjStack = layer.isAdjustmentStackEnabled()

            # finding the layerstack and contents of the layerstack that make up the adjustment stack on the layer
            source_adj_stack = layer.adjustmentStack()
            adjustments_in_src_stack = source_adj_stack.layerList()
            # reversing so that it is recreated in right order
            adjustments_inSrc_stack = reversed(adjustments_in_src_stack)

            # Creating adjustment stack on new layer and saving name of layerStack, then moving everything from old  layer to new adjustment stack
            if repairedSharing.hasAdjustmentStack():
                target_adj_stack = repairedSharing.adjustmentStack()
            else:
                repairedSharing.makeAdjustmentStack()
                target_adj_stack = repairedSharing.adjustmentStack()

            for adjustment in adjustments_inSrc_stack:
                target_adj_stack.moveLayer(adjustment)

            repairedSharing.setAdjustmentStackEnabled(_hasActiveAdjStack)


    if shareType == "layer":
        # create a new shared layer that is linked to original shared resource
        repairedSharing = currentStack.shareLayer(shared_target,layer)



    # Saving any layer options on the  layer to set it to the merged layer afterwards
    advBlend = layer.getAdvancedBlendComponent()
    layerBelow = layer.getLayerBelowBlendLut()
    thisLayer = layer.getThisLayerBlendLut()
    blendAmount = layer.blendAmount()
    blendAmountEnabled = layer.blendAmountEnabled()
    blendMode = layer.blendMode()
    blendType = layer.blendType()
    visibility =layer.isVisible()
    locked = layer.isLocked()
    colorTag = layer.colorTag()
    swizzle_r = layer.swizzle(mari.Layer.SWIZZLE_DST_RED)
    swizzle_g = layer.swizzle(mari.Layer.SWIZZLE_DST_GREEN)
    swizzle_b = layer.swizzle(mari.Layer.SWIZZLE_DST_BLUE)
    swizzle_a = layer.swizzle(mari.Layer.SWIZZLE_DST_ALPHA)


    # resetting attributes from original layer onto new layer
    repairedSharing.setAdvancedBlendComponent(advBlend)
    repairedSharing.setLayerBelowBlendLut(layerBelow)
    repairedSharing.setThisLayerBlendLut(thisLayer)
    repairedSharing.setBlendAmount(blendAmount)
    repairedSharing.setBlendAmountEnabled(blendAmountEnabled)
    repairedSharing.setBlendMode(blendMode)
    repairedSharing.setBlendType(blendType)
    repairedSharing.setVisibility(visibility)
    repairedSharing.setLocked(locked)
    repairedSharing.setColorTag(colorTag)
    repairedSharing.setSwizzle(mari.Layer.SWIZZLE_DST_RED,swizzle_r)
    repairedSharing.setSwizzle(mari.Layer.SWIZZLE_DST_GREEN,swizzle_g)
    repairedSharing.setSwizzle(mari.Layer.SWIZZLE_DST_BLUE,swizzle_b)
    repairedSharing.setSwizzle(mari.Layer.SWIZZLE_DST_ALPHA,swizzle_a)
    repairedSharing.setName(channelLayer_name)

    # closing original 'wrong' layer
    layer.close()


def duplicateChannel():

    if not isProjectSuitable(): #Check if project is suitable
        return False

    curChannel = mari.current.channel()
    geo = mari.current.geo()

    # Turning off viewport for better perfromance
    deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
    deactivateViewportToggle.trigger()

    mari.app.setWaitCursor()
    mari.history.startMacro('Duplicate Channel: '+ curChannel.name())

    # Stores Layer Objects together with ther UUID as key
    shared_layer_dict = {}
    # Stores any channel layers in the duplicated channel that need to be removed
    channelsToRemove = []

    hasSharedLayers = False
    hasChannelLayers = False



    # Fetches all associated layers of the channel to duplicate:
    layerlist = curChannel.layerList()
    deep_layerlist = layerList().getLayerList(layerlist,curChannel, layerList().returnTrue)

    # for each layer in full (deep) layerlist of src channel record the UUID of the sharing src as metadata onto the layer
    # while simultaneously storying the UUID together with the Object in a dict.
    for stack,layer in deep_layerlist:

        # Stores a list of UUIDs of layer siblings (shared resources)
        siblingUUIDs = []
        siblingUUIDsString = None

        # Clearing existing metadata in case the channel was duplicated once already, just for safety
        if layer.hasMetadata('DuplicateChannelUUID'):
            layer.removeMetadata('DuplicateChannelUUID')
        if layer.hasMetadata('DuplicateLayerUUID'):
            layer.removeMetadata('DuplicateLayerUUID')

        # Storing all associated shared resources with a UUID key in a dict, and setting a list of UUIDs as metadata
        if layer.isShared() is True and layer.isChannelLayer() is False:
            sibling = layer.siblingSharedLayerList()
            for item in sibling:
                # if uuid already exists on layer (because it was already processed from a shared resource): ignore.
                if item.uuid() in siblingUUIDs:
                    pass
                else:
                    siblingUUIDs.append(item.uuid())
                    shared_layer_dict[item.uuid()] = (item)
            siblingUUIDsString = ' '.join(siblingUUIDs)
            layer.setMetadata('DuplicateLayerUUID',siblingUUIDsString)

        # Storing Channel Layer UUID as Metdadata on Layer and recording channel object in dict.
        if layer.isChannelLayer():
            channel_uuid = layer.channel()
            channel_uuid = channel_uuid.uuid()
            layer.setMetadata('DuplicateChannelUUID',channel_uuid)
            shared_layer_dict[channel_uuid] = (layer.channel())

    # Duplicate Channel standard Mari way with all its bugs
    duplicate_channel = geo.createDuplicateChannel(curChannel)
    duplicate_channel.clearSelection()


    #  after the channel duplication, clearing out any set metdata on original channel
    for stack,layer in deep_layerlist:
        if layer.isShared() is True and layer.isChannelLayer() is False:
            if layer.hasMetadata('DuplicateLayerUUID'):
                layer.removeMetadata('DuplicateLayerUUID')
        elif layer.isChannelLayer():
            if layer.hasMetadata('DuplicateChannelUUID'):
                layer.removeMetadata('DuplicateChannelUUID')


    # Creating a deep layerlist of the duplicate channel
    duplicate_layerlist = duplicate_channel.layerList()
    deep_dup_layerlist = layerList().getLayerList(duplicate_layerlist,duplicate_channel, layerList().returnTrue)


    # for each layer in the level1 layerlist check its shared sybling and get the attributes saved
    for dup_stack,dup_layer in deep_dup_layerlist:

        duplicate_channel.clearSelection()
        dup_layer.makeCurrent()
        dup_layer.setSelected(True)

        # if the original layer was shared from another channel the sharing got destroyed by the channel duplication
        # so rebuilding the sharing. If the sharing still existed even after duplication it means it was a channel internal
        # sharing which remains intact even after copy/paste
        if dup_layer.hasMetadata('DuplicateLayerUUID'):

            # Checking amount of entries in the LayerUUID Metadata.
            # a) if layer is still shared and there is only one Metadata entry, we can disregard the layer
            # b) if the layer is still shared and there is more than one Metadata entry, we need to reshare it
            # c) if the layer is not shared but has Metadata entrie(s) we need to reshare it

            UUIMetaDData = dup_layer.metadata('DuplicateLayerUUID')
            UUIDStringSplit = UUIMetaDData.split()
            UUIDNumber = len(UUIDStringSplit)

            if dup_layer.isShared() and UUIDNumber == 1:
                dup_layer.removeMetadata('DuplicateLayerUUID')
                pass

            else:
                layer_uuid = UUIDStringSplit[0]
                restoreSharing("layer",dup_layer,mari.current.channel(),layer_uuid,shared_layer_dict)
                dup_layer.removeMetadata('DuplicateLayerUUID')

        # if it's a channel layer, the mari duplication caused a new channel to be created that will need to be removed
        # and the link to the original channel needs to be reset
        if dup_layer.isChannelLayer():
            if dup_layer.hasMetadata('DuplicateChannelUUID'):
                channel_uuid = dup_layer.metadata('DuplicateChannelUUID')
                restoreSharing("channel",dup_layer,mari.current.channel(),channel_uuid,shared_layer_dict)
                channelsToRemove.append(dup_layer.channel())


    # Removing any duplicate channels after channel layer rebuild completed
    # If the same channels got duplicated multiple times it can happen that there are duplicates in the list
    # and that once the first instance is removed, the rest cannot be found anymore.
    # So if it fails, assuming it is already removed and moving on
    for channel in channelsToRemove:
        try:
            geo.removeChannel(channel)
        except Exception:
            pass

    mari.history.stopMacro()
    mari.app.restoreCursor()

    deactivateViewportToggle.trigger()


# ------------------------------------------------------------------------------

def isProjectSuitable():
    "Checks project state and Mari version."
    MARI_3_0V1_VERSION_NUMBER = 30001202    # see below
    if mari.app.version().number() >= MARI_3_0V1_VERSION_NUMBER:

        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False

        geo = mari.geo.current()
        if geo is None:
            mari.utils.message("Please select an object to run.")
            return False

        chan = geo.currentChannel()
        if chan is None:
            mari.utils.message("Please select a channel to run.")
            return False

        return True

    else:
        mari.utils.message("You can only run this script in Mari 3.0v1 or newer.")
        return False


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    duplicateChannel()


