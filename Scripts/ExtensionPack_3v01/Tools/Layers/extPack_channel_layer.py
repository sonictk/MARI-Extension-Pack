# ------------------------------------------------------------------------------
# Channel Layer Tools
# ------------------------------------------------------------------------------
# Channel Layer Tools simplify the process of using the result of a Channel
# in another Channel. 3 Options exist: Add Channel Layer, Add Channel Layer as Mask, Add grouped Channel Layer Mask
# ------------------------------------------------------------------------------
# Originally written by Ben Neal, 2014
# http://bneall.blogspot.de/
# ------------------------------------------------------------------------------
# Rewritten & extended by Jens Kafitz, 2014/15
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
import os

USER_ROLE = 32          # PySide.Qt.UserRole

version = "3.0"     #UI VERSION

# ------------------------------------------------------------------------------


def _isProjectSuitable():
    """Checks project state and mari version"""
    MARI_3_0V1b2_VERSION_NUMBER = 30001202    # see below
    if mari.app.version().number() >= MARI_3_0V1b2_VERSION_NUMBER:

        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False, False

        return True, False

    else:
        mari.utils.message("You can only run this script in Mari 3.0v1 or newer.")
        return False, False


# ------------------------------------------------------------------------------


def makeChannelLayer(sourceChannel, mode, invert):
    """Creates Channel Layer, channel Layer Mask or channel Layer mask grouped"""

    deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
    deactivateViewportToggle.trigger()

    selectionData = getSelectedLayer().findSelection()
    currentStack = selectionData[2]
    currentLayer = selectionData[3]
    currentSelection = selectionData[4]

    layerName = currentLayer.name()

    # Existing Layer & BaseMaskStack Variables are used to get & store a layerlist of a maskstack after creation
    # in order to remove auto-created layers later on.
    existingLayer = ()
    removeExistingLayer = False
    baseMaskStack = None

    if mode == 'layer':
        mari.history.startMacro('Create channel Layer')
        for channel in sourceChannel:
            channelLayerName = channel.name()
            currentStack.createChannelLayer(channelLayerName, channel, None, 16)
        mari.history.stopMacro()

    else:

        if mode == 'maskgroup':
            if currentLayer.isShaderLayer():
                mari.utils.message('Groups are not supported for Shader Layers')
                return
            else:
                try:
                    ## New Group Layer
                    layerName = currentLayer.name()
                    mari.history.startMacro('Create grouped channel mask')
                    layerGroupName = '%s_grp' % layerName
                    selectionData = getSelectedLayer().findSelection()
                    currentStack = selectionData[2]
                    groupLayer = currentStack.groupLayers(currentSelection, None, '', 16)
                    groupLayer.setName(layerGroupName)
                    layerMaskStack = groupLayer.makeMaskStack()
                    baseMaskStack = layerMaskStack
                    existingLayer = baseMaskStack.layerList()
                    removeExistingLayer = True

                    ## Create Mask Channel Layer

                    for channel in sourceChannel:
                        channelLayerName = channel.name()
                        maskChannelLayerName = '%s(Shared Channel)' % channelLayerName
                        layer = layerMaskStack.createChannelLayer(maskChannelLayerName, channel)
                        # If more than one channelLayer is selected, set 2nd, 3rd etc to 'Screen' BlendMode
                        if channel is not sourceChannel[0]:
                            layer.setBlendMode(27)

                    if invert:
                        layerMaskStack.createAdjustmentLayer("Invert", "Filter/Invert")


                    # Removes old layers from MaskStack creation. Variable usually empty unless the stack was created by the script
                    if removeExistingLayer:
                        baseMaskStack.removeLayers(existingLayer)

                    clearFlags = mari.LayerStack.CLEAR_CURRENT_LAYER_SELECTION |mari.LayerStack.CLEAR_ADJUSTMENT_STACKS | mari.LayerStack.CLEAR_GROUPS | mari.LayerStack.CLEAR_MASK_STACKS
                    baseMaskStack.clearSelection(clearFlags)
                    mari.history.stopMacro()

                except Exception:
                    mari.history.stopMacro()
                    mari.utils.message("Add Channel Layer Mask to Group failed to execute correctly")
                    pass

        elif mode == 'mask':
            mari.history.startMacro('Create channel mask')

            channellayer_multiselection = len(sourceChannel)

            for layer in currentSelection:
                try:

                    # layer.makeCurrent()
                    layerName = layer.name()
                    currentLayer = layer
                    hasMask = False
                    performGrouping = False

                    # Triggering grouping in Maskstacks under certain conditions:
                    # Required: Layer needs to have existing mask
                    # And: Multiple ChannelLayers need to be selected or INVERT needs to be on
                    if channellayer_multiselection >=2 or invert:
                        performGrouping = True

                    ## New Layer Mask Stack.
                    ## If mask exists convert, if stack exists keep, else make new stack
                    if currentLayer.hasMaskStack():
                        layerMaskStack = currentLayer.maskStack()
                        baseMaskStack = layerMaskStack
                        hasMask = True
                        removeExistingLayer = False
                    elif currentLayer.hasMask():
                        layerMaskStack = currentLayer.makeMaskStack()
                        baseMaskStack = layerMaskStack
                        hasMask = True
                        removeExistingLayer = False

                    else:
                        layerMaskStack = currentLayer.makeMaskStack()
                        baseMaskStack = layerMaskStack
                        removeExistingLayer = True
                        existingLayer = layerMaskStack.layerList()
                        hasMask = False


                    # if the selected layer already had a mask and more than one channel layer is selected,
                    # create group 'ChannelLayer_grouped' in maskStack and set it to multiply
                    if hasMask and performGrouping:
                        grouplayer = layerMaskStack.createGroupLayer('ChannelLayer_Masks')
                        layerMaskStack = grouplayer.groupStack()
                        hasMask = False
                        grouplayer.setBlendMode(23)

                    ## Create Mask Channel Layer
                    for channel in sourceChannel:

                        try:

                            channelLayerName = channel.name()
                            maskChannelLayerName = '%s(Shared Channel)' % channelLayerName
                            layer = layerMaskStack.createChannelLayer(maskChannelLayerName, channel,None,mari.LayerStack.CLEAR_CURRENT_LAYER_SELECTION)
                            # If layer already had a mask and only one channel layer is added set layer to multiply
                            if hasMask:
                                layer.setBlendMode(23)

                            # If more than one channelLayer is selected set 2nd,3rd etc to 'Screen'.
                            # If layer already had a mask, this process will happen in a group 'ChannelLayer_Masks'
                            elif channel is not sourceChannel[0]:
                                layer.setBlendMode(27)



                        except Exception,e:
                            print(e)
                            mari.utils.message("Could not add Channel Layer: " + str(channel.name()))
                            pass


                    if invert:
                        layerMaskStack.createAdjustmentLayer("Invert","Filter/Invert")

                    # Removes old layers from MaskStack creation. Variable usually empty unless the stack was created by the script
                    if removeExistingLayer:
                        baseMaskStack.removeLayers(existingLayer)

                    clearFlags = mari.LayerStack.CLEAR_CURRENT_LAYER_SELECTION |mari.LayerStack.CLEAR_ADJUSTMENT_STACKS | mari.LayerStack.CLEAR_GROUPS | mari.LayerStack.CLEAR_MASK_STACKS
                    baseMaskStack.clearSelection(clearFlags)

                except Exception,e:
                    print(e)
                    mari.utils.message("Could not add Channel Layer to: " + str(layer.name()))
                    pass


            mari.history.stopMacro()

    deactivateViewportToggle.trigger()


# ------------------------------------------------------------------------------


class ChannelLayerUI(QtGui.QDialog):
    '''GUI to select channel to make into a channel-layer in the current channel
    modes: 'maskgroup', 'mask', 'layer'
    '''
    def __init__(self, mode):
        suitable = _isProjectSuitable()
        if suitable[0]:
            super(ChannelLayerUI, self).__init__()
            self.setFixedSize(340, 400)
            #Set window title and create a main layout
            title = "Channel Layer"
            if mode is 'mask':
                title = "Channel Layer Mask"
            if mode is 'maskgroup':
                title = "Channel Layer Group Mask"
            self.setWindowTitle(title)
            main_layout = QtGui.QVBoxLayout()

            #Create layout for middle section
            centre_layout = QtGui.QHBoxLayout()

            #Create channel layout, label, and widget. Finally populate.
            channel_layout = QtGui.QVBoxLayout()
            channel_header_layout = QtGui.QHBoxLayout()
            channel_label = QtGui.QLabel("<strong>Channels</strong>")
            channel_list = QtGui.QListWidget()
            channel_list.setSelectionMode(channel_list.ExtendedSelection)

            #Create filter box for channel list
            channel_filter_box = QtGui.QLineEdit()
            mari.utils.connect(channel_filter_box.textEdited, lambda: self.updateChannelFilter(channel_filter_box, channel_list))

            #Create layout and icon/label for channel filter
            channel_header_layout.addWidget(channel_label)
            channel_header_layout.addStretch()
            channel_search_icon = QtGui.QLabel()
            search_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + os.sep + 'Lookup.png')
            channel_search_icon.setPixmap(search_pixmap)
            channel_header_layout.addWidget(channel_search_icon)
            channel_header_layout.addWidget(channel_filter_box)

            #Populate Channel List, channellist gets full channel list from project and amount of channels on current object (which sit at the top of the list)
            channel_list= self.populateChannelList(channel_list)

            #Add filter layout and channel list to channel layout
            channel_layout.addLayout(channel_header_layout)
            channel_layout.addWidget(channel_list)

            #Add widgets to centre layout
            centre_layout.addLayout(channel_layout)

            #Create button layout and hook them up
            button_layout = QtGui.QHBoxLayout()
            ok_button = QtGui.QPushButton("&OK")
            cancel_button = QtGui.QPushButton("&Cancel")
            Invert_box = QtGui.QCheckBox('Invert Channel')
            if mode is not 'layer':
                button_layout.addWidget(Invert_box)
            button_layout.addStretch()
            button_layout.addWidget(ok_button)
            button_layout.addWidget(cancel_button)


            #Hook up OK/Cancel button clicked signal to accept/reject slot
            ok_button.clicked.connect(lambda: self.runCreate(mode,channel_list,Invert_box.isChecked()))
            cancel_button.clicked.connect(self.reject)


            #Add layouts to main layout and dialog
            main_layout.addLayout(centre_layout)
            main_layout.addLayout(button_layout)
            self.setLayout(main_layout)


# ------------------------------------------------------------------------------

    def populateChannelList(self,channel_list):
		"Add channels to channel list"
		selectionData = getSelectedLayer().findSelection()
		geo = selectionData[0]
		cur_chan = selectionData[1]
		chan_list = sorted(geo.channelList(), key=lambda x: unicode.lower( x.name() ) )

		for channel in chan_list:
			shaderChannel = channel.isShaderStack()
			if channel is cur_chan:
				pass
			else:
				if not shaderChannel:
					channel_list.addItem(channel.name())
					channel_list.item(channel_list.count() - 1).setData(USER_ROLE, channel)

		return channel_list

# ------------------------------------------------------------------------------

    def updateChannelFilter(self,channel_filter_box, channel_list):
        "For each item in the channel list display, set it to hidden if it doesn't match the filter text."

        match_words = channel_filter_box.text().lower().split()

        for item_index in range(channel_list.count()):
            item = channel_list.item(item_index)
            item_text_lower = item.text().lower()
            matches = all([word in item_text_lower for word in match_words])
            item.setHidden(not matches)


# ------------------------------------------------------------------------------

    def selectedChannel(self,channel_list):
        "get channel selection"

        multiSelection = []
        for item in channel_list.selectedItems():
            multiSelection.append(item.data(USER_ROLE))

        return multiSelection



    def runCreate(self,mode,channel_list,invert):
        "execute channel layer creation"
        sourceChannel = self.selectedChannel(channel_list)
        makeChannelLayer(sourceChannel,mode,invert)
        self.close()


# ------------------------------------------------------------------------------
# The following are used to find selections no matter where in the Mari Interface:
# returnTrue(),cl_getLayerList(),cl_findLayerSelection()
#
# This is to support a) Layered Shader Stacks b) deeply nested stacks (maskstack,adjustment stacks),
# as well as cases where users are working in pinned or docked channels without it being the current channel
# ------------------------------------------------------------------------------

class getSelectedLayer():
    """Searches for Layer Selection in Substacks and searches for current channel if currentChannel is not the
    selected one (when a channel is opened as floating or pinned palette)"""

    def __init__(self):
        curGeo = None
        curChannel = None
        curLayer = None


    def findSelection(self):
        """Searches for Layer Selection in Substacks and searches for current channel if currentChannel is not the
        selected one (when a channel is opened as floating or pinned palette)"""

        curGeo = mari.current.geo()
        curChannel = mari.current.channel()
        curStack = curChannel
        curLayer = mari.current.layer()
        channels = curGeo.channelList()

        layerStacks = ()
        curSelList = []
        chn_layerList = ()
        layer = None
        stack = None
        layerSelect = False

        if  curLayer.isSelected():
            chn_layerList = curChannel.layerList()
            layerStacks = self.cl_getLayerList(chn_layerList,curChannel,self.cl_returnTrue)

            for item in layerStacks:
                layer = item[1]
                stack = item[0]
                if layer.isSelected():
                    curSelList.append(layer)
                    layerSelect = True
                    curStack = stack
                    curChannel = curChannel

        else:

            for channel in channels:

                chn_layerList = channel.layerList()
                layerStacks = self.cl_getLayerList(chn_layerList,channel,self.cl_returnTrue)

                for item in layerStacks:
                    layer = item[1]
                    stack = item[0]
                    if layer.isSelected():
                        curLayer = layer
                        curStack = stack
                        curChannel = channel
                        curSelList.append(layer)
                        layerSelect = True

        if not layerSelect:
            mari.utils.message('No Layer Selection found. \n \n Please select at least one Layer.')

        return curGeo,curChannel,curStack,curLayer,curSelList



    def cl_returnTrue(self,layer):
        """Returns True for any object passed to it."""
        return True



    def cl_getLayerList(self,layer_list, stack, criterionFn):
        """Returns a list of all of the layers in the stack that match the given criterion function, including substacks."""
        matchingLayers = []
        tu = ()
        for layer in layer_list:
            if criterionFn(layer):
                tu = stack,layer
                matchingLayers.append(tu)
            if hasattr(layer, 'layerStack'):
                if layer.isChannelLayer():
                    pass
                else:
                    matchingLayers.extend(self.cl_getLayerList(layer.layerStack().layerList(),layer.layerStack(),criterionFn))
            if layer.hasMaskStack():
                matchingLayers.extend(self.cl_getLayerList(layer.maskStack().layerList(),layer.maskStack(), criterionFn))
            if hasattr(layer, 'hasAdjustmentStack') and layer.hasAdjustmentStack():
                matchingLayers.extend(self.cl_getLayerList(layer.adjustmentStack().layerList(),layer.adjustmentStack(), criterionFn))

        return matchingLayers

# ------------------------------------------------------------------------------


