
# ------------------------------------------------------------------------------
# Requirements: This Node requires Mari 2.5 (+) and MARI FunctionLibrary 1.06 (+)
# Available at: http://mari.ideascale.com/
# ------------------------------------------------------------------------------
# Mari Ideascale - Axis Mask
# Copyright (c) 2014 Jens Kafitz. All Rights Reserved.
# ------------------------------------------------------------------------------
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com
# Web: www.mari.ideascale.com
# Email: info@campi3d.com
# ------------------------------------------------------------------------------
# History:
# - 02/1/14	1.0 Release
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


def registerAxisMask():
	"Register Axis Mask - a simple way to set directonality of model "
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomProceduralLayerFromXMLFile("Geometry/Custom/Axis Mask", mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Geometry/JK_AxisMask.xml")
		print 'Registered Geometry Node : Axis Mask'
	except Exception as exc:
		print 'Error Registering Geometery Node : Axis Mask: ' + str(exc)


# ------------------------------------------------------------------------------

registerAxisMask()