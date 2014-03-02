polysurface Curvature
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

A Node to detect surface curvature for use in masking.
Due to limitations in openGl no smoothing of values is done.'
Your result will be only as good as your mesh is highres/dense enough.
There will always be some sort of faceting visible which is why it is usually
best to bury the node as a part of a mask stack or apply a gaussian filter afterwards.


Requirements: =======================================================================

- Mari 2.5 or above
- MARI Function Lib 1.06.005 or higher available at mari.ideascale.com



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

The new node is located under the /Procedurals/Geometry Icon - or simply press TAB
with the cursor in the Layer Palette and start typing "PolySurface Curvature"


History: ============================================================================

# - 12/16/13 - First Release for Mari 2.5. 
# - 02/08/14 - New Autoloader Structure