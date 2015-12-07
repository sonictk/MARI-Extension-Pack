# ------------------------------------------------------------------------------
# Toggle Layer Visibility/Lock
# ------------------------------------------------------------------------------
# Allows the user to affect Visibility & Lock State of multiple selected layers
# ------------------------------------------------------------------------------
# Written by Sreenivas Alapati, 2014
# Contributions & Extensions: Jens Kafitz, 2015
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


import mari

# ------------------------------------------------------------------------------

def findParentLayerStack(layer,layer_stack):
      "Returns the direct parent layer stack of the layer starting the search from the layer_stack"
      for search_layer in layer_stack.layerList():
          if search_layer==layer:
              return layer_stack
          if search_layer.isGroupLayer():
              result = findParentLayerStack(layer,search_layer.groupStack())
              if result is not None:
                  return result
          elif search_layer.hasMaskStack():
              result = findParentLayerStack(layer,search_layer.maskStack())
              if result is not None:
                  return result
      return None

# ------------------------------------------------------------------------------

def returnTrue(layer):
    """Returns True for any object passed to it."""
    return True

# ------------------------------------------------------------------------------
def getLayerList(layer_list, criterionFn):
    """Returns a list of all of the layers in the stack that match the given criterion function, including substacks."""
    matching_layer = []
    for layer in layer_list:
        if criterionFn(layer):
            matching_layer.append(layer)
        if hasattr(layer, 'layerStack'):
            matching_layer.extend(getLayerList(layer.layerStack().layerList(), criterionFn))
        if layer.hasMaskStack():
            matching_layer.extend(getLayerList(layer.maskStack().layerList(), criterionFn))
        if hasattr(layer, 'hasAdjustmentStack') and layer.hasAdjustmentStack():
            matching_layer.extend(getLayerList(layer.adjustmentStack().layerList(), criterionFn))

    return matching_layer
# ------------------------------------------------------------------------------

def findLayerSelection():
    """Searches for the current selection if mari.current.layer is not the same as layer.isSelected and returns a full list of layers of parent stacks"""

    curGeo = mari.geo.current()
    curChannel = curGeo.currentChannel()
    channels = curGeo.channelList()
    curLayer = mari.current.layer()

    layers = ()
    layerList = ()
    selectionList = []
    layerSelect = False
    parentLayers = []


    # If the current layer is selected I am assuming that the user has the channel selected as well
    if curLayer.isSelected():
        layerList = curChannel.layerList()
        layers = getLayerList(layerList,returnTrue)

        # scan layers in channels for selection and append to selectionList
        for layer in layers:
            if layer.isSelected():
                selectionList.append(layer)
                layerSelect = True

    # If the current layer is not selected go hunting for the selection in all channels
    else:
        for channel in channels:

            layerList = channel.layerList()
            layers = getLayerList(layerList,returnTrue)

            # scan layers in channels for selection and append to selectionList
            for layer in layers:
                if layer.isSelected():
                    selectionList.append(layer)
                    curChannel = channel
                    layerSelect = True


    # if nothing found:
    if not layerSelect:
        mari.utils.message('No Layer Selection found. \n \n Please select at least one Layer.')
        return


    # For each selected layer find the parent layerStack. For example for layers in groups this means the group
    for layer in selectionList:
        parents = findParentLayerStack(layer,curChannel)

        # for each parent LayerStack generate a full list of its layers and append one by one to parentLayers variable
        layer_list = parents.layerList()
        for layer in layer_list:
            parentLayers.append(layer)


    return parentLayers

# ------------------------------------------------------------------------------


def getLayersInGroup(group):
    ''' given a group will return all the layers in the group '''

    groupStack = group.layerStack()
    layerList = groupStack.layerList()

    return layerList

def layerData():
    ''' Updates the global Variables of all the layers, selected Layers,
    unselected layers and groups, selected groups and unselected groups '''

    global layers, selLayers, unSelLayers
    global groups, selGroups, unSelGroups

    if not mari.projects.current():
        mari.utils.message('No project currently open')
        return -1

    layerList = findLayerSelection()

    layers = [ layer for layer in layerList if not layer.isGroupLayer() ]
    selLayers = [ layer for layer in layers if layer.isSelected() ]
    unSelLayers = [ layer for layer in layers if not layer.isSelected() ]

    groups = [ layer for layer in layerList if layer.isGroupLayer() ]
    selGroups = [ group for group in groups if group.isSelected() ]
    unSelGroups = [ group for group in groups if not group.isSelected() ]


    return

def toggleSelVisibility():
    ''' Toggles the visibility of the selected layers '''


    if layerData() != -1:
        mari.history.startMacro('Toggle Selected Layer Visibility')
        mari.app.setWaitCursor()

        # Turning off viewport for better perfromance
        deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
        deactivateViewportToggle.trigger()
        for layer in selLayers:
            layer.setVisibility(not layer.isVisible())
        for group in selGroups:
            group.setVisibility(not group.isVisible())

        mari.app.restoreCursor()
        mari.history.stopMacro()
        deactivateViewportToggle.trigger()


    return

def toggleUnselVisibility():
    ''' Toggles the visibility of the un selected layers '''


    if layerData() != -1:
        mari.history.startMacro('Toggle Unselected Layer Visibility')
        mari.app.setWaitCursor()

        # Turning off viewport for better perfromance
        deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
        deactivateViewportToggle.trigger()

        for layer in unSelLayers:
            layer.setVisibility(not layer.isVisible())
        for group in unSelGroups:
            group.setVisibility(not group.isVisible())

        mari.app.restoreCursor()
        mari.history.stopMacro()
        deactivateViewportToggle.trigger()


    return

def toggleSelLock():
    ''' Toggles the lock status of the selected layers '''


    if layerData() != -1:
        mari.history.startMacro('Toggle Selected Layer Lock')
        mari.app.setWaitCursor()

        # Turning off viewport for better perfromance
        deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
        deactivateViewportToggle.trigger()

        for layer in selLayers:
            layer.setLocked(not layer.isLocked())
        for group in selGroups:
            group.setLocked(not group.isLocked())

        mari.app.restoreCursor()
        mari.history.stopMacro()
        deactivateViewportToggle.trigger()


    return

def toggleUnselLock():
    ''' Toggles the lock status of the Unselected layers '''


    if layerData() != -1:
        mari.history.startMacro('Toggle Unselected Layer Lock')
        mari.app.setWaitCursor()

        # Turning off viewport for better perfromance
        deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
        deactivateViewportToggle.trigger()

        for layer in unSelLayers:
            layer.setLocked(not layer.isLocked())

        for group in unSelGroups:
            group.setLocked(not group.isLocked())

        mari.app.restoreCursor()
        mari.history.stopMacro()
        deactivateViewportToggle.trigger()


    return


