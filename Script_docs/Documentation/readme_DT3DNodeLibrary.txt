DigiTecK3D Procedural Node Library
Copyright (c) 2013 DigiTecK3D. All Rights Reserved.
=====================================================================================  
                      	
Author: Miguel A Santiago Jr.       	
Web: www.digiteck3d.com				
Email: miguel@digiteck3d.com
    		
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

This is a Mari procedural nodelibrary that adds new procedural types like 

/Procedural/Custom/Voronoi/Cellular
/Adjustment/Custom/Paintable Gabor, 
/Procedural/Custom/Perlin/Inigo
/Procedural/Custom/Perlin/Turbulence
/Procedural/Custom/FBM/Brownian
/Procedural/Custom/multiFractal/Ridged Multi Noise

Known issues: =======================================================================

Paintable Gabor is prone to causing Display Driver crashes after a while when used in the Displacement Preview
Slot of a Shader


Requirements: =======================================================================

- Mari 2.5 or above
- MARI Function Library 1.07 or above 



Installation: =======================================================================


Please download and install the MARI Function Library at mari.ideascale.com


Take scripts and put them into your user preference script directory. Or any startup
script path that Mari has set. Once these are in place, Mari on startup will run through
the scripts folder and load the procedural library. Going to the Python tab and showing
the console will allow you to see the modules loading up. This is where if in any case
the loading fails it will let you know. 

Example:
	• On Linux+Mac: ~/Mari/Scripts/
	• On Windows: Documents/Mari/Scripts/	


Where to find the nodes: ============================================================

The new nodes are located under the /Procedurals/Custom/ Icon. 
Paintable Gabor Node is located under /Adjustments/Custom/


History: ============================================================================


# - 10/15/13	Release 1.0 of DT3D Procedural Node Library
# - 12/14/13	Release of 1.06 of DT3D Procedural Node Library
#				Final Python and Folder Structure for mari.ideascale.com
#				Exponential Frequency Growth
#				Flow Paintable Gabor Noise
# - 02/08/14    Released with new Autoloader Structure
# - 03/03/14    Added UVSpace Transformations, refactored UI
# - 04/21/14    Gabor will no longer throw an error when used in a Displacement Preview Shader,
				however it is discouraged to use it in such a way due to stability issues in the Displacement preview.
				



 
        