# ------------------------------------------------------------------------------
# Cache/Uncache Selected Channels
# ------------------------------------------------------------------------------
# Gives the user a UI to select Channels to cache or uncache.
# Additional options give consideration to shared layers & channels.
# Uncaching supports 'deep uncaching' of nested caches
# ------------------------------------------------------------------------------
# Written by Jens Kafitz, 2015 using UI Elements from Jorel Latraille, 2014
# ------------------------------------------------------------------------------
# http://mari.ideascale.com
# ------------------------------------------------------------------------------
# DISCLAIMER & TERMS OF USE:
#
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
import PySide.QtCore as QtCore

version = "0.01"

USER_ROLE = 32          # PySide.Qt.UserRole

# ------------------------------------------------------------------------------

# ----------------------------------------------
# Main UI Class:
# cacheSelectedChannelsGUI
#       __init__ : UI
#       populateChannelList: Add channels to UI
#       _cacheMode: Call if Caching Button is pressed, forwards to cacheUncache() class
#       _uncacheMode: Call if Uncaching Button is pressed, forwards to cacheUncache() class
#       _ignoreSharedLayers: Checks state of UI Checbox
#       _ignoreCachedLayers: Checks state of UI Checbox
#       _ignoreSharedChannels: Checks state of UI Checbox
#       _deepUncache: Checks state of UI Checbox
# ----------------------------------------------


class cacheSelectedChannelsGUI(QtGui.QDialog):
    "Create main UI."
    def __init__(self, parent=None):
        super(cacheSelectedChannelsGUI, self).__init__(parent)

        #Set window title and create a main layout
        self.setFixedSize(800, 600)
        # self.setSizePolicy(QSizePolicy:Expanding, QSizePolicy::Expanding)
        self.setWindowTitle("Cache Channel Selection")

        #Create overall ui layout
        main_layout = QtGui.QVBoxLayout()

        #Create layout for top section (channel selection)
        top_layout = QtGui.QHBoxLayout()

        #Create layout for bottom section (option selection)
        checkbox_layout = QtGui.QHBoxLayout()

        #Layout groups
        top_group = QtGui.QGroupBox()
        objectList_group = QtGui.QGroupBox()
        checkbox_group = QtGui.QGroupBox()
        button_group = QtGui.QGroupBox()


        #Create Channel layout, label, and widget. Finally populate.
        Channel_layout = QtGui.QVBoxLayout()
        Channel_header_layout = QtGui.QHBoxLayout()
        self.Channel_label = QtGui.QLabel("<strong>Channels</strong>")
        self.channel_list = QtGui.QListWidget()
        self.channel_list.setSelectionMode(self.channel_list.ExtendedSelection)

        #Create filter box for Channel list
        self.Channel_filter_box = QtGui.QLineEdit()
        mari.utils.connect(self.Channel_filter_box.textEdited, lambda: updateChannelFilter(self.Channel_filter_box, self.channel_list))

        #Create layout and icon/label for Channel filter
        Channel_header_layout.addWidget(self.Channel_label)
        Channel_header_layout.addStretch()
        self.Channel_search_icon = QtGui.QLabel()
        search_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
        self.Channel_search_icon.setPixmap(search_pixmap)
        Channel_header_layout.addWidget(self.Channel_search_icon)
        Channel_header_layout.addWidget(self.Channel_filter_box)

        #Populate Channel List, channellist gets full channel list from project and amount of channels on current object (which sit at the top of the list)
        self.channel_list= self.populateChannelList(self.channel_list)
        currentObjChannels = self.channel_list[1]
        self.channel_list = self.channel_list[0]

        #Add filter layout and Channel list to Channel layout
        Channel_layout.addLayout(Channel_header_layout)
        Channel_layout.addWidget(self.channel_list)

        #Create middle button section
        middle_button_layout = QtGui.QVBoxLayout()
        self.add_button = QtGui.QPushButton("+")
        self.remove_button = QtGui.QPushButton("-")
        middle_button_layout.addStretch()
        middle_button_layout.addWidget(self.add_button)
        middle_button_layout.addWidget(self.remove_button)
        middle_button_layout.addStretch()

        #Add wrapped QtGui.QListWidget with custom functions
        Cache_layout = QtGui.QVBoxLayout()
        Cache_header_layout = QtGui.QHBoxLayout()
        self.Cache_label = QtGui.QLabel("<strong>Channels To Cache</strong>")
        self.cache_list = ChannelsToCacheList()
        self.cache_list.setSelectionMode(self.cache_list.ExtendedSelection)

        #Create filter box for Cache list
        self.Cache_filter_box = QtGui.QLineEdit()
        mari.utils.connect(self.Cache_filter_box.textEdited, lambda: updateCacheFilter(self.Cache_filter_box, self.cache_list))

        #Create layout and icon/label for Cache filter
        Cache_header_layout.addWidget(self.Cache_label)
        Cache_header_layout.addStretch()
        self.Cache_search_icon = QtGui.QLabel()
        self.Cache_search_icon.setPixmap(search_pixmap)
        Cache_header_layout.addWidget(self.Cache_search_icon)
        Cache_header_layout.addWidget(self.Cache_filter_box)

        #Add filter layout and Cache list to Cache layout
        Cache_layout.addLayout(Cache_header_layout)
        Cache_layout.addWidget(self.cache_list)

        #Hook up add/remove buttons
        self.remove_button.clicked.connect(self.cache_list.removeChannels)
        self.add_button.clicked.connect(lambda: self.cache_list.addChannels(self.channel_list))

        #Add widgets to top layout
        top_layout.addLayout(Channel_layout)
        top_layout.addLayout(middle_button_layout)
        top_layout.addLayout(Cache_layout)

        # Add to top group
        top_group_layout = QtGui.QVBoxLayout()
        top_group_layout.addLayout(top_layout)
        top_group.setLayout(top_group_layout)

        #Add ObjectList layout and check boxes
        objectList_layout = QtGui.QGridLayout()
        displayAllObjBox = QtGui.QCheckBox('List all Objects')
        displayAllObjBox.clicked.connect(lambda: listAllObjects(self.channel_list,currentObjChannels,displayAllObjBox.isChecked()))
        objectList_layout.addWidget(displayAllObjBox)
        objectList_group.setLayout(objectList_layout)


        # Cache Checkbox Options Layout
        CacheOpt_layout = QtGui.QGridLayout()
        self.Cache_ignoreSharedLayers_box = QtGui.QCheckBox('Cache Shared Layers individually')
        self.Cache_ignoreSharedLayers_box.setChecked(True)
        CacheOpt_layout.addWidget(self.Cache_ignoreSharedLayers_box,0,0)

        self.Cache_ignoreSharedChannels_box = QtGui.QCheckBox('Skip Shared Channels')
        self.Cache_ignoreSharedChannels_box.setChecked(True)
        CacheOpt_layout.addWidget(self.Cache_ignoreSharedChannels_box,1,0)

        self.Cache_ignoreCachedLayers_box = QtGui.QCheckBox('Skip existing Cached Layers')
        self.Cache_ignoreCachedLayers_box.setChecked(True)
        CacheOpt_layout.addWidget(self.Cache_ignoreCachedLayers_box,2,0)

        # Cache Options Surround labeled Group Box
        cacheGroupBox = QtGui.QGroupBox("Cache Options")
        cacheGroupBox.setLayout(CacheOpt_layout)

        # UnCache Checkbox Options Layout
        UncacheOpt_layout = QtGui.QGridLayout()
        self.Cache_deepUncaching_box = QtGui.QCheckBox('Deep uncache nested caches')
        self.Cache_deepUncaching_box.setChecked(True)
        UncacheOpt_layout.addWidget(self.Cache_deepUncaching_box,0,2)

        # UnCache Options Surrounding labeled Group Box
        uncacheGroupBox = QtGui.QGroupBox("Uncache Options")
        uncacheGroupBox.setLayout(UncacheOpt_layout)


        # Cache/Uncache labeled GroupBox Layout added to groupbox
        groupbox_layout = QtGui.QGridLayout()
        groupbox_layout.addWidget(cacheGroupBox,0,0)
        groupbox_layout.addWidget(uncacheGroupBox,0,1)

        checkbox_group.setLayout(groupbox_layout)

        #Add widget groups to main layout
        main_layout.addWidget(top_group)
        main_layout.addWidget(objectList_group)
        main_layout.addWidget(checkbox_group)


        #Add Button group layout and check boxes
        button_group_layout = QtGui.QHBoxLayout()

        self.CacheBtn = QtGui.QPushButton('Cache Selection')
        self.UncacheBtn = QtGui.QPushButton('Uncache Selection')
        self.CancelBtn = QtGui.QPushButton('Cancel')
        # Populate
        button_group_layout.addWidget(self.CacheBtn)
        button_group_layout.addWidget(self.UncacheBtn)
        button_group_layout.addWidget(self.CancelBtn)
        # Connections
        self.CacheBtn.clicked.connect(lambda: self._cacheMode())
        self.UncacheBtn.clicked.connect(lambda: self._uncacheMode())
        self.CancelBtn.clicked.connect(self.reject)

        button_group.setLayout(button_group_layout)
        main_layout.addWidget(button_group)

        self.setLayout(main_layout)

        #calling once to cull the object list, whole thing doesn't really make for a snappy interface appearance
        listAllObjects(self.channel_list,currentObjChannels,displayAllObjBox.isChecked())


    #Add Channels to UI Channel List
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

    #queries UI option user selection
    def _getOptionSelection(self):
        args_dict_cache = {
        'ignoreSharedLayers' : self._ignoreSharedLayers(),
        'ignoreCachedLayers' : self._ignoreCachedLayers(),
        'ignoreSharedChannels' : self._ignoreSharedChannels(),
        }
        args_dict_uncache = {
        'deepUncache' : self._deepUncache()
        }
        return args_dict_cache,args_dict_uncache

    # caching execution stepping stone function
    def _cacheMode(self):
        currentChannels  =  self.cache_list.currentChannels()
        options = self._getOptionSelection()
        cacheUncache().cache_selection(currentChannels,options[0])
        self.accept()

    # uncaching execution stepping stone function
    def _uncacheMode(self):
        currentChannels  =  self.cache_list.currentChannels()
        options = self._getOptionSelection()
        cacheUncache().uncache_selection(currentChannels,options[1])
        self.accept()


    #Get CacheSharedLayers individually box (bool)
    def _ignoreSharedLayers(self):
        return self.Cache_ignoreSharedLayers_box.isChecked()

    #Get Skip existing cached layers box (bool)
    def _ignoreCachedLayers(self):
        return self.Cache_ignoreCachedLayers_box.isChecked()

    #Get Skip caching of shared channels box (bool)
    def _ignoreSharedChannels(self):
        return self.Cache_ignoreSharedChannels_box.isChecked()

    #Get deep uncache nested caches box (bool)
    def _deepUncache(self):
        return self.Cache_deepUncaching_box.isChecked()

# ------------------------------------------------------------------------------


# ----------------------------------------------
# ChannelsToCacheList:
#       __init__
#       currentChannels: Parses final channel selection from UI to cacheUncache()
#       addChannels: Adds Channels from ChannelList UI to ChannelsSelectedUI element
#       removeChannels: Removes Channels from ChannelsSelectedUI
# ----------------------------------------------


class ChannelsToCacheList(QtGui.QListWidget):
    "Stores a list of operations to perform."

    def __init__(self, title="For Caching"):
        super(ChannelsToCacheList, self).__init__()
        self._title = title
        self.setSelectionMode(self.ExtendedSelection)

    def currentChannels(self):
        return [self.item(index).data(USER_ROLE) for index in range(self.count())]

    def addChannels(self, channel_list):
        "Adds an operation from the current selections of Channels and directories."
        selected_items = channel_list.selectedItems()
        if selected_items == []:
            mari.utils.message("Please select at least one Channel.")
            return

        # Add Channels that aren't already added
        current_Channels = set(self.currentChannels())
        for item in selected_items:
            Channel = item.data(USER_ROLE)
            if Channel not in current_Channels:
                current_Channels.add(Channel)
                self.addItem(item.text())
                self.item(self.count() - 1).setData(USER_ROLE, Channel)

    def removeChannels(self):
        "Removes any currently selected operations."
        for item in reversed(self.selectedItems()):     # reverse so indices aren't modified
            index = self.row(item)
            self.takeItem(index)

# ------------------------------------------------------------------------------


# ----------------------------------------------
#  Updates Channel List in UI based on Filter Text Box
# ----------------------------------------------

def updateChannelFilter(Channel_filter_box, channel_list):
    "For each item in the Channel list display, set it to hidden if it doesn't match the filter text."
    match_words = Channel_filter_box.text().lower().split()
    for item_index in range(channel_list.count()):
        item = channel_list.item(item_index)
        item_text_lower = item.text().lower()
        matches = all([word in item_text_lower for word in match_words])
        item.setHidden(not matches)


# ------------------------------------------------------------------------------

# ----------------------------------------------
#  Updates ChannelToCache List in UI based on Filter Text Box
# ----------------------------------------------

def updateCacheFilter(cache_filter_box, cache_list):
    "For each item in the cache list display, set it to hidden if it doesn't match the filter text."
    match_words = cache_filter_box.text().lower().split()
    for item_index in range(cache_list.count()):
        item = cache_list.item(item_index)
        item_text_lower = item.text().lower()
        matches = all([word in item_text_lower for word in match_words])
        item.setHidden(not matches)

# ------------------------------------------------------------------------------

# ----------------------------------------------
#  Updates Channel List in UI based on listAllObjects Checkbox
# ----------------------------------------------


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


# ----------------------------------------------
# Main Class responsible for Caching/Uncaching
# cacheUncache:
#       __init__
#       cache_selection: Called when Cache Button is pressed, caches based on options selected
#       uncache_selection: Called when UnCache Button is pressed, uncaches based on options selected
#
# ----------------------------------------------

class cacheUncache():
    "Caches or Uncaches selection"
    def _init_(self,currentChannels,options):
        channelsToDo = currentChannels
        options = options

    def cache_selection(self,currentChannels,CacheOptions):
        " Caches selection"

        Channels_to_cache = currentChannels

        mari.history.startMacro('Cache Selected Channels')

      # Checking if any options are enabled, if none just run caching normally
        customOptionsOff = True
        for key,value in list(CacheOptions.items()):
            if value:
                customOptionsOff = False

        if customOptionsOff:

            for Channel in Channels_to_cache:
                geo = Channel.geoEntity()
                chanName = Channel.name()

                try:
                    currentLayer = Channel.currentLayer()
                    currentLayer.setSelected(False)
                    layerList = Channel.layerList()
                    layerList[0].setSelected(True)
                    layerList[0].setCachedUpToHere(True)

                except Exception:
                    pass
                    print "Channel " + chanName + " could not be cached"



        mari.history.stopMacro()


    def uncache_selection(self,currentChannels,UncacheOptions):
        " UnCaches selection"

        Channels_to_cache = currentChannels

        mari.history.startMacro('Uncache Selected Channels')


      # Checking if any options are enabled, if none just run caching normally
        customOptionsOff = True
        for key,value in list(UncacheOptions.items()):
            if value:
                customOptionsOff = False

        if customOptionsOff:

            for Channel in Channels_to_cache:
                geo = Channel.geoEntity()
                chanName = Channel.name()

                try:
                    currentLayer = Channel.currentLayer()
                    currentLayer.setSelected(False)
                    layerList = Channel.layerList()
                    layerList[0].setSelected(True)
                    layerList[0].setCachedUpToHere(False)

                except Exception:
                    pass
                    print "Channel " + chanName + " could not be uncached"

        mari.history.stopMacro()

# ------------------------------------------------------------------------------

# ----------------------------------------------
#  Checks Project State, Mari Version, Channel Count mininum
# ----------------------------------------------



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
                mari.utils.message("Please ensure all objects have at least one Channel.")
                return False

        return True

    else:
        mari.utils.message("You can only run this script in Mari 2.6v3 or newer.")
        return False

# ------------------------------------------------------------------------------

# ----------------------------------------------
#  Convenience Function to call UI
# ----------------------------------------------

def cacheSelectedChannels():
    "Cache selected Channels."
    if not isProjectSuitable():
        return

    #Create dialog and execute accordingly
    cacheSelectedChannelsGUI().exec_()

# ------------------------------------------------------------------------------


# cacheSelectedChannels()