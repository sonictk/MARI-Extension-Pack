# ------------------------------------------------------------------------------
# MaterialID from selection Groups
# ------------------------------------------------------------------------------
# Create Material IDs for user-selected selection groups
# ------------------------------------------------------------------------------
# Written by Jens Kafitz, 2015
# ------------------------------------------------------------------------------
# Web: www.campi3d.com
# Email: MariIdeas@campi3d.com
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
import random
import os

version = "0.05"

USER_ROLE = 32          # PySide.Qt.UserRole

# ------------------------------------------------------------------------------
class matIDFromSelectionGroupGUI(QtGui.QDialog):
    "Create main UI."
    def __init__(self, parent=None):
        super(matIDFromSelectionGroupGUI, self).__init__(parent)

        #Set window title and create a main layout
        self.setWindowTitle("Material ID from Selection Groups")
        main_layout = QtGui.QVBoxLayout()

        #Create layout for middle section
        centre_layout = QtGui.QHBoxLayout()

        #Create selGroup layout, label, and widget. Finally populate.
        selGroup_layout = QtGui.QVBoxLayout()
        selGroup_header_layout = QtGui.QHBoxLayout()
        selGroup_label = QtGui.QLabel("<strong>Selection Groups</strong>")
        sel_list = QtGui.QListWidget()
        sel_list.setSelectionMode(sel_list.ExtendedSelection)

        #Create filter box for selGroup list
        selGroups_filter_box = QtGui.QLineEdit()
        mari.utils.connect(selGroups_filter_box.textEdited, lambda: updateSelGroupsFilter(selGroups_filter_box, sel_list))

        #Create layout and icon/label for selGroup filter
        selGroup_header_layout.addWidget(selGroup_label)
        selGroup_header_layout.addStretch()
        selGroup_search_icon = QtGui.QLabel()
        search_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + os.sep + 'Lookup.png')
        selGroup_search_icon.setPixmap(search_pixmap)
        selGroup_header_layout.addWidget(selGroup_search_icon)
        selGroup_header_layout.addWidget(selGroups_filter_box)


        #Populate selGroup List, selGrouplist gets full selGroup list from project and amount of SelGroups on current object (which sit at the top of the list)
        sel_list= self.populateSelectionList(sel_list)
        sel_list = sel_list[0]


        #Add filter layout and selGroup list to selGroup layout
        selGroup_layout.addLayout(selGroup_header_layout)
        selGroup_layout.addWidget(sel_list)

        #Create middle button section
        middle_button_layout = QtGui.QVBoxLayout()
        add_button = QtGui.QPushButton("+")
        remove_button = QtGui.QPushButton("-")
        middle_button_layout.addStretch()
        middle_button_layout.addWidget(add_button)
        middle_button_layout.addWidget(remove_button)
        middle_button_layout.addStretch()

        #Add wrapped QtGui.QListWidget with custom functions
        matID_layout = QtGui.QVBoxLayout()
        matID_header_layout = QtGui.QHBoxLayout()
        matID_label = QtGui.QLabel("<strong>Create IDs for:</strong>")
        self.matID_list = SelGroupsToMatIDList()
        self.matID_list.setSelectionMode(self.matID_list.ExtendedSelection)

        #Create filter box for matID list
        matID_filter_box = QtGui.QLineEdit()
        mari.utils.connect(matID_filter_box.textEdited, lambda: updateMatIDFilter(matID_filter_box, self.matID_list))

        #Create layout and icon/label for matID filter
        matID_header_layout.addWidget(matID_label)
        matID_header_layout.addStretch()
        matID_search_icon = QtGui.QLabel()
        matID_search_icon.setPixmap(search_pixmap)
        matID_header_layout.addWidget(matID_search_icon)
        matID_header_layout.addWidget(matID_filter_box)


        #Add filter layout and matID list to matID layout
        matID_layout.addLayout(matID_header_layout)
        matID_layout.addWidget(self.matID_list)

        #Hook up add/remove buttons
        remove_button.clicked.connect(self.matID_list.removeSelGroups)
        add_button.clicked.connect(lambda: self.matID_list.addSelGroups(sel_list))

        #Add widgets to centre layout
        centre_layout.addLayout(selGroup_layout)
        centre_layout.addLayout(middle_button_layout)
        centre_layout.addLayout(matID_layout)


        #Create button & ChannelName layout and hook them up
        button_layout = QtGui.QHBoxLayout()
        ok_button = QtGui.QPushButton("&OK")
        cancel_button = QtGui.QPushButton("&Cancel")
        channel_label = QtGui.QLabel("<strong>Channel</strong>")


        # Channel Sizes
        self.channel_size = QtGui.QComboBox()
        self.channel_size.addItem("256", 256)
        self.channel_size.addItem("512", 512)
        self.channel_size.addItem("1024", 1024)
        self.channel_size.addItem("2048", 2048)
        self.channel_size.addItem("4096", 4096)
        self.channel_size.addItem("8192", 8192)
        self.channel_size.addItem("8192", 8192)
        self.channel_size.addItem("16384", 16384)
        self.channel_size.addItem("32768", 32768)
        self.channel_size.setCurrentIndex(3)

        self.channel_name = QtGui.QLineEdit("_materialID")
        self.channel_name.setMaximumWidth(115)

        button_layout.addWidget(channel_label)
        button_layout.addWidget(self.channel_name)
        button_layout.addWidget(self.channel_size)
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        #Hook up OK/Cancel button clicked signal to accept/reject slot
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)


        #Add layouts to main layout and dialog
        main_layout.addLayout(centre_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)



# ------------------------------------------------------------------------------

    def populateSelectionList(self,sel_list):


            sorted_list = sorted(mari.selection_groups.list(),key=lambda x: unicode.lower( x.entityName() ) )
            currentSelSetCount = len(sorted_list)
            currentSelSetRow = 0

            for item in sorted_list:
                    sel_list.addItem(item.entityName())
                    sel_list.item(sel_list.count() - 1).setData(USER_ROLE, item)
                    if item is mari.selection_groups.current():
                        currentSelSetRow = sel_list.count()-1

            # Set currently active selGroup to selected
            sel_list.setCurrentRow(currentSelSetRow)

            return sel_list, currentSelSetCount

# ------------------------------------------------------------------------------

    def getSelectionGroups(self):
        return self.matID_list.currentSelGroups()

    def getChannelName(self):
        return self.channel_name.text()

    def getChannelSize(self):
        return self.channel_size.itemData(self.channel_size.currentIndex(), 32)

# ------------------------------------------------------------------------------
class SelGroupsToMatIDList(QtGui.QListWidget):
    "Stores a list of operations to perform."

    def __init__(self, title="For Export"):
        super(SelGroupsToMatIDList, self).__init__()
        self._title = title
        self.setSelectionMode(self.ExtendedSelection)

    def currentSelGroups(self):
        return [self.item(index).data(USER_ROLE) for index in range(self.count())]

    def addSelGroups(self, sel_list):
        "Adds an operation from the current selections of SelGroups and directories."
        selected_items = sel_list.selectedItems()
        if selected_items == []:
            mari.utils.message("Please select at least one selGroup.")
            return

        # Add SelGroups that aren't already added
        current_SelGroups = set(self.currentSelGroups())
        for item in selected_items:
            selGroup = item.data(USER_ROLE)
            if selGroup not in current_SelGroups:
                current_SelGroups.add(selGroup)
                self.addItem(item.text())
                self.item(self.count() - 1).setData(USER_ROLE, selGroup)

    def removeSelGroups(self):
        "Removes any currently selected operations."
        for item in reversed(self.selectedItems()):     # reverse so indices aren't modified
            index = self.row(item)
            self.takeItem(index)

# ------------------------------------------------------------------------------
def updateSelGroupsFilter(selGroups_filter_box, sel_list):
    "For each item in the selGroup list display, set it to hidden if it doesn't match the filter text."

    match_words = selGroups_filter_box.text().lower().split()

    for item_index in range(sel_list.count()):
        item = sel_list.item(item_index)
        item_text_lower = item.text().lower()
        matches = all([word in item_text_lower for word in match_words])
        item.setHidden(not matches)


# ------------------------------------------------------------------------------
def updateMatIDFilter(matID_filter_box, matID_list):
    "For each item in the matID list display, set it to hidden if it doesn't match the filter text."
    match_words = matID_filter_box.text().lower().split()
    for item_index in range(matID_list.count()):
        item = matID_list.item(item_index)
        item_text_lower = item.text().lower()
        matches = all([word in item_text_lower for word in match_words])
        item.setHidden(not matches)

# ------------------------------------------------------------------------------
def isProjectSuitable():
    "Checks project state."
    MARI_3_0V1_VERSION_NUMBER = 30001202    # see below
    if mari.app.version().number() >= MARI_3_0V1_VERSION_NUMBER:

        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False

        return True

    else:
        mari.utils.message("You can only run this script in Mari 2.6v3 or newer.")
        return False

# ------------------------------------------------------------------------------
def matIDFromSelectionGroup():
    "Create MaterialIDs from Selection Groups."
    if not isProjectSuitable():
        return



    #Create dialog and execute accordingly
    dialog = matIDFromSelectionGroupGUI()
    SelGroups_to_matID = ()
    matIdChannelName = ()
    deactivateViewportToggle = None


    if dialog.exec_():
        SelGroups_to_matID = dialog.getSelectionGroups()
        if len(SelGroups_to_matID) > 0:
            mari.history.startMacro('Create MaterialIDs from Selection Groups')
            matIdChannelName = dialog.getChannelName()
            matIdChannelSize = dialog.getChannelSize()

            deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
            deactivateViewportToggle.trigger()

            fill = mari.actions.find('/Mari/Layers/Fill/Foreground')
            currentFGcolor = mari.colors.foreground()


            #Determine if Channel 'MaterialID' exists
            geo = mari.current.geo()
            channelList = geo.channelList()


            matIdChannelExists = False

            for channel in channelList:
                name = channel.name()
                if name == matIdChannelName:
                   matIDChannel = channel
                   matIdChannelExists = True
                   matIDChannel.makeCurrent()
                   pass

            if not matIdChannelExists:
                matID = geo.createChannel(matIdChannelName,matIdChannelSize,matIdChannelSize,8)
                FillColor = mari.Color(0,0,0,1)
                matID.createPaintableLayer(matIdChannelName,None,FillColor)



            for item in SelGroups_to_matID:

                r = random.randrange(0,9999)
                r = r / 9999.0
                g = random.randrange(0,9999)
                g = g / 9999.0
                b = random.randrange(0,9999)
                b = b / 9999.0
                r = abs(1.0 - r)
                g = abs(1.0 - g)
                b = abs(1.0 - b)

                channel = mari.current.channel()
                layer = mari.current.layer()
                channel.setCurrentLayer(layer)
                selectionmode = item.selectionMode()
                mari.selection_groups.setSelectionMode(selectionmode)
                mari.selection_groups.select(item)
                fillcolor = mari.Color(r,g,b,1)

                h = random.randrange(0,255)
                h = h / 255.0 *  r
                s = 1.0


                fillcolor.setH(h)
                fillcolor.setS(s)
                mari.colors.setForeground(fillcolor)
                fill.trigger()

            mari.colors.setForeground(currentFGcolor)
            deactivateViewportToggle.trigger()

            mari.history.stopMacro()

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    matIDFromSelectionGroup()