# ------------------------------------------------------------------------------
# Channel Layer Tools
# ------------------------------------------------------------------------------
# Channel Layer Tools simplify the process of using the result of a Channel
# in another Channel. 3 Options exist: Add Channel Layer, Add Channel Layer as Mask, Add grouped Channel Layer Mask
# ------------------------------------------------------------------------------
# http://mari.ideascale.com
# http://bneall.blogspot.de/
# ------------------------------------------------------------------------------
# Author: Ben Neal, 2014
# Contributions: Jens Kafitz, 2015
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
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:
    
        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False, False

        if mari.app.version().number() >= 20603300:
            return True, True

        return True, False
        
    else:
        mari.utils.message("You can only run this script in Mari 2.6v3 or newer.")
        return False, False



def makeChannelLayer(sourceChannel, mode, invert):

	geo =  mari.geo.current()
	channels = geo.channelList()
	currentChannel = mari.geo.current().currentChannel()
	currentLayer = mari.current.layer()
	layerName = currentLayer.name()
	channelLayerName = sourceChannel.name()

	if not currentLayer.isSelected():

		for channel in channels:
		    layers = channel.layerList()
		    for layer in layers:
		        
		        if layer.isSelected():
					currentChannel = channel
					currentLayer = layer
					break
		        if layer.hasMaskStack():
		            layerMask = layer.maskStack()
		            layerMaskList = layerMask.layerList()
		            for maskLayer in layerMaskList:
		                if maskLayer.isSelected():
							currentChannel = layerMask
							currentLayer = maskLayer
							break
           

	if mode == 'layer':
		mari.history.startMacro('Create channel Layer')
		currentChannel.createChannelLayer(channelLayerName, sourceChannel, None, 16)
		mari.history.stopMacro()
	else:
		
		
		if mode == 'maskgroup':
			if currentLayer.isShaderLayer():
				mari.utils.message('Groups are not supported for Shader Layers')
				return
			else:
				try:
					## New Group Layer
					mari.history.startMacro('Create grouped channel mask')
					layerGroupName = '%s_grp' % layerName
					groupLayer = currentChannel.groupLayers([currentLayer], None, None, 16)
					groupLayer.setName(layerGroupName)
					layerMaskStack = groupLayer.makeMaskStack()
					layerMaskStack.removeLayers(layerMaskStack.layerList())	
				except Exception:
					pass

		elif mode == 'mask':
			mari.history.startMacro('Create channel mask')

			## New Layer Mask Stack.
			## If mask exists convert, if stack exists keep, else make new stack
			if currentLayer.hasMaskStack():
				layerMaskStack = currentLayer.maskStack()
			elif currentLayer.hasMask():
				layerMaskStack = currentLayer.makeMaskStack()
			else:
				layerMaskStack = currentLayer.makeMaskStack()
				layerMaskStack.removeLayers(layerMaskStack.layerList())			

		
		## Create Mask Channel Layer
		maskChannelLayerName = '%s(Shared Channel)' % channelLayerName
		layerMaskStack.createChannelLayer(maskChannelLayerName, sourceChannel)

		if invert == 1:
			layerMaskStack.createAdjustmentLayer("Invert","Filter/Invert")
	
		mari.history.stopMacro()

class ChannelLayerUI(QtGui.QDialog):
	'''GUI to select channel to make into a channel-layer in the current channel
	modes: 'groupmask', 'mask', 'layer'
	'''
	def __init__(self, mode):
		suitable = _isProjectSuitable()
		if suitable[0]:
			super(ChannelLayerUI, self).__init__()
			## Dialog Settings
			self.setFixedSize(300, 100)
			self.setWindowTitle('Select Channel')
			## Vars
			self.mode = mode
			## Layouts
			layoutV1 = QtGui.QVBoxLayout()
			layoutH1 = QtGui.QHBoxLayout()
			self.setLayout(layoutV1)
			## Widgets
			self.chanCombo = QtGui.QComboBox()
			self.okBtn = QtGui.QPushButton('Ok')
			self.cancelBtn = QtGui.QPushButton('Cancel')
			self.invertBtn = QtGui.QCheckBox('Invert')
			## Populate 
			layoutV1.addWidget(self.chanCombo)
			layoutV1.addLayout(layoutH1)
			layoutH1.addWidget(self.cancelBtn)
			layoutH1.addWidget(self.okBtn)
			if mode is not 'layer':
				layoutH1.addWidget(self.invertBtn)
			## Connections
			self.okBtn.clicked.connect(self.runCreate)
			self.cancelBtn.clicked.connect(self.close)
			## Init
			self.init()
	
	def init(self):
		currentChannel = mari.geo.current().currentChannel()
		channelList = mari.geo.current().channelList()
		for channel in channelList:
			shaderChannel = channel.isShaderStack()
			if channel is not currentChannel and not shaderChannel:
				self.chanCombo.addItem(channel.name(), channel)
	
	def selectedChannel(self):
		return self.chanCombo.itemData(self.chanCombo.currentIndex(),32)

	def invertChannel(self):
		return self.invertBtn.isChecked()

	
	def runCreate(self):
		sourceChannel = self.selectedChannel()
		invert = self.invertChannel()
		makeChannelLayer(sourceChannel, self.mode,invert)
		self.close()

		
