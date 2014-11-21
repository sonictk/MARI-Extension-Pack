Polysurface Curvature
Copyright (c) 2013 Jens Kafitz. All Rights Reserved.
=====================================================================
                      	
Author: Jens Kafitz      	
Web: www.campi3d.com			
Email: MariIdeas@campi3d.com

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

A Node to detect surface curvature for use in masking.
Due to limitations in openGl no smoothing of values is done.'
Your result will be only as good as your mesh is highres/dense enough.
There will always be some sort of faceting visible which is why it 
is usually best to bury the node as a part of a mask stack or 
apply a gaussian filter afterwards.


Requirements: =======================================================

- Mari 2.5 or above
- MARI Function Lib 1.06.005 (+) available at mari.ideascale.com



Installation: =======================================================


Please download and install the MARI Function Library V1.06.005 
or higher at mari.ideascale.com


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

The new node is located under the /Procedurals/Geometry Icon - 
or simply press TAB with the cursor in the Layer Palette and 
start typing "PolySurface Curvature"


History: ============================================================

# - 12/16/13
    First Release for Mari 2.5.

# - 02/08/14
    New Autoloader Structure

# - 04/21/14
    Fixed Shader Error when Node used in a Displacement Preview