# -------------------------------------------------------------------
# Requirements: This Node Library requires MARI FunctionLibary 
                 1.07 or higher,available at mari.ideascale.com
# -------------------------------------------------------------------
# FBM Pack A - fbm+, multiFBM, vector FBM
# Copyright (c) 2013 Jens Kafitz. All Rights Reserved.
# -------------------------------------------------------------------
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com      
# Web: www.mari.ideascale.com   
# Email: info@campi3d.com
# -------------------------------------------------------------------
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

A Tutorial for the Node Pack is available here:
https://vimeo.com/81253436

More indepth infos based on a previous version is available in this 
video: https://vimeo.com/72116387 

Hover over the Attributes to get a short description of their
functionality.

fBm, vector fbm and multi-fBm procedural nodes useful for weathering,
masking and terrain.

Requirements: =======================================================

- Mari 2.5 or above
- MARI Function Library 1.07 or above (http://mari.ideascale.com/)


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

The new nodes are located under the /Procedurals/Custom/FBM Icon.
They are currently called FBM+ , multiFBM and vec FBM


History: ============================================================


# - 08/12/13
    released for Mari 2.0

# - 08/13/13
    Threshold + SoftClip is now evaluated on a normalized version of
    the noise giving much more even results

# - 12/12/13
    Release for Mari 2.5
    Added compatibility with Mari Function Lib for Transforms
    and Noises - requires MARI Function Lib 1.06 or higher
    Added Vector FBM
    multiFBM Value Mapping is now using a smoother algorithm
    giving more organic results
    Baseline Features added to fbm and vfbm
    Amplitute Features added to all FBMs
    Invert Feature added to all FBMs
    Preview Handle Feature added to multiFBM
    Added Ability to invert just negative noise values ("valleys") by
    using Absolute Value
    Added Thresholding to all FBMs
    Added Ability to propagate negative noise values as either black
    or transparent into the end result
    Removed Propagation Features from multiFBM to reduce node
    handling complexity

# - 02/08/14
    Updated with new Autoloader Structure

# - 03/03/14
    Added UVSpace Transformations, refactored UI

Credits: ============================================================



 
        