DigiTecK3D Procedural Node Library
Copyright (c) 2013 DigiTecK3D. All Rights Reserved.
=====================================================================                	
Author: Miguel A Santiago Jr.       	
Web: www.digiteck3d.com				
Email: miguel@digiteck3d.com
#----------------------------------------------------------------
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
 
1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
 
2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
 
3. Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.
 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
LIMITED TO,THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF HE
POSSIBILITY OF SUCH DAMAGE.
#----------------------------------------------------------------


Info: ===============================================================

This is a Mari procedural nodelibrary that adds new procedural types
like 

/Procedural/Custom/Voronoi/Cellular
/Adjustment/Custom/Paintable Gabor, 
/Procedural/Custom/Perlin/Inigo
/Procedural/Custom/Perlin/Turbulence
/Procedural/Custom/FBM/Brownian
/Procedural/Custom/multiFractal/Ridged Multi Noise

Known issues: =======================================================

Paintable Gabor is prone to causing Display Driver crashes after a
while when used in the Displacement Preview Slot of a Shader


Requirements: =======================================================

- Mari 2.5 or above
- MARI Function Library 1.07 or above 


Installation: =======================================================


Please download and install the MARI Function Library V1.07 or higher
at mari.ideascale.com


Take scripts and put them into your user preference script directory.
Or any startup script path that Mari has set. Once these are in 
place, Mari on startup will run through the scripts folder and load
the procedural library. Going to the Python tab and showing the 
console will allow you to see the modules loading up. This is where
if in any case the loading fails it will let you know. 


Example:
	• On Linux+Mac: ~/Mari/Scripts/
	• On Windows: Documents/Mari/Scripts/	



Where to find the nodes: ============================================

The new nodes are located under the /Procedurals/Custom/ Icon. 
Paintable Gabor Node is located under /Adjustments/Custom/


History: ============================================================


# - 10/15/13
    Release 1.0 of DT3D Procedural Node Library

# - 12/14/13
    Release of 1.06 of DT3D Procedural Node Library
    Final Python and Folder Structure for mari.ideascale.com
    Exponential Frequency Growth
    Flow Paintable Gabor Noise

# - 02/08/14
    Released with new Autoloader Structure

# - 03/03/14
    Added UVSpace Transformations, refactored UI

# - 04/21/14
    Gabor will no longer throw an error when used in a Displacement
    Preview Shader, however it is discouraged to use it in such a way
    due to stability issues in the Displacement preview.
				



 
        