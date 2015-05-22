# ------------------------------------------------------------------------------
# Batch Convert to Paintable
# ------------------------------------------------------------------------------
# Convert selected layers to paintable layers.
# Other than the default MARI Convert to paintable, this works on all selected layers.
# Default MARI Convert to Paintable is replaced with this version.
# ------------------------------------------------------------------------------
# coding: utf-8
# ------------------------------------------------------------------------------
# Written by Jorel Latraille, 2014
# ------------------------------------------------------------------------------
# http://mari.ideascale.com
# http://www.jorel-latraille.com/
# http://www.thefoundry.co.uk
# ------------------------------------------------------------------------------
# DISCLAIMER & TERMS OF USE:
#
# Copyright (c) The Foundry 2014.
# All rights reserved.
#
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


def returnTrue(layer):
    """Returns True for any object passed to it."""
    return True

# ------------------------------------------------------------------------------
def getLayerList(layer_list, criterionFn):
    """Returns a list of all of the layers in the stack that match the given criterion function, including substacks."""
    matching = []
    for layer in layer_list:
        if criterionFn(layer):
            matching.append(layer)
        if hasattr(layer, 'layerStack'):
            matching.extend(getLayerList(layer.layerStack().layerList(), criterionFn))
        if layer.hasMaskStack():
            matching.extend(getLayerList(layer.maskStack().layerList(), criterionFn))
        if hasattr(layer, 'hasAdjustmentStack') and layer.hasAdjustmentStack():
            matching.extend(getLayerList(layer.adjustmentStack().layerList(), criterionFn))

    return matching

# ------------------------------------------------------------------------------
# currently not used:
def getGroupLayerList(layer_list, criterionFn):
    """Returns a list of all of the layers in the stack including top level group contents"""
    matching = []
    for layer in layer_list:
        if criterionFn(layer):
            matching.append(layer)
        if layer.isGroupLayer():
            matching.extend(getLayerList(layer.layerStack().layerList(), criterionFn))

    return matching
# ------------------------------------------------------------------------------

def findLayerSelection():
    """Searches for the current selection if mari.current.layer is not the same as layer.isSelected"""

    curGeo = mari.geo.current()
    curChannel = curGeo.currentChannel()
    channels = curGeo.channelList()
    curLayer = mari.current.layer()

    layers = ()
    layerSelList = []
    chn_layerList = ()

    layerSelect = False

    if curLayer.isSelected():
    # If current layer is indeed selected one just trawl through current channel to find others
        layerSelect = True
        chn_layerList = curChannel.layerList()
        layers = getLayerList(chn_layerList,returnTrue)

        for layer in layers:
            if layer.isSelected():
                layerSelList.append(layer)

    else:
    # If current layer is not selected it means that a selection sits somewhere else (non-current channel)
    # so we are going trawling through the entire channel list including substacks to find it

        for channel in channels:

            chn_layerList = channel.layerList()
            layers = getLayerList(chn_layerList,returnTrue)

            for layer in layers:

                if layer.isSelected():
                    curLayer = layer
                    curChannel = channel
                    layerSelect = True
                    layerSelList.append(layer)


    if not layerSelect:
        mari.utils.message('No Layer Selection found. \n \n Please select at least one Layer.')


    return curGeo,curLayer,curChannel,layerSelList


# ------------------------------------------------------------------------------
def convertToPaintable():
    "Convert selected layers to paintable layers."
    if not isProjectSuitable(): #Check if project is suitable
        return False

    # Turning off viewport for better perfromance
    deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
    deactivateViewportToggle.trigger()

    # FInding selection. 2 is channel 3 is layer selection list
    geo_data = findLayerSelection()
    selected_layer = geo_data[3]
    selected_channel = geo_data[2]



    for layer in selected_layer:

        layername = layer.name()
        mari.history.startMacro('Convert to Paintable -  Layer:'+ '"'+ layername + '"')

        layer.makeCurrent()



        if layer.isChannelLayer():

            _hasMaskStack = False
            _hasMask = False

            layer_maskStack = ()
            layer_mask = ()
            channelLayer_name = layer
            selected_channel.clearSelection(1)
            selected_channel.clearSelection(2)
            selected_channel.clearSelection(4)
            channelLayer_name.setSelected(True)

            # Deselecting everything since I need to merge channel layer
            # With full selection I would merge channellayers AND other layers
            # into one


            if layer.hasMask() and not layer.hasMaskStack():
                # Creating a templayer and assigning the mask from the channellayer
                # to keep it through the merge process. In the end reassigning the maskStack
                # and closing layer
                _hasMaskStack = False
                _hasMask = True
                layer_mask = layer.maskImageSet()
                masksave = selected_channel.createPaintableLayer("channelLayer_maskstack", layer, flags=1)
                masksave.setMaskImageSet(layer_mask)

            if layer.hasMaskStack():
                # Creating a templayer and assigning the maskstqck from the channellayer
                # to keep it through the merge process. In the end reassigning the maskStack
                # and closing layer
                _hasMaskStack = True
                _hasMask = False
                layer_maskStack = layer.maskStack()
                masksave = selected_channel.createPaintableLayer("channelLayer_maskstack", layer, flags=1)
                masksave.setMaskStack(layer_maskStack)



            # Saving any layer options on the channel layer to set it to the merged layer afterwards
            advBlend = layer.getAdvancedBlendComponent()
            layerBelow = layer.getLayerBelowBlendLut()
            thisLayer = layer.getThisLayerBlendLut()
            blendAmount = layer.blendAmount()
            blendAmountEnabled = layer.blendAmountEnabled()
            blendMode = layer.blendMode()
            blendType = layer.blendType()
            visibility =layer.isVisible()
            colorTag = layer.colorTag()
            swizzle_r = layer.swizzle(0)
            swizzle_g = layer.swizzle(1)
            swizzle_b = layer.swizzle(2)
            swizzle_a = layer.swizzle(3)


            # 'Convert to paintable' Channel Layer Style
            mergeLayer = mari.actions.get('/Mari/Layers/Merge Layers')
            mergeLayer.trigger()


            # resetting attributes from channel layer onto new layer
            new_layer = findLayerSelection()[3][0]
            new_layer.setAdvancedBlendComponent(advBlend)
            new_layer.setLayerBelowBlendLut(layerBelow)
            new_layer.setThisLayerBlendLut(thisLayer)
            new_layer.setBlendAmount(blendAmount)
            new_layer.setBlendAmountEnabled(blendAmountEnabled)
            new_layer.setBlendMode(blendMode)
            new_layer.setBlendType(blendType)
            new_layer.setVisibility(visibility)
            new_layer.setColorTag(colorTag)
            new_layer.setSwizzle(0,swizzle_r)
            new_layer.setSwizzle(1,swizzle_g)
            new_layer.setSwizzle(2,swizzle_b)
            new_layer.setSwizzle(3,swizzle_a)
            new_layer.setName(layername)

            # if channel layer has mask stack reassign it from out templayer and close out templayer
            if _hasMaskStack:
                new_layer.setMaskStack(layer_maskStack)
                masksave.close()
            if _hasMask:
                new_layer.setMaskImageSet(layer_mask)
                masksave.close()


            for layer in selected_layer:
                if layer is not channelLayer_name:
                    layer.setSelected(True)


        # if it is not a channel layer we can just use regular convert to paintable
        else:
            layer.makeCurrent()
            convertToPaintable = mari.actions.get('/Mari/Layers/Convert To Paintable')
            convertToPaintable.trigger()


        mari.history.stopMacro()

    deactivateViewportToggle.trigger()


# ------------------------------------------------------------------------------
def isProjectSuitable():
    "Checks project state and Mari version."
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:

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

        if len(chan.layerList()) == 0:
            mari.utils.message("Please select a layer to run.")
            return False

        return True

    else:
        mari.utils.message("You can only run this script in Mari 2.6v3 or newer.")
        return False

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    convertToPaintable()