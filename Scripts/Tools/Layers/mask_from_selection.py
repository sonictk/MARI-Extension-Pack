# ------------------------------------------------------------------------------
# Mask From Selection
# Modified for Weta Digital: Jens Kafitz // jkafitz@wetafx.co.nz
# ------------------------------------------------------------------------------
# http://mari.ideascale.com
# ------------------------------------------------------------------------------
# Original Author: Ben Neal
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


def selectionMask(invert):
	currentObj = mari.geo.current()
	currentChan = currentObj.currentChannel()
	currentLayer = currentChan.currentLayer()
	selectedPatches = currentObj.selectedPatches()
	
	newMaskImageSet = currentLayer.makeMask()
	mari.history.startMacro('Create custom mask')
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

