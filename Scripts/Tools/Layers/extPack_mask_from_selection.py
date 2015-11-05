# ------------------------------------------------------------------------------
# Mask from Selection
# ------------------------------------------------------------------------------
# Creates a Mask based on selected patches
# ------------------------------------------------------------------------------
# http://mari.ideascale.com
# http://bneall.blogspot.de/
# ------------------------------------------------------------------------------
# Written by Ben Neal, 2014
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


# -------------------------------------------------------------------

# ------------------------------------------------------------------------------    
# The following are used to find multi selections no matter where in the Mari Interface:
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
   
        chn_layerList = curChannel.layerList()
        layers = getLayerList(chn_layerList,returnTrue)
        
        for layer in layers:
    
            if layer.isSelected():

                layerSelList.append(layer)
                layerSelect = True       

    else:
    
        for channel in channels:
            
            chn_layerList = channel.layerList()
            layers = getLayerList(chn_layerList,returnTrue)
        
            for layer in layers:
    
                if layer.isSelected():
                    curLayer = layer
                    curChannel = channel
                    layerSelList.append(layer)
                    layerSelect = True

    
    if not layerSelect:
        mari.utils.message('No Layer Selection found. \n \n Please select at least one Layer.')


    return curGeo,curLayer,curChannel,layerSelList


# ------------------------------------------------------------------------------

def selectionMask(invert):
 	suitable = _isProjectSuitable()
 	if not suitable[0]:
 	      return

	mari.history.startMacro('Create Mask from Selection')

	geo_data = findLayerSelection()
	currentObj = geo_data[0]
	currentLayer = geo_data[1]
	currentSelection = geo_data[3]
	selectedPatches = currentObj.selectedPatches()

	
	for layer in currentSelection:

		currentLayer = layer

		if currentLayer.isShaderLayer():

			if currentLayer.hasMaskStack():
				layerMaskStack = currentLayer.maskStack()
				newMask = layerMaskStack.createPaintableLayer('MaskFromSelection')
				newMaskImageSet = newMask.imageSet()
			else:
				layerMaskStack = currentLayer.makeMaskStack()
				newMask = layerMaskStack.createPaintableLayer('MaskFromSelection')
				newMaskImageSet = newMask.imageSet()

		else:

			if currentLayer.hasMaskStack():
				layerMaskStack = currentLayer.maskStack()
				newMask = layerMaskStack.createPaintableLayer('MaskFromSelection')
				newMaskImageSet = newMask.imageSet()		

			elif currentLayer.hasMask():
				layerMaskStack = currentLayer.makeMaskStack()
				newMask = layerMaskStack.createPaintableLayer('MaskFromSelection')
				newMaskImageSet = newMask.imageSet()
			else:
				newMask = currentLayer.makeMask()
				newMaskImageSet = newMask
	
	
		for image in newMaskImageSet.imageList():
			if invert == False:
				image.fill(mari.Color(0.0, 0.0, 0.0, 1.0))
			else:
				image.fill(mari.Color(1.0, 1.0, 1.0, 1.0))
		
		for patch in selectedPatches:
			selectedImage = currentObj.patchImage(patch, newMaskImageSet)
			if invert == False:
				selectedImage.fill(mari.Color(1.0, 1.0, 1.0, 1.0))
			else:
				selectedImage.fill(mari.Color(0.0, 0.0, 0.0, 1.0))

	mari.history.stopMacro()

