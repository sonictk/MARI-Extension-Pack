# ------------------------------------------------------------------------------
# Duplicate and flatten selected channels
# ------------------------------------------------------------------------------
# Duplicate and flatten selected channels. The Channel is first duplicated, then flattened, then renamed
# to the original name. The unflattened Channel is suffixed with _original.
# coding: utf-8
# ------------------------------------------------------------------------------
# Written by Jorel Latraille, 2014
# Modified by Jens Kafitz, 2015
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
import PySide.QtGui as QtGui

version = "0.05"

USER_ROLE = 32          # PySide.Qt.UserRole

# ------------------------------------------------------------------------------       
class FlattenSelectedChannelsGUI(QtGui.QDialog):
    "Create main UI."
    def __init__(self, parent=None):
        super(FlattenSelectedChannelsGUI, self).__init__(parent)

        #Set window title and create a main layout
        self.setWindowTitle("Duplicate & Flatten Selected Channels")
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
        mari.utils.connect(channel_filter_box.textEdited, lambda: updateChannelFilter(channel_filter_box, channel_list))
        
        #Create layout and icon/label for channel filter
        channel_header_layout.addWidget(channel_label)
        channel_header_layout.addStretch()
        channel_search_icon = QtGui.QLabel()
        search_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
        channel_search_icon.setPixmap(search_pixmap)
        channel_header_layout.addWidget(channel_search_icon)
        channel_header_layout.addWidget(channel_filter_box)
 
        #Populate Channel List, channellist gets full channel list from project and amount of channels on current object (which sit at the top of the list)
        channel_list= self.populateChannelList(channel_list)
        currentObjChannels = channel_list[1]
        channel_list = channel_list[0]

        
        #Add filter layout and channel list to channel layout
        channel_layout.addLayout(channel_header_layout)
        channel_layout.addWidget(channel_list)
        
        #Create middle button section
        middle_button_layout = QtGui.QVBoxLayout()
        add_button = QtGui.QPushButton("+")
        remove_button = QtGui.QPushButton("-")
        middle_button_layout.addStretch()
        middle_button_layout.addWidget(add_button)
        middle_button_layout.addWidget(remove_button)
        middle_button_layout.addStretch()
        
        #Add wrapped QtGui.QListWidget with custom functions
        flatten_layout = QtGui.QVBoxLayout()
        flatten_header_layout = QtGui.QHBoxLayout()
        flatten_label = QtGui.QLabel("<strong>Channels To Flatten</strong>")
        self.flatten_list = ChannelsToFlattenList()
        self.flatten_list.setSelectionMode(self.flatten_list.ExtendedSelection)
        
        #Create filter box for flatten list
        flatten_filter_box = QtGui.QLineEdit()
        mari.utils.connect(flatten_filter_box.textEdited, lambda: updateFlattenFilter(flatten_filter_box, self.flatten_list))
        
        #Create layout and icon/label for flatten filter
        flatten_header_layout.addWidget(flatten_label)
        flatten_header_layout.addStretch()
        flatten_search_icon = QtGui.QLabel()
        flatten_search_icon.setPixmap(search_pixmap)
        flatten_header_layout.addWidget(flatten_search_icon)
        flatten_header_layout.addWidget(flatten_filter_box)

        
        #Add filter layout and flatten list to flatten layout
        flatten_layout.addLayout(flatten_header_layout)
        flatten_layout.addWidget(self.flatten_list)
        
        #Hook up add/remove buttons
        remove_button.clicked.connect(self.flatten_list.removeChannels)
        add_button.clicked.connect(lambda: self.flatten_list.addChannels(channel_list))

        #Add widgets to centre layout
        centre_layout.addLayout(channel_layout)
        centre_layout.addLayout(middle_button_layout)
        centre_layout.addLayout(flatten_layout)

        
        #Create button layout and hook them up
        button_layout = QtGui.QHBoxLayout()
        ok_button = QtGui.QPushButton("&OK")
        cancel_button = QtGui.QPushButton("&Cancel")
        displayAllObjBox = QtGui.QCheckBox('List all Objects')
        button_layout.addWidget(displayAllObjBox)
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        #Hook up OK/Cancel button clicked signal to accept/reject slot
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        #Hook up List All Object Checkbox
        displayAllObjBox.clicked.connect(lambda: listAllObjects(channel_list,currentObjChannels,displayAllObjBox.isChecked()))

        
        #Add layouts to main layout and dialog
        main_layout.addLayout(centre_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        
        #calling once to cull the object list, whole thing doesn't really make for a snappy interface appearance
        listAllObjects(channel_list,currentObjChannels,displayAllObjBox.isChecked())       
  
# ------------------------------------------------------------------------------

    def populateChannelList(self,channel_list):

        #Populate geo : channel list widget
            geo_list = sorted(mari.geo.list(), key=lambda x: x.name())
            chan_list = []
            sorted_list = []
    
            for geo in geo_list:
                # add geo in alphabetical sorting with all channels for each geo in alphabetical sorting, except current one which will go to the top
                if geo is not mari.geo.current():
                    sorted_list = sorted(geo.channelList(), key=lambda x: unicode.lower( x.name() ) )
                    chan_list.append((geo.name(), sorted_list))
                    
    
            # Push current object to the top of the list
            currentObjName = mari.current.geo().name()
            sorted_list = sorted(mari.geo.current().channelList(),key=lambda x: unicode.lower( x.name() ) )
            currentChannelCount = len(sorted_list)
            currentObj = (currentObjName,sorted_list)       
            chan_list.insert(0,currentObj)
    
            for item in chan_list:
                shaderChannelCountCheck = False
                if item[0] is currentObjName:
                    shaderChannelCountCheck = True
                for channel in item[1]:
                    shaderChannel = channel.isShaderStack()
                    if shaderChannel and shaderChannelCountCheck:
                        currentChannelCount -= 1     
                    if not shaderChannel:
                        channel_list.addItem(item[0] + ' : ' + channel.name())
                        channel_list.item(channel_list.count() - 1).setData(USER_ROLE, channel)
                        if channel is mari.current.channel():
                            currentChannelRow = channel_list.count()-1
    
            # Set currently active channel to selected
            channel_list.setCurrentRow(currentChannelRow)      
            
            return channel_list, currentChannelCount

# ------------------------------------------------------------------------------
        
    def getChannelsToFlatten(self):
        return self.flatten_list.currentChannels()

# ------------------------------------------------------------------------------   
class ChannelsToFlattenList(QtGui.QListWidget):
    "Stores a list of operations to perform."
    
    def __init__(self, title="For Export"):
        super(ChannelsToFlattenList, self).__init__()
        self._title = title
        self.setSelectionMode(self.ExtendedSelection)
        
    def currentChannels(self):
        return [self.item(index).data(USER_ROLE) for index in range(self.count())]
        
    def addChannels(self, channel_list):
        "Adds an operation from the current selections of channels and directories."
        selected_items = channel_list.selectedItems()
        if selected_items == []:
            mari.utils.message("Please select at least one channel.")
            return
        
        # Add channels that aren't already added
        current_channels = set(self.currentChannels())
        for item in selected_items:
            channel = item.data(USER_ROLE)
            if channel not in current_channels:
                current_channels.add(channel)
                self.addItem(item.text())
                self.item(self.count() - 1).setData(USER_ROLE, channel)
        
    def removeChannels(self):
        "Removes any currently selected operations."
        for item in reversed(self.selectedItems()):     # reverse so indices aren't modified
            index = self.row(item)
            self.takeItem(index)    

# ------------------------------------------------------------------------------
def updateChannelFilter(channel_filter_box, channel_list):
    "For each item in the channel list display, set it to hidden if it doesn't match the filter text."
    
    match_words = channel_filter_box.text().lower().split()
   
    for item_index in range(channel_list.count()):
        item = channel_list.item(item_index)
        item_text_lower = item.text().lower()
        matches = all([word in item_text_lower for word in match_words])
        item.setHidden(not matches)


# ------------------------------------------------------------------------------
def listAllObjects(channel_list, cur_obj_channels, showAll):
    """For each item in the channel list display, set it to hidden if it doesn't match current Object."""

    if showAll:
        listSize = channel_list.count()
        for index in range(cur_obj_channels,listSize):
            item = channel_list.item(index)
            item.setHidden(False)

    else:
        listSize = channel_list.count()
        for index in range(cur_obj_channels,listSize):
            item = channel_list.item(index)
            item.setHidden(True)


# ------------------------------------------------------------------------------
def updateFlattenFilter(flatten_filter_box, flatten_list):
    "For each item in the flatten list display, set it to hidden if it doesn't match the filter text."
    match_words = flatten_filter_box.text().lower().split()
    for item_index in range(flatten_list.count()):
        item = flatten_list.item(item_index)
        item_text_lower = item.text().lower()
        matches = all([word in item_text_lower for word in match_words])
        item.setHidden(not matches)
    
# ------------------------------------------------------------------------------
def isProjectSuitable():
    "Checks project state."
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:
    
        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False
        
        geo_list = mari.geo.list()
        for geo in geo_list:
            channel_list = geo.channelList()
            if channel_list == 0:
                mari.utils.message("Please ensure all objects have at least one channel.")
                return False

        return True
    
    else:
        mari.utils.message("You can only run this script in Mari 2.6v3 or newer.")
        return False

# ------------------------------------------------------------------------------                  
def flattenSelectedChannels():
    "Duplicate and flatten selected channels."
    if not isProjectSuitable():
        return
    
    mari.history.startMacro('Duplicate & Flatten Channels')

    #Create dialog and execute accordingly
    dialog = FlattenSelectedChannelsGUI()
    if dialog.exec_():
        channels_to_flatten = dialog.getChannelsToFlatten()
        
        for channel in channels_to_flatten:
            orig_name = channel.name()
            geo = channel.geoEntity()
            flatten_channel = geo.createDuplicateChannel(channel, channel.name() + '_flatten')
            flatten_channel.flatten()
            channel.setName(channel.name() + '_original')
            flatten_channel.setName(orig_name)

    mari.history.stopMacro()
    
# ------------------------------------------------------------------------------            
  
if __name__ == "__main__":
    flattenSelectedChannels()