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
import os
import ast
import json

USER_ROLE = 32      # PySide.Qt.UserRole
JSON_FILE = 'CollectionPins_ExtPack_3v0.json'
version = "3.0"     #UI VERSION


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

class EditPin_UI(QtGui.QDialog):
    '''GUI to edit existing Pins '''
    def __init__(self):
        super(EditPin_UI, self).__init__()
        self.setFixedSize(340, 400)
        #Set window title and create a main layout
        title = "Edit Pins"
        self.setWindowTitle(title)
        main_layout = QtGui.QVBoxLayout()

        #Create layout for middle section
        centre_layout = QtGui.QHBoxLayout()

        #Create channel layout, label, and widget. Finally populate.
        action_layout = QtGui.QVBoxLayout()
        action_header_layout = QtGui.QHBoxLayout()
        action_label = QtGui.QLabel("<strong>Collection Pins</strong>")
        action_list = QtGui.QListWidget()
        action_list.setSelectionMode(action_list.ExtendedSelection)

        #Create filter box for channel list
        action_filter_box = QtGui.QLineEdit()
        # mari.utils.connect(action_filter_box.textEdited, None)
        mari.utils.connect(action_filter_box.textEdited, lambda: self.updateActionFilter(action_filter_box, action_list))


        #Create layout and icon/label for channel filter
        action_header_layout.addWidget(action_label)
        action_header_layout.addStretch()
        action_search_icon = QtGui.QLabel()
        search_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + os.sep + 'Lookup.png')
        action_search_icon.setPixmap(search_pixmap)
        action_header_layout.addWidget(action_search_icon)
        action_header_layout.addWidget(action_filter_box)

        #Populate Channel List, channellist gets full channel list from project and amount of channels on current object (which sit at the top of the list)
        action_list= self.populateActionList(action_list)

        #Add filter layout and channel list to channel layout
        action_layout.addLayout(action_header_layout)
        action_layout.addWidget(action_list)

        #Add widgets to centre layout
        centre_layout.addLayout(action_layout)

        #Create button layout and hook them up
        button_layout = QtGui.QHBoxLayout()
        removeButton = QtGui.QPushButton("Remove Pin")
        cancel_button = QtGui.QPushButton("&Cancel")
        button_layout.addStretch()
        button_layout.addWidget(removeButton)
        button_layout.addWidget(cancel_button)


        # Hook up OK/Cancel button clicked signal to accept/reject slot
        removeButton.clicked.connect(lambda: self.runRemove(action_list))
        cancel_button.clicked.connect(self.reject)

        #Add layouts to main layout and dialog
        main_layout.addLayout(centre_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    # ------------------------------------------------------------------------------

    def populateActionList(self,action_list):
        """Add collection pins to pin list"""

        actions = checkCollectionPins()
        for action in actions:
            if action.name() == 'Quick Pin':
                pass
            else:
                action_list.addItem(action.name())
                action_list.item(action_list.count() - 1).setData(USER_ROLE, action)

        return action_list
    # ------------------------------------------------------------------------------

    def updateActionFilter(self,action_filter_box, action_list):
        "For each item in the list display, set it to hidden if it doesn't match the filter text."

        match_words = action_filter_box.text().lower().split()

        for item_index in range(action_list.count()):
            item = action_list.item(item_index)
            item_text_lower = item.text().lower()
            matches = all([word in item_text_lower for word in match_words])
            item.setHidden(not matches)

    # ------------------------------------------------------------------------------

    def selectedAction(self,action_list):
        "get action selection"

        multiSelection = []
        for item in action_list.selectedItems():
            multiSelection.append(item.data(USER_ROLE))

        return multiSelection

    # ------------------------------------------------------------------------------

    def runRemove(self,action_list):
        "execute removal of pins"
        selected_action = self.selectedAction(action_list)
        self.removePins(selected_action)
        self.close()

    # ------------------------------------------------------------------------------

    def removePins(self,actions):
        "removes a bunch of actions from the menu"

        UI_path = 'MainWindow/&Layers/' + u'Add Pinned Layer'
        for action in actions:
            layerName = action.name()
            mari.menus.removeAction(action,UI_path)
            actionXML('removeAction',layerName,None,None,None,None)

        self.addPlaceholderPin()


    # ------------------------------------------------------------------------------

    def addPlaceholderPin(self):
        "adds a placeholder collection pin in case no other collection pin exists"

        collectionPins = checkCollectionPins()
        if len(collectionPins) == 1:
            placeholder = mari.actions.find('/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/No Collection Pins')
            UI_path = 'MainWindow/&Layers/' + u'Add Pinned Layer'
            mari.menus.addAction(placeholder,UI_path)

# ------------------------------------------------------------------------------

class actionXML(object):
    """ Read,writes and removes actions to and from the projects collection pin xml"""

    def __init__(self,mode,name,uuid,layertype,actionpath,actionscript):
        self.xmlFile = self.getProjectPath()
        if mode == 'addAction':
            self.saveActionToFile(name,uuid,layertype,actionpath,actionscript)
        if mode == 'removeAction':
            self.removeActionFromFile(name)
        if mode == 'restoreAction':
            self.restoreProjectActions()
    # ------------------------------------------------------------------------------

    def saveActionToFile(self,name,uuid,layertype,actionpath,actionscript):
        "stores a new action to be launched on project open"

        data = {}

        if os.path.exists(self.xmlFile):
            with open(self.xmlFile, "r") as jsonFile:
                try:
                    data = json.load(jsonFile)
                except Exception:
                    pass

        data[name] = uuid,layertype,actionscript

        with open(self.xmlFile, "w+") as jsonFile:
            jsonFile.write(json.dumps(data))

    # ------------------------------------------------------------------------------

    def removeActionFromFile(self,name):
        "stores a new action to be launched on project open"

        data = {}

        if os.path.exists(self.xmlFile):
            with open(self.xmlFile, "r") as jsonFile:
                try:
                    data = json.load(jsonFile)
                    data.pop(name,0)
                except Exception:
                    pass

        with open(self.xmlFile, "w+") as jsonFile:
            jsonFile.write(json.dumps(data))


    # ------------------------------------------------------------------------------

    def restoreProjectActions(self):
        "restores any previous pins on project load, removing other ones from previous open project"

        data = {}
        UI_path = 'MainWindow/&Layers/' + u'Add Pinned Layer'

        # Clearing any qiick pins from previous projects
        loadQuickPin = mari.actions.find('/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/Quick Pin')
        loadQuickPin.setScript('mari.customScripts.emptyPin()')


        if os.path.exists(self.xmlFile):
            with open(self.xmlFile, "r") as jsonFile:
                try:
                    data = json.load(jsonFile)
                except Exception:
                    pass

            for action in data:
                action_string = data[action][2]
                uuid = data[action][0]
                layerType = data[action][1]

                # recreating layer actions, setting icon and adding to AddPinnedLayer Menu
                layer = findLayerUUID(layerType,uuid)
                if layer != None:
                    collectionLayerAction = mari.actions.create('/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/' + action,action_string)
                    icon_path = setCollectionPinIcon(layerType,layer)
                    collectionLayerAction.setIcon(icon_path)
                    mari.menus.addAction(collectionLayerAction,UI_path)

            # Checking if placeholder is still around and removing if collection pins exist
            collectionPins = checkCollectionPins()
            if len(collectionPins) > 2:
                for pin in collectionPins:
                    if pin.name() == 'No Collection Pins':
                        mari.menus.removeAction(pin,UI_path)


    # ------------------------------------------------------------------------------

    def getProjectPath(self):
        "resolves the path to the xml file used to store actions for a project"

        global JSON_FILE

        # Going the complicated way instead to retrieve the path instead of using cachePath() in case there are multiple cache directories:
        project = mari.current.project()
        project_info = project.info()
        project_file = project_info.projectPath()
        project_path = os.path.split(project_file)[0]
        json_path = os.path.join(project_path,JSON_FILE)

        return json_path

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

def findLayerUUID(layertype,UUID):
    """Looks for a layer based on its uuid"""

    curGeo = mari.geo.current()
    channels = curGeo.channelList()
    layerTarget = None

    for channel in channels:

        if layertype ==  '1': #channel mode
            if channel.uuid() == UUID:
                layerTarget = channel
        else:
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

def addQuickPin(mode):
    """Adds a Layer selection to the Quick Pin"""

    # find project uuid
    projectUUID = str(mari.current.project().uuid())

    layerTypeLst = []
    layerUUIDLst = []
    layerNameLst= []

    # Find selected layers
    if mode == 'channel':
        layerSelection = [mari.current.channel()]
        layerType = '1'
    else:
        selection = findLayerSelection()
        layerSelection = selection[3]
        layerType = '0'

    for layer in layerSelection:

        layerPrettyName = layer.name()
        layerName = str( layerPrettyName )
        layerUUID = str(layer.uuid() )

        if hasattr(layer, 'isChannelLayer'):
            if layer.isChannelLayer():
                layerType = '1' #Type Channel
                layerPrettyName = layer.channel().name()
                layerName = str( layer.channel().name() )
                layerUUID = str( layer.channel().uuid() )

        layerTypeLst.append(str(layerType))
        layerNameLst.append( layerName )
        layerUUIDLst.append( layerUUID )

    # Build the unique string for the layer identifier
    LayerIDString = '"' + str(layerTypeLst) + '"'+ ',' +'"' + str(layerNameLst) + '"'+ ',' +'"' + str(projectUUID) +'"'+ ',' +'"'+ str(layerUUIDLst) +'"'

    # Replacing the existing action script with the new one for the current quick pin
    loadQuickPin = mari.actions.find('/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/Quick Pin')
    loadQuickPin.setScript('mari.customScripts.triggerQuickPin(' + LayerIDString + ')' )

# ------------------------------------------------------------------------------

def triggerQuickPin(layerType,layerName,project_uuid,layer_uuid):
    """Adds shared layers from the Quick Pin"""

    if project_uuid != mari.current.project().uuid():
        mari.utils.message('You do not have a layer pinned yet','No pinned Layers found')
        return

    # Find selected layers
    selection = findLayerSelection()
    curLayer = selection[1]
    curChannel = selection[2]
    listCount = 0


    # Reformatting of the layer_uuids in case multiple layers were selected
    layer_type_list = ast.literal_eval(layerType)
    layer_uuid_list = ast.literal_eval(layer_uuid)
    layer_name_list = ast.literal_eval(layerName)

    for uuid in layer_uuid_list:

        layerType_item = layer_type_list[listCount]
        layertoShare = findLayerUUID(layerType_item,uuid)

        if layertoShare is not None:

            layerShareName = layertoShare.name()
            listCount += 1

            #  share the layer from the pin or create channel layer from original chanel
            if layerType_item == '0':
                curChannel.shareLayer(layertoShare,curLayer)
            else:
                if layertoShare == curChannel:
                    mari.utils.message('The pinned channel is the active channel.\nYou cannot add a channel to itself','Channel is active channel')
                else:
                    curChannel.createChannelLayer(layerShareName,layertoShare,curLayer)


        else:
            mari.utils.message('Could not find layer associated to Quick Pin: \n\nMissing or deleted Layer for Pin:  '+ layer_name_list[listCount] +'\n\nThe Add Pinned Layer operation did not fully complete','Process did not complete')
            return

# ------------------------------------------------------------------------------

def checkCollectionPins():
    """ Returns the first action under the separator"""

    actionList = mari.menus.actions('MainWindow','&Layers','Add Pinned Layer')
    return actionList

# ------------------------------------------------------------------------------

def clearPins():
    """ Clears the list of collection pins and adds a placeholder"""

    collectionPins = checkCollectionPins()
    UI_path = 'MainWindow/&Layers/' + u'Add Pinned Layer'
    for pin in collectionPins:
        if pin.name() == 'Quick Pin':
            pass
        else:
            mari.menus.removeAction(pin,UI_path)

    placeholder = mari.actions.find('/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/No Collection Pins')
    mari.menus.addAction(placeholder,UI_path)


# ------------------------------------------------------------------------------

def setCollectionPinIcon(LayerType,Layer):
    """ Determines what Icon Type to set on the Collection Pin"""

    mariResourcePath = mari.resources.path(mari.resources.ICONS)
    iconPath = ''

    if LayerType == '1': #Channel
        icon_filename = 'Channel.16x16.png'
        iconPath = os.path.join(mariResourcePath,icon_filename)
    else:
        if Layer.isPaintableLayer():
            icon_filename = 'Painting.16x16.png'
            iconPath = os.path.join(mariResourcePath,icon_filename)
        elif Layer.isProceduralLayer():
            icon_filename = 'AddNoise.16x16.png'
            iconPath = os.path.join(mariResourcePath,icon_filename)
        elif Layer.isChannelLayer():
            icon_filename = 'Channel.16x16.png'
            iconPath = os.path.join(mariResourcePath,icon_filename)
        elif Layer.isGroupLayer():
            icon_filename = 'Folder.16x16.png'
            iconPath = os.path.join(mariResourcePath,icon_filename)
        elif Layer.isGraphLayer():
            icon_filename = 'NodeGraph.16x16.png'
            iconPath = os.path.join(mariResourcePath,icon_filename)
        elif Layer.isAdjustmentLayer():
            icon_filename = 'ColorCurves.16x16.png'
            iconPath = os.path.join(mariResourcePath,icon_filename)

    return iconPath

# ------------------------------------------------------------------------------

def duplicatePinName(duplicate_name):
    """ Warns the user that a Pin with the Name already exists """

    mari.utils.message('A collection pin with the selected Layer Name already exists\n\nPIN NAME EXISTS: '+duplicate_name +'\n\nRemove the Pin or rename the new Layer to be pinned.','Duplicate Pin Name')

# ------------------------------------------------------------------------------

def addCollectionPin(mode):
    """Adds a Layer selection to the Collection Pins
        Collection Pins are sticky pins that do stay around till the user removes them """

    # find project uuid
    projectUUID = str(mari.current.project().uuid())
    previousActionExists = True

    # Find selected layers
    if mode == 'channel':
        layerSelection = [mari.current.channel()]
        layerType = '1'
    else:
        findSelection = findLayerSelection()
        layerSelection = findSelection[3]
        layerType = '0'

    for layer in layerSelection:

        placeholderExists = False
        duplicateNotFound = True

        # list of all collection pins
        collectionPins = checkCollectionPins()

        layerPrettyName = layer.name()
        layerName = str( layerPrettyName )
        layerUUID = str(layer.uuid() )

        if mode != 'channel':
            if layer.isChannelLayer() is True:
                layerType = '1' #Type Channel
                layerPrettyName = layer.channel().name()
                layerName = str( layer.channel().name() )
                layerUUID = str( layer.channel().uuid() )
            else:
                layerType = '0'

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
            LayerIDString = '"' + str(layerType) + '"'+ ',' +'"' + str(layerName) + '"'+ ',' +'"' + str(projectUUID) +'"'+ ',' +'"'+ str(layerUUID) +'"'
            # first collection pin in the list. There are fringe cases where it is possible
            # that no collection pin exists AND no 'no collection pin' item was added.
            # So if the list index goes out of range I am catching it.
            try:
                previousAction = collectionPins[1]
            except Exception:
                previousActionExists = False

            # creating an action associated with the layer
            UI_path = 'MainWindow/&Layers/' + u'Add Pinned Layer'
            action_path = '/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/' + layerName
            action_script = 'mari.customScripts.triggerCollectionPin(' + LayerIDString + ')'
            collectionLayerAction = mari.actions.create(action_path,action_script)
            actionXML('addAction',layerName,layerUUID,layerType,action_path,action_script)

            if previousActionExists:
                mari.menus.addAction(collectionLayerAction,UI_path,previousAction.name())
            else:
                mari.menus.addAction(collectionLayerAction,UI_path)

            icon_path = setCollectionPinIcon(layerType,layer)
            collectionLayerAction.setIconPath(icon_path)

            # if the placeholder action exists, remove it
            if placeholderExists:
                mari.menus.removeAction(placeholder,UI_path)

# ------------------------------------------------------------------------------

def updateCollectionPin(layerType,layer_uuid,oldname,layerobj,newname,project_uuid):
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
        LayerIDString = '"' + str(layerType) +'"'+ ',' +'"' + str(newname) +'"'+ ',' +'"' + str(project_uuid) +'"'+ ',' +'"'+ str(layer_uuid) +'"'

        # Create a new action with the correct name, also add to json file
        new_action_path = '/Mari/MARI Extension Pack/Layers/Pin Layers/Pins/' + newname
        new_action_script = 'mari.customScripts.triggerCollectionPin(' + LayerIDString + ')'
        newaction = mari.actions.create(new_action_path,new_action_script )
        actionXML('addAction',newname,layer_uuid,layerType,new_action_path,new_action_script)

        icon_path = setCollectionPinIcon(layerType,layerobj)
        newaction.setIconPath(icon_path)

        # insert new action into menu above old action
        mari.menus.addAction(newaction,UI_path,oldname)

        # remove old action from menu and json
        mari.menus.removeAction(oldaction,UI_path)
        actionXML('removeAction',oldname,None,None,None,None)

# ------------------------------------------------------------------------------

def triggerCollectionPin(layertype,layerName,project_uuid,layer_uuid):
    """ Executes the sharing operation on a collection pin"""

    current_project_uuid = mari.current.project().uuid()

    if project_uuid != current_project_uuid:
            mari.utils.message('The Layer associated to this pin is in another project','Layer Pin refers to different project')
            return

    # Find selected layers
    selection = findLayerSelection()
    curLayer = selection[1]
    curChannel = selection[2]

    layertoShare = findLayerUUID(layertype,layer_uuid)


    if layertoShare is not None:

        layerShareName = layertoShare.name()


        # if the layername given to the pin is different then the name corresponding to the uuid it means the user has renamed the layer
        # in the meantime. Ask to update the Pin Name

        if layerShareName != layerName:
            info_dialog = InfoUI(layerName,layerShareName)
            info_dialog.exec_()
            info_reply = info_dialog.buttonRole(info_dialog.clickedButton())
            # If User chooses to Ignore problematic paths, we will remove the prolematic ones from the dictionary
            if info_reply is QtGui.QMessageBox.ButtonRole.YesRole:
                updateCollectionPin(layertype,layer_uuid,layerName,layertoShare,layerShareName,current_project_uuid)
            else:
                pass

        #  share the layer from the pin or create channel layer from original chanel
        if layertype == '0':
            curChannel.shareLayer(layertoShare,curLayer)
        else:
            if layertoShare == curChannel:
                mari.utils.message('The pinned channel is the active channel.\nYou cannot add a channel to itself','Channel is active channel')
            else:
                curChannel.createChannelLayer(layerShareName,layertoShare,curLayer)

    else:
        # if layer does not exist anymore, throw warning then remove obsolete action from menu and json file
        mari.utils.message('Could not find layer associated to Collection Pin: \n\nMissing or deleted Layer for Pin:  '+ layerName +'\n\nThe broken Collection Pin was removed from the menu','Process did not complete')
        mari.menus.removeAction('MainWindow/&Layers/Add Pinned Layer/'+layerName )
        actionXML('removeAction',layerName,None,None,None,None)
        return

# ------------------------------------------------------------------------------

