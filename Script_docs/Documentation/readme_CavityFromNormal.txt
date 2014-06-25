#----------------------------------------------------------------
# Requirements: This Node requires Mari 2.5 or higher
#----------------------------------------------------------------
# Cavity from Tangent Space Normal
# Copyright (c) 2014 Antoni Kujawa. All Rights Reserved.
#----------------------------------------------------------------
# Author: Antoni Kujawa
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

Info:
=================================================================

This is a cavity map adjustment that requires a tangent space normal 
map to work (it is essentially emulating what xNormal does).
It works best with hard surface details. I would recommend applying 
it to a 16bit Normal Map for best results.

Please note, this is not necessarily a true cavity map generation but
a very rough approximation. 

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


Where to find the nodes:
============================================================

The new nodes are located under Adjustments/Custom/


History:
=================================================================

# - 04/05/14
    v1.0 Release

# - 06/21/16 
    v1.05 Release, fixed a bug when evaluating tangent space.



 
        