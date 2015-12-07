# ------------------------------------------------------------------------------
# Clone Merge Layers
# ------------------------------------------------------------------------------
# Clone & Merge Layers will duplicate selected layers and merge them into one.
# Merging is done for either all patches or selected patches.
# ------------------------------------------------------------------------------
# Written by Sreenivas Alapati, 2014
# Contributions & Extension: Jens Kafitz, 2015
# ------------------------------------------------------------------------------
# http://cg-cnu.blogspot.in/
# http://www.campi3d.com
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



def _isProjectSuitable():
    """Checks project state."""
    MARI_3_0V1_VERSION_NUMBER = 30001202    # see below
    if mari.app.version().number() >= MARI_3_0V1_VERSION_NUMBER:

        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False, False

        if mari.app.version().number() >= 30001202:
            return True, True

        return True, False

    else:
        mari.utils.message("You can only run this script in Mari 3.0v1 or newer.")
        return False, False

# ------------------------------------------------------------------------------
# The following are used to find selections no matter where in the Mari Interface:
# returnTru(),getLayerList(),findLayerSelection()
#
# This is to support a) Layered Shader Stacks b) deeply nested stacks (maskstack,adjustment stacks),
# as well as cases where users are working in pinned or docked channels without it being the current channel

# ------------------------------------------------------------------------------

def returnTrue(layer):
    """Returns True for any object passed to it."""
    return True

# ------------------------------------------------------------------------------
def getLayerList(layer_list, criterionFn):
    """Returns a list of all of the layers in the stack that match the given criterion function, including substacks."""
    matching = []
    for layer in layer_list:
        if criterionFn(layer):
            matching.append(layer)
        if hasattr(layer, 'layerStack'):
            matching.extend(getLayerList(layer.layerStack().layerList(), criterionFn))
        if layer.hasMaskStack():
            matching.extend(getLayerList(layer.maskStack().layerList(), criterionFn))
        if hasattr(layer, 'hasAdjustmentStack') and layer.hasAdjustmentStack():
            matching.extend(getLayerList(layer.adjustmentStack().layerList(), criterionFn))
        if layer.isGroupLayer():
            matching.extend(getLayerList(layer.layerStack().layerList(), criterionFn))
        if layer.isChannelLayer():
            matching.extend(getLayerList(layer.channel().layerList(), criterionFn))

    return matching
# ------------------------------------------------------------------------------

def findLayerSelection():
    """Searches for the current selection if mari.current.layer is not the same as layer.isSelected"""

    curGeo = mari.geo.current()
    curChannel = curGeo.currentChannel()
    channels = curGeo.channelList()
    curLayer = mari.current.layer()

    layers = ()
    layerSelList = []
    chn_layerList = ()

    layerSelect = False

    if curLayer.isSelected():
    # If current layer is indeed selected one just trawl through current channel to find others
        layerSelect = True
        chn_layerList = curChannel.layerList()
        layers = getLayerList(chn_layerList,returnTrue)

        for layer in layers:
            if layer.isSelected():
                layerSelList.append(layer)

    else:
    # If current layer is not selected it means that a selection sits somewhere else (non-current channel)
    # so we are going trawling through the entire channel list including substacks to find it

        for channel in channels:

            chn_layerList = channel.layerList()
            layers = getLayerList(chn_layerList,returnTrue)

            for layer in layers:

                if layer.isSelected():
                    curLayer = layer
                    curChannel = channel
                    layerSelect = True
                    layerSelList.append(layer)


    if not layerSelect:
        mari.utils.message('No Layer Selection found. \n \n Please select at least one Layer.')


    return curGeo,curLayer,curChannel,layerSelList

# ------------------------------------------------------------------------------

def clone_merge_layers(mode):
    ''' Creates a merge duplicate of selected layers - patch modes ALL or SELECTED'''

    suitable = _isProjectSuitable()
    if not suitable[0]:
          return

    locked_layers = False

    geo_data = findLayerSelection()
    # Geo Data = 0 current geo, 1 current channel , 2 current layer, 3 current selection list
    curGeo = geo_data[0]
    curChan = geo_data[2]
    curLayer = geo_data[1]
    curSel = geo_data[3]
    curActiveLayerName = str(curLayer.name())

    patches = list(curGeo.patchList())
    unSelPatches = [ patch for patch in patches if not patch.isSelected() ]

    deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
    deactivateViewportToggle.trigger()

    mari.app.setWaitCursor()
    mari.history.startMacro('Clone & Merge Layers')


    copyAction = mari.actions.find('/Mari/Layers/Copy')
    copyAction.trigger()

    pasteAction = mari.actions.find('/Mari/Layers/Paste')
    pasteAction.trigger()

    #running search for selection again in order to get a list of all duplicated layers
    geo_data = findLayerSelection()
    # Geo Data = 0 current geo, 1 current channel , 2 current layer, 3 current selection list
    curGeo = geo_data[0]
    curChan = geo_data[2]
    curLayer = geo_data[1]
    curSel = geo_data[3]
    channelLayerLst = []
    #running search from all current selected layers to get a full list of all associated layers such as masks etc.
    nested_layers = getLayerList(curSel,returnTrue)
    # lookin through all layers that are associated with duplicates if there are any channel layers where we duplicated channels
    for layer in nested_layers:
        if layer.isChannelLayer():
            channelLayerLst.append(layer.channel())
        if layer.isLocked():
            layer.setLocked(False)

    mergeAction = mari.actions.find('/Mari/Layers/Merge Layers')
    mergeAction.trigger()

    # rerunning layer search
    geo_data = findLayerSelection()

    curLayer = geo_data[1]

    if mode == 'selected':
        if len(patches) != len(unSelPatches):

            imgSet = curLayer.imageSet()

            for patch in unSelPatches:
                uv = patch.uvIndex()
                patchImg = imgSet.image(uv, -1)
                patchImg.fill(mari.Color(1,0,0,0))


    curLayer.setName(curActiveLayerName + '_mrgDup')

    # removing any channels we duplicated in the process of copy/paste
    for channel in channelLayerLst:
        try:
            curGeo.removeChannel(channel)
        except Exception:
            continue

    mari.history.stopMacro()
    mari.app.restoreCursor()

    deactivateViewportToggle.trigger()

    return


# ---------------------------------------------------------------


class CloneMergeGUI(QtGui.QDialog):
    '''GUI to select Clone Merge for selected patches or all patches'''

    def __init__(self):
        suitable = _isProjectSuitable()
        if suitable[0]:
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

    def runCreateSelected(self):
        clone_merge_layers('selected')
        self.close()

    def runCreateAll(self):
    	clone_merge_layers('none')
    	self.close()

