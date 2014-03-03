Vibrance
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

An adjustment Layer to adjust the Vibrance.
Vibrance will saturate pixels with lower saturation more than ones with higher saturation values.
By choosing "Desaturate" the effect is inverted. Higher saturated colors are desaturated more than lower ones.
Saturation can be remapped (evaluated first) for different effects by modifying the curves.The default curve mimicks what Phototshop and Lightroom do.
For completion a multiplier field exists, however in most cases the default value of 1 will give best results.


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

The Vibrance Node will appear under the Custom Folder in the Adjustment Layer Dialog.


History: ============================================================================


04/12/13 - 1.0 release
11/30/13 - Release for Mari 2.5
12/15/13 - Re-release for Mari 2.5 with new Folder Structure
02/08/14 - New Autoloader Structure




Credits: ============================================================================


 
        