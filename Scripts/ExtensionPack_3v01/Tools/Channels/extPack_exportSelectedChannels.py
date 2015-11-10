# ------------------------------------------------------------------------------
# Export Selected Channels
# ------------------------------------------------------------------------------
# Export selected channels from one or more objects
# coding: utf-8
# ------------------------------------------------------------------------------
# Originally written by Jorel Latraille, 2014
# ------------------------------------------------------------------------------
# http://www.jorel-latraille.com/
# http://www.thefoundry.co.uk
# http://www.jenskafitz.com
# ------------------------------------------------------------------------------
# Additions by Jens Kafitz, 2015
#  - PySide Conversion
#  - Path / Template Field Separation
#  - List All Objects
#  - Modified Textures Metadata fixes
#  - Modified Textures notices changes in channel layers now
#  - Resolution Exports
#  - Texture Post Processing
#  - Hiding of Mari Internal Channels and Channel sorting in line with Channel Palette
#  - Preselecting channels
#  - UI Fixes & Changes
#  - Mari UI Integration
#  - Remembering of Settings
#  - Path Field Dialog and Folder Creation System
# ------------------------------------------------------------------------------
# If you are reading this and you want to understand what is going on - good luck and sorry for the mess.
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


import mari, os, hashlib
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
from PySide.QtCore import QSettings
import subprocess
import inspect


version = "3.0"     #UI VERSION
Settings_Group = "Export_Selected_Channels_" + version    #The Settings Group in the Mari Config File

USER_ROLE = 34          # PySide.Qt.UserRole
CHANNEL_NODE = None     # A Global Channel Variable for dynamically resized Channel Nodes
CHANNEL_DUP = None      # A Global Channel Variable for dynamically resized Channel Objects
EXPORT_SELECTED = False # A Global Variable for Export Selected Patches
EXPORT_PATH_DICT = {}   # A Dictionary to log all exported File paths if post processing is required


# ------------------------------------------------------------------------------
class ExportSelectedChannelsUI(QtGui.QDialog):
    """Export channels from one or more objects."""
    def __init__(self, bool_, mode,parent=None):
        super(ExportSelectedChannelsUI, self).__init__(parent)

        # Storing Widget Settings between sessions here:
        self.SETTINGS = mari.Settings()

        self.dialog_mode = mode

        #Set window title and create a main layout
        self._optionsLoad()
        self.bool_ = bool_
        self.setWindowTitle("Export Custom Channel Selection")
        main_layout = QtGui.QVBoxLayout()
        top_group = QtGui.QGroupBox()
        modified_box_group = QtGui.QGroupBox()
        options_box_group = QtGui.QGroupBox()
        res_box_group = QtGui.QGroupBox()

        #Create layout for middle section
        top_layout = QtGui.QHBoxLayout()

        #Create channel layout, label, and widget. Finally populate.
        channel_layout = QtGui.QVBoxLayout()
        channel_header_layout = QtGui.QHBoxLayout()
        self.channel_label = QtGui.QLabel("<strong>Channels</strong>")
        self.channel_list = QtGui.QListWidget()
        self.channel_list.setSelectionMode(self.channel_list.ExtendedSelection)

        #Create filter box for channel list
        self.channel_filter_box = QtGui.QLineEdit()
        mari.utils.connect(self.channel_filter_box.textEdited, lambda: _updateChannelFilter(self.channel_filter_box, self.channel_list))

        #Create layout and icon/label for channel filter
        channel_header_layout.addWidget(self.channel_label)
        channel_header_layout.addStretch()
        self.channel_search_icon = QtGui.QLabel()
        search_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + os.sep + 'Lookup.png')
        self.channel_search_icon.setPixmap(search_pixmap)
        channel_header_layout.addWidget(self.channel_search_icon)
        channel_header_layout.addWidget(self.channel_filter_box)

        #Populate Channel List, channellist gets full channel list from project and amount of channels on current object (which sit at the top of the list)
        self.channel_list= self.populateChannelList(self.channel_list)
        currentObjChannels = self.channel_list[1]
        self.channel_list = self.channel_list[0]

        #Add filter layout and channel list to channel layout
        channel_layout.addLayout(channel_header_layout)
        channel_layout.addWidget(self.channel_list)

        #Create middle button section
        middle_button_layout = QtGui.QVBoxLayout()
        self.add_button = QtGui.QPushButton("+")
        self.remove_button = QtGui.QPushButton("-")
        middle_button_layout.addStretch()
        middle_button_layout.addWidget(self.add_button)
        middle_button_layout.addWidget(self.remove_button)
        middle_button_layout.addStretch()

        #Add wrapped QtGui.QListWidget with custom functions
        export_layout = QtGui.QVBoxLayout()
        export_header_layout = QtGui.QHBoxLayout()
        self.export_label = QtGui.QLabel("<strong>Channels To Export</strong>")
        self.export_list = ChannelsToExportList()
        self.export_list.setSelectionMode(self.export_list.ExtendedSelection)

        #Create filter box for export list
        self.export_filter_box = QtGui.QLineEdit()
        mari.utils.connect(self.export_filter_box.textEdited, lambda: _updateExportFilter(self.export_filter_box, self.export_list))

        #Create layout and icon/label for export filter
        export_header_layout.addWidget(self.export_label)
        export_header_layout.addStretch()
        self.export_search_icon = QtGui.QLabel()
        self.export_search_icon.setPixmap(search_pixmap)
        export_header_layout.addWidget(self.export_search_icon)
        export_header_layout.addWidget(self.export_filter_box)

        #Add filter layout and export list to export layout
        export_layout.addLayout(export_header_layout)
        export_layout.addWidget(self.export_list)

        #Hook up add/remove buttons
        self.remove_button.clicked.connect(self.export_list._removeChannels)
        self.add_button.clicked.connect(lambda: self.export_list._addChannels(self.channel_list))

        #Add widgets to top layout
        top_layout.addLayout(channel_layout)
        top_layout.addLayout(middle_button_layout)
        top_layout.addLayout(export_layout)


        #Add path layout
        path_layout = QtGui.QGridLayout()

        #Get mari default path and template. If dialog is called in mode 'flattened' get flattened Sequence Template, otherwise normal one
        path = os.path.abspath(mari.resources.path(mari.resources.DEFAULT_EXPORT))
        if self.dialog_mode == 'flattened':
            template = mari.resources.flattenedSequenceTemplate()
        else:
            template = mari.resources.sequenceTemplate()

        export_path_template = os.path.join(path, template)

        #Add path line input and button, also set text to Mari default path and template
        path_label = QtGui.QLabel('Base Path:')
        self.path_line_edit = QtGui.QLineEdit()
        self.path_line_edit.setToolTip('Define your export base path here.\nWhen a $ Variable is found all subfolders will be \ncreated automatically without user prompts\nSupported Variables are: \n\n$ENTITY\n$CHANNEL\n$LAYER\n$UDIM\n$FRAME\n')
        path_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) +  os.sep + 'ExportImages.png')
        icon = QtGui.QIcon(path_pixmap)
        path_button = QtGui.QPushButton(icon, "")
        path_button.setToolTip('Browse for Export Folder')
        path_button.clicked.connect(self._getPath)
        self.path_line_edit.setText(path)

        #Add path line input and button to middle layout
        path_layout.addWidget(path_label,0,0)
        path_layout.addWidget(self.path_line_edit,0,1)
        path_layout.addWidget(path_button,0,2)

        #Add Template line input & Reset Template Button
        template_label = QtGui.QLabel('Template:')
        self.template_line_edit = QtGui.QLineEdit()
        self.template_line_edit.setToolTip('Use this section to define an export template. \nYou can use Variables to create subfolders here as well. \nSupported Variables are: \n\n$ENTITY\n$CHANNEL\n$LAYER\n$UDIM\n$FRAME\n')
        self.template_line_edit.setText(template)

        template_reset_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + os.sep + 'Reset.png')
        template_reset_icon = QtGui.QIcon(template_reset_pixmap)
        self.template_reset_button = QtGui.QPushButton(template_reset_icon, "")
        self.template_reset_button.setToolTip('Reset Export Template to Project Default')
        self.template_reset_button.clicked.connect(self._resetExportPathTemplate)


        #Add template line input and file format dropdown to middle layout
        path_layout.addWidget(template_label,0,3)
        path_layout.addWidget(self.template_line_edit,0,4)
        path_layout.addWidget(self.template_reset_button,0,5)

        #Add to top group
        top_checkbox_group_layout = QtGui.QVBoxLayout()

        #Add Display all Objects check box
        displayAllObjBox = QtGui.QCheckBox('List all Objects')
        displayAllObjBox.setToolTip('If ON, all channels from all objects in the project will be shown')
        displayAllObjBox.clicked.connect(lambda: listAllObjects(self.channel_list,currentObjChannels,displayAllObjBox.isChecked()))

        #Add export everything check box
        self.export_everything_box = QtGui.QCheckBox('Export Everything')
        self.export_everything_box.setToolTip('Exports all Channels for all Objects')
        self.export_everything_box.clicked.connect(self._exportEverything)

        top_checkbox_group_layout.addLayout(top_layout)
        top_checkbox_group_layout.addLayout(path_layout)
        top_checkbox_group_layout.addWidget(displayAllObjBox)
        top_checkbox_group_layout.addWidget(self.export_everything_box)
        top_group.setLayout(top_checkbox_group_layout)


        #Add middle group layout and check boxes
        middle_checkbox_group_layout = QtGui.QGridLayout()

        self.export_only_modified_textures_box = QtGui.QCheckBox('Only Modified Textures')
        self.export_only_modified_textures_box.setToolTip('Exports only modified UDIMs. Requires at least one previous export with this tool\nPlease note this is only considered when exporting all Patches.\nWhen exporting only selected patches, this setting is ignored.')
        self.export_only_modified_textures_box.setChecked(False)

        self.run_postprocessing_box = QtGui.QCheckBox('Execute Post Process Commands')
        self.run_postprocessing_box.setToolTip('When on, any post process script specified\nunder "Post Process" Dialog will be executed')
        self.run_postprocessing_box.setChecked(False)

        middle_checkbox_group_layout.addWidget(self.export_only_modified_textures_box,0,0)
        middle_checkbox_group_layout.addWidget(self.run_postprocessing_box,0,1)

        modified_box_group.setLayout(middle_checkbox_group_layout)

        #Add check box layout.
        check_box_layout = QtGui.QGridLayout()

        #Add export option check boxes
        self.export_flattened_box = QtGui.QCheckBox('Export Flattened')
        self.export_flattened_box.setToolTip('Flattens layer stacks for export. If OFF all layers of channels will be exported separately')
        self.export_full_patch_bleed_box = QtGui.QCheckBox('Full Patch Bleed')
        self.export_full_patch_bleed_box.setToolTip('Turns edge bleed on/off. Existing edge bleed won''t be removed')
        self.export_small_textures_box = QtGui.QCheckBox('Enable Small Textures')
        self.export_small_textures_box.setToolTip('If ON, patches that have flat colors will be exported at 8x8 pixel resolution')
        if self.bool_:
            self.export_remove_alpha_box = QtGui.QCheckBox('Remove Alpha')
            self.export_remove_alpha_box.setToolTip('If ON, Transparency will be removed from exported UDIMS')

        #Add tick boxes and buttons to bottom layout
        check_box_layout.addWidget(self.export_flattened_box, 0, 0)
        check_box_layout.addWidget(self.export_full_patch_bleed_box, 1, 0)
        check_box_layout.addWidget(self.export_small_textures_box, 1, 1)
        if self.bool_:
            check_box_layout.addWidget(self.export_remove_alpha_box, 1, 2)

        # if dialog is being called in 'flattened' mode:
        if self.dialog_mode == 'flattened':
            self.export_flattened_box.setChecked(True)
        else:
            self.export_flattened_box.setChecked(False)

        self.export_small_textures_box.setChecked(True)
        self.export_full_patch_bleed_box.setChecked(True)
        self.export_remove_alpha_box.setChecked(False)

        options_box_group.setLayout(check_box_layout)

        #Add radio button layout.
        res_box_layout = QtGui.QGridLayout()
        res_label = QtGui.QLabel("Export Resolution:")
        res_label.setToolTip('Allows you do export your Channel non-destructively at a different resolution\nthan it is in your Mari project')

        self.res_full = QtGui.QRadioButton('Full')
        self.res_full.setToolTip('Exports your Channel at 100% resolution')
        self.res_halve = QtGui.QRadioButton('Half')
        self.res_halve.setToolTip('Exports your Channel at 50% resolution')
        self.res_quarter = QtGui.QRadioButton('Quarter')
        self.res_quarter.setToolTip('Exports your Channel at 25% resolution')
        self.res_eighth = QtGui.QRadioButton('Eighth')
        self.res_eighth.setToolTip('Exports your Channel at 12.5% resolution')

        res_box_layout.addWidget(res_label,0,0)
        res_box_layout.addWidget(self.res_full,0,1)
        res_box_layout.addWidget(self.res_halve,0,2)
        res_box_layout.addWidget(self.res_quarter,0,3)
        res_box_layout.addWidget(self.res_eighth,0,4)
        self.res_full.setChecked(True)

        res_box_group.setLayout(res_box_layout)

        #Add widget groups to main layout
        main_layout.addWidget(top_group)
        main_layout.addWidget(modified_box_group)
        main_layout.addWidget(options_box_group)
        main_layout.addWidget(res_box_group)

        #Add check box layout.
        button_layout = QtGui.QHBoxLayout()

        # Add Export, Cancel and Script buttons
        self.ok_btn = QtGui.QPushButton('Export All Patches')
        self.ok_sel_btn = QtGui.QPushButton('Export Selected Patches')
        self.ok_sel_btn.setToolTip('Please note that "Only Modified Textures" Setting is ignored\nand all selected patches will be exported')

        self.cancel_btn = QtGui.QPushButton('Cancel')
        self.script_btn = QtGui.QPushButton('Post Process')
        self.script_btn.setToolTip('Allows you to set up a series of shell commands\nthat should be run on the exported channels')


        self.ok_btn.clicked.connect(self._checkInput)
        self.ok_sel_btn.clicked.connect(self._exportSelectedPatches)
        self.ok_sel_btn.clicked.connect(self._checkInput)

        self.cancel_btn.clicked.connect(self.reject)
        self.script_btn.clicked.connect(self._CommandUI)

        button_layout.addWidget(self.script_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.ok_sel_btn)
        button_layout.addWidget(self.cancel_btn)

        # main_layout.addWidget(button_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        #calling once to cull the object list, whole thing doesn't really make for a snappy interface appearance
        listAllObjects(self.channel_list,currentObjChannels,displayAllObjBox.isChecked())
        self._optionsLoad()
        self._exportEverything()

    def _optionsSave(self):
        """Saves UI Options between sessions."""

        for name, obj in inspect.getmembers(self):

            self.SETTINGS.beginGroup(Settings_Group)
            if isinstance(obj, QtGui.QLineEdit):
                state = None
                if self.dialog_mode == 'flattened':
                    if name is 'template_line_edit':
                        state = obj.text()
                        self.SETTINGS.setValue(name + '_flattened',state)
                else:
                    if name is 'template_line_edit':
                        state = obj.text()
                        self.SETTINGS.setValue(name,state)

            if isinstance(obj, QtGui.QCheckBox):
                state = obj.isChecked()
                self.SETTINGS.setValue(name,state)

            self.SETTINGS.endGroup()

    def _optionsLoad(self):
        """Loads UI Options between sessions."""


        for name, obj in inspect.getmembers(self):
            self.SETTINGS.beginGroup(Settings_Group)

            if isinstance(obj, QtGui.QCheckBox):
                state_string = self.SETTINGS.value(name)
                if name != 'export_flattened_box':
                    if state_string == "true":
                        obj.setChecked(True)
                    if state_string == "false":
                        obj.setChecked(False)

            if isinstance(obj, QtGui.QLineEdit):
                state = None
                if name is 'template_line_edit':
                    if self.dialog_mode == 'flattened':
                        state = unicode(self.SETTINGS.value(name + '_flattened'))
                    else:
                        state = unicode(self.SETTINGS.value(name))
                    if state != 'None':
                        obj.setText(state)

            self.SETTINGS.endGroup()


    #Generate List of Channels for the Channel List
    def populateChannelList(self,channel_list):
        ''' Adds Channels to a Channel List '''
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
        currentObjName = ''
        currentChan = ''
        currentChannelCount = 0
        if mari.current.geo() is not None:
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
                    if mari.current.geo() is not None:
                        currentChan = mari.current.channel()
                    if channel is currentChan:
                        currentChannelRow = channel_list.count()-1

        # Set currently active channel to selected
        if mari.current.geo() is not None:
            channel_list.setCurrentRow(currentChannelRow)

        return channel_list, currentChannelCount


    #Hide parts of interface if export everything is ticked
    def _exportEverything(self):
        _bool = self.export_everything_box.isChecked()
        self.channel_label.setHidden(_bool)
        self.channel_search_icon.setHidden(_bool)
        self.channel_filter_box.setHidden(_bool)
        self.channel_list.setHidden(_bool)
        self.export_label.setHidden(_bool)
        self.export_search_icon.setHidden(_bool)
        self.export_filter_box.setHidden(_bool)
        self.export_list.setHidden(_bool)
        self.add_button.setHidden(_bool)
        self.remove_button.setHidden(_bool)

    #Get the path from existing directory
    def _getPath(self):
        path = QtGui.QFileDialog.getExistingDirectory(None,"Export Path",self.path_line_edit.text())
        if path == "":
            return
        else:
            self._setPath(os.path.abspath(path))

    #Set the path line edit box text to be the path provided
    def _setPath(self, path):
        self.path_line_edit.setText(path)

    #Are you in Export Selected Patches Mode ?
    def _exportSelectedPatches(self):
        global EXPORT_SELECTED
        EXPORT_SELECTED = True


    #Check path and template will work, check if export everything box is ticked if not make sure there are some channels to export
    def _checkInput(self):

        file_types = ['.' + format for format in mari.images.supportedWriteFormats()]
        file_types_str = []
        for format in file_types:
            type_str = format.encode('utf-8')
            file_types_str.append(type_str)

        path_template = self.path_line_edit.text()
        if path_template.endswith(os.sep):
            path_template = path_template[:-1]
        template_template = self.template_line_edit.text()
        full_path = os.path.join(path_template, template_template)
        if not template_template.endswith(tuple(file_types)):
            mari.utils.message("File Extension is not supported: '%s'" %(os.path.split(template_template)[1])+ '\n\nSupported File Extensions: \n'+ str(file_types_str),'Invalid File Extension specified')
            return
        if self.export_everything_box.isChecked():
            pass
        elif len(self.export_list._currentChannels()) == 0:
            mari.utils.message("Please add a channel to export.")
            return

        if not os.path.exists(path_template):
            path_string = str(path_template)
            if '$' in path_string:
                self._optionsSave()
                self.accept()
            else:
                title = 'Create Directories'
                text = 'Folder does not exist "%s".' %(path_template)
                info = 'Create the path?'
                info_dialog = InfoUI(title, text, info)
                info_dialog.exec_()
                info_reply = info_dialog.buttonRole(info_dialog.clickedButton())
                if info_reply is QtGui.QMessageBox.ButtonRole.RejectRole:
                    return
                else:
                    try:
                        os.makedirs(path_template)
                        self._optionsSave()
                        self.accept()
                    except Exception:
                        pass # Assuming that a previous channel already created the path
                        self._optionsSave()
                        self.accept()
        else:
            self._optionsSave()
            self.accept()

    #Get list of channels to export from the export list
    def _getChannelsToExport(self):
        return self.export_list._currentChannels()

    #Get export path and template
    def _getExportPathTemplate(self):
        ''' sample the export template used to generate the file name'''
        path = self.path_line_edit.text()
        template = self.template_line_edit.text()
        if template.startswith('/') or template.startswith('\\'):
            template = template[1:]
        if path.endswith('/') or path.endswith('\\'):
            path = path[:-1]
        return os.path.join(path, template)

    def _resetExportPathTemplate(self):
        ''' reset the path template to whatever is set in the project'''
        if self.dialog_mode == 'flattened':
            original_template = mari.resources.flattenedSequenceTemplate()
        else:
            original_template = mari.resources.sequenceTemplate()

        self.template_line_edit.setText(original_template)

    #Get export everything box is ticked (bool)
    def _getExportEverything(self):
        return self.export_everything_box.isChecked()

    #Get export only modified textures box is ticked (bool)
    def _getExportOnlyModifiedTextures(self):
        return self.export_only_modified_textures_box.isChecked()

    #Get export flattened box is ticked (bool)
    def _getExportFlattened(self):
        return self.export_flattened_box.isChecked()

    #Get export small textures box is ticked (bool)
    def _getExportFullPatchBleed(self):
        return self.export_full_patch_bleed_box.isChecked()

    #Get export small textures box is ticked (bool)
    def _getExportSmallTextures(self):
        if self.export_small_textures_box.isChecked():
            return False
        else:
            return True


    #Get export remove alpha box is ticked (bool)
    def _getExportRemoveAlpha(self):
        if self.bool_:
            return self.export_remove_alpha_box.isChecked()
        else:
            return False

    #Get chosen resolution
    def _getResolution(self):
        if self.res_full.isChecked():
            return 1
        elif self.res_halve.isChecked():
            return 2
        elif self.res_quarter.isChecked():
            return 4
        elif self.res_eighth.isChecked():
            return 8

    #Get Post Processing Checkbox State (bool)
    def _getPostProcess(self):
        return self.run_postprocessing_box.isChecked()

    # launches the UI for the Command Line Tools
    def _CommandUI(self):
        cmd_dialog = PostProcessUI()
        cmd_dialog.exec_()

# ------------------------------------------------------------------------------

class ChannelsToExportList(QtGui.QListWidget):
    """Stores a list of operations to perform."""

    def __init__(self, title="For Export"):
        super(ChannelsToExportList, self).__init__()
        self._title = title
        self.setSelectionMode(self.ExtendedSelection)

    def _currentChannels(self):
        return [self.item(index).data(USER_ROLE) for index in range(self.count())]

    def _addChannels(self, channel_list):
        "Adds an operation from the current selections of channels and directories."
        selected_items = channel_list.selectedItems()
        if selected_items == []:
            mari.utils.message("Please select at least one channel.")
            return

        # Add channels that aren't already added
        current_channels = set(self._currentChannels())
        for item in selected_items:
            channel = item.data(USER_ROLE)
            if channel not in current_channels:
                current_channels.add(channel)
                self.addItem(item.text())
                self.item(self.count() - 1).setData(USER_ROLE, channel)

    def _removeChannels(self):
        "Removes any currently selected operations."
        for item in reversed(self.selectedItems()):     # reverse so indices aren't modified
            index = self.row(item)
            self.takeItem(index)

# ------------------------------------------------------------------------------
def _updateChannelFilter(channel_filter_box, channel_list):
    """For each item in the channel list display, set it to hidden if it doesn't match the filter text."""
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
def _updateExportFilter(export_filter_box, export_list):
    """For each item in the export list display, set it to hidden if it doesn't match the filter text."""
    match_words = export_filter_box.text().lower().split()
    for item_index in range(export_list.count()):
        item = export_list.item(item_index)
        item_text_lower = item.text().lower()
        matches = all([word in item_text_lower for word in match_words])
        item.setHidden(not matches)

# ------------------------------------------------------------------------------
class InfoUI(QtGui.QMessageBox):
    """Show the user information for them to make a decision on whether to procede."""
    def __init__(self, title, text, info=None, details=None, bool_=False, parent=None):
        super(InfoUI, self).__init__(parent)

        # Create info gui
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(QtGui.QMessageBox.Warning)
        if not info == None:
            self.setInformativeText(info)
        if not details == None:
            self.setDetailedText(details)
        if not bool_:
            self.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            self.setDefaultButton(QtGui.QMessageBox.Ok)

# ------------------------------------------------------------------------------

class createResizedChannel(object):
    '''Handles dynamic resizing of Channels for exporting them at lower resolution then they are in mari'''
    def __init__(self, channel,relative_size,parent=None):

        self.ResizedChannel = None

        size_dict = {256:mari.ImageSet.SIZE_256,
                         512:mari.ImageSet.SIZE_512,
                         1024:mari.ImageSet.SIZE_1024,
                         2048:mari.ImageSet.SIZE_2048,
                         4096:mari.ImageSet.SIZE_4096,
                         8192:mari.ImageSet.SIZE_8192,
                         16384:mari.ImageSet.SIZE_16384,
                         32768:mari.ImageSet.SIZE_32768
                        }

        # Current Scene Data
        current_channel = channel
        current_channel_UUID = current_channel.uuid()
        current_geo = channel.geoEntity()
        current_graph = current_geo.nodeGraph()
        nodelist = current_graph.nodeList()
        channel_node = None
        node_id = -1

        # searching for channel node
        # while I could use Channel.ChannelNode to get the corresponding Node I need the
        # Number of the Channel Node in the List of Nodes so going the hard way
        for node in nodelist:
            node_id += 1
            if node.uuid() == current_channel_UUID:
                channel_node = node
                break

        # Saving what is attached to the Channel
        channel_input = channel_node.inputNode('Input')

        # writing a duplicate of the channel node
        channel_node_ls = (nodelist[node_id],)
        stringFromNode = current_graph.nodesToString(channel_node_ls)

        #hooking up to a signal first so I can find the node I am about to create
        # Hopefully this can be removed in a future version of Mari.
        mari.utils.connect(mari.nodes.nodeCreated, setNodeFromSignal)
        current_graph.nodesFromString(stringFromNode)
        mari.utils.disconnect(mari.nodes.nodeCreated,setNodeFromSignal)

        # Finding Channel corresponding to new Channel node
        node_uuid = CHANNEL_NODE.uuid()
        self.ResizedChannel = findChannelFromUUID(node_uuid,current_geo)


        # Resizing new Channel to target resolution dependency
        index_ls = []
        size_var = mari.ImageSet.SIZE_256

        for patch in current_geo.patchList():
            index = patch.uvIndex()
            index_ls = [index,]
            height = self.ResizedChannel.width(index)

            height /= relative_size
            if height < 256:
                height = 256
            if height > 32768:
                height = 32768
            size_var = size_dict[height]

            self.ResizedChannel.resize(size_var,index_ls)

        CHANNEL_NODE.setInputNode('Input',channel_input)


        def getNodeFromSignal(Node):
            ''' Returns a new Node from a signal response,that a new one is created in the Nodegraph '''
            self.ResizedChannel_Node = Node

        def getResizedChannel():
            ''' Returns the Channel Object that was created by the script'''
            return self.ResizedChannel

def setNodeFromSignal(Node):
    global CHANNEL_NODE
    CHANNEL_NODE = Node

def findChannelFromUUID(uuid,geo):
    ''' Returns a channel object based on an input uuid'''
    curGeo = geo
    channelList = curGeo.channelList()

    for channel in channelList:
        if channel.uuid() == uuid:
            global CHANNEL_DUP
            CHANNEL_DUP = channel
            return channel
            break

# ------------------------------------------------------------------------------

def _exportChannels(args_dict):

    global EXPORT_SELECTED

    save_options = mari.Image.DEFAULT_OPTIONS
    if args_dict['full_patch_bleed']:
        save_options = save_options | mari.Image.ENABLE_FULL_PATCH_BLEED
    elif args_dict['small_textures']:
        save_options = save_options | mari.Image.DISABLE_SMALL_UNIFORMS
    elif args_dict['remove_alpha']:
        save_options = save_options | mari.Image.REMOVE_ALPHA


    #Check if export flattened is ticked, if not export unflattened
    path = args_dict['path']

    for channel in args_dict['channels']:
        # only export flattened (aka baking) if the channel requires it:
        single_layer_channel = checkChannelForSingleLayer(channel)

        if args_dict['flattened'] and single_layer_channel == False:
            current_geo = channel.geoEntity()
            channel_to_export = channel
            channel_resolution = args_dict['resolution']
            if channel_resolution == 1:
                channel_to_export = channel
            else:
                createResizedChannel(channel,channel_resolution)
                channel_to_export = CHANNEL_DUP

            uv_index_list = []
            metadata = []
            if args_dict['only_modified_textures']:
                uv_index_list, metadata = _onlyModifiedTextures(channel)
                if len(uv_index_list) == 0:
                    if channel_resolution != 1:
                        current_geo.nodeGraph().removeNode(CHANNEL_NODE)
                    continue

            # if doing any post processing make sure to log all exported files
            if args_dict['post_process']:
                attachImageSignals(current_geo)

            try:

                #  If running in 'ExportSelectedPatches Mode' vs All Images
                if EXPORT_SELECTED:
                    channel_to_export.exportSelectedPatchesFlattened(path, save_options, None)
                else:
                    channel_to_export.exportImagesFlattened(path, save_options, uv_index_list)


                EXPORT_SELECTED = False

                # if doing any post processing detach the previously set signal connection after export and run post process
                if args_dict['post_process']:
                    detachImageSignals(current_geo)
                    if not mari.app.wasProcessingCanceled():
                        postProcessExport()

                # if exporting lower resolution, get rid of temp channel node
                if channel_resolution != 1:
                    current_geo.nodeGraph().removeNode(CHANNEL_NODE)


            except Exception, e:
                mari.utils.message('Failed to export "%s"' %e)
                detachImageSignals(current_geo)
                EXPORT_SELECTED = False
                if channel_resolution != 1:
                    current_geo.nodeGraph().removeNode(CHANNEL_NODE)
                return

            for data in metadata:
                channel.setMetadata(*data)
                channel.setMetadataDisplayName(data[0],str(data[0]) + ' Modified Texture Export')
                channel.setMetadataFlags(data[0],mari.Metadata.METADATA_EDITABLE)
            channel.setMetadata('OnlyModifiedTextures', True)
            channel.setMetadataFlags('OnlyModifiedTextures',mari.Metadata.METADATA_EDITABLE)
            channel.setMetadataEnabled('OnlyModifiedTextures', False)

        else:

                channel_to_export = channel
                channel_resolution = args_dict['resolution']
                if channel_resolution == 1:
                    channel_to_export = channel
                else:
                    createResizedChannel(channel,channel_resolution)
                    channel_to_export = CHANNEL_DUP

                uv_index_list = []
                metadata = []
                if args_dict['only_modified_textures']:
                    uv_index_list, metadata = _onlyModifiedTextures(channel)
                    if len(uv_index_list) == 0:
                        if channel_resolution != 1:
                            current_geo.nodeGraph().removeNode(CHANNEL_NODE)
                        continue

                # if doing any post processing make sure to log all exported files
                if args_dict['post_process']:
                    attachImageSignals(current_geo)


                try:

                    #  If running in 'ExportSelectedPatches Mode' vs All Images
                    if EXPORT_SELECTED:
                        channel_to_export.exportSelectedPatches(path, save_options, None)
                    else:
                        channel_to_export.exportImages(path, save_options, uv_index_list)

                    EXPORT_SELECTED = False

                    # if doing any post processing detach the previously set signal connection after export and run post process
                    if args_dict['post_process']:
                        detachImageSignals(current_geo)
                        if not mari.app.wasProcessingCanceled():
                            postProcessExport()

                    # if exporting lower resolution, get rid of temp channel node
                    if channel_resolution != 1:
                        current_geo.nodeGraph().removeNode(CHANNEL_NODE)


                except Exception, e:
                    mari.utils.message('Failed to export "%s"' %e)
                    detachImageSignals(current_geo)
                    EXPORT_SELECTED = False
                    if channel_resolution != 1:
                        current_geo.nodeGraph().removeNode(CHANNEL_NODE)
                    return
                for data in metadata:
                    channel.setMetadata(*data)
                    channel.setMetadataDisplayName(data[0],str(data[0]) + ' Modified Texture Export')
                    channel.setMetadataFlags(data[0],mari.Metadata.METADATA_EDITABLE)
                channel.setMetadata('OnlyModifiedTextures', True)
                channel.setMetadataFlags('OnlyModifiedTextures',mari.Metadata.METADATA_EDITABLE)
                channel.setMetadataEnabled('OnlyModifiedTextures', False)


    #If successful let the user know
    mari.utils.message("Export Successful")

# ------------------------------------------------------------------------------
def _exportEverything(args_dict):
    """Export everything, all geo and all channels"""

    global EXPORT_SELECTED

    geo_list = mari.geo.list()
    channels = []
    for geo in geo_list:
        channels.extend(geo.channelList())
    save_options = mari.Image.DEFAULT_OPTIONS
    if args_dict['full_patch_bleed']:
        save_options = save_options | mari.Image.ENABLE_FULL_PATCH_BLEED
    elif args_dict['small_textures']:
        save_options = save_options | mari.Image.DISABLE_SMALL_UNIFORMS
    elif args_dict['remove_alpha']:
        save_options = save_options | mari.Image.REMOVE_ALPHA
    #Check if export flattened is ticked, if not export unflattened
    path = args_dict['path']

    for channel in channels:

        # only export flattened (aka baking) if the channel requires it:
        single_layer_channel = checkChannelForSingleLayer(channel)

        if args_dict['flattened'] and single_layer_channel == False:

            current_geo = channel.geoEntity()
            channel_to_export = channel
            channel_resolution = args_dict['resolution']
            if channel_resolution == 1:
                channel_to_export = channel
            else:
                createResizedChannel(channel,channel_resolution)
                channel_to_export = CHANNEL_DUP

            uv_index_list = []
            metadata = []
            if args_dict['only_modified_textures']:
                uv_index_list, metadata = _onlyModifiedTextures(channel)
                if len(uv_index_list) == 0:
                    if channel_resolution != 1:
                        current_geo.nodeGraph().removeNode(CHANNEL_NODE)
                    continue

            # if doing any post processing make sure to log all exported files
            if args_dict['post_process']:
                attachImageSignals(current_geo)

            try:

                #  If running in 'ExportSelectedPatches Mode' vs All Images
                if EXPORT_SELECTED:
                    channel_to_export.exportSelectedPatchesFlattened(path, save_options, None)
                else:
                    channel_to_export.exportImagesFlattened(path, save_options, uv_index_list)

                EXPORT_SELECTED = False

                # if doing any post processing detach the previously set signal connection after export and run post process
                if args_dict['post_process']:
                    detachImageSignals(current_geo)
                    if not mari.app.wasProcessingCanceled():
                        postProcessExport()

                # if exporting lower resolution, get rid of temp channel node
                if channel_resolution != 1:
                    current_geo.nodeGraph().removeNode(CHANNEL_NODE)

            except Exception, e:
                mari.utils.message('Failed to export "%s"' %e)
                detachImageSignals(current_geo)
                EXPORT_SELECTED = False
                if channel_resolution != 1:
                    current_geo.nodeGraph().removeNode(CHANNEL_NODE)
                return
            for data in metadata:
                channel.setMetadata(*data)
                channel.setMetadataDisplayName(data[0],str(data[0]) + ' Modified Texture Export')
                channel.setMetadataFlags(data[0],mari.Metadata.METADATA_EDITABLE)
            channel.setMetadata('OnlyModifiedTextures', True)
            channel.setMetadataFlags('OnlyModifiedTextures',mari.Metadata.METADATA_EDITABLE)
            channel.setMetadataEnabled('OnlyModifiedTextures', False)

        else:
            channel_to_export = channel
            channel_resolution = args_dict['resolution']
            if channel_resolution == 1:
                channel_to_export = channel
            else:
                createResizedChannel(channel,channel_resolution)
                channel_to_export = CHANNEL_DUP

            uv_index_list = []
            metadata = []
            if args_dict['only_modified_textures']:
                uv_index_list, metadata = _onlyModifiedTextures(channel)
                if len(uv_index_list) == 0:
                    continue

            # if doing any post processing make sure to log all exported files
            if args_dict['post_process']:
                attachImageSignals(current_geo)


            try:

                #  If running in 'ExportSelectedPatches Mode' vs All Images
                if EXPORT_SELECTED:
                    channel_to_export.exportSelectedPatches(path, save_options, None)
                else:
                    channel_to_export.exportImages(path, save_options, uv_index_list)

                EXPORT_SELECTED = False

                # if doing any post processing detach the previously set signal connection after export and run post process
                if args_dict['post_process']:
                    detachImageSignals(current_geo)
                    if not mari.app.wasProcessingCanceled():
                        postProcessExport()

                # if exporting lower resolution, get rid of temp channel node
                if channel_resolution != 1:
                    current_geo.nodeGraph().removeNode(CHANNEL_NODE)

            except Exception, e:
                mari.utils.message('Failed to export "%s"' %e)
                detachImageSignals(current_geo)
                EXPORT_SELECTED = False
                if channel_resolution != 1:
                    current_geo.nodeGraph().removeNode(CHANNEL_NODE)
                return
            for data in metadata:
                channel.setMetadata(*data)
                channel.setMetadataDisplayName(data[0],str(data[0]) + ' Modified Texture Export')
                channel.setMetadataFlags(data[0],mari.Metadata.METADATA_EDITABLE)
            channel.setMetadata('OnlyModifiedTextures', True)
            channel.setMetadataFlags('OnlyModifiedTextures',mari.Metadata.METADATA_EDITABLE)
            channel.setMetadataEnabled('OnlyModifiedTextures', False)

    #If successful let the user know
    mari.utils.message("Export Successful")

# ------------------------------------------------------------------------------

def checkChannelForSingleLayer(channel):
    '''Checks if a Channel just consists of a single paint layer'''

    layerList = channel.layerList()

    if len(layerList) > 1:
        return False

    else:
        layer = layerList[0]
        paintableLayer = layer.isPaintableLayer()
        adjustments = layer.hasAdjustmentStack()
        mask = layer.hasMask()
        maskStack = layer.hasMaskStack()
        if paintableLayer and not adjustments and not mask and not maskStack:
            return True
        else:
            return False



# ------------------------------------------------------------------------------

def saveFileListFromExportSignal(summary):

    ''' Saves Filepaths from the ImageExported Signal'''
    print summary

# ------------------------------------------------------------------------------

def exportSelectedChannels(mode):
    """Export selected channels."""
    suitable = _isProjectSuitable()
    if not suitable[0]:
        return

    #Create dialog and execute accordingly
    dialog = ExportSelectedChannelsUI(suitable[1],mode)
    # dialog.uiSettings_load(dialog, settings)
    if dialog.exec_():
        args_dict = {
        'channels' : dialog._getChannelsToExport(),
        'path' : dialog._getExportPathTemplate(),
        'flattened' : dialog._getExportFlattened(),
        'full_patch_bleed' : dialog._getExportFullPatchBleed(),
        'small_textures' : dialog._getExportSmallTextures(),
        'remove_alpha' : dialog._getExportRemoveAlpha(),
        'only_modified_textures' : dialog._getExportOnlyModifiedTextures(),
        'resolution': dialog._getResolution(),
        'post_process': dialog._getPostProcess()
        }
        if dialog._getExportEverything():
            _exportEverything(args_dict)
        else:
            _exportChannels(args_dict)

# ------------------------------------------------------------------------------
def _onlyModifiedTextures(channel):
    """Manage channels so only modified patch images get exported"""
    if channel.hasMetadata('OnlyModifiedTextures'):
        uv_index_list, metadata = _getChangedUvIndexes(channel)
    else:
        uv_index_list, metadata = _setChannelUvIndexes(channel)
    return uv_index_list, metadata

# ------------------------------------------------------------------------------
def _getChangedUvIndexes(channel):
    """Get uv indexes with new hashes"""
    geo = channel.geoEntity()
    all_layers = _getAllLayers(channel.layerList())
    patch_list = geo.patchList()
    uv_index_list = []
    metadata = []
    for patch in patch_list:
        hash_ = _createHash(patch, all_layers,channel)
        try:
            if not hash_ == channel.metadata(str(patch.uvIndex()) ):
                uv_index_list.append(patch.uvIndex())
                metadata.append((str(patch.uvIndex()), hash_))
        except Exception:
                uv_index_list.append(patch.uvIndex())
                metadata.append((str(patch.uvIndex()), hash_))
    return uv_index_list, metadata

# ------------------------------------------------------------------------------
def _setChannelUvIndexes(channel):
    """Set the channel metadata uv index hash"""
    geo = channel.geoEntity()
    all_layers = _getAllLayers(channel.layerList())
    patch_list = geo.patchList()
    uv_index_list = []
    metadata = []
    for patch in patch_list:
        hash_ = _createHash(patch, all_layers, channel)
        uv_index_list.append(patch.uvIndex())
        metadata.append((str(patch.uvIndex()), hash_))
    return uv_index_list, metadata

# ------------------------------------------------------------------------------
def _createHash(patch, all_layers,channel):
    """Create hashes on channel for all layers"""
    hash_ = ''
    index = patch.uvIndex()

    # Checking COLOR and SCALAR Colorspaces
    hash_ += channel.colorspaceConfig().resolveColorspace(mari.ColorspaceConfig.ColorspaceStage.COLORSPACE_STAGE_NATIVE)
    hash_ += channel.colorspaceConfig().resolveColorspace(mari.ColorspaceConfig.ColorspaceStage.COLORSPACE_STAGE_OUTPUT)
    hash_ += channel.colorspaceConfig().resolveColorspace(mari.ColorspaceConfig.ColorspaceStage.COLORSPACE_STAGE_WORKING)

    hash_ += channel.scalarColorspaceConfig().resolveColorspace(mari.ColorspaceConfig.ColorspaceStage.COLORSPACE_STAGE_NATIVE)
    hash_ += channel.scalarColorspaceConfig().resolveColorspace(mari.ColorspaceConfig.ColorspaceStage.COLORSPACE_STAGE_OUTPUT)
    hash_ += channel.scalarColorspaceConfig().resolveColorspace(mari.ColorspaceConfig.ColorspaceStage.COLORSPACE_STAGE_WORKING)

    for layer in all_layers:
        hash_ += _basicLayerData(layer)

        if layer.isAdjustmentLayer():
            for adjustmentParameter in layer.primaryAdjustmentParameters():
                hash_ += str(layer.getPrimaryAdjustmentParameter(adjustmentParameter))
            # If this layer has a secondary adjustment then capture that data as well.
            if layer.hasSecondaryAdjustment():
                for adjustmentParameter in layer.secondaryAdjustmentParameters():
                    hash_ += str(layer.getPrimaryAdjustmentParameter(adjustmentParameter))

        elif layer.isProceduralLayer():
                for proceduralParameter in layer.proceduralParameters():
                    if 'Cache' in proceduralParameter:
                        continue
                    parameterValue = layer.getProceduralParameter(proceduralParameter)
                    if isinstance(parameterValue, mari.Color):
                        hash_ += str(parameterValue.rgba())
                    elif isinstance(parameterValue, mari.LookUpTable):
                        hash_ += parameterValue.controlPointsAsString()
                    else:
                        hash_ += str(parameterValue)

        elif layer.isPaintableLayer():
            hash_ += layer.imageSet().image(index).hash()

        elif layer.hasMask() and not layer.hasMaskStack():
            hash_ += layer.maskImageSet().image(index).hash()

    return _sha256(hash_)

# ------------------------------------------------------------------------------
def _getAllLayers(layer_list):
    """Returns a list of all of the layers in the layer stack, including substacks."""
    return _getMatchingLayers(layer_list, _returnTrue)

# ------------------------------------------------------------------------------
def _returnTrue(*object):
    """Return True for anything passed to this function."""
    return True

# ------------------------------------------------------------------------------
def _getMatchingLayers(layer_list, criterionFn):
    """Returns a list of all of the layers in the stack that match the given criterion function, including substacks."""
    matching = []
    for layer in layer_list:
        if criterionFn(layer):
            matching.append(layer)
        if hasattr(layer, 'layerStack'):
            matching.extend(_getMatchingLayers(layer.layerStack().layerList(), criterionFn))
        if layer.hasMaskStack():
            matching.extend(_getMatchingLayers(layer.maskStack().layerList(), criterionFn))
        if hasattr(layer, 'hasAdjustmentStack') and layer.hasAdjustmentStack():
            matching.extend(_getMatchingLayers(layer.adjustmentStack().layerList(), criterionFn))
        if layer.isChannelLayer():
            matching.extend(_getMatchingLayers(layer.channel().layerList(), criterionFn))

    return matching

# ------------------------------------------------------------------------------
def _basicLayerData(layer):
    """Collect basic layer data common to all types of layers."""
    return str(layer.hash()) + \
    str(layer.blendAmount()) + \
    str(layer.blendMode()) + \
    str(layer.blendModeStr()) + \
    str(layer.isVisible()) + \
    str()

# ------------------------------------------------------------------------------
def _sha256(string):
    """Returns a hash for the given string."""
    sha256 = hashlib.sha256()
    sha256.update(string)
    return sha256.hexdigest()

# ------------------------------------------------------------------------------

class PostProcessUI(QtGui.QDialog):
    """UI to enter Shell Commands that are executed after Channel Export"""
    def __init__(self):
        super(PostProcessUI, self).__init__()

        # Storing Widget Settings between sessions here:
        self.SETTINGS = mari.Settings()

        # Dialog Settings
        # self.setFixedSize(800, 600)
        self.setWindowTitle('Set Post Process Commands')
        # Layouts & Boxes
        window_layout_box = QtGui.QVBoxLayout()
        info_layout_grid = QtGui.QGridLayout()
        command_layout_grid = QtGui.QGridLayout()
        button_layout_box = QtGui.QHBoxLayout()
        info_group_box = QtGui.QGroupBox('Info')
        command_group_box = QtGui.QGroupBox("Commands")

        self.setLayout(window_layout_box)

        # Info Widgets
        self.Descr_Command =  QtGui.QLabel(
"The fields below allow you to specify shell commands or scripts to be executed for each exported channel.\n\
Commands are executed in the order they appear. Only active commands will be executed,\n\
and you will need to turn on the 'Run Post Processing' Checkbox in the Main Dialog\n\n\
You can pass several variables to commands from the Export Tool such as\n\n\
$FILENAME - gets replaced with the Filename (including extension) of each exported File. Available in 'per File' mode only.\n\
$FILENAME_NOEXT - gets replaced with the Filename (without extension) of each exported File. Available in 'per File' mode only.\n\
$FULLPATH - gets replaced with the full path and filename (with extension) of each exported File. Available in 'per File' mode only.\n\
$FULLPATH_NOEXT - gets replaced with the full path and filename (without extension) of each exported File. Available in 'per File' mode only.\n\
$DIRECTORY - gets replaced with the Directory path to the File(s). Folder will include a trailing slash.\n\
$DIRECTORY_NOSLASH - gets replaced with the Directory path to the Files(s). Folder will not include a trailing slash")


        info_layout_grid.addWidget(self.Descr_Command,3,2)
        info_group_box.setLayout(info_layout_grid)


        #Labels
        ExecutableLabel = QtGui.QLabel('Executable')
        ExecutableLabel.setToolTip('The Executable Field should contain the Filename or Path and Filename\nof the application you want to execute')
        ArgumentsLabel = QtGui.QLabel('Arguments')
        ExecutableLabel.setToolTip('The Arguments Field should contain any arguments or\nflags passed to the executable file')


        command_layout_grid.addWidget(ExecutableLabel,1,2)
        command_layout_grid.addWidget(ArgumentsLabel,1,3)

        # Command Line Code Widges
        # Variable Widgets Variable A
        self.Active_CmdA = QtGui.QCheckBox()
        self.Active_CmdA.setToolTip('A shell command to be executed after each channel export')
        self.Exec_CmdA = QtGui.QLineEdit()
        self.Script_CmdA = QtGui.QLineEdit()
        self.Exec_CmdA.setToolTip('The Executable Field should contain the Filename or Path and Filename\nof the application you want to execute')
        self.Script_CmdA.setToolTip('The Arguments Field should contain any arguments or\nflags passed to the executable file')



        radioButtonGrpA = QtGui.QButtonGroup(self)

        self.pChan_A = QtGui.QRadioButton('Per Channel')
        self.pChan_A.setToolTip('The Command will be executed once per exported Channel')
        self.pFile_A = QtGui.QRadioButton('Per File')
        self.pFile_A.setToolTip('The Command will be executed once per exported File')

        radioButtonGrpA.addButton(self.pChan_A)
        radioButtonGrpA.addButton(self.pFile_A)

        command_layout_grid.addWidget(self.Active_CmdA,2,0)
        command_layout_grid.addWidget(self.Exec_CmdA,2,2)
        command_layout_grid.addWidget(self.Script_CmdA,2,3)
        command_layout_grid.addWidget(self.pChan_A,2,4)
        command_layout_grid.addWidget(self.pFile_A,2,5)
        self.pChan_A.setChecked(True)


        # Connections:
        #### Activate Checkbox:
        Active_CmdA_checkbox_connect = lambda: self._disableUIElements(self.Active_CmdA, self.Exec_CmdA, self.Script_CmdA,self.pChan_A,self.pFile_A)
        self.Active_CmdA.clicked.connect(Active_CmdA_checkbox_connect)

        # Variable Widgets Variable B
        self.Active_CmdB = QtGui.QCheckBox()
        self.Active_CmdB.setToolTip('A shell command to be executed after each channel export')
        self.Exec_CmdB = QtGui.QLineEdit()
        self.Script_CmdB = QtGui.QLineEdit()
        self.Exec_CmdB.setToolTip('The Executable Field should contain the Filename or Path and Filename\nof the application you want to execute')
        self.Script_CmdB.setToolTip('The Arguments Field should contain any arguments or\nflags passed to the executable file')


        radioButtonGrpB = QtGui.QButtonGroup(self)

        self.pChan_B = QtGui.QRadioButton('Per Channel')
        self.pChan_B.setToolTip('The Command will be executed once per exported Channel')
        self.pFile_B = QtGui.QRadioButton('Per File')
        self.pFile_B.setToolTip('The Command will be executed once per exported File')

        radioButtonGrpB.addButton(self.pChan_B)
        radioButtonGrpB.addButton(self.pFile_B)

        command_layout_grid.addWidget(self.Active_CmdB,3,0)
        command_layout_grid.addWidget(self.Exec_CmdB,3,2)
        command_layout_grid.addWidget(self.Script_CmdB,3,3)
        command_layout_grid.addWidget(self.pChan_B,3,4)
        command_layout_grid.addWidget(self.pFile_B,3,5)
        self.pChan_B.setChecked(True)

        # Connections:
        #### Activate Checkbox:
        Active_CmdB_checkbox_connect = lambda: self._disableUIElements(self.Active_CmdB,self.Exec_CmdB,self.Script_CmdB,self.pChan_B,self.pFile_B)
        self.Active_CmdB.clicked.connect(Active_CmdB_checkbox_connect)

        # Variable Widgets Variable C
        self.Active_CmdC = QtGui.QCheckBox()
        self.Active_CmdC.setToolTip('A shell command to be executed after each channel export')
        self.Exec_CmdC = QtGui.QLineEdit()
        self.Script_CmdC = QtGui.QLineEdit()
        self.Exec_CmdC.setToolTip('The Executable Field should contain the Filename or Path and Filename\nof the application you want to execute')
        self.Script_CmdC.setToolTip('The Arguments Field should contain any arguments or\nflags passed to the executable file')


        radioButtonGrpC = QtGui.QButtonGroup(self)

        self.pChan_C = QtGui.QRadioButton('Per Channel')
        self.pChan_C.setToolTip('The Command will be executed once per exported Channel')
        self.pFile_C = QtGui.QRadioButton('Per File')
        self.pFile_C.setToolTip('The Command will be executed once per exported File')

        radioButtonGrpC.addButton(self.pChan_C)
        radioButtonGrpC.addButton(self.pFile_C)

        command_layout_grid.addWidget(self.Active_CmdC,4,0)
        command_layout_grid.addWidget(self.Exec_CmdC,4,2)
        command_layout_grid.addWidget(self.Script_CmdC,4,3)
        command_layout_grid.addWidget(self.pChan_C,4,4)
        command_layout_grid.addWidget(self.pFile_C,4,5)
        self.pChan_C.setChecked(True)

        # Connections:
        #### Activate Checkbox:
        Active_CmdC_checkbox_connect = lambda: self._disableUIElements(self.Active_CmdC,self.Exec_CmdC,self.Script_CmdC,self.pChan_C,self.pFile_C)
        self.Active_CmdC.clicked.connect(Active_CmdC_checkbox_connect)

        command_group_box.setLayout(command_layout_grid)

         # APPLY CANCEL BUTTONS
        # Widget OK / Cancel Button
        self.OkBtn = QtGui.QPushButton('Set Commands')
        self.CancelBtn = QtGui.QPushButton('Cancel')
        # Add Apply Cancel Buttons to Button Layout
        button_layout_box.addWidget(self.OkBtn)
        button_layout_box.addWidget(self.CancelBtn)
        # Connections:
        self.OkBtn.clicked.connect(self._setCommand)
        self.CancelBtn.clicked.connect(self.reject)
        # Add sub Layouts to main Window Box Layout
        window_layout_box.addWidget(info_group_box)
        window_layout_box.addWidget(command_group_box)
        window_layout_box.addLayout(button_layout_box)

        # loading user settings from config (last user modifications) and setting base path to per project if exists
        self._restoreCommand()

        # Initialize UI Elements, checks if Variables are set active and if not disables UI elements
        self._disableUIElements(self.Active_CmdA,self.Exec_CmdA,self.Script_CmdA,self.pChan_A,self.pFile_A)
        self._disableUIElements(self.Active_CmdB,self.Exec_CmdB,self.Script_CmdB,self.pChan_B,self.pFile_B)
        self._disableUIElements(self.Active_CmdC,self.Exec_CmdC,self.Script_CmdC,self.pChan_C,self.pFile_C)


    def _setCommand(self):
        '''Writes the set commands to the config file when command dialog confirmed'''

        CmdA_Active = self.Active_CmdA.isChecked()
        CmdB_Active = self.Active_CmdB.isChecked()
        CmdC_Active = self.Active_CmdC.isChecked()

        ExecA = self.Exec_CmdA.text()
        ExecB = self.Exec_CmdB.text()
        ExecC = self.Exec_CmdC.text()

        CmdA = self.Script_CmdA.text()
        CmdB = self.Script_CmdB.text()
        CmdC = self.Script_CmdC.text()

        CmdA_pChannel = self.pChan_A.isChecked()
        CmdA_pFile = self.pFile_A.isChecked()
        CmdB_pChannel = self.pChan_B.isChecked()
        CmdB_pFile = self.pFile_B.isChecked()
        CmdC_pChannel = self.pChan_C.isChecked()
        CmdC_pFile = self.pFile_C.isChecked()

        self.SETTINGS.beginGroup(Settings_Group)

        self.SETTINGS.setValue('PostCommandA_Active',CmdA_Active)
        self.SETTINGS.setValue('PostCommandB_Active',CmdB_Active)
        self.SETTINGS.setValue('PostCommandC_Active',CmdC_Active)

        self.SETTINGS.setValue('PostExecutableA',ExecA)
        self.SETTINGS.setValue('PostExecutableB',ExecB)
        self.SETTINGS.setValue('PostExecutableC',ExecC)

        self.SETTINGS.setValue('PostCommandA',CmdA)
        self.SETTINGS.setValue('PostCommandB',CmdB)
        self.SETTINGS.setValue('PostCommandC',CmdC)

        self.SETTINGS.setValue('PostCommandA_perChannel',CmdA_pChannel)
        self.SETTINGS.setValue('PostCommandA_perFile',CmdA_pFile)
        self.SETTINGS.setValue('PostCommandB_perChannel',CmdB_pChannel)
        self.SETTINGS.setValue('PostCommandB_perFile',CmdB_pFile)
        self.SETTINGS.setValue('PostCommandC_perChannel',CmdC_pChannel)
        self.SETTINGS.setValue('PostCommandC_perFile',CmdC_pFile)

        self.SETTINGS.endGroup()

        self.accept()

    def _restoreCommand(self):
        ''' Reads the commands set previously and restores them when opening the command dialog'''

        self.SETTINGS.beginGroup(Settings_Group)

        self.Exec_CmdA.setText(self.SETTINGS.value('PostExecutableA'))
        self.Exec_CmdB.setText(self.SETTINGS.value('PostExecutableB'))
        self.Exec_CmdC.setText(self.SETTINGS.value('PostExecutableC'))

        self.Script_CmdA.setText(self.SETTINGS.value('PostCommandA'))
        self.Script_CmdB.setText(self.SETTINGS.value('PostCommandB'))
        self.Script_CmdC.setText(self.SETTINGS.value('PostCommandC'))

        self.Active_CmdA.setChecked( (self.SETTINGS.value('PostCommandA_Active')== 'true'))
        self.Active_CmdB.setChecked( (self.SETTINGS.value('PostCommandB_Active')== 'true'))
        self.Active_CmdC.setChecked( (self.SETTINGS.value('PostCommandC_Active')== 'true'))

        self.pFile_A.setChecked( (self.SETTINGS.value('PostCommandA_perFile')== 'true'))
        self.pFile_B.setChecked( (self.SETTINGS.value('PostCommandB_perFile')== 'true'))
        self.pFile_C.setChecked( (self.SETTINGS.value('PostCommandC_perFile')== 'true'))

        self.pChan_A.setChecked( (self.SETTINGS.value('PostCommandA_perChannel')== 'true'))
        self.pChan_B.setChecked( (self.SETTINGS.value('PostCommandB_perChannel')== 'true'))
        self.pChan_C.setChecked( (self.SETTINGS.value('PostCommandC_perChannel')== 'true'))

        self.SETTINGS.endGroup()


    def _disableUIElements(self, obj_active, obj_exec, obj_cmd, obj_pChan, obj_pFile):
        """ Disables UI elements if Actvivate checkbox is off"""

        if not obj_active.isChecked():
            obj_cmd.setReadOnly(True)
            obj_exec.setReadOnly(True)
            obj_exec.setEnabled(False)
            obj_cmd.setEnabled(False)
            obj_pChan.setEnabled(False)
            obj_pFile.setEnabled(False)
        else:
            obj_cmd.setReadOnly(False)
            obj_cmd.setEnabled(True)
            obj_exec.setReadOnly(False)
            obj_exec.setEnabled(True)
            obj_pChan.setEnabled(True)
            obj_pFile.setEnabled(True)


# ------------------------------------------------------------------------------
# The following are used for post processing

def getNewImageset(Set):
    ''' records all exported file paths into a dict for later processing'''
    imageList = Set.imageList()
    global EXPORT_PATH_DICT
    for image in imageList:
        key = image.lastExportPath()
        # key = key.replace('\\',r'\\')
        EXPORT_PATH_DICT[key] = key

def attachImageSignals(geo):
    ''' monitors changes to image sets to catch internal imagesets'''
    mari.utils.connect(geo.imageSetAdded,getNewImageset)
    mari.utils.connect(geo.imageSetMadeCurrent,getNewImageset)

def detachImageSignals(geo):
    ''' disconnects monitoring of  changes to image sets to catch internal imagesets'''
    mari.utils.disconnect(geo.imageSetAdded,getNewImageset)
    mari.utils.disconnect(geo.imageSetMadeCurrent,getNewImageset)


def getPostProcessSettings():
    ''' Reads the set post processing settings and commands'''

    SETTINGS = mari.Settings()

    SETTINGS.beginGroup(Settings_Group)

    CmdA = SETTINGS.value('PostCommandA').encode('unicode-escape')
    CmdB = SETTINGS.value('PostCommandB').encode('unicode-escape')
    CmdC = SETTINGS.value('PostCommandC').encode('unicode-escape')

    ExecA = SETTINGS.value('PostExecutableA').encode('unicode-escape')
    ExecB = SETTINGS.value('PostExecutableB').encode('unicode-escape')
    ExecC = SETTINGS.value('PostExecutableC').encode('unicode-escape')



    Active_CmdA = ( (SETTINGS.value('PostCommandA_Active')== 'true'))
    Active_CmdB = ( (SETTINGS.value('PostCommandB_Active')== 'true'))
    Active_CmdC = ( (SETTINGS.value('PostCommandC_Active')== 'true'))

    pFile_A = ( (SETTINGS.value('PostCommandA_perFile')== 'true'))
    pFile_B = ( (SETTINGS.value('PostCommandB_perFile')== 'true'))
    pFile_C = ( (SETTINGS.value('PostCommandC_perFile')== 'true'))

    pChan_A = ( (SETTINGS.value('PostCommandA_perChannel')== 'true'))
    pChan_B = ( (SETTINGS.value('PostCommandB_perChannel')== 'true'))
    pChan_C = ( (SETTINGS.value('PostCommandC_perChannel')== 'true'))

    SETTINGS.endGroup()

    return ExecA,ExecB,ExecC,CmdA,CmdB,CmdC,Active_CmdA,Active_CmdB,Active_CmdC,pFile_A,pFile_B,pFile_C


def postProcessExport():
    '''Runs any Post Process Commands for an exported Channel'''
    global EXPORT_PATH_DICT

    temp_dict = EXPORT_PATH_DICT
    EXPORT_PATH_DICT = {}

    ExecA,ExecB,ExecC,CmdA,CmdB,CmdC,Active_CmdA,Active_CmdB,Active_CmdC,pFile_A,pFile_B,pFile_C = getPostProcessSettings()

    # COMMANDS ARE RUNNING IN ORDER: COMMAND A FIRST, COMMAND B then COMMAND C
    # This is to ensure Command dependencies work correctly

    # PER CHANNEL MODE:
    # finding the path for use in per channel mode
    for item in temp_dict:
        if not temp_dict[item]:
            pass
        else:
            path,filename = os.path.split(item)
            break


    # ------------- COMMAND A ------------------------

    # Executing COMMAND A - PER CHANNEL
    if Active_CmdA and not pFile_A:
        if not ExecA: #if Executable is empty skip
            pass
        else:
            args = [ExecA]
            if not CmdA: #if arguments are empty skip
                pass
            else:
                CmdA_replace = CmdA.replace('$DIRECTORY_NOSLASH', path)
                CmdA_replace = CmdA_replace.replace('$DIRECTORY', path + os.sep)
                optionsList = CmdA_replace.split()
                for option in optionsList:
                    args.append(option)
            subprocess.Popen(args)

    # Executing COMMAND A - PER FILE
    if pFile_A and Active_CmdA:
        for item in temp_dict:
            if not temp_dict[item]:
                pass
            else:
                path,filename = os.path.split(item)
                filename_noExt = os.path.splitext(filename)[0]

                if Active_CmdA and pFile_A:
                    if not ExecA: #if Executable is empty skip
                        pass
                    else:
                        args = [ExecA]
                        if not CmdA: #if arguments are empty skip
                            pass
                        else:
                            CmdA_replace = CmdA.replace('$DIRECTORY_NOSLASH', path)
                            CmdA_replace = CmdA_replace.replace('$DIRECTORY', path + os.sep)
                            CmdA_replace = CmdA_replace.replace('$FILENAME_NOEXT', filename_noExt)
                            CmdA_replace = CmdA_replace.replace('$FILENAME', filename)
                            CmdA_replace = CmdA_replace.replace('$FULLPATH_NOEXT', path + os.sep + filename_noExt)
                            CmdA_replace = CmdA_replace.replace('$FULLPATH', item)
                            optionsList = CmdA_replace.split()
                            for option in optionsList:
                                args.append(option)
                        subprocess.Popen(args)


    # ------------- COMMAND B ------------------------

    # Executing COMMAND B - PER CHANNEL
    if Active_CmdB and not pFile_B:
        if not ExecB: #if Executable is empty skip
            pass
        else:
            args = [ExecB]
            if not CmdB: #if arguments are empty skip
                pass
            else:
                CmdB_replace = CmdB.replace('$DIRECTORY_NOSLASH', path)
                CmdB_replace = CmdB_replace.replace('$DIRECTORY', path + os.sep)
                optionsList = CmdB_replace.split()
                for option in optionsList:
                    args.append(option)
            subprocess.Popen(args)

    # Executing COMMAND B - PER FILE
    if pFile_B and Active_CmdB:
        for item in temp_dict:
            if not temp_dict[item]:
                pass
            else:
                path,filename = os.path.split(item)
                filename_noExt = os.path.splitext(filename)[0]

                if Active_CmdB and pFile_B:
                    if not ExecB: #if Executable is empty skip
                        pass
                    else:
                        args = [ExecB]
                        if not CmdB: #if arguments are empty skip
                            pass
                        else:
                            CmdB_replace = CmdB.replace('$DIRECTORY_NOSLASH', path)
                            CmdB_replace = CmdB_replace.replace('$DIRECTORY', path + os.sep)
                            CmdA_replace = CmdB_replace.replace('$FILENAME_NOEXT', filename_noExt)
                            CmdB_replace = CmdB_replace.replace('$FILENAME', filename)
                            CmdB_replace = CmdB_replace.replace('$FULLPATH_NOEXT', path + os.sep + filename_noExt)
                            CmdB_replace = CmdB_replace.replace('$FULLPATH', item)
                            optionsList = CmdB_replace.split()
                            for option in optionsList:
                                args.append(option)
                        subprocess.Popen(args)


    # ------------- COMMAND C ------------------------

    # Executing COMMAND C - PER CHANNEL
    if Active_CmdC and not pFile_C:
        if not ExecC: #if Executable is empty skip
            pass
        else:
            args = [ExecC]
            if not CmdC: #if arguments are empty skip
                pass
            else:
                CmdC_replace = CmdC.replace('$DIRECTORY_NOSLASH', path)
                CmdC_replace = CmdC_replace.replace('$DIRECTORY', path + os.sep)
                optionsList = CmdC_replace.split()
                for option in optionsList:
                    args.append(option)
            subprocess.Popen(args)

    # Executing COMMAND C - PER FILE
    if pFile_C and Active_CmdC:
        for item in temp_dict:
            if not temp_dict[item]:
                pass
            else:
                path,filename = os.path.split(item)
                filename_noExt = os.path.splitext(filename)[0]

                if Active_CmdC and pFile_C:
                    if not ExecC: #if Executable is empty skip
                        pass
                    else:
                        args = [ExecC]
                        if not CmdC: #if arguments are empty skip
                            pass
                        else:
                            CmdC_replace = CmdC.replace('$DIRECTORY_NOSLASH', path)
                            CmdC_replace = CmdC_replace.replace('$DIRECTORY', path + os.sep)
                            CmdA_replace = CmdC_replace.replace('$FILENAME_NOEXT', filename_noExt)
                            CmdC_replace = CmdC_replace.replace('$FILENAME', filename)
                            CmdC_replace = CmdC_replace.replace('$FULLPATH_NOEXT', path + os.sep + filename_noExt)
                            CmdC_replace = CmdC_replace.replace('$FULLPATH', item)
                            optionsList = CmdC_replace.split()
                            for option in optionsList:
                                args.append(option)
                        subprocess.Popen(args)


# ------------------------------------------------------------------------------

def _isProjectSuitable():
    """Checks project state."""
    MARI_3_0V1b2_VERSION_NUMBER = 30001202    # see below
    if mari.app.version().number() >= MARI_3_0V1b2_VERSION_NUMBER:

        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False, False

        if mari.app.version().number() >= MARI_3_0V1b2_VERSION_NUMBER:
            return True, True

        return True, False

    else:
        mari.utils.message("You can only run this script in Mari 3.0v1 or newer.")
        return False, False

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    exportSelectedChannels()