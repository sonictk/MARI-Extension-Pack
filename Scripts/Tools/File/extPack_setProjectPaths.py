# Notes:
#  Some logic errors in _resetToProjectTemplate: How can you reset to a project default if it was already changed ?
# Maybe on launch for the first time save out the defaults into separate QSettings Group so it can be recalled later ?

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
            # self.setFixedSize(700, 600)
            self.setWindowTitle('Set Project Default Paths')

            # Layouts & Boxes
            window_layout_box = QtGui.QVBoxLayout()
            group_layout_box = QtGui.QVBoxLayout()
            base_layout_grid = QtGui.QGridLayout()
            variable_layout_grid = QtGui.QGridLayout()
            misc_layout_grid = QtGui.QGridLayout()
            button_layout_box = QtGui.QHBoxLayout()
            base_group_box = QtGui.QGroupBox('Project Base Path')
            asset_group_box = QtGui.QGroupBox("Asset Paths")
            misc_group_box = QtGui.QGroupBox("Misc Paths")

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


            base_group_box.setLayout(base_layout_grid)


            # Asset Widges
            # Variable Widgets Variable A
            self.Active_VarA = QtGui.QCheckBox()
            self.Active_VarA.setToolTip('Allows you to activate or deactivate changes to this Default Path')
            self.Descr_VarA = QtGui.QLabel("TEXTURE MAPS (Import)")
            self.Descr_VarA.setToolTip('The default Path that should be used when Importing Textures')
            self.Path_VarA = QtGui.QLineEdit()
            self.path_button_VarA = QtGui.QPushButton(path_icon, "")
            self.path_button_VarA.setToolTip('Browse for Folder')
            self.templateReset_VarA = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarA.setToolTip('Reset to Project Default')
            self.link_VarA = QtGui.QCheckBox('Relative to Base')
            self.link_VarA.setToolTip('Relative to Base ON will add a $BASE variable to your path. \n If the $BASE Variable exists and you turn it off, the path will be fully resolved')
            variable_layout_grid.addWidget(self.Active_VarA,2,0)
            variable_layout_grid.addWidget(self.Descr_VarA,2,1)
            variable_layout_grid.addWidget(self.Path_VarA,2,2)
            variable_layout_grid.addWidget(self.path_button_VarA,2,3)
            variable_layout_grid.addWidget(self.templateReset_VarA,2,4)
            variable_layout_grid.addWidget(self.link_VarA,2,5)

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



            # Variable Widgets Variable C
            self.Active_VarC = QtGui.QCheckBox()
            self.Active_VarC.setToolTip('Allows you to activate or deactivate changes to this Default Path')
            self.Descr_VarC = QtGui.QLabel("TEXTURE MAPS (Export):")
            self.Descr_VarC.setToolTip('The default Path that should be used when Exporting Textures')
            self.Path_VarC = QtGui.QLineEdit()
            self.path_button_VarC = QtGui.QPushButton(path_icon, "")
            self.path_button_VarC.setToolTip('Browse for Folder')
            self.templateReset_VarC = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarC.setToolTip('Reset to Project Default')
            self.link_VarC = QtGui.QCheckBox('Relative to Base')
            self.link_VarC.setToolTip('Relative to Base ON will add a $BASE variable to your path. \n If the $BASE Variable exists and you turn it off, the path will be fully resolved')
            variable_layout_grid.addWidget(self.Active_VarC,3,0)
            variable_layout_grid.addWidget(self.Descr_VarC,3,1)
            variable_layout_grid.addWidget(self.Path_VarC,3,2)
            variable_layout_grid.addWidget(self.path_button_VarC,3,3)
            variable_layout_grid.addWidget(self.templateReset_VarC,3,4)
            variable_layout_grid.addWidget(self.link_VarC,3,5)

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




            # Variable Widgets Variable D
            self.Active_VarD = QtGui.QCheckBox()
            self.Active_VarD.setToolTip('Allows you to activate or deactivate changes to this Default Path')
            self.Descr_VarD = QtGui.QLabel("GEOMETRY (Import):")
            self.Descr_VarD.setToolTip('The default Path that should be used when Importing new Objects')
            self.Path_VarD = QtGui.QLineEdit()
            self.path_button_VarD = QtGui.QPushButton(path_icon, "")
            self.path_button_VarD.setToolTip('Browse for Folder')
            self.templateReset_VarD = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarD.setToolTip('Reset to Project Default')
            self.link_VarD = QtGui.QCheckBox('Relative to Base')
            self.link_VarD.setToolTip('Relative to Base ON will add a $BASE variable to your path. \n If the $BASE Variable exists and you turn it off, the path will be fully resolved')
            variable_layout_grid.addWidget(self.Active_VarD,4,0)
            variable_layout_grid.addWidget(self.Descr_VarD,4,1)
            variable_layout_grid.addWidget(self.Path_VarD,4,2)
            variable_layout_grid.addWidget(self.path_button_VarD,4,3)
            variable_layout_grid.addWidget(self.templateReset_VarD,4,4)
            variable_layout_grid.addWidget(self.link_VarD,4,5)

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


            # Variable Widgets Variable E
            self.Active_VarE = QtGui.QCheckBox()
            self.Active_VarE.setToolTip('Allows you to activate or deactivate changes to this Default Path')
            self.Descr_VarE = QtGui.QLabel("IMAGE MANAGER (Import/Export):")
            self.Descr_VarE.setToolTip('The default Path that should be used when Importing or Exporting from the Image Manager')
            self.Path_VarE = QtGui.QLineEdit()
            self.path_button_VarE = QtGui.QPushButton(path_icon, "")
            self.path_button_VarE.setToolTip('Browse for Folder')
            self.templateReset_VarE = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarE.setToolTip('Reset to Project Default')
            self.link_VarE = QtGui.QCheckBox('Relative to Base')
            self.link_VarE.setToolTip('Relative to Base ON will add a $BASE variable to your path. \n If the $BASE Variable exists and you turn it off, the path will be fully resolved')
            variable_layout_grid.addWidget(self.Active_VarE,5,0)
            variable_layout_grid.addWidget(self.Descr_VarE,5,1)
            variable_layout_grid.addWidget(self.Path_VarE,5,2)
            variable_layout_grid.addWidget(self.path_button_VarE,5,3)
            variable_layout_grid.addWidget(self.templateReset_VarE,5,4)
            variable_layout_grid.addWidget(self.link_VarE,5,5)

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



            # Variable Widgets Variable F
            self.Active_VarF = QtGui.QCheckBox()
            self.Active_VarF.setToolTip('Allows you to activate or deactivate changes to this Default Path')
            self.Descr_VarF = QtGui.QLabel("RENDERS/TURNTABLES (Export):")
            self.Descr_VarF.setToolTip('The default Path that should be used when doing Screenshots & Turntables')
            self.Path_VarF = QtGui.QLineEdit()
            self.path_button_VarF = QtGui.QPushButton(path_icon, "")
            self.path_button_VarF.setToolTip('Browse for Folder')
            self.templateReset_VarF = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarF.setToolTip('Reset to Project Default')
            self.link_VarF = QtGui.QCheckBox('Relative to Base')
            self.link_VarF.setToolTip('Relative to Base ON will add a $BASE variable to your path. \n If the $BASE Variable exists and you turn it off, the path will be fully resolved')
            variable_layout_grid.addWidget(self.Active_VarF,6,0)
            variable_layout_grid.addWidget(self.Descr_VarF,6,1)
            variable_layout_grid.addWidget(self.Path_VarF,6,2)
            variable_layout_grid.addWidget(self.path_button_VarF,6,3)
            variable_layout_grid.addWidget(self.templateReset_VarF,6,4)
            variable_layout_grid.addWidget(self.link_VarF,6,5)

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




            # Variable Widgets Variable G
            self.Active_VarG = QtGui.QCheckBox()
            self.Active_VarG.setToolTip('Allows you to activate or deactivate changes to this Default Path')
            self.Descr_VarG = QtGui.QLabel("ARCHIVE (Import/Export):")
            self.Descr_VarG.setToolTip('The default Path that should be used when loading or saving an Archive')
            self.Path_VarG = QtGui.QLineEdit()
            self.path_button_VarG = QtGui.QPushButton(path_icon, "")
            self.path_button_VarG.setToolTip('Browse for Folder')
            self.templateReset_VarG = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarG.setToolTip('Reset to Project Default')
            self.link_VarG = QtGui.QCheckBox('Relative to Base')
            self.link_VarG.setToolTip('Relative to Base ON will add a $BASE variable to your path. \n If the $BASE Variable exists and you turn it off, the path will be fully resolved')
            variable_layout_grid.addWidget(self.Active_VarG,7,0)
            variable_layout_grid.addWidget(self.Descr_VarG,7,1)
            variable_layout_grid.addWidget(self.Path_VarG,7,2)
            variable_layout_grid.addWidget(self.path_button_VarG,7,3)
            variable_layout_grid.addWidget(self.templateReset_VarG,7,4)
            variable_layout_grid.addWidget(self.link_VarG,7,5)

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



            asset_group_box.setLayout(variable_layout_grid)


            # Variable Widgets Variable H
            self.Active_VarH = QtGui.QCheckBox()
            self.Active_VarH.setToolTip('Allows you to activate or deactivate changes to this Default Path')
            self.Descr_VarH = QtGui.QLabel("SHELVES (Import/Export):")
            self.Descr_VarH.setToolTip('The default Path that should be used when loading or saving Shelves')
            self.Path_VarH = QtGui.QLineEdit()
            self.path_button_VarH = QtGui.QPushButton(path_icon, "")
            self.path_button_VarH.setToolTip('Browse for Folder')
            self.templateReset_VarH = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarH.setToolTip('Reset to Project Default')
            self.link_VarH = QtGui.QCheckBox('Relative to Base')
            self.link_VarH.setToolTip('Relative to Base ON will add a $BASE variable to your path. \n If the $BASE Variable exists and you turn it off, the path will be fully resolved')
            misc_layout_grid.addWidget(self.Active_VarH,8,0)
            misc_layout_grid.addWidget(self.Descr_VarH,8,1)
            misc_layout_grid.addWidget(self.Path_VarH,8,2)
            misc_layout_grid.addWidget(self.path_button_VarH,8,3)
            misc_layout_grid.addWidget(self.templateReset_VarH,8,4)
            misc_layout_grid.addWidget(self.link_VarH,8,5)

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



            # Variable Widgets Variable I
            self.Active_VarI = QtGui.QCheckBox()
            self.Active_VarI.setToolTip('Allows you to activate or deactivate changes to this Default Path')
            self.Descr_VarI = QtGui.QLabel("CAM/PROJECTOR (Import/Export):")
            self.Descr_VarI.setToolTip('The default Path that should be used when Importing or Eporting Cameras or Projectors')
            self.Path_VarI = QtGui.QLineEdit()
            self.path_button_VarI = QtGui.QPushButton(path_icon, "")
            self.path_button_VarI.setToolTip('Browse for Folder')
            self.templateReset_VarI = QtGui.QPushButton(templateReset_icon, "")
            self.templateReset_VarI.setToolTip('Reset to Project Default')
            self.link_VarI = QtGui.QCheckBox('Relative to Base')
            self.link_VarI.setToolTip('Relative to Base ON will add a $BASE variable to your path. \n If the $BASE Variable exists and you turn it off, the path will be fully resolved')
            misc_layout_grid.addWidget(self.Active_VarI,9,0)
            misc_layout_grid.addWidget(self.Descr_VarI,9,1)
            misc_layout_grid.addWidget(self.Path_VarI,9,2)
            misc_layout_grid.addWidget(self.path_button_VarI,9,3)
            misc_layout_grid.addWidget(self.templateReset_VarI,9,4)
            misc_layout_grid.addWidget(self.link_VarI,9,5)

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



            misc_group_box.setLayout(misc_layout_grid)


            # APPLY CANCEL BUTTONS
            # Widget OK / Cancel Button
            self.AllBtn = QtGui.QPushButton('Set Project')
            self.SelectedBtn = QtGui.QPushButton('Cancel')
            # Add Apply Cancel Buttons to Button Layout
            button_layout_box.addWidget(self.AllBtn)
            button_layout_box.addWidget(self.SelectedBtn)


            # Add sub Layouts to main Window Box Layout
            window_layout_box.addWidget(base_group_box)
            window_layout_box.addWidget(asset_group_box)
            window_layout_box.addWidget(misc_group_box)
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
            obj_browse.setEnabled(False)
            obj_reset.setEnabled(False)
            obj_link.setEnabled(False)
        else:
            obj_path.setReadOnly(False)
            obj_path.setEnabled(True)
            obj_browse.setEnabled(True)
            obj_reset.setEnabled(True)
            obj_link.setEnabled(True)






# class pathProcessing():
#     """Handles path operations on the individual variable fields"""

#     def __init__(self):
#         super(pathProcessing, self).__init__()






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