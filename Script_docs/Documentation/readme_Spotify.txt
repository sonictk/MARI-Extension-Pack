Spotify Fractal
Copyright (c) 2013 Jens Kafitz. All Rights Reserved.
=====================================================================================  
                      	
Author: Jens Kafitz      	
Web: www.campi3d.com			
Email: jens@campi3d.com
    		
License: ============================================================================

This program is free software: you can redistribute it and/or modify it under the terms 
of the GNU General Public License as published by the Free Software Foundation, either 
version 3 of the License, or (at your option) any later version.										
																			
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details.								
																			
You should have received a copy of the GNU General Public License along with this program.  
If not, see <http://www.gnu.org/licenses/>.

Info: =============================================================================== 


A new multiFractal Node for Mari useful for aging effects, unique patterns and terrain


Requirements: =======================================================================

- Mari 2.5 or above
- MARI Function Library 1.06.005 or above (http://mari.ideascale.com/)



Installation: =======================================================================


Please download and install the MARI Function Library V1.06 or higher at 
http://mari.ideascale.com/


Take scripts and put them into your user preference script directory. Or any startup
script path that Mari has set. Once these are in place, Mari on startup will run through
the scripts folder and load the procedural library. Going to the Python tab and showing
the console will allow you to see the modules loading up. This is where if in any case
the loading fails it will let you know. 


Example:
	• On Linux: /Mari/Scripts/
	• On Windows: Documents/Mari/Scripts/	



Where to find the nodes: ============================================================

The new nodes are located under the /Procedurals/Custom/multiFractal Icon - or simply press TAB
with the cursor in the Layer Palette and type "Spotify"


History: ============================================================================

# - 04/15/13	1.0 Release
# - 08/02/13 	Fixed Issue where the node breaks sometimes when multiple copies are in the same layerstack
# - 11/30/13	1.1 Release for Mari 2.5.
# 				New Default Values to better show what the node can do
# 				Replaced transform controls with the ones from the MARI Function Library
# 				Added Thresholding Controls
# - 12/15/13	Re-released for Mari 2.5 with new Folder Structure
# - 02/08/14	Autoloader structure
# - 02/10/14	Color A/B added