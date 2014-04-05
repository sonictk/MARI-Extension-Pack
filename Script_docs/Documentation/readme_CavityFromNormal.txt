# ------------------------------------------------------------------------------
# Requirements: This Node requires Mari 2.5 or higher
# ------------------------------------------------------------------------------
# Cavity from Tangent Space Normal
# Copyright (c) 2014 Antoni Kujawa. All Rights Reserved.
# ------------------------------------------------------------------------------
# Author: Antoni Kujawa
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


Info: =============================================================================== 

This is a cavity map adjustment that requires a sculpted tangent space normal map to work
(its essentially emulating what xNormal does).
It works best with hard surface details. I would recommend applying it to a 16bit Normal Map for best results.

Requirements: =======================================================================

- Mari 2.5 or above

Installation: =======================================================================


Take scripts and put them into your user preference script directory. Or any startup
script path that Mari has set. Once these are in place, Mari on startup will run through
the scripts folder and load the procedural library. Going to the Python tab and showing
the console will allow you to see the modules loading up. This is where if in any case
the loading fails it will let you know. 


Example:
	• On Linux+Mac: ~/Mari/Scripts/
	• On Windows: Documents/Mari/Scripts/	



Where to find the nodes: ============================================================

The new nodes are located under Adjustments/Custom/


History: ============================================================================

04/05/14 v1.0 Release



 
        