# ------------------------------------------------------------------------------
# Unproject Layer To Image Manager
# Modified for Weta: Jens Kafitz // jkafitz@wetafx.co.nz
# ------------------------------------------------------------------------------
# http://mari.ideascale.com
# ------------------------------------------------------------------------------
# Original Author: Antoni Kujawa
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


import os
import mari



def unprojLayerPaint():
  projectionCamera = mari.actions.get ("/Mari/Canvas/Projection/Create Projector") 
  projectionCamera.trigger()
  mari.projectors.current().setName("CurrentLayer")
  mari.projectors.current().setName("CurrentLayer")
  mari.projectors.current().setUseShader("Current Layer")
  mari.projectors.current().setLightingMode(0)
  mari.projectors.current().setSize (4096, 4096)
  mari.projectors.current().setBitDepth (8)
  unprojDir = os.path.expanduser('~') + "/"
  unprojectFileLoc = "{1}{0}.png".format(mari.projectors.current().name(), unprojDir)
  print unprojectFileLoc
  mari.projectors.current().unprojectToFile(unprojectFileLoc)
  mari.projectors.remove("CurrentLayer")
  mari.images.load(unprojectFileLoc)
  mari.tools.setCurrent("Paint Through")
  return 

def unproject_layer_to_imageman():

  unprojLayerPaint()
