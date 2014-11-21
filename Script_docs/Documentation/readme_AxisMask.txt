# ---------------------------------------------------------------
# Requirements: Requires Mari 2.5 (+) and MARIFunctionLibary 1.06 (+)
# Available at: http://mari.ideascale.com/
#----------------------------------------------------------------
# Axis Mask - A simplified way to mask an object based on directions.
# Copyright (c) 2013 Jens Kafitz. All Rights Reserved.
#----------------------------------------------------------------
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com
# Web: www.mari.ideascale.com
# Email: MariIdeas@campi3d.com
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


Information and Usage: ===========================================

The Axis Mask node simplifies the process of masking an object based
on directions.
Previously you would be required to add a Object Normal or
Custom Object Normal Node and use multiple Adjustments to try and
isolate the correct axis, adding multiple substacks to your main 
layer stack.

The Axis Mask combines multiple steps into one single easy to use and
create Mask Node. Simply select the Axis you wish to Mask out 
(multiples are possible).

A Falloff Control allows you to finetune the gradient, while the 
jitter allows for some randomization of the mask.

Other features include ScreenMode ("Black is transparent") and 
post-rotation for masks that aren't supposed to be aligned perfectly
in object space.



Requirements: =======================================================

- Mari 2.5 or above
- MARI Function Library 1.06.005 or above 


Installation: =======================================================


Please download and install the MARI Function Library V1.06 or higher
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

The new nodes are located under the Procedural Icon in 
Folder Geometry/Custom


History: ============================================================

# History:
# - 02/1/14
    1.0 Release

# - 02/08/14
    1.01 Release with new Autoloader Structure
    
# - 04/21/14
    1.02 Release.
    Fixed an Error when used in a Channel plugged
    into Displacement preview


Credits: ============================================================

Based on Custom Surface Normal available at mari.ideascale.com

 
        