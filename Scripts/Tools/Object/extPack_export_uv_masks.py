# ------------------------------------------------------------------------------
# Export UV Masks
# ------------------------------------------------------------------------------
# Allows the user export all UV Masks of one or multiple Geos.
# Option can be found under the Objects Menu
# ------------------------------------------------------------------------------
# Written by Jorel Latraille, 2014
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

import mari, os
import PySide.QtGui as QtGui

version = "0.05"

USER_ROLE = 32          # PySide.Qt.UserRole


g_eum_window = None
g_eum_cancelled = False
directory = ''
g_file_types = ['.' + format for format in mari.images.supportedWriteFormats()]
list.sort(g_file_types)

# ------------------------------------------------------------------------------
def exportUVMasks():
    "Export UV masks initialise"
    global directory
    
    #Check project is suitable
    if not isProjectSuitable():
        return False        
        
    #Get directory to export to
    directory = mari.utils.misc.getExistingDirectory(parent=None, caption='Export UV Masks', dir='')
    if directory == "":
        return False
        
    showUI()    

# ------------------------------------------------------------------------------    
def exportMasks(g_eum_window, q_geo_list, file_type_combo):
    "Export the masks"
    geo_list = q_geo_list.currentGeometry()
    file_type = file_type_combo.currentText()

    if len(geo_list) == 0:
        return False
        
    g_eum_window.reject()
     
    #Export selected geo UV masks 
    for geo in geo_list:
        mari.geo.setCurrent(geo)
        geo_name = geo.name()
        patch_list = geo.patchList()
        patch_udims = []
        for patch in patch_list:
            patch_udims.append(int(patch.name()))
            patch.setSelected(False)
        for patch in patch_udims:
            uv_mask = mari.actions.get('/Mari/Geometry/Patches/UV Mask to Image Manager')
            index = patch - 1001
            geo.patch(index).setSelected(True)
            uv_mask.trigger()
            geo.patch(index).setSelected(False)        
            image_list = mari.images.list()
            mari.images.saveImages(image_list[-1:], os.path.join(directory, "%s.mask.%d.%s" %(geo_name, patch, file_type)))
            index = len(image_list) - 1
            image_list[index].close()
    mari.utils.message("Export UV Masks Complete.")

# ------------------------------------------------------------------------------
def showUI():
    "Copy paint from one or more patches to other patches, for all layers and geometry."
    #Create UI
    
    #Check project state
    if not isProjectSuitable():
        return False
    
    #Create main dialog, add main layout and set title
    global g_eum_window
    g_eum_window = QtGui.QDialog()
    eum_layout = QtGui.QVBoxLayout()
    g_eum_window.setLayout(eum_layout)
    g_eum_window.setWindowTitle("Export UV Masks")
    
    #Create layout for middle section
    centre_layout = QtGui.QHBoxLayout()
    
    #Create geometry layout, label, and widget. Finally populate.
    geo_layout = QtGui.QVBoxLayout()
    geo_header_layout = QtGui.QHBoxLayout()
    geo_label = QtGui.QLabel("<strong>Geometry</strong>")
    geo_list = QtGui.QListWidget()
    geo_list.setSelectionMode(geo_list.ExtendedSelection)
    
    filter_box = QtGui.QLineEdit()
    mari.utils.connect(filter_box.textEdited, lambda: updateFilter(filter_box, geo_list))
    
    geo_header_layout.addWidget(geo_label)
    geo_header_layout.addStretch()
    geo_search_icon = QtGui.QLabel()
    search_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + '/Lookup.png')
    geo_search_icon.setPixmap(search_pixmap)
    geo_header_layout.addWidget(geo_search_icon)
    geo_header_layout.addWidget(filter_box)
    
    geo = mari.geo.current()
    for geo in mari.geo.list():
        geo_list.addItem(geo.name())
        geo_list.item(geo_list.count() - 1).setData(USER_ROLE, geo)
    
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
    geometry_to_copy_label = QtGui.QLabel("<strong>Geometry to export UV masks from.</strong>")
    geometry_to_copy_widget = GeoToExportList()
    geometry_to_copy_layout.addWidget(geometry_to_copy_label)
    geometry_to_copy_layout.addWidget(geometry_to_copy_widget)
    
    #Hook up add/remove buttons
    remove_button.clicked.connect(geometry_to_copy_widget.removeGeometry)
    add_button.clicked.connect(lambda: geometry_to_copy_widget.addGeometry(geo_list))

    #Add widgets to centre layout
    centre_layout.addLayout(geo_layout)
    centre_layout.addLayout(middle_button_layout)
    centre_layout.addLayout(geometry_to_copy_layout)

    #Add centre layout to main layout
    eum_layout.addLayout(centre_layout)

    #Add bottom layout.
    bottom_layout = QtGui.QHBoxLayout()
    
    #Add file type options
    file_type_combo_text = QtGui.QLabel('File Types:')
    file_type_combo = QtGui.QComboBox()
    for file_type in g_file_types:
        file_type_combo.addItem(file_type)
    file_type_combo.setCurrentIndex(file_type_combo.findText('.tif'))
    
    bottom_layout.addWidget(file_type_combo_text)
    bottom_layout.addWidget(file_type_combo)
    bottom_layout.addStretch()
    
    #Add OK Cancel buttons layout, buttons and add
    main_ok_button = QtGui.QPushButton("OK")
    main_cancel_button = QtGui.QPushButton("Cancel")
    main_ok_button.clicked.connect(lambda: exportMasks(g_eum_window, geometry_to_copy_widget, file_type_combo))
    main_cancel_button.clicked.connect(g_eum_window.reject)    
    bottom_layout.addWidget(main_ok_button)
    bottom_layout.addWidget(main_cancel_button)
    
    #Add browse lines to main layout
    eum_layout.addLayout(bottom_layout)
    
    # Display
    g_eum_window.show()
    
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
def updateFilter(filter_box, geo_list):
    "For each item in the geo list display, set it to hidden if it doesn't match the filter text."
    match_words = filter_box.text().lower().split()
    for item_index in range(geo_list.count()):
        item = geo_list.item(item_index)
        item_text_lower = item.text().lower()
        matches = all([word in item_text_lower for word in match_words])
        item.setHidden(not matches)

   
# ------------------------------------------------------------------------------
def isProjectSuitable():
    "Checks project state and Mari version."
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:
        
        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False

        return True
        
    else:
        mari.utils.message("You can only run this script in Mari 2.6v3 or newer.")
        return False

# ------------------------------------------------------------------------------    
if __name__ == "__main__":
    exportUVMasks()