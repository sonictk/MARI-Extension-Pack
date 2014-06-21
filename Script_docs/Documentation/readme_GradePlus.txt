# -------------------------------------------------------------------
# GradePlus - A Grade Node with added functionality
# Copyright (c) 2013 Jens Kafitz. All Rights Reserved.
# -------------------------------------------------------------------
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com      
# Web: www.mari.ideascale.com   
# Email: info@campi3d.com
# -------------------------------------------------------------------
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

This is a modification of the default Mari Grade Node. Added features include:


1) modify individual color channels by selecting the RGBA checkboxes
2) Using Colorpicker to set custom colors for each value
   Please note the ColorValue will be multiplied with whatever is set on the sliders unless the result would be black.




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

The Grade+ Node will appear under the Custom Folder in the Adjustment Layer Dialog.


History: ============================================================================

# - 08/17/13 released
# - 11/18/13 Mari 2.5 compatible version released and colorSelectors added
#  -12/14/13 Re-release with new Folder Structure
#  -02/08/14 Autoloader structure added

Credits: ============================================================================

Based on the node developed by the Foundry

 
        