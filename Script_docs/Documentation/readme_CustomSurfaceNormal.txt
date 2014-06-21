#----------------------------------------------------------------# Requirements: This Node Library requires MARI FunctionLibary 1.06.005
# Available at: http://mari.ideascale.com/
#----------------------------------------------------------------# Custom Object Normal - added controls to influence normal orientation
# Copyright (c) 2013 Jens Kafitz. All Rights Reserved.
#----------------------------------------------------------------# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com
# Web: www.mari.ideascale.com
# Email: info@campi3d.com
#----------------------------------------------------------------# This program is free software: you can redistribute it and/or modify
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


Information:
=================================================================

This is a modification of the default Mari Object Normal. Added functionality includes Transform (rotate,translate, scale) controls




Requirements: =================================================================

- Mari 2.5 or above
- MARI Function Library 1.06.005 or above 


Installation: =================================================================

Please download and install the MARI Function Library V1.06 or higher at mari.ideascale.com


Take scripts and put them into your user preference script directory. Or any startup
script path that Mari has set. Once these are in place, Mari on startup will run through
the scripts folder and load the procedural library. Going to the Python tab and showing
the console will allow you to see the modules loading up. This is where if in any case
the loading fails it will let you know. 


Example:
	• On Linux+Mac: ~/Mari/Scripts/
	• On Windows: Documents/Mari/Scripts/	



Where to find the nodes: ============================================================

The new nodes are located under the Procedural Icon in Folder Geometry/Custom


History: =================================================================

# History:
# - 04/15/13	1.0 Release
# - 11/15/13	1.1 Release for Mari 2.5, modified for 					consistency with DT3D Function Lib
# - 12/14/13	Release for Mari 2.5 with python structure
# - 02/08/13	Release with new Autoloader Structure
# - 04/21/13	Fixed a bug when Node was used in Shader 					Displacement Preview

Credits: =================================================================

Based on the node developed by the Foundry

 
        