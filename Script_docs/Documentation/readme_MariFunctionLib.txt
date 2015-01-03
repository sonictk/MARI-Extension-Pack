MARI Function Library 1.09
Copyright (c) 2015 MARI.IDEASCALE.COM All Rights Reserved.
===================================================================== 
                      	
Contributors: =======================================================

Author: Miguel A Santiago Jr.       	
Web: www.digiteck3d.com				
Email: miguel@digiteck3d.com

Author: Jens Kafitz
Web: www.campi3d.com				
Email: MariIdeas@campi3d.com

Author: Nicholas Breslow
Web: http://nbreslow.com/			
Email: nick@nbreslow.com

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

This is a Mari procedural library that adds new procedural functions
like Cellular, Gabor, Perlin, Value, Simplex, Brownian, Turbulence,
Inigo Multi-Fractal, Ridged Fractal noise and  more.

This isn't simply just a shader library that adds new nodes 
to Mari, but overall adds new functionality to the shader API that 
other shader writers can access and modify to create there own 
shaders from the various new noise functions added in code to the 
Mari shader API. 

This is the core of the library that allows to implement various other standard
noise functions that are normally found in basic procedural 
libraries. The library also finally adds back in the full featured 
cellular noise function with various feature sets to mimic organic
cellular patterns. Along with these new additions the library 
also introduces a port of the Gabor noise function into the library,
This is a special type of noise with anisotropic noise properties.

Best of all the library falls into the open source domain under
the 3-Clause BSD License and will include all of the source 
code for you to modify, learn, or just continue to improve and add
to it yourself. So you are free to do with it what you will.


A collabarative space for development is available here:

https://github.com/campi3d/IdeascaleNodePack


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


History: ============================================================

# - 10/15/13
    V1.0 Release of Procedural Function Library

# - 12/14/13
    V1.06 Release of Procedural Function Library
    Fixed bug in vec4 softThreshold Function

# - 07/01/13
    MAC+Linux Fixes

# - 02/08/14
    V1.06.005 release with new autoloader structure

# - 02/11/14
    Fixed a bug with vec3+vec4 remaps

# - 03/03/14
    v1.07 release. NB_ Function Branch added, various additions in 
    ID + DT3D Library
    Updated SDK Documentation

# - 04/21/14
    v1.07.05 release. Fixed a problem with UV Transformations, 
    added FullVibrance() Function






 
        