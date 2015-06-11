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


# ------------------------------------------------------------------------------

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
        if layer.isGroupLayer():
            matching.extend(getLayerList(layer.layerStack().layerList(), criterionFn))
        if layer.isChannelLayer():
            matching.extend(getLayerList(layer.channel().layerList(), criterionFn))

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

def patchBake():
    '''Bakes selected Patches to Image Manager'''

    if not mari.projects.current():
    	mari.utils.message('No project currently open', title = 'Error')
    	return


    # Checking for OS to determine slash handling
    if mari.app.version().isWindows():
        path = str(mari.resources.path("MARI_USER_PATH")).replace("\\", "/")
    else:
        path = str( mari.resources.path("MARI_USER_PATH") )


    # Determine general Selection Info
    curGeo = mari.geo.current()
    curChan = curGeo.currentChannel()
    # MARI 3 Only:
    # colorSpace = curChan.colorspaceConfig()
    curChanName = str(curChan.name())
    layers = curChan.layerList()
    patchList = list (curGeo.patchList() )
    selPatchList = [patch for patch in patchList if patch.isSelected() ]


    if len(selPatchList) == 0:
    	mari.utils.message('Select at least one patch', title = 'Error')
    	return

    # Deactivate Viewport for increases Spped
    deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
    deactivateViewportToggle.trigger()


    mari.history.startMacro('Patch Bake to Image Manager')
    mari.app.setWaitCursor()

    for layer in layers:
    	layer.setSelected(True)

    copyAction = mari.actions.find('/Mari/Layers/Copy')
    copyAction.trigger()

    pasteAction = mari.actions.find('/Mari/Layers/Paste')
    pasteAction.trigger()


    #running search for current selection in order to get a list of all duplicated layers
    geo_data = findLayerSelection()
    # Geo Data = 0 current geo, 1 current channel , 2 current layer, 3 current selection list
    curSel = geo_data[3]
    channelLayerLst = []
    #running search from all current selected layers to get a full list of all associated layers such as masks etc.
    nested_layers = getLayerList(curSel,returnTrue)
    # lookin through all layers that are associated with duplicates if there are any channel layers where we duplicated channels
    for layer in nested_layers:
        if layer.isChannelLayer():
            channelLayerLst.append(layer.channel())


    # merging the duplicated layers into one
    curChan.mergeLayers()

    # determine new current layer (result of merge),set name and grab its image set
    curLayer = curChan.currentLayer()
    curLayer.setName('BakeToImageManager')
    curImgSet = curLayer.imageSet()


    # extract current image set to image manager
    for patch in selPatchList:
        try:
            uv = patch.uvIndex()
            curPatchIndex = str(patch.udim())
            savePath = path + curChanName + '.' + curPatchIndex + '.tif'
            patchImg = curImgSet.image(uv, -1)
            patchImg.saveAs(savePath)
            # MARI 2.6:
            mari.images.load(savePath)
            # MARI 3:
            # mari.images.open(savePath,colorSpace)
            os.remove(savePath)

        except Exception:
            mari.history.stopMacro()
            mari.app.restoreCursor()
            pass


    # Running cleanup: Close newly created layer out, close any channel duplicates that may have been created as a result of copy+paste
    # of channel layers
    curLayer.close()
    for channel in channelLayerLst:
        try:
            curGeo.removeChannel(channel)
        except Exception:
            continue


    # Stop Macro, restore cursor, refresh viewport
    mari.history.stopMacro()
    mari.app.restoreCursor()
    deactivateViewportToggle.trigger()


def patch_bake_to_imageman():
    patchBake()



