# ------------------------------------------------------------------------------
# Export Geometry
# ------------------------------------------------------------------------------
# .Allows you to export your Geometry as OBJs out of MARI
# ------------------------------------------------------------------------------
# Written by Jens Kafitz, 2015
# ------------------------------------------------------------------------------
# www.jenskafitz.com
# ------------------------------------------------------------------------------
# Last Modified: 18 August 2015
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
import mari, os
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
from PySide.QtCore import QSettings
import inspect

version = "3.0"         #UI VERSION

USER_ROLE = 32          # PySide.Qt.UserRole


# ------------------------------------------------------------------------------
def exportGEOs(mode):
    "Export Geometry initialise"

    #Check project is suitable
    if not isProjectSuitable():
            return False

    dialog = exportGEOUI(mode)

    # Dialogs can be run in two modes: Full and Light.
    # Light will only work on the current geo.
    if dialog.exec_():
        if mode == 'light':
            geo = [mari.geo.current()]
        else:
            geo = dialog.geometry_to_copy_widget
        export_path = dialog._getExportPathTemplate()
        path = export_path[0]
        template = export_path[1]
        exportGeo(dialog,mode,geo,path,template)


# ------------------------------------------------------------------------------
def exportGeo(UI, ui_mode,q_geo_list,path,template):
    "Export the Geometry"

    try:
        if ui_mode == 'light':
            geo_list = q_geo_list
        else:
            geo_list = q_geo_list.currentGeometry()

        if len(geo_list) == 0:
                mari.utils.message('Please add at least one Object','No Objects added to Export List')
                return False

        else:

                deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
                deactivateViewportToggle.trigger()

                UI.close()

                #Export selected geo
                for geo in geo_list:
                        geoVisibility = geo.isVisible()
                        if geoVisibility is False:
                            geo.setVisibility(True)
                        mari.geo.setCurrent(geo)
                        geo_name = geo.name()

                        # Checking Path for Variables
                        # If any $ Variables are found all folder creation will happen automatically
                        # This is different from cases where a user specifies an explicit subfolder in the path line
                        # If an explicit subfolder is named a dialog will come up asking to create that folder
                        # That part is handled as part of the InfoUI() call previously
                        if template.startswith('/') or template.startswith('\\'):
                            template = template[1:]
                        if path.endswith('/') or path.endswith('\\'):
                            path = path[:-1]
                        export_path_template = os.path.join(path, template)
                        export_path_template = export_path_template.replace('$ENTITY', geo_name)
                        if not os.path.exists(os.path.split(export_path_template)[0]):
                                os.makedirs(os.path.split(export_path_template)[0])

                        if UI.SubdBox.isChecked():
                            geo.setSubdivisionLevel(0)
                        geo.save(export_path_template)
                        if geoVisibility is False:
                            geo.setVisibility(False)
                        print 'Geometry Export to ' + export_path_template + ' successful'




        deactivateViewportToggle.trigger()
        mari.utils.message("Export Geometry Complete.",'Export Successful')

    except Exception,e:
            print(e)
            mari.utils.message("Export Geometry failed to complete.")
            deactivateViewportToggle.trigger()

# ------------------------------------------------------------------------------
class exportGEOUI(QtGui.QDialog):
    "Export Geoemtry."
    def __init__(self, mode, parent=None):
        super(exportGEOUI, self).__init__(parent)

        # Storing Widget Settings between sessions here:
        self.SETTINGS = mari.Settings()

        #Create main dialog, add main layout and set title
        self._optionsLoad()
        self.setWindowTitle("Export Geometry")
        if mode == 'light':
            self.setFixedSize(700, 160)
        main_layout = QtGui.QVBoxLayout()
        self.setLayout(main_layout)


        if mode != "light":

            #Create layout for middle section
            centre_layout = QtGui.QHBoxLayout()

            #Create geometry layout, label, and widget. Finally populate.
            geo_layout = QtGui.QVBoxLayout()
            geo_header_layout = QtGui.QHBoxLayout()
            geo_label = QtGui.QLabel("<strong>Geometry</strong>")
            geo_list = QtGui.QListWidget()
            geo_list.setSelectionMode(geo_list.ExtendedSelection)

            filter_box = QtGui.QLineEdit()
            mari.utils.connect(filter_box.textEdited, lambda: self.updateFilter(filter_box, geo_list))

            geo_header_layout.addWidget(geo_label)
            geo_header_layout.addStretch()
            geo_search_icon = QtGui.QLabel()
            search_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + os.sep + 'Lookup.png')
            geo_search_icon.setPixmap(search_pixmap)
            geo_header_layout.addWidget(geo_search_icon)
            geo_header_layout.addWidget(filter_box)

            geo = mari.geo.current()
            for geo_item in mari.geo.list():
                    geo_list.addItem(geo_item.name())
                    geo_list.item(geo_list.count() - 1).setData(USER_ROLE, geo_item)
                    if geo_item is geo:
                            currentGeoRow = geo_list.count()-1

            # Set currently active channel to selected
            # Catch errors if a locator is selected
            if geo is not None:
                geo_list.setCurrentRow(currentGeoRow)

            geo_layout.addLayout(geo_header_layout)
            geo_layout.addWidget(geo_list)

            #Create middle button section
            middle_button_layout = QtGui.QVBoxLayout()
            add_button = QtGui.QPushButton("+")
            remove_button = QtGui.QPushButton("-")
            middle_button_layout.addStretch()
            middle_button_layout.addWidget(add_button)
            middle_button_layout.addWidget(remove_button)
            middle_button_layout.addStretch()

            #Add wrapped QtGui.QListWidget with custom functions
            geometry_to_copy_layout = QtGui.QVBoxLayout()
            geometry_to_copy_label = QtGui.QLabel("<strong>Geometry to Export</strong>")
            self.geometry_to_copy_widget = GeoToExportList()
            geometry_to_copy_layout.addWidget(geometry_to_copy_label)
            geometry_to_copy_layout.addWidget(self.geometry_to_copy_widget)

            #Hook up add/remove buttons
            remove_button.clicked.connect(self.geometry_to_copy_widget.removeGeometry)
            add_button.clicked.connect(lambda: self.geometry_to_copy_widget.addGeometry(geo_list))

            #Add widgets to centre layout
            centre_layout.addLayout(geo_layout)
            centre_layout.addLayout(middle_button_layout)
            centre_layout.addLayout(geometry_to_copy_layout)

            #Add centre layout to main layout
            main_layout.addLayout(centre_layout)

        #Add path layout
        path_layout = QtGui.QGridLayout()

        #Get mari default path and template
        self.path = os.path.abspath(mari.resources.path(mari.resources.DEFAULT_GEO))
        self.template = '$ENTITY.obj'

        #Add path line input and button, also set text to Mari default path and template
        path_label = QtGui.QLabel('Path:')
        self.path_line_edit = QtGui.QLineEdit()
        self.path_line_edit.setToolTip('Define your export base path here.\nWhen a $ Variable is found all subfolders will be \ncreated automatically without user prompts\nSupported Variables are: \n\n$ENTITY - Entity is a placeholder for your object name\n')

        path_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) +  os.sep + 'ExportImages.png')
        icon = QtGui.QIcon(path_pixmap)
        path_button = QtGui.QPushButton(icon, "")
        path_button.setToolTip('Browse for Export Folder')
        path_button.clicked.connect(self._getPath)
        self.path_line_edit.setText(self.path)

        #Add path line input and button to middle layout
        path_layout.addWidget(path_label,0,0)
        path_layout.addWidget(self.path_line_edit,0,1)
        path_layout.addWidget(path_button,0,2)

        #Add Template line input & Reset Template Button
        template_label = QtGui.QLabel('Template:')
        self.template_line_edit = QtGui.QLineEdit()
        self.template_line_edit.setToolTip('Use this section to define an export template. \nYou can use Variables to create subfolders here as well. \nSupported Variables are: \n\n$ENTITY - Entity is a placeholder for your object name\n')
        self.template_line_edit.setText(self.template)

        template_reset_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + os.sep + 'Reset.png')
        template_reset_icon = QtGui.QIcon(template_reset_pixmap)
        self.template_reset_button = QtGui.QPushButton(template_reset_icon, "")
        self.template_reset_button.setToolTip('Reset Export Template to Project Default')
        self.template_reset_button.clicked.connect(self._resetExportPathTemplate)


        #Add template line input and file format dropdown to middle layout
        path_layout.addWidget(template_label,0,3)
        path_layout.addWidget(self.template_line_edit,0,4)
        path_layout.addWidget(self.template_reset_button,0,5)

        #Add browse lines & template to main layout
        main_layout.addLayout(path_layout)


        # Add Checkbox Layout & group box
        chkbox_layout = QtGui.QHBoxLayout()
        checkbox_group_box = QtGui.QGroupBox("Options")

        #Add Display all Objects check box
        self.SubdBox = QtGui.QCheckBox('Always save without Subdivision (level0)')
        self.SubdBox.setToolTip('If ON, all objects are exported at level 0 Subdivision, regardless of their current subd state')
        self.SubdBox.setChecked(True)
        chkbox_layout.addWidget(self.SubdBox)
        checkbox_group_box.setLayout(chkbox_layout)

        main_layout.addWidget(checkbox_group_box)


        #Add bottom layout.
        bottom_layout = QtGui.QHBoxLayout()

        #Add OK Cancel buttons layout, buttons and add
        main_ok_button = QtGui.QPushButton("OK")
        main_cancel_button = QtGui.QPushButton("Cancel")
        main_ok_button.clicked.connect(self._checkInput)

        main_cancel_button.clicked.connect(self.reject)
        bottom_layout.addWidget(main_ok_button)
        bottom_layout.addWidget(main_cancel_button)

        #Add browse lines to main layout
        main_layout.addLayout(bottom_layout)

        self._optionsLoad()


    # Save the UI Settings (File emplate)
    def _optionsSave(self):
            """Saves UI Options between sessions."""

            for name, obj in inspect.getmembers(self):
                    self.SETTINGS.beginGroup("Export_Geometry_" + version)
                    if isinstance(obj, QtGui.QLineEdit):
                            state = None
                            if name is 'template_line_edit':
                                    state = obj.text()
                                    self.SETTINGS.setValue(name,state)

                    self.SETTINGS.endGroup()

    # Load the UI Settings (File emplate)
    def _optionsLoad(self):
            """Loads UI Options between sessions."""

            for name, obj in inspect.getmembers(self):
                    self.SETTINGS.beginGroup("Export_Geometry_" + version)

                    if isinstance(obj, QtGui.QLineEdit):
                            state = None
                            if name is 'template_line_edit':
                                    state = unicode(self.SETTINGS.value(name))
                                    if state != 'None':
                                            obj.setText(state)

                    self.SETTINGS.endGroup()

    #Get the path from existing directory
    def _getPath(self):
            """Returns Path from Browsing"""
            path = QtGui.QFileDialog.getExistingDirectory(None,"Export Path",self.path_line_edit.text())
            if path == "":
                    return
            else:
                    self._setPath(os.path.abspath(path))

    #Set the path line edit box text to be the path provided
    def _setPath(self, path):
            """Sets the path selected from browsing to the Path field"""
            self.path_line_edit.setText(path)


    def _checkInput(self):
            """checks the user input for path and templates"""
            file_types = ['.obj','.OBJ']
            file_types_str = ['.obj','.OBJ']

            path_template = self.path_line_edit.text()
            if path_template.endswith(os.sep):
                    path_template = path_template[:-1]
            template_template = self.template_line_edit.text()
            full_path = os.path.join(path_template, template_template)
            if not template_template.endswith(tuple(file_types)):
                    mari.utils.message("File Extension is not supported: '%s'" %(os.path.split(template_template)[1])+ '\n\nSupported File Extensions: \n'+ str(file_types_str),'Invalid File Extension specified')
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



    #Get export path and template
    def _getExportPathTemplate(self):
            ''' sample the export template used to generate the file name'''
            self.path = self.path_line_edit.text()
            self.template = self.template_line_edit.text()
            return self.path,self.template

    #Reset the Export File Template to what is set on project
    def _resetExportPathTemplate(self):
            ''' reset the path template to whatever is set in the project'''
            original_template = '$ENTITY.obj'
            self.template_line_edit.setText(original_template)


    def updateFilter(self,filter_box, geo_list):
            "For each item in the geo list display, set it to hidden if it doesn't match the filter text."
            match_words = filter_box.text().lower().split()
            for item_index in range(geo_list.count()):
                    item = geo_list.item(item_index)
                    item_text_lower = item.text().lower()
                    matches = all([word in item_text_lower for word in match_words])
                    item.setHidden(not matches)


# ------------------------------------------------------------------------------
class GeoToExportList(QtGui.QListWidget):
        "Stores a list of operations to perform."

        def __init__(self, title="For Export"):
                super(GeoToExportList, self).__init__()
                self._title = title
                self.setSelectionMode(self.ExtendedSelection)

        def currentGeometry(self):
                return [self.item(index).data(USER_ROLE) for index in range(self.count())]

        def addGeometry(self, geo_list):
                "Adds an operation from the current selections of geometry and directories."
                selected_items = geo_list.selectedItems()
                if selected_items == []:
                        mari.utils.message("Please select at least one object.")
                        return
                else:

                        # Add geometry that aren't already added
                        current_geometry = set(self.currentGeometry())
                        for item in selected_items:
                                geo = item.data(USER_ROLE)
                                if geo not in current_geometry:
                                        current_geometry.add(geo)
                                        self.addItem(geo.name())
                                        self.item(self.count() - 1).setData(USER_ROLE, geo)

        def removeGeometry(self):
                "Removes any currently selected operations."
                for item in reversed(self.selectedItems()):     # reverse so indices aren't modified
                        index = self.row(item)
                        self.takeItem(index)

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

def isProjectSuitable():
        "Checks project state and Mari version."
        MARI_3_0V1_VERSION_NUMBER = 30001202    # see below
        if mari.app.version().number() >= MARI_3_0V1_VERSION_NUMBER:

                if mari.projects.current() is None:
                        mari.utils.message("Please open a project before running.","No Project Open")
                        return False

                return True

        else:
                mari.utils.message("You can only run this script in Mari 3.0v1 or newer.")
                return False

# ------------------------------------------------------------------------------
if __name__ == "__main__":
        exportGEOs('full')