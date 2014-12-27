# ------------------------------------------------------------------------------
# Toggle Layer Visibility/Lock
# Modified for Weta Digital: Jens Kafitz // jkafitz@wetafx.co.nz
# ------------------------------------------------------------------------------
# http://mari.ideascale.com
# ------------------------------------------------------------------------------
# Original Author: Jorel Latraille, The Foundry 2013
# ------------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

import mari

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
    
    curGeo = mari.geo.current()
    curChan = curGeo.currentChannel()

    layerList = list (curChan.layerList())    
    
    layers = [ layer for layer in layerList if not layer.isGroupLayer() ]
    selLayers = [ layer for layer in layers if layer.isSelected() ]
    unSelLayers = [ layer for layer in layers if not layer.isSelected() ]
    
    groups = [ layer for layer in layerList if layer.isGroupLayer() ]
    selGroups = [ group for group in groups if group.isSelected() ]
    unSelGroups = [ group for group in groups if not group.isSelected() ]

    if len(unSelGroups) != 0:
        
        for unSelGroup in unSelGroups:
            layersInGroup = list (getLayersInGroup(unSelGroup))

            for layer in layersInGroup:
                if layer.isGroupLayer():
                    if layer.isSelected():
                        selGroups.append(layer)
                    else:
                        unSelGroups.append(layer)
                else:
                    if layer.isSelected():
                        selLayers.append(layer)
                    else:
                        unSelLayers.append(layer)
    return

def toggleSelVisibility():
    ''' Toggles the visibility of the selected layers '''
    
    if layerData() != -1:
        mari.history.startMacro('Toggle Selected Layer Visibility')
        mari.app.setWaitCursor()

        for layer in selLayers:
            layer.setVisibility(not layer.isVisible())
        for group in selGroups:
            group.setVisibility(not group.isVisible())
        
        mari.app.restoreCursor()
        mari.history.stopMacro()
    
    return

def toggleUnselVisibility():
    ''' Toggles the visibility of the un selected layers '''
    
    if layerData() != -1:
        mari.history.startMacro('Toggle Unselected Layer Visibility')
        mari.app.setWaitCursor()

        for layer in unSelLayers:
            layer.setVisibility(not layer.isVisible())

        mari.app.restoreCursor()
        mari.history.stopMacro()
    
    return

def toggleSelLock():
    ''' Toggles the lock status of the selected layers '''
    
    if layerData() != -1:
        mari.history.startMacro('Toggle Selected Layer Lock')
        mari.app.setWaitCursor()

        for layer in selLayers:
            layer.setLocked(not layer.isLocked())
        for group in selGroups:
            group.setLocked(not group.isLocked())
        
        mari.app.restoreCursor()
        mari.history.stopMacro()
    
    return

def toggleUnselLock():
    ''' Toggles the lock status of the Unselected layers '''
    
    if layerData() != -1:
        mari.history.startMacro('Toggle Unselected Layer Lock')
        mari.app.setWaitCursor()

        for layer in unSelLayers:
            layer.setLocked(not layer.isLocked())

        for group in unSelGroups:
            group.setLocked(not group.isLocked())

        mari.app.restoreCursor()
        mari.history.stopMacro()
    
    return
    

