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
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore


# ------------------------------------------------------------------------------

class InfoUI(QtGui.QMessageBox):
    """Informs the user that a layername has changed"""
    def __init__(self, pinName,layerName, parent=None):
        super(InfoUI, self).__init__(parent)

        # Create info gui
        self.setWindowTitle('Source Layer Name different from Pin')
        self.setIcon(QtGui.QMessageBox.Question)
        self.setText('The layer name associated to this Pin has changed.\n\nPin Name: '+ pinName +'\nLayer Name: ' + layerName + '\n\nDo you wish to update the Pin Name ?')
        self.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        self.setDefaultButton(QtGui.QMessageBox.Yes)


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
    # Try ast.literal_eval(STRING) instead
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
    return actionList


# ------------------------------------------------------------------------------

def duplicatePinName(duplicate_name):
    """ Warns the user that a Pin with the Name already exists """

    mari.utils.message('A collection pin with the selected Layer Name already exists\n\nPIN NAME EXISTS: '+duplicate_name +'\n\nRemove the Pin or rename the new Layer to be pinned.','Duplicate Pin Name')


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

        placeholderExists = False
        duplicateNotFound = True

        # list of all collection pins
        collectionPins = checkCollectionPins()

        layerPrettyName = layer.name()
        layerName = str( layerPrettyName )
        layerUUID = str(layer.uuid() )

        # Checking for duplicate Pin Names first
        for pin in collectionPins:

            if pin.name() == layerPrettyName:
                duplicatePinName(layerPrettyName)
                duplicateNotFound = False

            if pin.name() == 'No Collection Pins':
                placeholderExists = True
                placeholder = pin

        #  if no duplicate found, proceed
        if duplicateNotFound:

            # Build the unique string for the layer identifier
            LayerIDString = '"' + layerName +'"'+ ',' +'"' + projectUUID +'"'+ ',' +'"'+ layerUUID +'"'

            # first collection pin in the list
            previousAction = collectionPins[1]

            # creating an action associated with the layer
            UI_path = 'MainWindow/&Layers/' + u'Add Pinned Layer'
            collectionLayerAction = mari.actions.create('/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/' + layerName,'mari.customScripts.triggerCollectionPin(' + LayerIDString + ')' )
            mari.menus.addAction(collectionLayerAction,UI_path,previousAction.name())

            # if the placeholder action exists, remove it
            if placeholderExists:
                mari.menus.removeAction(placeholder,UI_path)

# ------------------------------------------------------------------------------

def updateCollectionPin(layer_uuid,oldname,newname,project_uuid):
    """ Updates the Name of a collection pin if the source layer has changed in name"""


    # list of all collection pins
    collectionPins = checkCollectionPins()
    duplicateNotFound = True

    # Checking for duplicate Pin Names first
    for pin in collectionPins:

        if pin.name() == newname:
            duplicatePinName(newname)
            duplicateNotFound = False

    # if no duplicate found, proceed
    if duplicateNotFound:

        UI_path = 'MainWindow/&Layers/' + u'Add Pinned Layer'

        # find the old action with the wrong name
        oldaction = mari.actions.find('/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/'+ oldname)

        # Build the unique string for the layer identifier
        LayerIDString = '"' + newname +'"'+ ',' +'"' + project_uuid +'"'+ ',' +'"'+ layer_uuid +'"'

        # Create a new action with the correct name
        newaction = mari.actions.create('/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/' + newname,'mari.customScripts.triggerCollectionPin(' + LayerIDString + ')' )

        # insert new action into menu above old action
        mari.menus.addAction(newaction,UI_path,oldname)

        # remove old action from menu
        mari.menus.removeAction(oldaction,UI_path)


# ------------------------------------------------------------------------------

def triggerCollectionPin(layerName,project_uuid,layer_uuid):
    """ Executes the sharing operation on a collection pin"""

    current_project_uuid = mari.current.project().uuid()

    if project_uuid != current_project_uuid:
            mari.utils.message('The Layer associated to this pin is in another project','Layer Pin refers to different project')
            return

    # Find selected layers
    selection = findLayerSelection()
    curLayer = selection[1]
    curChannel = selection[2]

    layertoShare = findLayerUUID(layer_uuid)


    if layertoShare is not None:

        # if the layername given to the pin is different then the name corresponding to the uuid it means the user has renamed the layer
        # in the meantime. Ask to update the Pin Name

        layerShareName = layertoShare.name()

        if layerShareName != layerName:
            info_dialog = InfoUI(layerName,layerShareName)
            info_dialog.exec_()
            info_reply = info_dialog.buttonRole(info_dialog.clickedButton())
            # If User chooses to Ignore problematic paths, we will remove the prolematic ones from the dictionary
            if info_reply is QtGui.QMessageBox.ButtonRole.YesRole:
                updateCollectionPin(layer_uuid,layerName,layerShareName,current_project_uuid)
            else:
                pass

        #  share the layer from the pin
        curChannel.shareLayer(layertoShare,curLayer)

    else:
        mari.utils.message('Could not find layer associated to Collection Pin: '+ layerName,'Process did not complete')
        return