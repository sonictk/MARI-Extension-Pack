class CloneMergeGUI(QtGui.QDialog):
    '''GUI to select Clone Merge for selected patches or all patches'''

    def __init__(self):
        suitable = [True,True]
        if suitable[0]:
            super(CloneMergeGUI, self).__init__()
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
            template_reset_pixmap = QtGui.QPixmap(mari.resources.path(mari.resources.ICONS) + os.sep + 'Reset.png')
            template_reset_icon = QtGui.QIcon(template_reset_pixmap)


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
            self.Descr_VarA = QtGui.QLabel("TEXTURE MAPS (Import)")
            self.Path_VarA = QtGui.QLineEdit()
            self.path_button_VarA = QtGui.QPushButton(path_icon, "")
            self.path_button_VarA.setToolTip('Browse for Folder')
            self.template_reset_VarA = QtGui.QPushButton(template_reset_icon, "")
            self.template_reset_VarA.setToolTip('Reset to Project Default')
            self.link_VarA = QtGui.QCheckBox('Relative to Base')
            variable_layout_grid.addWidget(self.Active_VarA,2,0)
            variable_layout_grid.addWidget(self.Descr_VarA,2,1)
            variable_layout_grid.addWidget(self.Path_VarA,2,2)
            variable_layout_grid.addWidget(self.path_button_VarA,2,3)
            variable_layout_grid.addWidget(self.template_reset_VarA,2,4)
            variable_layout_grid.addWidget(self.link_VarA,2,5)


            # Variable Widgets Variable B
            self.Active_VarB = QtGui.QCheckBox()
            self.Descr_VarB = QtGui.QLabel("TEXTURE MAPS (Import)")
            self.Path_VarB = QtGui.QLineEdit()
            self.path_button_VarB = QtGui.QPushButton(path_icon, "")
            self.path_button_VarB.setToolTip('Browse for Folder')
            self.template_reset_VarB = QtGui.QPushButton(template_reset_icon, "")
            self.template_reset_VarB.setToolTip('Reset to Project Default')
            self.link_VarB = QtGui.QCheckBox('Relative to Base')
            variable_layout_grid.addWidget(self.Active_VarB,2,0)
            variable_layout_grid.addWidget(self.Descr_VarB,2,1)
            variable_layout_grid.addWidget(self.Path_VarB,2,2)
            variable_layout_grid.addWidget(self.path_button_VarB,2,3)
            variable_layout_grid.addWidget(self.template_reset_VarB,2,4)
            variable_layout_grid.addWidget(self.link_VarB,2,5)

            # Variable Widgets Variable C
            self.Active_VarC = QtGui.QCheckBox()
            self.Descr_VarC = QtGui.QLabel("TEXTURE MAPS (Export):")
            self.Path_VarC = QtGui.QLineEdit()
            self.path_button_VarC = QtGui.QPushButton(path_icon, "")
            self.path_button_VarC.setToolTip('Browse for Folder')
            self.template_reset_VarC = QtGui.QPushButton(template_reset_icon, "")
            self.template_reset_VarC.setToolTip('Reset to Project Default')
            self.link_VarC = QtGui.QCheckBox('Relative to Base')
            variable_layout_grid.addWidget(self.Active_VarC,3,0)
            variable_layout_grid.addWidget(self.Descr_VarC,3,1)
            variable_layout_grid.addWidget(self.Path_VarC,3,2)
            variable_layout_grid.addWidget(self.path_button_VarC,3,3)
            variable_layout_grid.addWidget(self.template_reset_VarC,3,4)
            variable_layout_grid.addWidget(self.link_VarC,3,5)


            # Variable Widgets Variable D
            self.Active_VarD = QtGui.QCheckBox()
            self.Descr_VarD = QtGui.QLabel("GEOMETRY (Import):")
            self.Path_VarD = QtGui.QLineEdit()
            self.path_button_VarD = QtGui.QPushButton(path_icon, "")
            self.path_button_VarD.setToolTip('Browse for Folder')
            self.template_reset_VarD = QtGui.QPushButton(template_reset_icon, "")
            self.template_reset_VarD.setToolTip('Reset to Project Default')
            self.link_VarD = QtGui.QCheckBox('Relative to Base')
            variable_layout_grid.addWidget(self.Active_VarD,4,0)
            variable_layout_grid.addWidget(self.Descr_VarD,4,1)
            variable_layout_grid.addWidget(self.Path_VarD,4,2)
            variable_layout_grid.addWidget(self.path_button_VarD,4,3)
            variable_layout_grid.addWidget(self.template_reset_VarD,4,4)
            variable_layout_grid.addWidget(self.link_VarD,4,5)

            # Variable Widgets Variable E
            self.Active_VarE = QtGui.QCheckBox()
            self.Descr_VarE = QtGui.QLabel("IMAGE MANAGER (Import/Export):")
            self.Path_VarE = QtGui.QLineEdit()
            self.path_button_VarE = QtGui.QPushButton(path_icon, "")
            self.path_button_VarE.setToolTip('Browse for Folder')
            self.template_reset_VarE = QtGui.QPushButton(template_reset_icon, "")
            self.template_reset_VarE.setToolTip('Reset to Project Default')
            self.link_VarE = QtGui.QCheckBox('Relative to Base')
            variable_layout_grid.addWidget(self.Active_VarE,5,0)
            variable_layout_grid.addWidget(self.Descr_VarE,5,1)
            variable_layout_grid.addWidget(self.Path_VarE,5,2)
            variable_layout_grid.addWidget(self.path_button_VarE,5,3)
            variable_layout_grid.addWidget(self.template_reset_VarE,5,4)
            variable_layout_grid.addWidget(self.link_VarE,5,5)


            # Variable Widgets Variable F
            self.Active_VarF = QtGui.QCheckBox()
            self.Descr_VarF = QtGui.QLabel("RENDERS/TURNTABLES (Export):")
            self.Path_VarF = QtGui.QLineEdit()
            self.path_button_VarF = QtGui.QPushButton(path_icon, "")
            self.path_button_VarF.setToolTip('Browse for Folder')
            self.template_reset_VarF = QtGui.QPushButton(template_reset_icon, "")
            self.template_reset_VarF.setToolTip('Reset to Project Default')
            self.link_VarF = QtGui.QCheckBox('Relative to Base')
            variable_layout_grid.addWidget(self.Active_VarF,6,0)
            variable_layout_grid.addWidget(self.Descr_VarF,6,1)
            variable_layout_grid.addWidget(self.Path_VarF,6,2)
            variable_layout_grid.addWidget(self.path_button_VarF,6,3)
            variable_layout_grid.addWidget(self.template_reset_VarF,6,4)
            variable_layout_grid.addWidget(self.link_VarF,6,5)


            # Variable Widgets Variable G
            self.Active_VarG = QtGui.QCheckBox()
            self.Descr_VarG = QtGui.QLabel("ARCHIVE (Import/Export):")
            self.Path_VarG = QtGui.QLineEdit()
            self.path_button_VarG = QtGui.QPushButton(path_icon, "")
            self.path_button_VarG.setToolTip('Browse for Folder')
            self.template_reset_VarG = QtGui.QPushButton(template_reset_icon, "")
            self.template_reset_VarG.setToolTip('Reset to Project Default')
            self.link_VarG = QtGui.QCheckBox('Relative to Base')
            variable_layout_grid.addWidget(self.Active_VarG,7,0)
            variable_layout_grid.addWidget(self.Descr_VarG,7,1)
            variable_layout_grid.addWidget(self.Path_VarG,7,2)
            variable_layout_grid.addWidget(self.path_button_VarG,7,3)
            variable_layout_grid.addWidget(self.template_reset_VarG,7,4)
            variable_layout_grid.addWidget(self.link_VarG,7,5)

            asset_group_box.setLayout(variable_layout_grid)


            # Variable Widgets Variable H
            self.Active_VarH = QtGui.QCheckBox()
            self.Descr_VarH = QtGui.QLabel("SHELFS (Import/Export):")
            self.Path_VarH = QtGui.QLineEdit()
            self.path_button_VarH = QtGui.QPushButton(path_icon, "")
            self.path_button_VarH.setToolTip('Browse for Folder')
            self.template_reset_VarH = QtGui.QPushButton(template_reset_icon, "")
            self.template_reset_VarH.setToolTip('Reset to Project Default')
            self.link_VarH = QtGui.QCheckBox('Relative to Base')
            misc_layout_grid.addWidget(self.Active_VarH,8,0)
            misc_layout_grid.addWidget(self.Descr_VarH,8,1)
            misc_layout_grid.addWidget(self.Path_VarH,8,2)
            misc_layout_grid.addWidget(self.path_button_VarH,8,3)
            misc_layout_grid.addWidget(self.template_reset_VarH,8,4)
            misc_layout_grid.addWidget(self.link_VarH,8,5)


            # Variable Widgets Variable I
            self.Active_VarI = QtGui.QCheckBox()
            self.Descr_VarI = QtGui.QLabel("CAM/PROJECTOR (Import/Export):")
            self.Path_VarI = QtGui.QLineEdit()
            self.path_button_VarI = QtGui.QPushButton(path_icon, "")
            self.path_button_VarI.setToolTip('Browse for Folder')
            self.template_reset_VarI = QtGui.QPushButton(template_reset_icon, "")
            self.template_reset_VarI.setToolTip('Reset to Project Default')
            self.link_VarI = QtGui.QCheckBox('Relative to Base')
            misc_layout_grid.addWidget(self.Active_VarI,9,0)
            misc_layout_grid.addWidget(self.Descr_VarI,9,1)
            misc_layout_grid.addWidget(self.Path_VarI,9,2)
            misc_layout_grid.addWidget(self.path_button_VarI,9,3)
            misc_layout_grid.addWidget(self.template_reset_VarI,9,4)
            misc_layout_grid.addWidget(self.link_VarI,9,5)

            misc_group_box.setLayout(misc_layout_grid)


            # APPLY CANCEL BUTTONS
            # Widget OK / Cancel Button
            self.AllBtn = QtGui.QPushButton('Set Paths')
            self.SelectedBtn = QtGui.QPushButton('Cancel')
            # Add Apply Cancel Buttons to Button Layout
            button_layout_box.addWidget(self.AllBtn)
            button_layout_box.addWidget(self.SelectedBtn)


            # Add sub Layouts to main Window Box Layout
            window_layout_box.addWidget(base_group_box)
            window_layout_box.addWidget(asset_group_box)
            window_layout_box.addWidget(misc_group_box)
            window_layout_box.addLayout(button_layout_box)

            #

CloneMergeGUI().exec_()