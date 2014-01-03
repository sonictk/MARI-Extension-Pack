setRange
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

A simple remap node with optional component (r,g,b,a) remapping and global Scale Factor.
Useful for example
1) to make 32bit displacement maps
2) define custom specular values from a black to white map
3) Do simple level/contrast adjustments


Requirements: =======================================================================

- Mari 2.5 or above


Installation: =======================================================================



Take scripts and put them into your user preference script directory. Or any startup
script path that Mari has set. Once these are in place, Mari on startup will run through
the scripts folder and load the procedural library. Going to the Python tab and showing
the console will allow you to see the modules loading up. This is where if in any case
the loading fails it will let you know. 


Example:
	• On Linux: /Mari/Scripts/
	• On Windows: Documents/Mari/Scripts/	



Where to find the nodes: ============================================================

The Grade+ Node will appear under the Custom Folder in the Adjustment Layer Dialog.


History: ============================================================================

04/02/13 A bug in the clamping was fixed that prevented the node from being flattened correctly

05/20/13 Node re-released for Mari 2.0

11/30/13 Mari 2.5 Version released

12/14/13 Re-released for Mari 2.5 with new Folder Structure



Credits: ============================================================================


 
        