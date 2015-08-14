# Notes:
#  Some logic errors in _resetToProjectTemplate: How can you reset to a project default if it was already changed ?
# Maybe on launch for the first time save out the defaults into separate QSettings Group so it can be recalled later ?
#
# There are redundant debug print statements in _setPath()
# To do:
# - get rid of print statements in _setPath
# - check against BASE Variable on execution (error if empty)
# - folder creation
# - save template defaults
# - save user changes
# - double check os+seps


import mari, os
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
from PySide.QtCore import QSettings
import inspect



class setProjectPathUI(QtGui.QDialog):
    """GUI to set your Project Paths"""

    def __init__(self):
        suitable = _isProjectSuitable()
        if suitable[0]:
            super(setProjectPathUI, self).__init__()
            # Dialog Settings
            # self.setFixedSize(800, 600)
            self.setWindowTitle('Set Project Default Paths')

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
            self.Descr_BaseInfo =  QtGui.QLabel("Base Path can be used to set paths relative to it by using the Variable $BASE in fields below\ne.g: $BASE\ReferenceImages, $BASE\Model, $BASE\Textures etc.")
            self.Descr_Base = QtGui.QLabel("Base Path")
            self.Path_Base = QtGui.QLineEdit()
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
            self.Active_VarA.setToolTip('The default Path that should be used when Importing Textures')
            self.Path_VarA = QtGui.QLineEdit()
            self.path_button_VarA = QtGui.QPushButton(path_icon, "")
            self.path_button_VarA.setToolTip('Browse for Folder')
            self.templateReset_VarA = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarA.setToolTip('Reset to Project Default')
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
            self.Active_VarC.setToolTip('The default Path that should be used when Exporting Textures')
            self.Path_VarC = QtGui.QLineEdit()
            self.path_button_VarC = QtGui.QPushButton(path_icon, "")
            self.path_button_VarC.setToolTip('Browse for Folder')
            self.templateReset_VarC = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarC.setToolTip('Reset to Project Default')
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
            self.Active_VarD = QtGui.QCheckBox("GEOMETRY (Import):")
            self.Active_VarD.setToolTip('The default Path that should be used when Importing new Objects')
            self.Path_VarD = QtGui.QLineEdit()
            self.path_button_VarD = QtGui.QPushButton(path_icon, "")
            self.path_button_VarD.setToolTip('Browse for Folder')
            self.templateReset_VarD = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarD.setToolTip('Reset to Project Default')
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
            self.Active_VarE.setToolTip('The default Path that should be used when Importing or Exporting from the Image Manager')
            self.Path_VarE = QtGui.QLineEdit()
            self.path_button_VarE = QtGui.QPushButton(path_icon, "")
            self.path_button_VarE.setToolTip('Browse for Folder')
            self.templateReset_VarE = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarE.setToolTip('Reset to Project Default')
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
            self.Active_VarF.setToolTip('The default Path that should be used when doing Screenshots & Turntables')
            self.Path_VarF = QtGui.QLineEdit()
            self.path_button_VarF = QtGui.QPushButton(path_icon, "")
            self.path_button_VarF.setToolTip('Browse for Folder')
            self.templateReset_VarF = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarF.setToolTip('Reset to Project Default')
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
            self.Active_VarG.setToolTip('The default Path that should be used when loading or saving an Archive')
            self.Path_VarG = QtGui.QLineEdit()
            self.path_button_VarG = QtGui.QPushButton(path_icon, "")
            self.path_button_VarG.setToolTip('Browse for Folder')
            self.templateReset_VarG = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarG.setToolTip('Reset to Project Default')
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
            self.Active_VarH.setToolTip('The default Path that should be used when loading or saving Shelves')
            self.Path_VarH = QtGui.QLineEdit()
            self.path_button_VarH = QtGui.QPushButton(path_icon, "")
            self.path_button_VarH.setToolTip('Browse for Folder')
            self.templateReset_VarH = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarH.setToolTip('Reset to Project Default')
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
            self.Active_VarI.setToolTip('The default Path that should be used when Importing or Eporting Cameras or Projectors')
            self.Path_VarI = QtGui.QLineEdit()
            self.path_button_VarI = QtGui.QPushButton(path_icon, "")
            self.path_button_VarI.setToolTip('Browse for Folder')
            self.templateReset_VarI = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarI.setToolTip('Reset to Project Default')
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
            self.templateReset_VarJ = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarJ.setToolTip('Reset to Project Default')
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
            self.templateReset_VarK = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarK.setToolTip('Reset to Project Default')
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
            self.templateReset_VarL = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarL.setToolTip('Reset to Project Default')
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
            self.templateReset_VarM = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarM.setToolTip('Reset to Project Default')
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
        """ Returns the default path that was set at project launch"""

        if pathVariable is 'Tex_Export':
            return mari.resources.path(mari.resources.DEFAULT_EXPORT)
        elif pathVariable is 'Tex_Import':
            return mari.resources.path(mari.resources.DEFAULT_IMPORT)
        elif pathVariable is 'Archive':
            return mari.resources.path(mari.resources.DEFAULT_ARCHIVE)
        elif pathVariable is 'Camera':
            return mari.resources.path(mari.resources.DEFAULT_CAMERA)
        elif pathVariable is 'Geo':
            return mari.resources.path(mari.resources.DEFAULT_GEO)
        elif pathVariable is 'Image':
            return mari.resources.path(mari.resources.DEFAULT_IMAGE)
        elif pathVariable is 'Shelf':
            return mari.resources.path(mari.resources.DEFAULT_SHELF)
        elif pathVariable is 'Render':
            return mari.resources.path(mari.resources.DEFAULT_RENDER)
        elif pathVariable is 'Sequence':
            return mari.resources.sequenceTemplate()
        elif pathVariable is 'Sequence_Flat':
            return mari.resources.flattenedSequenceTemplate()
        elif pathVariable is 'PTEXSequence':
            return mari.resources.ptexSequenceTemplate()
        elif pathVariable is 'PTEXSequence_Flat':
            return mari.resources.ptexFlattenedSequenceTemplate()
        elif pathVariable is None:
            return ''

    def _setProjectTemplate(self, obj, pathVariable):
        """ Gets the default path variable and sets the QLineEditField in Main UI to Value"""

        # pathVar = pathVariable
        path = self._getProjectTemplate(pathVariable)
        obj.setText(path)


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
                    path_to_create = base_var_final_dict[key][5]
                    os.makedirs(path_to_create)
            else:
                return












        # self.accept()

        else:
            print 'all good'
            return

#
        # variable_path = dict_val_01.text()
#
        # resolved_val = variable_path.replace('$BASE', base_val)
        # return resolved_val


    def _setPath(self):
        """ Sets the new value for activated variables"""


        # Set Texture Import Path
        if self.Active_VarA.isChecked:
            pathA = self._checkInput(self.Path_VarA)
            mari.resources.setPath(mari.resources.DEFAULT_IMPORT,pathA)
        # Set Texture Export Path
        if self.Active_VarC.isChecked:
            pathC = self._checkInput(self.Path_VarC)
            mari.resources.setPath(mari.resources.DEFAULT_EXPORT,pathC)
        # Set Geo Path
        if self.Active_VarD.isChecked:
            pathD = self._checkInput(self.Path_VarD)
            mari.resources.setPath(mari.resources.DEFAULT_GEO,pathD)
        # Set Tmage Manager Path
        if self.Active_VarE.isChecked:
            pathE = self._checkInput(self.Path_VarE)
            mari.resources.setPath(mari.resources.DEFAULT_IMAGE,pathE)
        # Set Render Path
        if self.Active_VarF.isChecked:
            pathF = self._checkInput(self.Path_VarF)
            mari.resources.setPath(mari.resources.DEFAULT_RENDER,pathF)
        # Set Archive Path
        if self.Active_VarG.isChecked:
            pathG = self._checkInput(self.Path_VarG)
            mari.resources.setPath(mari.resources.DEFAULT_ARCHIVE,pathG)
        # Set Shelf Path
        if self.Active_VarH.isChecked:
            pathH = self._checkInput(self.Path_VarH)
            mari.resources.setPath(mari.resources.DEFAULT_SHELF,pathH)
        # Set Camera Path
        if self.Active_VarI.isChecked:
            pathI = self._checkInput(self.Path_VarI)
            mari.resources.setPath(mari.resources.DEFAULT_CAMERA,pathI)
        # Set Texture Flattened Temaplte
        if self.Active_VarJ.isChecked:
            mari.resources.setFlattenedSequenceTemplate(self.Path_VarJ.text())
        # Set Texture Temaplte
        if self.Active_VarK.isChecked:
            mari.resources.setSequenceTemplate(self.Path_VarK.text())
        # Set PTEX Flattened Temaplte
        if self.Active_VarL.isChecked:
            mari.resources.setPtexFlattenedSequenceTemplate(self.Path_VarL.text())
        # Set PTEX Temaplte
        if self.Active_VarM.isChecked:
            mari.resources.setPtexSequenceTemplate(self.Path_VarM.text())


        # print mari.resources.path(mari.resources.DEFAULT_EXPORT)
        # print mari.resources.path(mari.resources.DEFAULT_IMPORT)
        # print mari.resources.path(mari.resources.DEFAULT_ARCHIVE)
        # print mari.resources.path(mari.resources.DEFAULT_CAMERA)
        # print mari.resources.path(mari.resources.DEFAULT_GEO)
        # print mari.resources.path(mari.resources.DEFAULT_IMAGE)
        # print mari.resources.path(mari.resources.DEFAULT_SHELF)
        # print mari.resources.path(mari.resources.DEFAULT_RENDER)
        # print mari.resources.sequenceTemplate()
        # print mari.resources.flattenedSequenceTemplate()
        # print mari.resources.ptexSequenceTemplate()
        # print mari.resources.ptexFlattenedSequenceTemplate()

        self.accept()


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


setProjectPathUI().exec_()