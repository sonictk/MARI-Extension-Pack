# ------------------------------------------------------------------------------
# Set Project Paths
# ------------------------------------------------------------------------------
# SetProjectPaths will allow you to configure Default paths and File Templates
# for your project (Texture Export+Import Paths, Image Manager Default Paths etc.)
# You can use variables such as $BASE in a pathfield to set paths relative to a
# main project path
# ------------------------------------------------------------------------------
# Written by Jens Kafitz, 2015
# ------------------------------------------------------------------------------
# http://www.jenskafitz.com
# ------------------------------------------------------------------------------
# Last Modified: 16 August 2015
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
import json

JSON_FILE = 'ProjectPaths_ExtPack_3v0.json'
version = '3.0' #UI Version

#  TO DO
#  Move save StartupTemplate out of class
#  Hook StartupTemplate save to ProjectLoad Signal

class setProjectPathUI(QtGui.QDialog):
    """GUI to set your Project Paths"""
    def __init__(self):
        super(setProjectPathUI, self).__init__()

        # Storing Widget Settings between sessions here:
        self.SETTINGS = mari.Settings()
        # Saving initial Path Settings at Startup of Dialog

        # Dialog Settings
        # self.setFixedSize(800, 600)
        self.setWindowTitle('Set Project Defaults')
        # Layouts & Boxes
        window_layout_box = QtGui.QVBoxLayout()
        group_layout_box = QtGui.QVBoxLayout()
        base_layout_grid = QtGui.QGridLayout()
        variable_layout_grid = QtGui.QGridLayout()
        misc_layout_grid = QtGui.QGridLayout()
        file_layout_grid = QtGui.QGridLayout()
        button_layout_box = QtGui.QHBoxLayout()
        base_group_box = QtGui.QGroupBox('Project Base Path (optional)')
        asset_group_box = QtGui.QGroupBox("Asset Paths")
        misc_group_box = QtGui.QGroupBox("Misc Paths")
        file_group_box = QtGui.QGroupBox("File Templates")
        self.setLayout(window_layout_box)
        # VARIABLE FIELDS
        self.Descr =  QtGui.QLabel("Default Paths:")
        path_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) +  os.sep + 'ExportImages.png')
        path_icon = QtGui.QIcon(path_pixmap)
        templateReset_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + os.sep + 'Reset.png')
        templateReset_icon = QtGui.QIcon(templateReset_pixmap)
        # Base Widgets
        self.Descr_BaseInfo =  QtGui.QLabel(
        "Base Path can be used to set paths relative to it by using the Variable $BASE in fields below\n \
        e.g: $BASE\ReferenceImages, $BASE\Model, $BASE\Textures etc.")
        self.Descr_Base = QtGui.QLabel("Base Path")
        self.Path_Base = QtGui.QLineEdit()
        self.Path_Base.setToolTip(
        'Enter a base path to be used in fields with a $BASE Variable.\nFolders do not need to exist.\nIf you enter a Foldername that does not exist, you have the choice to create it.')
        self.path_button_Base = QtGui.QPushButton(path_icon, "")
        self.path_button_Base.setToolTip('Browse for Folder')
        base_layout_grid.addWidget(self.Descr_Base,2,0)
        base_layout_grid.addWidget(self.Path_Base,2,2)
        base_layout_grid.addWidget(self.path_button_Base,2,3)
        base_layout_grid.addWidget(self.Descr_BaseInfo,3,2)
        # Connections:
        #### Browse Button:
        Browse_Base_button_connect = lambda: self._browseForDirectory(self.Path_Base)
        self.path_button_Base.clicked.connect(Browse_Base_button_connect)
        base_group_box.setLayout(base_layout_grid)

        # Asset Widges
        # Variable Widgets Variable A
        self.Active_VarA = QtGui.QCheckBox("TEXTURE MAPS (Import)")
        self.Active_VarA.setToolTip('The default Path that should be used when Importing Textures.\nBy toggling this off the path field will be reset to whatever path is currently set')
        self.Path_VarA = QtGui.QLineEdit()
        self.Path_VarA.setToolTip('Path to be used for Variable.\nIf the path contains folders that do not exist, they can be created for you.\nUse a variable $BASE to set paths relative to Base Path')
        self.path_button_VarA = QtGui.QPushButton(path_icon, "")
        self.path_button_VarA.setToolTip('Browse for Folder')
        self.templateReset_VarA = QtGui.QPushButton(templateReset_icon, "")
        self.templateReset_VarA.setToolTip('Reset to Project Default\nThis will reset the path field to the path that was active on project open\nbut BEFORE the projects original setProjectPath settings were restored.\n\nIf in your pipeline you have automatic ways of setting the paths\nthis will restore to their state')
        self.link_VarA = QtGui.QCheckBox('Relative to Base')
        self.link_VarA.setCheckable(True)
        self.link_VarA.setToolTip('With RelativeToBase ON, the entered Path will be scanned for similarities to your Base Path.\nIf parts are identical they will be replaced with a $BASE variable.\nIf your Path contains a $BASE Variable and you uncheck RelativeToBase the Path will be fully resolved')
        variable_layout_grid.addWidget(self.Active_VarA,2,0)
        variable_layout_grid.addWidget(self.Path_VarA,2,2)
        variable_layout_grid.addWidget(self.path_button_VarA,2,3)
        variable_layout_grid.addWidget(self.templateReset_VarA,2,4)
        variable_layout_grid.addWidget(self.link_VarA,2,5)
        # Default Path
        self._setProjectTemplate(self.Path_VarA,'Tex_Import')
        # Connections:
        #### Activate Checkbox:
        Active_VarA_checkbox_connect = lambda: self._disableUIElements(self.Active_VarA,self.Path_VarA,self.path_button_VarA,self.templateReset_VarA,self.link_VarA)
        self.Active_VarA.clicked.connect(Active_VarA_checkbox_connect)
        #### Reset Button:
        Reset_VarA_button_connect = lambda: self._setProjectTemplate(self.Path_VarA,'Tex_Import')
        self.templateReset_VarA.clicked.connect(Reset_VarA_button_connect)
        #### Browse Button:
        Browse_VarA_button_connect = lambda: self._browseForDirectory(self.Path_VarA)
        self.path_button_VarA.clicked.connect(Browse_VarA_button_connect)
        #### Path Field:
        Path_VarA_changed_connect = lambda: self._checkPathForBase(self.Path_VarA,self.link_VarA)
        self.Path_VarA.textChanged.connect(Path_VarA_changed_connect)
        #### Base Link Field:
        Link_VarA_checkbox_connect = lambda: self._resolveBASEVariable(self.Path_Base,self.Path_VarA,self.link_VarA)
        self.link_VarA.clicked.connect(Link_VarA_checkbox_connect)
        # Variable Widgets Variable C
        self.Active_VarC = QtGui.QCheckBox("TEXTURE MAPS (Export):")
        self.Active_VarC.setToolTip('The default Path that should be used when Exporting Textures.\nBy toggling this off the path field will be reset to whatever path is currently set')
        self.Path_VarC = QtGui.QLineEdit()
        self.Path_VarC.setToolTip('Path to be used for Variable.\nIf the path contains folders that do not exist, they can be created for you.\nUse a variable $BASE to set paths relative to Base Path')
        self.path_button_VarC = QtGui.QPushButton(path_icon, "")
        self.path_button_VarC.setToolTip('Browse for Folder')
        self.templateReset_VarC = QtGui.QPushButton(templateReset_icon, "")
        self.templateReset_VarC.setToolTip('Reset to Project Default\nThis will reset the path field to the path that was active on project open\nbut BEFORE the projects original setProjectPath settings were restored.\n\nIf in your pipeline you have automatic ways of setting the paths\nthis will restore to their state')
        self.link_VarC = QtGui.QCheckBox('Relative to Base')
        self.link_VarC.setToolTip('With RelativeToBase ON, the entered Path will be scanned for similarities to your Base Path.\nIf parts are identical they will be replaced with a $BASE variable.\nIf your Path contains a $BASE Variable and you uncheck RelativeToBase the Path will be fully resolved')
        variable_layout_grid.addWidget(self.Active_VarC,3,0)
        variable_layout_grid.addWidget(self.Path_VarC,3,2)
        variable_layout_grid.addWidget(self.path_button_VarC,3,3)
        variable_layout_grid.addWidget(self.templateReset_VarC,3,4)
        variable_layout_grid.addWidget(self.link_VarC,3,5)
        # Default Path
        self._setProjectTemplate(self.Path_VarC,'Tex_Export')
        # Connections:
        #### Activate Checkbox:
        Active_VarC_checkbox_connect = lambda: self._disableUIElements(self.Active_VarC,self.Path_VarC,self.path_button_VarC,self.templateReset_VarC,self.link_VarC)
        self.Active_VarC.clicked.connect(Active_VarC_checkbox_connect)
        #### Reset Button:
        Reset_VarC_button_connect = lambda: self._setProjectTemplate(self.Path_VarC,'Tex_Export')
        self.templateReset_VarC.clicked.connect(Reset_VarC_button_connect)
        #### Browse Button:
        Browse_VarC_button_connect = lambda: self._browseForDirectory(self.Path_VarC)
        self.path_button_VarC.clicked.connect(Browse_VarC_button_connect)
        #### Path Field:
        Path_VarC_changed_connect = lambda: self._checkPathForBase(self.Path_VarC,self.link_VarC)
        self.Path_VarC.textChanged.connect(Path_VarC_changed_connect)
        #### Base Link Field:
        Link_VarC_checkbox_connect = lambda: self._resolveBASEVariable(self.Path_Base,self.Path_VarC,self.link_VarC)
        self.link_VarC.clicked.connect(Link_VarC_checkbox_connect)
        # Variable Widgets Variable D
        self.Active_VarD = QtGui.QCheckBox("GEOMETRY (Import/Export):")
        self.Active_VarD.setToolTip('The default Path that should be used when Importing/Exporting Objects.\nBy toggling this off the path field will be reset to whatever path is currently set')
        self.Path_VarD = QtGui.QLineEdit()
        self.Path_VarD.setToolTip('Path to be used for Variable.\nIf the path contains folders that do not exist, they can be created for you.\nUse a variable $BASE to set paths relative to Base Path')
        self.path_button_VarD = QtGui.QPushButton(path_icon, "")
        self.path_button_VarD.setToolTip('Browse for Folder')
        self.templateReset_VarD = QtGui.QPushButton(templateReset_icon, "")
        self.templateReset_VarD.setToolTip('Reset to Project Default\nThis will reset the path field to the path that was active on project open\nbut BEFORE the projects original setProjectPath settings were restored.\n\nIf in your pipeline you have automatic ways of setting the paths\nthis will restore to their state')
        self.link_VarD = QtGui.QCheckBox('Relative to Base')
        self.link_VarD.setToolTip('With RelativeToBase ON, the entered Path will be scanned for similarities to your Base Path.\nIf parts are identical they will be replaced with a $BASE variable.\nIf your Path contains a $BASE Variable and you uncheck RelativeToBase the Path will be fully resolved')
        variable_layout_grid.addWidget(self.Active_VarD,4,0)
        variable_layout_grid.addWidget(self.Path_VarD,4,2)
        variable_layout_grid.addWidget(self.path_button_VarD,4,3)
        variable_layout_grid.addWidget(self.templateReset_VarD,4,4)
        variable_layout_grid.addWidget(self.link_VarD,4,5)
        # Default Path
        self._setProjectTemplate(self.Path_VarD,'Geo')
        # Connections:
        #### Activate Checkbox:
        Active_VarD_checkbox_connect = lambda: self._disableUIElements(self.Active_VarD,self.Path_VarD,self.path_button_VarD,self.templateReset_VarD,self.link_VarD)
        self.Active_VarD.clicked.connect(Active_VarD_checkbox_connect)
        #### Reset Button:
        Reset_VarD_button_connect = lambda: self._setProjectTemplate(self.Path_VarD,'Geo')
        self.templateReset_VarD.clicked.connect(Reset_VarD_button_connect)
        #### Browse Button:
        Browse_VarD_button_connect = lambda: self._browseForDirectory(self.Path_VarD)
        self.path_button_VarD.clicked.connect(Browse_VarD_button_connect)
        #### Path Field:
        Path_VarD_changed_connect = lambda: self._checkPathForBase(self.Path_VarD,self.link_VarD)
        self.Path_VarD.textChanged.connect(Path_VarD_changed_connect)
        #### Base Link Field:
        Link_VarD_checkbox_connect = lambda: self._resolveBASEVariable(self.Path_Base,self.Path_VarD,self.link_VarD)
        self.link_VarD.clicked.connect(Link_VarD_checkbox_connect)
        # Variable Widgets Variable E
        self.Active_VarE = QtGui.QCheckBox("IMAGE MANAGER (Import/Export):")
        self.Active_VarE.setToolTip('The default Path that should be used when Importing or Exporting from the Image Manager.\nBy toggling this off the path field will be reset to whatever path is currently set')
        self.Path_VarE = QtGui.QLineEdit()
        self.Path_VarE.setToolTip('Path to be used for Variable.\nIf the path contains folders that do not exist, they can be created for you.\nUse a variable $BASE to set paths relative to Base Path')
        self.path_button_VarE = QtGui.QPushButton(path_icon, "")
        self.path_button_VarE.setToolTip('Browse for Folder')
        self.templateReset_VarE = QtGui.QPushButton(templateReset_icon, "")
        self.templateReset_VarE.setToolTip('Reset to Project Default\nThis will reset the path field to the path that was active on project open\nbut BEFORE the projects original setProjectPath settings were restored.\n\nIf in your pipeline you have automatic ways of setting the paths\nthis will restore to their state')
        self.link_VarE = QtGui.QCheckBox('Relative to Base')
        self.link_VarE.setToolTip('With RelativeToBase ON, the entered Path will be scanned for similarities to your Base Path.\nIf parts are identical they will be replaced with a $BASE variable.\nIf your Path contains a $BASE Variable and you uncheck RelativeToBase the Path will be fully resolved')
        variable_layout_grid.addWidget(self.Active_VarE,5,0)
        variable_layout_grid.addWidget(self.Path_VarE,5,2)
        variable_layout_grid.addWidget(self.path_button_VarE,5,3)
        variable_layout_grid.addWidget(self.templateReset_VarE,5,4)
        variable_layout_grid.addWidget(self.link_VarE,5,5)
        # Default Path
        self._setProjectTemplate(self.Path_VarE,'Image')
        # Connections:
        #### Activate Checkbox:
        Active_VarE_checkbox_connect = lambda: self._disableUIElements(self.Active_VarE,self.Path_VarE,self.path_button_VarE,self.templateReset_VarE,self.link_VarE)
        self.Active_VarE.clicked.connect(Active_VarE_checkbox_connect)
        #### Reset Button:
        Reset_VarE_button_connect = lambda: self._setProjectTemplate(self.Path_VarE,'Image')
        self.templateReset_VarE.clicked.connect(Reset_VarE_button_connect)
        #### Browse Button:
        Browse_VarE_button_connect = lambda: self._browseForDirectory(self.Path_VarE)
        self.path_button_VarE.clicked.connect(Browse_VarE_button_connect)
        #### Path Field:
        Path_VarE_changed_connect = lambda: self._checkPathForBase(self.Path_VarE,self.link_VarE)
        self.Path_VarE.textChanged.connect(Path_VarE_changed_connect)
        #### Base Link Field:
        Link_VarE_checkbox_connect = lambda: self._resolveBASEVariable(self.Path_Base,self.Path_VarE,self.link_VarE)
        self.link_VarE.clicked.connect(Link_VarE_checkbox_connect)
        # Variable Widgets Variable F
        self.Active_VarF = QtGui.QCheckBox("RENDERS/TURNTABLES (Export):")
        self.Active_VarF.setToolTip('The default Path that should be used when doing Screenshots & Turntables.\nBy toggling this off the path field will be reset to whatever path is currently set')
        self.Path_VarF = QtGui.QLineEdit()
        self.Path_VarF.setToolTip('Path to be used for Variable.\nIf the path contains folders that do not exist, they can be created for you.\nUse a variable $BASE to set paths relative to Base Path')
        self.path_button_VarF = QtGui.QPushButton(path_icon, "")
        self.path_button_VarF.setToolTip('Browse for Folder')
        self.templateReset_VarF = QtGui.QPushButton(templateReset_icon, "")
        self.templateReset_VarF.setToolTip('Reset to Project Default\nThis will reset the path field to the path that was active on project open\nbut BEFORE the projects original setProjectPath settings were restored.\n\nIf in your pipeline you have automatic ways of setting the paths\nthis will restore to their state')
        self.link_VarF = QtGui.QCheckBox('Relative to Base')
        self.link_VarF.setToolTip('With RelativeToBase ON, the entered Path will be scanned for similarities to your Base Path.\nIf parts are identical they will be replaced with a $BASE variable.\nIf your Path contains a $BASE Variable and you uncheck RelativeToBase the Path will be fully resolved')
        variable_layout_grid.addWidget(self.Active_VarF,6,0)
        variable_layout_grid.addWidget(self.Path_VarF,6,2)
        variable_layout_grid.addWidget(self.path_button_VarF,6,3)
        variable_layout_grid.addWidget(self.templateReset_VarF,6,4)
        variable_layout_grid.addWidget(self.link_VarF,6,5)
        # Default Path
        self._setProjectTemplate(self.Path_VarF,'Render')
        # Connections:
        #### Activate Checkbox:
        Active_VarF_checkbox_connect = lambda: self._disableUIElements(self.Active_VarF,self.Path_VarF,self.path_button_VarF,self.templateReset_VarF,self.link_VarF)
        self.Active_VarF.clicked.connect(Active_VarF_checkbox_connect)
        #### Reset Button:
        Reset_VarF_button_connect = lambda: self._setProjectTemplate(self.Path_VarF,'Render')
        self.templateReset_VarF.clicked.connect(Reset_VarF_button_connect)
        #### Browse Button:
        Browse_VarF_button_connect = lambda: self._browseForDirectory(self.Path_VarF)
        self.path_button_VarF.clicked.connect(Browse_VarF_button_connect)
        #### Path Field:
        Path_VarF_changed_connect = lambda: self._checkPathForBase(self.Path_VarF,self.link_VarF)
        self.Path_VarF.textChanged.connect(Path_VarF_changed_connect)
        #### Base Link Field:
        Link_VarF_checkbox_connect = lambda: self._resolveBASEVariable(self.Path_Base,self.Path_VarF,self.link_VarF)
        self.link_VarF.clicked.connect(Link_VarF_checkbox_connect)
        # Variable Widgets Variable G
        self.Active_VarG = QtGui.QCheckBox("ARCHIVE (Import/Export):")
        self.Active_VarG.setToolTip('The default Path that should be used when loading or saving an Archive.\nBy toggling this off the path field will be reset to whatever path is currently set')
        self.Path_VarG = QtGui.QLineEdit()
        self.Path_VarG.setToolTip('Path to be used for Variable.\nIf the path contains folders that do not exist, they can be created for you.\nUse a variable $BASE to set paths relative to Base Path')
        self.path_button_VarG = QtGui.QPushButton(path_icon, "")
        self.path_button_VarG.setToolTip('Browse for Folder')
        self.templateReset_VarG = QtGui.QPushButton(templateReset_icon, "")
        self.templateReset_VarG.setToolTip('Reset to Project Default\nThis will reset the path field to the path that was active on project open\nbut BEFORE the projects original setProjectPath settings were restored.\n\nIf in your pipeline you have automatic ways of setting the paths\nthis will restore to their state')
        self.link_VarG = QtGui.QCheckBox('Relative to Base')
        self.link_VarG.setToolTip('With RelativeToBase ON, the entered Path will be scanned for similarities to your Base Path.\nIf parts are identical they will be replaced with a $BASE variable.\nIf your Path contains a $BASE Variable and you uncheck RelativeToBase the Path will be fully resolved')
        variable_layout_grid.addWidget(self.Active_VarG,7,0)
        variable_layout_grid.addWidget(self.Path_VarG,7,2)
        variable_layout_grid.addWidget(self.path_button_VarG,7,3)
        variable_layout_grid.addWidget(self.templateReset_VarG,7,4)
        variable_layout_grid.addWidget(self.link_VarG,7,5)
        # Default Path
        self._setProjectTemplate(self.Path_VarG,'Archive')
        # Connections:
        #### Activate Checkbox:
        Active_VarG_checkbox_connect = lambda: self._disableUIElements(self.Active_VarG,self.Path_VarG,self.path_button_VarG,self.templateReset_VarG,self.link_VarG)
        self.Active_VarG.clicked.connect(Active_VarG_checkbox_connect)
        #### Reset Button:
        Reset_VarG_button_connect = lambda: self._setProjectTemplate(self.Path_VarG,'Archive')
        self.templateReset_VarG.clicked.connect(Reset_VarG_button_connect)
        #### Browse Button:
        Browse_VarG_button_connect = lambda: self._browseForDirectory(self.Path_VarG)
        self.path_button_VarG.clicked.connect(Browse_VarG_button_connect)
        #### Path Field:
        Path_VarG_changed_connect = lambda: self._checkPathForBase(self.Path_VarG,self.link_VarG)
        self.Path_VarG.textChanged.connect(Path_VarG_changed_connect)
        #### Base Link Field:
        Link_VarG_checkbox_connect = lambda: self._resolveBASEVariable(self.Path_Base,self.Path_VarG,self.link_VarG)
        self.link_VarG.clicked.connect(Link_VarG_checkbox_connect)
        asset_group_box.setLayout(variable_layout_grid)
        # MISC Widgets
        # Variable Widgets Variable H
        self.Active_VarH = QtGui.QCheckBox("SHELVES (Import/Export):")
        self.Active_VarH.setToolTip('The default Path that should be used when loading or saving Shelves.\nBy toggling this off the path field will be reset to whatever path is currently set')
        self.Path_VarH = QtGui.QLineEdit()
        self.Path_VarH.setToolTip('Path to be used for Variable.\nIf the path contains folders that do not exist, they can be created for you.\nUse a variable $BASE to set paths relative to Base Path')
        self.path_button_VarH = QtGui.QPushButton(path_icon, "")
        self.path_button_VarH.setToolTip('Browse for Folder')
        self.templateReset_VarH = QtGui.QPushButton(templateReset_icon, "")
        self.templateReset_VarH.setToolTip('Reset to Project Default\nThis will reset the path field to the path that was active on project open\nbut BEFORE the projects original setProjectPath settings were restored.\n\nIf in your pipeline you have automatic ways of setting the paths\nthis will restore to their state')
        self.link_VarH = QtGui.QCheckBox('Relative to Base')
        self.link_VarH.setToolTip('With RelativeToBase ON, the entered Path will be scanned for similarities to your Base Path.\nIf parts are identical they will be replaced with a $BASE variable.\nIf your Path contains a $BASE Variable and you uncheck RelativeToBase the Path will be fully resolved')
        misc_layout_grid.addWidget(self.Active_VarH,8,0)
        misc_layout_grid.addWidget(self.Path_VarH,8,2)
        misc_layout_grid.addWidget(self.path_button_VarH,8,3)
        misc_layout_grid.addWidget(self.templateReset_VarH,8,4)
        misc_layout_grid.addWidget(self.link_VarH,8,5)
        # Default Path
        self._setProjectTemplate(self.Path_VarH,'Shelf')
        # Connections:
        #### Activate Checkbox:
        Active_VarH_checkbox_connect = lambda: self._disableUIElements(self.Active_VarH,self.Path_VarH,self.path_button_VarH,self.templateReset_VarH,self.link_VarH)
        self.Active_VarH.clicked.connect(Active_VarH_checkbox_connect)
        #### Reset Button:
        Reset_VarH_button_connect = lambda: self._setProjectTemplate(self.Path_VarH,'Shelf')
        self.templateReset_VarH.clicked.connect(Reset_VarH_button_connect)
        #### Browse Button:
        Browse_VarH_button_connect = lambda: self._browseForDirectory(self.Path_VarH)
        self.path_button_VarH.clicked.connect(Browse_VarH_button_connect)
        #### Path Field:
        Path_VarH_changed_connect = lambda: self._checkPathForBase(self.Path_VarH,self.link_VarH)
        self.Path_VarH.textChanged.connect(Path_VarH_changed_connect)
        #### Base Link Field:
        Link_VarH_checkbox_connect = lambda: self._resolveBASEVariable(self.Path_Base,self.Path_VarH,self.link_VarH)
        self.link_VarH.clicked.connect(Link_VarH_checkbox_connect)
        # Variable Widgets Variable I
        self.Active_VarI = QtGui.QCheckBox("CAM/PROJECTOR (Import/Export):")
        self.Active_VarI.setToolTip('The default Path that should be used when Importing or Eporting Cameras or Projectors.\nBy toggling this off the path field will be reset to whatever path is currently set')
        self.Path_VarI = QtGui.QLineEdit()
        self.Path_VarI.setToolTip('Path to be used for Variable.\nIf the path contains folders that do not exist, they can be created for you.\nUse a variable $BASE to set paths relative to Base Path')
        self.path_button_VarI = QtGui.QPushButton(path_icon, "")
        self.path_button_VarI.setToolTip('Browse for Folder')
        self.templateReset_VarI = QtGui.QPushButton(templateReset_icon, "")
        self.templateReset_VarI.setToolTip('Reset to Project Default\nThis will reset the path field to the path that was active on project open\nbut BEFORE the projects original setProjectPath settings were restored.\n\nIf in your pipeline you have automatic ways of setting the paths\nthis will restore to their state')
        self.link_VarI = QtGui.QCheckBox('Relative to Base')
        self.link_VarI.setToolTip('With RelativeToBase ON, the entered Path will be scanned for similarities to your Base Path.\nIf parts are identical they will be replaced with a $BASE variable.\nIf your Path contains a $BASE Variable and you uncheck RelativeToBase the Path will be fully resolved')
        misc_layout_grid.addWidget(self.Active_VarI,9,0)
        misc_layout_grid.addWidget(self.Path_VarI,9,2)
        misc_layout_grid.addWidget(self.path_button_VarI,9,3)
        misc_layout_grid.addWidget(self.templateReset_VarI,9,4)
        misc_layout_grid.addWidget(self.link_VarI,9,5)
        # Default Path
        self._setProjectTemplate(self.Path_VarI,'Camera')
        # Connections:
        #### Activate Checkbox:
        Active_VarI_checkbox_connect = lambda: self._disableUIElements(self.Active_VarI,self.Path_VarI,self.path_button_VarI,self.templateReset_VarI,self.link_VarI)
        self.Active_VarI.clicked.connect(Active_VarI_checkbox_connect)
        #### Reset Button:
        Reset_VarI_button_connect = lambda: self._setProjectTemplate(self.Path_VarI,'Camera')
        self.templateReset_VarI.clicked.connect(Reset_VarI_button_connect)
        #### Browse Button:
        Browse_VarI_button_connect = lambda: self._browseForDirectory(self.Path_VarI)
        self.path_button_VarI.clicked.connect(Browse_VarI_button_connect)
        #### Path Field:
        Path_VarI_changed_connect = lambda: self._checkPathForBase(self.Path_VarI,self.link_VarI)
        self.Path_VarI.textChanged.connect(Path_VarI_changed_connect)
        #### Base Link Field:
        Link_VarI_checkbox_connect = lambda: self._resolveBASEVariable(self.Path_Base,self.Path_VarI,self.link_VarI)
        self.link_VarI.clicked.connect(Link_VarI_checkbox_connect)
        misc_group_box.setLayout(misc_layout_grid)
        # File Template Widgets
        # Variable Widgets Variable J
        self.Active_VarJ = QtGui.QCheckBox("Texture Flattened:")
        self.Active_VarJ.setToolTip('The default file template that should be used for flattened UDIM sequences\nIt is possible to specify subfolders here.\nSupported Variables are: \n\n$ENTITY\n$CHANNEL\n$LAYER\n$UDIM\n$FRAME\n')
        self.Path_VarJ = QtGui.QLineEdit()
        self.Path_VarJ.setToolTip('The default file template that should be used for flattened UDIM sequences\nIt is possible to specify subfolders here.\nSupported Variables are: \n\n$ENTITY\n$CHANNEL\n$LAYER\n$UDIM\n$FRAME\n')
        self.templateReset_VarJ = QtGui.QPushButton(templateReset_icon, "")
        self.templateReset_VarJ.setToolTip('Reset to Project Default\nThis will reset the path field to the path that was active on project open\nbut BEFORE the projects original setProjectPath settings were restored.\n\nIf in your pipeline you have automatic ways of setting the paths\nthis will restore to their state')
        file_layout_grid.addWidget(self.Active_VarJ,9,0)
        file_layout_grid.addWidget(self.Path_VarJ,9,1)
        file_layout_grid.addWidget(self.templateReset_VarJ,9,2)
        # Default Template
        self._setProjectTemplate(self.Path_VarJ,'Sequence_Flat')
        # Connections:
        #### Activate Checkbox:
        Active_VarJ_checkbox_connect = lambda: self._disableUIElements(self.Active_VarJ,self.Path_VarJ,None,self.templateReset_VarJ,None)
        self.Active_VarJ.clicked.connect(Active_VarJ_checkbox_connect)
        #### Reset Button:
        Reset_VarJ_button_connect = lambda: self._setProjectTemplate(self.Path_VarJ,'Sequence_Flat')
        self.templateReset_VarJ.clicked.connect(Reset_VarJ_button_connect)
        # Variable Widgets Variable K
        self.Active_VarK = QtGui.QCheckBox("Texture:")
        self.Active_VarK.setToolTip('The default file template that should be used for UDIM (non-flattened) sequences\nIt is possible to specify subfolders here.\nSupported Variables are: \n\n$ENTITY\n$CHANNEL\n$LAYER\n$UDIM\n$FRAME\n')
        self.Path_VarK = QtGui.QLineEdit()
        self.Path_VarK.setToolTip('The default file template that should be used for UDIM (non-flattened) sequences\nIt is possible to specify subfolders here.\nSupported Variables are: \n\n$ENTITY\n$CHANNEL\n$LAYER\n$UDIM\n$FRAME\n')
        self.templateReset_VarK = QtGui.QPushButton(templateReset_icon, "")
        self.templateReset_VarK.setToolTip('Reset to Project Default\nThis will reset the path field to the path that was active on project open\nbut BEFORE the projects original setProjectPath settings were restored.\n\nIf in your pipeline you have automatic ways of setting the paths\nthis will restore to their state')
        file_layout_grid.addWidget(self.Active_VarK,9,3)
        file_layout_grid.addWidget(self.Path_VarK,9,4)
        file_layout_grid.addWidget(self.templateReset_VarK,9,5)
        # Default Template
        self._setProjectTemplate(self.Path_VarK,'Sequence')
        # Connections:
        #### Activate Checkbox:
        Active_VarK_checkbox_connect = lambda: self._disableUIElements(self.Active_VarK,self.Path_VarK,None,self.templateReset_VarK,None)
        self.Active_VarK.clicked.connect(Active_VarK_checkbox_connect)
        #### Reset Button:
        Reset_VarK_button_connect = lambda: self._setProjectTemplate(self.Path_VarK,'Sequence')
        self.templateReset_VarK.clicked.connect(Reset_VarK_button_connect)
        # Variable Widgets Variable L
        self.Active_VarL = QtGui.QCheckBox("PTEX Flattened:")
        self.Active_VarL.setToolTip('The default file template that should be used for flattened PTEX\nIt is possible to specify subfolders here.\nSupported Variables are: \n\n$ENTITY\n$CHANNEL\n$LAYER\n$UDIM\n$FRAME\n')
        self.Path_VarL = QtGui.QLineEdit()
        self.Path_VarL.setToolTip('The default file template that should be used for flattened PTEX\nIt is possible to specify subfolders here.\nSupported Variables are: \n\n$ENTITY\n$CHANNEL\n$LAYER\n$UDIM\n$FRAME\n')
        self.templateReset_VarL = QtGui.QPushButton(templateReset_icon, "")
        self.templateReset_VarL.setToolTip('Reset to Project Default\nThis will reset the path field to the path that was active on project open\nbut BEFORE the projects original setProjectPath settings were restored.\n\nIf in your pipeline you have automatic ways of setting the paths\nthis will restore to their state')
        file_layout_grid.addWidget(self.Active_VarL,10,0)
        file_layout_grid.addWidget(self.Path_VarL,10,1)
        file_layout_grid.addWidget(self.templateReset_VarL,10,2)
        # Default Template
        self._setProjectTemplate(self.Path_VarL,'PTEXSequence_Flat')
        # Connections:
        #### Activate Checkbox:
        Active_VarL_checkbox_connect = lambda: self._disableUIElements(self.Active_VarL,self.Path_VarL,None,self.templateReset_VarL,None)
        self.Active_VarL.clicked.connect(Active_VarL_checkbox_connect)
        #### Reset Button:
        Reset_VarL_button_connect = lambda: self._setProjectTemplate(self.Path_VarL,'PTEXSequence_Flat')
        self.templateReset_VarL.clicked.connect(Reset_VarL_button_connect)
        # Variable Widgets Variable M
        self.Active_VarM = QtGui.QCheckBox("PTEX:")
        self.Active_VarM.setToolTip('The default file template that should be used for PTEX (non-flattened) sequences\nIt is possible to specify subfolders here.\nSupported Variables are: \n\n$ENTITY\n$CHANNEL\n$LAYER\n$UDIM\n$FRAME\n')
        self.Path_VarM = QtGui.QLineEdit()
        self.Path_VarM.setToolTip('The default file template that should be used for PTEX (non-flattened) sequences\nIt is possible to specify subfolders here.\nSupported Variables are: \n\n$ENTITY\n$CHANNEL\n$LAYER\n$UDIM\n$FRAME\n')
        self.templateReset_VarM = QtGui.QPushButton(templateReset_icon, "")
        self.templateReset_VarM.setToolTip('Reset to Project Default\nThis will reset the path field to the path that was active on project open\nbut BEFORE the projects original setProjectPath settings were restored.\n\nIf in your pipeline you have automatic ways of setting the paths\nthis will restore to their state')
        file_layout_grid.addWidget(self.Active_VarM,10,3)
        file_layout_grid.addWidget(self.Path_VarM,10,4)
        file_layout_grid.addWidget(self.templateReset_VarM,10,5)
        # Default Template
        self._setProjectTemplate(self.Path_VarM,'PTEXSequence')
        # Connections:
        #### Activate Checkbox:
        Active_VarM_checkbox_connect = lambda: self._disableUIElements(self.Active_VarM,self.Path_VarM,None,self.templateReset_VarM,None)
        self.Active_VarM.clicked.connect(Active_VarM_checkbox_connect)
        #### Reset Button:
        Reset_VarM_button_connect = lambda: self._setProjectTemplate(self.Path_VarM,'PTEXSequence')
        self.templateReset_VarM.clicked.connect(Reset_VarM_button_connect)
        file_group_box.setLayout(file_layout_grid)
        # APPLY CANCEL BUTTONS
        # Widget OK / Cancel Button
        self.OkBtn = QtGui.QPushButton('Set Project')
        self.CancelBtn = QtGui.QPushButton('Cancel')
        # Add Apply Cancel Buttons to Button Layout
        button_layout_box.addWidget(self.OkBtn)
        button_layout_box.addWidget(self.CancelBtn)
        # Connections:
        self.OkBtn.clicked.connect(self._checkInput)
        self.CancelBtn.clicked.connect(self.reject)
        # Add sub Layouts to main Window Box Layout
        window_layout_box.addWidget(base_group_box)
        window_layout_box.addWidget(asset_group_box)
        window_layout_box.addWidget(misc_group_box)
        window_layout_box.addWidget(file_group_box)
        window_layout_box.addLayout(button_layout_box)

        # loading user settings from config (last user modifications) and setting base path to per project if exists
        self._userSettingsLoad()
        self._perProjectBasePathLoad(self.Path_Base)

        # Initialize UI Elements, checks if Variables are set active and if not disables UI elements
        self._disableUIElements(self.Active_VarA,self.Path_VarA,self.path_button_VarA,self.templateReset_VarA,self.link_VarA)
        self._disableUIElements(self.Active_VarC,self.Path_VarC,self.path_button_VarC,self.templateReset_VarC,self.link_VarC)
        self._disableUIElements(self.Active_VarD,self.Path_VarD,self.path_button_VarD,self.templateReset_VarD,self.link_VarD)
        self._disableUIElements(self.Active_VarE,self.Path_VarE,self.path_button_VarE,self.templateReset_VarE,self.link_VarE)
        self._disableUIElements(self.Active_VarF,self.Path_VarF,self.path_button_VarF,self.templateReset_VarF,self.link_VarF)
        self._disableUIElements(self.Active_VarG,self.Path_VarG,self.path_button_VarG,self.templateReset_VarG,self.link_VarG)
        self._disableUIElements(self.Active_VarH,self.Path_VarH,self.path_button_VarH,self.templateReset_VarH,self.link_VarH)
        self._disableUIElements(self.Active_VarI,self.Path_VarI,self.path_button_VarI,self.templateReset_VarI,self.link_VarI)
        self._disableUIElements(self.Active_VarJ,self.Path_VarJ,None,self.templateReset_VarJ,None)
        self._disableUIElements(self.Active_VarK,self.Path_VarK,None,self.templateReset_VarK,None)
        self._disableUIElements(self.Active_VarL,self.Path_VarL,None,self.templateReset_VarL,None)
        self._disableUIElements(self.Active_VarM,self.Path_VarM,None,self.templateReset_VarM,None)

    def _getProjectTemplate(self,pathVariable):
        """ Returns the default path that was set at project launch, saved in extPack json file of project"""

        state_string = readXMLValue('Default',pathVariable)
        return state_string


    def _setProjectTemplate(self, obj, pathVariable):
        """ Gets the default path variable and sets the QLineEditField in Main UI to Value"""

        path = self._getProjectTemplate(pathVariable)
        obj.setText(path)


    def _setCurrentTemplateToField(self,obj,pathVariable):
        """
        Sets the currently active variable path to a text field
        This is not the same as the project Template but gives whatever
        is currently set - user edited or not
        """

        current_template_dict = {'Project'    : mari.projects.current().uuid(),
                                 'Tex_Export' : mari.resources.path(mari.resources.DEFAULT_EXPORT),
                                 'Tex_Import' : mari.resources.path(mari.resources.DEFAULT_IMPORT),
                                 'Archive' : mari.resources.path(mari.resources.DEFAULT_ARCHIVE),
                                 'Camera' : mari.resources.path(mari.resources.DEFAULT_CAMERA),
                                 'Geo' : mari.resources.path(mari.resources.DEFAULT_GEO),
                                 'Image' : mari.resources.path(mari.resources.DEFAULT_IMAGE),
                                 'Shelf' : mari.resources.path(mari.resources.DEFAULT_SHELF),
                                 'Render' : mari.resources.path(mari.resources.DEFAULT_RENDER),
                                 'Sequence' : mari.resources.sequenceTemplate(),
                                 'Sequence_Flat' : mari.resources.flattenedSequenceTemplate(),
                                 'PTEXSequence' : mari.resources.ptexSequenceTemplate(),
                                 'PTEXSequence_Flat' : mari.resources.ptexFlattenedSequenceTemplate()
                                }

        for key in current_template_dict:
            if key == pathVariable:
                obj.setText(current_template_dict[key])


    def _browseForDirectory(self, obj):
        """ Gets a path from a dialog"""

        path = QtGui.QFileDialog.getExistingDirectory(None,"Export Path",obj.text())
        if path == "":
            return
        else:
            obj.setText(path)


    def _disableUIElements(self, obj_active, obj_path,obj_browse,obj_reset,obj_link):
        """ Disables UI elements if Actvivate checkbox is off"""

        if not obj_active.isChecked():
            obj_path.setReadOnly(True)
            obj_path.setEnabled(False)
            if obj_browse is not None:
                obj_browse.setEnabled(False)
            obj_reset.setEnabled(False)
            if obj_link is not None:
                obj_link.setEnabled(False)
        else:
            obj_path.setReadOnly(False)
            obj_path.setEnabled(True)
            if obj_browse is not None:
                obj_browse.setEnabled(True)
            obj_reset.setEnabled(True)
            if obj_link is not None:
                obj_link.setEnabled(True)

        self._resetDisabledToCurrent()


    def _resetDisabledToCurrent(self):
        """ Resets disabled Path Fields to the current state of the variable. Sort of like reset to current variable"""

        # if a row is inactive reset it to default automtically:
        # Set Texture Import Path
        if not self.Active_VarA.isChecked():
            self._setCurrentTemplateToField(self.Path_VarA,'Tex_Import')
        # Set Texture Export Path
        if not self.Active_VarC.isChecked():
            self._setCurrentTemplateToField(self.Path_VarC,'Tex_Export')
        # Set Geo Path
        if not self.Active_VarD.isChecked():
            self._setCurrentTemplateToField(self.Path_VarD,'Geo')
        # Set Tmage Manager Path
        if not self.Active_VarE.isChecked():
            self._setCurrentTemplateToField(self.Path_VarE,'Image')
        # Set Render Path
        if not self.Active_VarF.isChecked():
            self._setCurrentTemplateToField(self.Path_VarF,'Render')
        # Set Archive Path
        if not self.Active_VarG.isChecked():
            self._setCurrentTemplateToField(self.Path_VarG,'Archive')
        # Set Shelf Path
        if not self.Active_VarH.isChecked():
            self._setCurrentTemplateToField(self.Path_VarH,'Shelf')
        # Set Camera Path
        if not self.Active_VarI.isChecked():
            self._setCurrentTemplateToField(self.Path_VarI,'Camera')
        # Set Texture Flattened Temaplte
        if not self.Active_VarJ.isChecked():
            self._setCurrentTemplateToField(self.Path_VarJ,'Sequence_Flat')
        # Set Texture Temaplte
        if not self.Active_VarK.isChecked():
            self._setCurrentTemplateToField(self.Path_VarK,'Sequence')
        # Set PTEX Flattened Temaplte
        if not self.Active_VarL.isChecked():
            self._setCurrentTemplateToField(self.Path_VarL,'PTEXSequence_Flat')
        # Set PTEX Temaplte
        if not self.Active_VarM.isChecked():
            self._setCurrentTemplateToField(self.Path_VarM,'PTEXSequence')


    def _checkPathForBase(self,text_path, base_link):
        """ Checks the user input while typing if it contains Variable $BASE
        It it exists, it will auto-activate the corresponding linked to base checkbox """

        text = text_path.text()
        base_found = text.find('$BASE')
        if base_found is not -1:
            base_link.setChecked(True)
        else:
            base_link.setChecked(False)


    def _resolveBASEVariable(self,base_path,text_path,base_link):
        """ When the user deactivates a base_link checkbox and a $BASE variable is found
        the Variable will be replaced in the text field with the full path."""

        text = text_path.text()
        base_path_text = base_path.text()

        if base_path_text.endswith('/') or base_path_text.endswith('\\'):
            base_path_text = base_path_text[:-1]

        # If it is checked and a path is found that corresponds to Base Path, insert Variable
        if base_link.isChecked() and base_path_text:
            base_find = text.replace(base_path_text,'$BASE')
            text_path.setText(base_find)

        # Otherwise if BASE Variable is found and link is unchecked, replace variable with path
        if not base_link.isChecked():
            base_search = text.find('$BASE')
            if base_search is -1: #base is not contained in variable path
                base_var_found = False
            else: #base is contained in variable path
                base_var_found = True
            # if base path is empty but base variable is foundthrow a user message
            if not base_path_text and base_var_found:
                mari.utils.message('The Base Path is empty.\n Unable to resolve $BASE Variable to full Path','Unable to resolve Base Path')
                base_link.setChecked(True)
                return
            else:
                base_find = text.replace('$BASE',base_path_text)
                text_path.setText(base_find)


    def _checkInput(self):
        """Checks and resolves the entered path when dialog is accepted and launches necessary dialogs (create dirs)"""

        # Dictionary: Key - Variable Active Field - Variable Path Field - Variable to set - $BASE found - Path Exists
        var_dict = {
                    'TEXTURE MAPS (import)' :  [self.Active_VarA, self.Path_VarA, mari.resources.DEFAULT_IMPORT, True,False],
                    'TEXTURE MAPS (export)' :  [self.Active_VarC, self.Path_VarC, mari.resources.DEFAULT_EXPORT, True,False],
                    'GEOMETRY (import)'        :  [self.Active_VarD, self.Path_VarD, mari.resources.DEFAULT_GEO,True,False],
                    'IMAGE MANAGER (import/export)'      :  [self.Active_VarE, self.Path_VarE, mari.resources.DEFAULT_IMAGE,True,False],
                    'RENDERS/TURNTABLES (export)'     :  [self.Active_VarF, self.Path_VarF, mari.resources.DEFAULT_RENDER,True,False],
                    'ARCHIVE (import/export)'    :  [self.Active_VarG, self.Path_VarG, mari.resources.DEFAULT_ARCHIVE,True,False],
                    'SHELVES (import/export)'      :  [self.Active_VarH, self.Path_VarH, mari.resources.DEFAULT_SHELF,True,False],
                    'CAM/PROJECTOR (import/export)'     :  [self.Active_VarI, self.Path_VarI, mari.resources.DEFAULT_CAMERA,True,False]
                    }


        base_path_text = self.Path_Base.text()
        if base_path_text.endswith('/') or base_path_text.endswith('\\'):
            base_path_text = base_path_text[:-1]
        base_found = False
        base_found_in_var = False
        base_var_dict = {} # created to Check for $BASE Variables
        base_var_final_dict = {} # contains the finished list of items that are active, including their states for folderExist & $BASE Var.
        base_var_exist_dict = {} #used to give details to the Error UI if an invalid $BASE Variable is used
        var_folder_exist_dict = {} #used to give details to the Error UI what folders need to be created

        # Checking dictionary for $BASE Variables:
        for key in var_dict:
            dict_val_00 = var_dict[key][0] # Is Field Active ?
            dict_val_01 = var_dict[key][1] # What is the PathText of the Active Field
            dict_val_02 = var_dict[key][2] # The Variable associated to the Field
            dict_val_03 = var_dict[key][3] # Is there a $BASE Variable in the Path ?
            dict_val_04 = var_dict[key][4] # Does the resolved Path exist ?

            if dict_val_00.isChecked(): #Only check active rows
                row_active = True
                variable_path = dict_val_01.text()
                contains_base_val = variable_path.find('$BASE')
                if contains_base_val is -1:
                    base_found_in_var = False
                else:
                    base_found_in_var = True
                    base_found = True
                    base_var_exist_dict[key] = key

                # Set dictionary entries in new dict- if the $BASE Variable was found or not and if the row is active
                # Use old values for other ones
                base_var_dict[key] = [row_active,dict_val_01,dict_val_02,base_found_in_var,dict_val_04]


        # When there are base variables used but the base_path is empty pop a question
        if base_found and not base_path_text:
            # Generating a textmessage for the Details of the Info Box
            key_list = []
            for key in base_var_exist_dict:
                key_list.append(base_var_exist_dict[key])

            info_dialog = Base_InfoUI(key_list)
            info_dialog.exec_()
            info_reply = info_dialog.buttonRole(info_dialog.clickedButton())
            # If User chooses to Ignore problematic paths, we will remove the prolematic ones from the dictionary
            if info_reply is QtGui.QMessageBox.ButtonRole.AcceptRole:
                for key in base_var_exist_dict:
                    base_var_dict.pop(key)
            else:
                return

        # if base_path is not empty but does not exist, throw dialog to create it
        if base_path_text:
            if not os.path.exists(base_path_text):
                title = 'Create Base Directory'
                text = 'Base Path Subfolder does not exist: \n\n "%s".' %base_path_text
                info = 'Create the path?'
                info_dialog = InfoUI(title, text, info)
                info_dialog.exec_()
                info_reply = info_dialog.buttonRole(info_dialog.clickedButton())
                if info_reply is QtGui.QMessageBox.ButtonRole.RejectRole:
                    return
                else:
                    if not os.path.exists(base_path_text):
                        os.makedirs(base_path_text)


        var_missing_folders = False

        # Check all the Subfolders on all active variables
        for key in base_var_dict:
            var_folder_exists = False
            dict_val_00 = base_var_dict[key][0] # Is Field Active ?
            dict_val_01 = base_var_dict[key][1] # What is the PathText of the Active Field
            dict_val_02 = base_var_dict[key][2] # The Variable associated to the Field
            dict_val_03 = base_var_dict[key][3] # Is there a $BASE Variable in the Path ?
            dict_val_04 = base_var_dict[key][4] # Does the resolved Path exist ?

            if dict_val_00: #Only check active rows
                if base_path_text.endswith('/') or base_path_text.endswith('\\'):
                    base_path_text = base_path_text[:-1]
                dict_val_01_resolve = dict_val_01.text()
                dict_val_01_resolve = dict_val_01_resolve.replace('$BASE',base_path_text)
                if os.path.exists(dict_val_01_resolve):
                    var_folder_exists = True
                else:
                    var_folder_exists = False
                    var_missing_folders = True
                    var_folder_exist_dict[key] = dict_val_01_resolve

                # Set dictionary entries in new dict- if the $BASE Variable was found or not and if the row is active
                # Use old values for other ones
                base_var_final_dict[key] = [dict_val_00,dict_val_01,dict_val_02,dict_val_03,var_folder_exists,dict_val_01_resolve]


        # if we came across missing folders throw a dialog:
        if var_missing_folders:
            # Generating a textmessage for the Details of the Info Box
            key_list_B = []
            for key in var_folder_exist_dict:
                key_list_B.append(key + ': ' + var_folder_exist_dict[key])

            info_dialog_B = VarDir_InfoUI(key_list_B)
            info_dialog_B.exec_()
            info_reply_B = info_dialog_B.buttonRole(info_dialog_B.clickedButton())
            # If User chooses to create the missing Folders grab the keys from var_folder_exist_dict and the
            # resolved path from base_var_final_dict and make folders.
            if info_reply_B is QtGui.QMessageBox.ButtonRole.AcceptRole:
                for key in var_folder_exist_dict:
                    try:
                        path_to_create = base_var_final_dict[key][5]
                        os.makedirs(path_to_create)
                    except Exception:
                        pass #assuming that a previous field already created the folder
            else:
                return

        # if a base path is used store it to json file for later use
        if base_found:
            self._perProjectBasePathSave(base_path_text)

        self._setPath(base_var_final_dict)


    def _setPath(self,var_dict):
        """ Sets the new value for activated variables"""

        print 'SET PROJECT performed the following actions:\n'

        for key in var_dict:
            dict_ACTIVE = var_dict[key][0] # Is Field Active ?
            dict_PATHTEXT = var_dict[key][1] # What is the PathText of the Active Field
            dict_VARIABLE = var_dict[key][2] # The Variable associated to the Field
            dict_BASEVAR = var_dict[key][3] # Is there a $BASE Variable in the Path ?
            dict_DIREXIST = var_dict[key][4] # Does the resolved Path exist ?
            dict_RESOLVEDPATH = var_dict[key][5] # Final resolved Path (converted $BASE Variable)

            if dict_ACTIVE:
                try:
                    if dict_RESOLVEDPATH.endswith('/') or dict_RESOLVEDPATH.endswith('\\'):
                        dict_RESOLVEDPATH = dict_RESOLVEDPATH[:-1]
                    mari.resources.setPath(dict_VARIABLE,dict_RESOLVEDPATH)
                    actionXML('addPath','UserDefined',dict_VARIABLE,dict_RESOLVEDPATH)
                    print dict_VARIABLE + ' set to: ' + dict_RESOLVEDPATH
                except Exception:
                    mari.utils.message('Unable to set path for Variable: \n' + key)
                    pass

        # Sequence Templates:
        try:
            # Set Texture Flattened Temaplte
            if self.Active_VarJ.isChecked():
                template = self.Path_VarJ.text()
                if template.startswith('/') or template.startswith('\\'):
                    template = template[1:]
                mari.resources.setFlattenedSequenceTemplate(template)
                actionXML('addPath','UserDefined','Sequence_Flat',template)
                print 'Flattened Sequence Template' + ' set to: ' + template
            # Set Texture Temaplte
            if self.Active_VarK.isChecked():
                template = self.Path_VarK.text()
                if template.startswith('/') or template.startswith('\\'):
                    template = template[1:]
                mari.resources.setSequenceTemplate(template)
                actionXML('addPath','UserDefined','Sequence',template)
                print 'Sequence Template' + ' set to: ' + template
            # Set PTEX Flattened Temaplte
            if self.Active_VarL.isChecked():
                template = self.Path_VarL.text()
                if template.startswith('/') or template.startswith('\\'):
                    template = template[1:]
                mari.resources.setPtexFlattenedSequenceTemplate(template)
                actionXML('addPath','UserDefined','PTEXSequence_Flat',template)
                print 'PTEX Flattened Template' + ' set to: ' + template
            # Set PTEX Temaplte
            if self.Active_VarM.isChecked():
                template = self.Path_VarM.text()
                if template.startswith('/') or template.startswith('\\'):
                    template = template[1:]
                mari.resources.setPtexSequenceTemplate(template)
                actionXML('addPath','UserDefined','PTEXSequence',template)
                print 'PTEX Template' + ' set to: ' + template
        except Exception:
            mari.utils.message('Unable to set sequence templates. Check formatting.')
            pass

        self._userSettingsSave()
        self.accept()


    def _userSettingsSave(self):
        """Saves UI Options between sessions into MARI Config."""

        for name, obj in inspect.getmembers(self):
            self.SETTINGS.beginGroup("setProjectPaths_" + version)
            if isinstance(obj, QtGui.QLineEdit):
                state = None
                state = obj.text()
                self.SETTINGS.setValue(name,state)

            if isinstance(obj, QtGui.QCheckBox):
                state = obj.isChecked()
                self.SETTINGS.setValue(name,state)

            self.SETTINGS.endGroup()

        # saving $BASE Path to json file


    def _userSettingsLoad(self):
        """Loads UI Options between sessions from MARI Config"""


        for name, obj in inspect.getmembers(self):
            self.SETTINGS.beginGroup("setProjectPaths_" + version)

            if isinstance(obj, QtGui.QCheckBox):
                state_string = self.SETTINGS.value(name)
                if state_string == "true":
                    obj.setChecked(True)
                if state_string == "false":
                    obj.setChecked(False)

            if isinstance(obj, QtGui.QLineEdit):
                state = None
                state = unicode(self.SETTINGS.value(name))
                if state != 'None':
                    obj.setText(state)

            self.SETTINGS.endGroup()

        self._resetDisabledToCurrent()

    def _perProjectBasePathSave(self,base_path):
        """
        When the user accepts the dialog and is using a $BASE Variable anywhere
        the BasePath is saved to json file so I can restore the Path to the
        BasePath Textfield the next time the Project & setprojectpaths is opened

        """

        actionXML('addPath','BASE_PATH_SETTING','SetProjectPath_BASE',base_path)


    def _perProjectBasePathLoad(self,base_path):
        """
        Checks if this project already had custom project paths set that involved a $BASE Variable
        If one is found, the path of $BASE is restored, otherwise the last used one is used that was
        saved as part of _userSettingsSave/Loads

        """

        savedBasePath = readXMLValue('BASE_PATH_SETTING','SetProjectPath_BASE')
        if savedBasePath is not None:
            base_path.setText(savedBasePath)


# ------------------------------------------------------------------------------

class actionXML(object):
    """
     Read,writes and removes paths to and from the projects project path json file
     var_type determines type of variable: user set variable or project default
     variable is the type of path to be set and path the new path for the variable

    """

    def __init__(self,mode,var_type,variable,path):
        self.xmlFile = getProjectPath()
        if mode == 'addPath':
            self.savePathToFile(var_type,variable,path)
        if mode == 'removePath':
            self.removePathFromFile(var_type,variable)
    # ------------------------------------------------------------------------------

    def savePathToFile(self,var_type,variable,path):
        "stores a specifc project path for a given variable"

        data = {}

        if os.path.exists(self.xmlFile):
            with open(self.xmlFile, "r") as jsonFile:
                try:
                    data = json.load(jsonFile)
                except Exception:
                    pass

        key = variable + '-' + var_type
        data[key] = var_type,variable,path

        with open(self.xmlFile, "w+") as jsonFile:
            jsonFile.write(json.dumps(data))

    # ------------------------------------------------------------------------------

    def removePathFromFile(self,var_type,variable):
        "removes a variable from the json file"

        data = {}

        if os.path.exists(self.xmlFile):
            with open(self.xmlFile, "r") as jsonFile:
                try:
                    data = json.load(jsonFile)
                    key = variable + '-' + var_type
                    data.pop(key,0)
                except Exception:
                    pass

        with open(self.xmlFile, "w+") as jsonFile:
            jsonFile.write(json.dumps(data))


    # ------------------------------------------------------------------------------


def readXMLValue(var_type,variable):
    """ Returns a specific variable path from the Project Path json file"""

    xmlFile = getProjectPath()
    data = {}
    path = None

    if os.path.exists(xmlFile):
        with open(xmlFile, "r") as jsonFile:
            try:
                data = json.load(jsonFile)
                key = variable + '-' + var_type
                path = data[key][2]
            except Exception:
                pass

    return path

# ------------------------------------------------------------------------------

class restoreProjectPaths(object):
    """
    Sets the project paths back to the way they were when the project closed
    Also handles saving of project default paths before SetProjectPath changes
    """
    def __init__(self):
        startupTemplate = self._saveStartupTemplate()
        restoreChanges = self._restorePreviousPaths()

    def _saveStartupTemplate(self):
        """ Stores the State of Variables right after project launch so we can reset to it via Template Reset Buttons"""

        template_dict = {'Project'    : mari.projects.current().uuid(),
                         'Tex_Export' : mari.resources.path(mari.resources.DEFAULT_EXPORT),
                         'Tex_Import' : mari.resources.path(mari.resources.DEFAULT_IMPORT),
                         'Archive' : mari.resources.path(mari.resources.DEFAULT_ARCHIVE),
                         'Camera' : mari.resources.path(mari.resources.DEFAULT_CAMERA),
                         'Geo' : mari.resources.path(mari.resources.DEFAULT_GEO),
                         'Image' : mari.resources.path(mari.resources.DEFAULT_IMAGE),
                         'Shelf' : mari.resources.path(mari.resources.DEFAULT_SHELF),
                         'Render' : mari.resources.path(mari.resources.DEFAULT_RENDER),
                         'Sequence' : mari.resources.sequenceTemplate(),
                         'Sequence_Flat' : mari.resources.flattenedSequenceTemplate(),
                         'PTEXSequence' : mari.resources.ptexSequenceTemplate(),
                         'PTEXSequence_Flat' : mari.resources.ptexFlattenedSequenceTemplate()
                        }


        for key in template_dict:
            actionXML('addPath','Default',key,template_dict[key])

    def _restorePreviousPaths(self):
        """ If the user had made any changes to project paths when the project was last open, this restores the paths """

        xmlFile = getProjectPath()
        data = {}

        # Variable dictionary. There are some that return nothing since there is no variable for them
        # but I am just including them in the dict so no key error occurs and doing a try except routine around them.
        var_dict = {
                    'MARI_DEFAULT_IMPORT_PATH'     :  mari.resources.DEFAULT_IMPORT,
                    'MARI_DEFAULT_EXPORT_PATH'     :  mari.resources.DEFAULT_EXPORT,
                    'MARI_DEFAULT_GEOMETRY_PATH'   :  mari.resources.DEFAULT_GEO,
                    'MARI_DEFAULT_IMAGE_PATH'      :  mari.resources.DEFAULT_IMAGE,
                    'MARI_DEFAULT_RENDER_PATH'     :  mari.resources.DEFAULT_RENDER,
                    'MARI_DEFAULT_ARCHIVE_PATH'    :  mari.resources.DEFAULT_ARCHIVE,
                    'MARI_DEFAULT_SHELF_PATH'      :  mari.resources.DEFAULT_SHELF,
                    'MARI_DEFAULT_CAMERA_PATH'     :  mari.resources.DEFAULT_CAMERA,
                    'Sequence_Flat'                :  'INVALID',    #included to avoid key errors
                    'Sequence'                     :  'INVALID',    #included to avoid key errors
                    'PTEXSequence_Flat'            :  'INVALID',    #included to avoid key errors
                    'PTEXSequence'                 :  'INVALID'    #included to avoid key errors
                    }

        if os.path.exists(xmlFile):
            with open(xmlFile, "r") as jsonFile:
                try:
                    data = json.load(jsonFile)
                except Exception:
                    pass

        for key in data:
            if data[key][0] == 'UserDefined':
                varToSet = var_dict[data[key][1]]
                try:
                    path = data[key][2]
                    if path.endswith('/') or path.endswith('\\'):
                        path = path[:-1]
                    mari.resources.setPath(varToSet,path)
                except Exception:
                    pass

                # checking sequence templates that don't have MARI variables
                if data[key][1] == 'Sequence_Flat':
                    path = data[key][2]
                    if path.startswith('/') or path.startswith('\\'):
                        path = path[1:]
                    mari.resources.setFlattenedSequenceTemplate(path)
                elif data[key][1] == 'Sequence':
                    path = data[key][2]
                    if path.startswith('/') or path.startswith('\\'):
                        path = path[1:]
                    mari.resources.setSequenceTemplate(path)
                elif data[key][1] == 'PTEXSequence_Flat':
                    path = data[key][2]
                    if path.startswith('/') or path.startswith('\\'):
                        path = path[1:]
                    mari.resources.setPtexFlattenedSequenceTemplate(path)
                elif data[key][1] == 'PTEXSequence':
                    path = data[key][2]
                    if path.startswith('/') or path.startswith('\\'):
                        path = path[1:]
                    mari.resources.setPtexSequenceTemplate(path)

# ------------------------------------------------------------------------------

def getProjectPath():
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

class Base_InfoUI(QtGui.QMessageBox):
    """Informs the user that a $BASE Variable was used but no Base Path was specified"""
    def __init__(self,where_do_base_variables_exist, parent=None):
        super(Base_InfoUI, self).__init__(parent)

        infotxt = '$BASE Variables found in:'
        base_number = len(where_do_base_variables_exist)
        for item in where_do_base_variables_exist:
            infotxt = infotxt + '\n' + item

        # Create info gui
        self.setWindowTitle('No Base Path specified')
        self.setIcon(QtGui.QMessageBox.Warning)
        self.setText('You are using $BASE Variables in one or more active Fields\nbut no valid Base Path is specified\n\nHow do you wish to proceed ?')
        self.setInformativeText('Ignore will skip any paths with $BASE Variables')
        self.setDetailedText(infotxt)
        self.setStandardButtons(QtGui.QMessageBox.Ignore | QtGui.QMessageBox.Cancel)
        self.setDefaultButton(QtGui.QMessageBox.Ignore)

# ------------------------------------------------------------------------------

class VarDir_InfoUI(QtGui.QMessageBox):
    """Informs the user that a $BASE Variable was used but no Base Path was specified"""
    def __init__(self,which_folders_do_not_exist, parent=None):
        super(VarDir_InfoUI, self).__init__(parent)

        infotxt = ''
        base_number = len(which_folders_do_not_exist)
        for item in which_folders_do_not_exist:
            infotxt = infotxt + '\n' + item + ' does not exist'

        # Create info gui
        self.setWindowTitle('Folders do not exist')
        self.setIcon(QtGui.QMessageBox.Warning)
        self.setText('Some Variable Folder you specified do not exist (see Details).\n\nDo you wish to create the missing Folders ?')
        self.setDetailedText(infotxt)
        self.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        self.setDefaultButton(QtGui.QMessageBox.Ok)

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

def setProjectPath():
    """Execute UI"""

    #Check project is suitable
    if not _isProjectSuitable()[1]:
        return
    else:
        dialog = setProjectPathUI()
        dialog.exec_()

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    setProjectPath()


