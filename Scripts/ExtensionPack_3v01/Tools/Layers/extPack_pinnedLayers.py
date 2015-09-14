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

def emptyQuickPin():
    """ Executed if no layer has been pinned but user triggers quick pin"""

    mari.utils.message('You do not have a Layer added as a Quick Pin','No Layer pinned yet')
    return

# ------------------------------------------------------------------------------

def addQuickPin():
    """Adds a Layer selection to the Quick Pin"""

    # Find selected layers
    selection = findLayerSelection()
    layerSelection = selection[3]

    # find project uuid
    projectUUID = str(mari.current.project().uuid())

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


def triggerQuickPin(layerName,project_uuid,layer_uuid):
    """Adds shared layers from the Quick Pin"""

    if project_uuid != mari.current.project().uuid():
        mari.utils.message('You do not have a layer pinned yet','No pinned Layers found')
        return

    # Find selected layers
    selection = findLayerSelection()
    curLayer = selection[1]
    curChannel = selection[2]
    layerCount = 0

    # Reformatting of the layer_uuids in case multiple layers were selected
    # CBB but works for now.
    layer_uuid_list = layer_uuid.replace("['","")
    layer_uuid_list = layer_uuid_list.replace("]","")
    layer_uuid_list = layer_uuid_list.replace("'","")
    layer_uuid_list = layer_uuid_list.replace(" ","")
    layer_uuid_list = layer_uuid_list.split(",")

    layer_name_list = layerName.replace("['","")
    layer_name_list = layer_name_list.replace("]","")
    layer_name_list = layer_name_list.replace("'","")
    layer_name_list = layer_name_list.replace(" ","")
    layer_name_list = layer_name_list.split(",")


    for uuid in layer_uuid_list:

        layertoShare = findLayerUUID(uuid)

        if layertoShare is not None:
            curChannel.shareLayer(layertoShare,curLayer)
            layerCount += 1

        else:
            mari.utils.message('Could not find layer associated to Quick Pin: '+ layer_name_list[layerCount],'Process did not complete')
            return

# ------------------------------------------------------------------------------

def checkCollectionPins():
    """ Returns the first action under the separator"""

    actionList = mari.menus.actions('MainWindow','&Layers','Add Pinned Layer')
    return actionList[1]

# ------------------------------------------------------------------------------


def addCollectionPin():
    """Adds a Layer selection to the Collection Pins
        Collection Pins are sticky pins that do stay around till the user removes them """


    # Find selected layers
    selection = findLayerSelection()
    layerSelection = selection[3]

    # find project uuid
    projectUUID = str(mari.current.project().uuid())


    for layer in layerSelection:

        layerName = str( layer.name() )
        layerUUID = str(layer.uuid() )

        # Build the unique string for the layer identifier
        LayerIDString = '"' + layerName +'"'+ ',' +'"' + projectUUID +'"'+ ',' +'"'+ layerUUID +'"'

        # checking the menu items in the AddPinnedLayer Submenu in order to correctly insert the layer in the top position
        # and remove the NoCollectionPin Item if necessary
        previousAction = checkCollectionPins()

        # creating an action associated with the layer
        UI_path = 'MainWindow/&Layers/' + u'Add Pinned Layer'
        collectionLayerAction = mari.actions.create('/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/' + layerName,'mari.customScripts.triggerCollectionPin(' + LayerIDString + ')' )
        mari.menus.addAction(collectionLayerAction,UI_path,previousAction.name())

        if previousAction.name() == 'No Collection Pins':
            mari.menus.removeAction(previousAction,UI_path)

# ------------------------------------------------------------------------------


def triggerCollectionPin(layerName,project_uuid,layer_uuid):
    """ Executes the sharing operation on a collection pin"""

    if project_uuid != mari.current.project().uuid():
            mari.utils.message('The Layer associated to this pin is in another project','Layer Pin refers to different project')
            return

    # Find selected layers
    selection = findLayerSelection()
    curLayer = selection[1]
    curChannel = selection[2]

    layertoShare = findLayerUUID(layer_uuid)

    if layertoShare is not None:
        curChannel.shareLayer(layertoShare,curLayer)

    else:
        mari.utils.message('Could not find layer associated to Collection Pin: '+ layerName,'Process did not complete')
        return