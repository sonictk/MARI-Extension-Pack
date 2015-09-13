# ------------------------------------------------------------------------------
# Pinned Layers
# ------------------------------------------------------------------------------
# Allows the user to add a layer as a quick link for sharing to the ui
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
        if hasattr(layer, 'layerStack') is True and layer.isChannelLayer() is False:
            matching.extend(getLayerList(layer.layerStack().layerList(), criterionFn))
        if layer.hasMaskStack():
            matching.extend(getLayerList(layer.maskStack().layerList(), criterionFn))
        if hasattr(layer, 'hasAdjustmentStack') and layer.hasAdjustmentStack():
            matching.extend(getLayerList(layer.adjustmentStack().layerList(), criterionFn))
        if layer.isGroupLayer():
            matching.extend(getLayerList(layer.layerStack().layerList(), criterionFn))

    return matching
# ------------------------------------------------------------------------------

def findLayerUUID(UUID):
    """Looks for a layer based on its uuid"""

    curGeo = mari.geo.current()
    channels = curGeo.channelList()
    layerTarget = None

    for channel in channels:

        chn_layerList = channel.layerList()
        layers = getLayerList(chn_layerList,returnTrue)

        for layer in layers:
            if layer.uuid() == UUID:
                layerTarget = layer


    return layerTarget


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

def AddQuickPin():
    """Adds a Layer to the Quick Pins"""

    # Find selected layers
    selection = findLayerSelection()
    layerSelection = selection[3]

    # find project uuid
    projectUUID = str(mari.current.project().uuid())

    # UI Path for Quick Pins
    UI_path = 'MainWindow/&Layers/' + u'Add Pinned Layer'

    layerUUID = []
    layerName = []

    for layer in layerSelection:

        layerName.append( str(layer.name()) )
        layerUUID.append( str(layer.uuid()) )

    # Build the unique string for the layer identifier
    LayerIDString = '"' + str(layerName) +'"'+ ',' +'"' + projectUUID +'"'+ ',' +'"'+ str(layerUUID) +'"'

    # Replacing the existing action script with the new one for the current quick pin
    loadQuickPin = mari.actions.find('/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/Quick Pin')
    loadQuickPin.setScript('mari.customScripts.triggerQuickPin(' + LayerIDString + ')' )

# ------------------------------------------------------------------------------

def emptyQuickPin():
    """ Triggered when the Quick Pin loaded is unassigned """

    mari.utils.message('The Quick Pin link is empty.\n Use "Layer/Pin/Save Quick Pin" first','No Layer pinned yet')

# ------------------------------------------------------------------------------


def triggerQuickPin(layerName,project_uuid,layer_uuid):
    """Adds a shared layer from the Quick Pins and removes the Action associated with it later on"""

    if project_uuid != mari.current.project().uuid():
        mari.utils.message('This Layer does not belong to this project','Layer in different project')
        return

    # Find selected layers
    selection = findLayerSelection()
    curLayer = selection[1]
    curChannel = selection[2]

    # Dodgy reformatting of the layer_uuids in case multiple layers were selected
    # CBB but works for now.
    layer_uuid_list = layer_uuid.replace("['","")
    layer_uuid_list = layer_uuid_list.replace("]","")
    layer_uuid_list = layer_uuid_list.replace("'","")
    layer_uuid_list = layer_uuid_list.replace(" ","")
    layer_uuid_list = layer_uuid_list.split(",")
    # Reversing list
    # layer_uuid_list_rev = layer_uuid_list[::-1]

    for uuid in layer_uuid_list:

        layertoShare = findLayerUUID(uuid)

        if layertoShare is not None:
            curChannel.shareLayer(layertoShare,curLayer)
            # curLayer = mari.current.layer()

        else:
            mari.utils.message('Could not find layer associated to Quick Pin: '+ layerName,'A problem occurred')
            return



    # # Setting the Load Quick Pin to empty
    # loadQuickPin = mari.actions.find('/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/Quick Pin')
    # loadQuickPin.setScript('mari.customScripts.emptyQuickPin()')


