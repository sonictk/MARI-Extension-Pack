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
# ------------------------------------------------------------------------------
# Rewritten & Extended by Jens Kafitz, 2015
# ------------------------------------------------------------------------------
# http://www.campi3d.com
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
import inspect


version = "3.0"     #UI VERSION

USER_ROLE = 34          # PySide.Qt.UserRole


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
        middle_group = QtGui.QGroupBox()
        bottom_group = QtGui.QGroupBox()

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
        middle_checkbox_group_layout = QtGui.QHBoxLayout()

        self.export_only_modified_textures_box = QtGui.QCheckBox('Only Modified Textures')
        self.export_only_modified_textures_box.setToolTip('Exports only modified UDIMs. Requires at least one previous export with this tool')
        self.export_only_modified_textures_box.setChecked(False)
        middle_checkbox_group_layout.addWidget(self.export_only_modified_textures_box)
        middle_group.setLayout(middle_checkbox_group_layout)

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

        bottom_group.setLayout(check_box_layout)

        #Add widget groups to main layout
        main_layout.addWidget(top_group)
        main_layout.addWidget(middle_group)
        main_layout.addWidget(bottom_group)

        # Add OK Cancel buttons
        self.button_box = QtGui.QDialogButtonBox()
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.button_box.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self._checkInput)
        self.button_box.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.reject)

        #Add bottom layout to main layout and set main layout to dialog's layout
        main_layout.addWidget(self.button_box)
        self.setLayout(main_layout)

        #calling once to cull the object list, whole thing doesn't really make for a snappy interface appearance
        listAllObjects(self.channel_list,currentObjChannels,displayAllObjBox.isChecked())
        self._optionsLoad()




    def _optionsSave(self):
        """Saves UI Options between sessions."""

        for name, obj in inspect.getmembers(self):

            self.SETTINGS.beginGroup("Export_Selected_Channels_" + version)
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
            self.SETTINGS.beginGroup("Export_Selected_Channels_" + version)

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
def _exportChannels(args_dict):

    save_options = mari.Image.DEFAULT_OPTIONS
    if args_dict['full_patch_bleed']:
        save_options = save_options | mari.Image.ENABLE_FULL_PATCH_BLEED
    elif args_dict['small_textures']:
        save_options = save_options | mari.Image.DISABLE_SMALL_UNIFORMS
    elif args_dict['remove_alpha']:
        save_options = save_options | mari.Image.REMOVE_ALPHA


    #Check if export flattened is ticked, if not export unflattened
    path = args_dict['path']
    if args_dict['flattened']:
        for channel in args_dict['channels']:
            uv_index_list = []
            metadata = []
            if args_dict['only_modified_textures']:
                uv_index_list, metadata = _onlyModifiedTextures(channel)
                if len(uv_index_list) == 0:
                    continue
            try:
                channel.exportImagesFlattened(path, save_options, uv_index_list)
            except Exception, e:
                mari.utils.message('Failed to export "%s"' %e)
                return
            for data in metadata:
                channel.setMetadata(*data)
                channel.setMetadataDisplayName(data[0],str(data[0]) + ' Modified Texture Export')
                channel.setMetadataFlags(data[0],mari.Metadata.METADATA_EDITABLE)
            channel.setMetadata('OnlyModifiedTextures', True)
            channel.setMetadataFlags('OnlyModifiedTextures',mari.Metadata.METADATA_EDITABLE)
            channel.setMetadataEnabled('OnlyModifiedTextures', False)
    else:
        for channel in args_dict['channels']:
            uv_index_list = []
            metadata = []
            if args_dict['only_modified_textures']:
                uv_index_list, metadata = _onlyModifiedTextures(channel)
                if len(uv_index_list) == 0:
                    continue
            try:
                channel.exportImages(path, save_options, uv_index_list)
            except Exception, e:
                mari.utils.message('Failed to export "%s"' %e)
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
    if args_dict['flattened']:
        for channel in channels:
            uv_index_list = []
            metadata = []
            if args_dict['only_modified_textures']:
                uv_index_list, metadata = _onlyModifiedTextures(channel)
                if len(uv_index_list) == 0:
                    continue
            try:
                channel.exportImagesFlattened(path, save_options, uv_index_list)
            except Exception, e:
                mari.utils.message('Failed to export "%s"' %e)
                return
            for data in metadata:
                channel.setMetadata(*data)
                channel.setMetadataDisplayName(data[0],str(data[0]) + ' Modified Texture Export')
                channel.setMetadataFlags(data[0],mari.Metadata.METADATA_EDITABLE)
            channel.setMetadata('OnlyModifiedTextures', True)
            channel.setMetadataFlags('OnlyModifiedTextures',mari.Metadata.METADATA_EDITABLE)
            channel.setMetadataEnabled('OnlyModifiedTextures', False)
    else:
        for channel in channels:
            uv_index_list = []
            metadata = []
            if agrs_dict['only_modified_textures']:
                uv_index_list, metadata = _onlyModifiedTextures(channel)
                if len(uv_index_list) == 0:
                    continue
            try:
                channel.exportImages(path, save_options, uv_index_list)
            except Exception, e:
                mari.utils.message('Failed to export "%s"' %e)
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
        'only_modified_textures' : dialog._getExportOnlyModifiedTextures()
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