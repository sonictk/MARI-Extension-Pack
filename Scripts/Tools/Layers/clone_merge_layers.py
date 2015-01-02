# ------------------------------------------------------------------------------
# Clone Merge Layers
# ------------------------------------------------------------------------------
# Clone & Merge Layers will duplicate selected layers and merge them into one.
# Merging is done for either all patches or selected patches.
# ------------------------------------------------------------------------------
# http://mari.ideascale.com
# http://cg-cnu.blogspot.in/
# ------------------------------------------------------------------------------
# Written by Sreenivas Alapati, 2014
# Modified for MARI Extension Pack by Jens Kafitz, 2015
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

from PySide import QtGui
import mari


def clone_merge_layers(mode):
    ''' Creates a merge duplicate of selected layers - patch modes ALL or SELECTED'''
    
    curGeo = mari.geo.current()
    curChan = curGeo.currentChannel()
    curActiveLayerName = str(curChan.currentLayer().name())
    
    patches = list(curGeo.patchList())
    unSelPatches = [ patch for patch in patches if not patch.isSelected() ]
    
    mari.app.setWaitCursor()
    mari.history.startMacro('Clone & Merge Layers')

    copyAction = mari.actions.find('/Mari/Layers/Copy')
    copyAction.trigger()
    
    pasteAction = mari.actions.find('/Mari/Layers/Paste')
    pasteAction.trigger()
    
    curChan.mergeLayers()
    
    curLayer = curChan.currentLayer()

    if mode == 'selected':
        if len(patches) != len(unSelPatches):
        
            imgSet = curLayer.imageSet()
        
            for patch in unSelPatches:
                uv = patch.uvIndex()
                patchImg = imgSet.image(uv, -1)
                patchImg.fill(mari.Color(1,0,0,0))
    
        
    curLayer.setName(curActiveLayerName + '_mrgDup')
    mari.history.stopMacro()
    mari.app.restoreCursor()

    return


# ---------------------------------------------------------------


class CloneMergeGUI(QtGui.QDialog):
    '''GUI to select Clone Merge for selected patches or all patches'''

    def __init__(self):
        super(CloneMergeGUI, self).__init__()
        # Dialog Settings
        self.setFixedSize(300, 100)
        self.setWindowTitle('Clone & Merge Layers')
        # Layouts
        layoutV1 = QtGui.QVBoxLayout()
        layoutH1 = QtGui.QHBoxLayout()
        self.setLayout(layoutV1)
        # Widgets
        self.Descr =  QtGui.QLabel("Clone and merge selected layers for:")
        self.AllBtn = QtGui.QPushButton('All Patches')
        self.SelectedBtn = QtGui.QPushButton('Selected Patches')
        # Populate 
        layoutV1.addWidget(self.Descr)
        layoutV1.addLayout(layoutH1)
        layoutH1.addWidget(self.AllBtn)
        layoutH1.addWidget(self.SelectedBtn)
        # Connections
        self.AllBtn.clicked.connect(self.runCreateAll)
        self.SelectedBtn.clicked.connect(self.runCreateSelected)
        # Init
        # self.run()

    def runCreateSelected(self):
        clone_merge_layers('selected')
        self.close()

    def runCreateAll(self):
    	clone_merge_layers('none')
    	self.close()


