Texture Scatter UV (TILE)
Copyright (c) 2015 Jens Kafitz. All Rights Reserved.
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



ATTENTION WINDOWS USERS: ============================================

Due to the complexity of the Node when baking, flattening or 
converting to paintable this Node will cause a Display Driver Timeout
 under Windows when used with Maris default settings.

This is due to a Windows "Feature" in the registry defining that after
two seconds of seemingly no activity on your GPU the Driver is 
considered crashed (even if it isn't).


WORKAROUND:

In order to avoid the display driver Crash we need to ensure Mari 
splits the processing during the flattening operation into small 
chunks especially when a lot of textures & layers are used in the node 
(it works out of the boxwith lower settings generally)

This is achieved in MARI by switching the Max Render Size for 
Baking to a low Value:

- EDIT/PREFERENCES/GPU TAB
- MAX RENDER SIZE FOR BAKING: 256 (default is 1024)

It is generally fine to keep at 256 and will speed up baking of 
complex procedural setups.  Otherwise please reset to default after 
use of TextureScatter_UV Node.



Info: ===============================================================

A UV based Texture Bombing Node that is capable of producing tileable
textures when applied to a standard plane.
(exported for example out or MAYA)


Installation: ======================================================

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

The TextureScatter_UV Node will appear under the Procedural/Environment/Custom/ Folder


Options: =============================================================

     -------------------- Density ------------------------

     Layers
     The amount of loops the Node runs to fill the uvs.
     1 Layer means no or very little features will overlap.
     Increasing this setting will linearly slow this node down
     (4 layers twice as slow as 2 layers etc.)

     Density
     The Density of Features on each Layer. Increasing this
     Value does not affect performance

     Clumping
     Higher Values here will selectively cull any textures to create
     pcokets of features. Use the NoiseScale to Randomize the pocket
     distribution.


     NoiseScale
     The Scale of the Noise used to create all randomization
     of the Node (Distribution, HSV Shift etc.)
     Low Values here generally lead to sparser distribution of
     features.

     --------------------  Scale -------------------------

     Scene Size
     A Multiplier on a variety of Values to easily compensate
     for scale of your scene

     Scale
     The Scale of each textured "cell" that is being generated

     ScaleRnd
     Applies a Scale Randomization to each cell. Lower values here
     will give less large scale jumps

     % Original
     A percentage of all cells to keep at their original size without
     applied ScaleRnd.

     -------------------- Rotation -----------------------

     Min Rotation / Max Rotation
     A rotational range that all cells get processed through.

     -------------------- HSV Shift ----------------------

     Cell Blend Mode
     The Blend Mode that is being used inbetween cells.
     This is different from the regular Layer Blend Mode.
     The cells will be blended together based on the Cell Blend Mode,
     then the result of this will be blended with other layers based
     on the regular layer blend mode

     Min Hue/Max Hue
     A Hue Shift Range that all cells get processed through

     Min Sat/Max Sat
     A Saturation Shift Range that all cells get processed through

     Min Val/Max Val
     A Value Shift Range that all cells get processed through

     Clamp
     For example when a cell blend mode of "add" is used, it is
     possible for values to go over 1.0. This generally affects the
     result of masks etc. Clamping will cut off all values above
     1.0 and below 0.0.

     Value Offset
     A global value offet (plus/minus) that is applied to all cells.
     This can be used in conjunction with the Layer Attenuation
     (see below)

     Layer Attenuation
     A value that is added/subtracted from your textures 
     for each layer the Node generates. This is very useful to 
     create proper height maps. 
     For example when used on leaves, leaves that are above other
     leaves will be brighter.

     -----------------Texture Map A,B,C,D -------------------

     Activate Texture (B,C,D)
     Turn on the use of Texture Maps B,C or D. Please Note
     Texture Map A is always in use.

     Importance
     Determines the Percentage each Texture is going to contribute
     to the final result.
     Please note this is evaluated one after the other.
     So for example an importance of 1.0 on TextureMapA and 1.0 on
     TextureMapB will cause TextureMapB to override TextureMapA.

     Map A,B,C,D
     The Texture to be used for scattering. Alphas/Transparency
     are supported.

     Invert Map
     Will invert the Texture Map used.

     Alpha
     Determines how the Alpha of the Map should be treated:

     	- From Map
     	Uses Transparency saved in Texture Map

     	- Alpha is Luminance
     	White Values in your Map will be used to determine opacity.
     	Black is transparent.

      	- Alpha is inverted Luminance
     	Black Values in your Map will be used to determine opacity.
     	White is transparent. 

     Scale
     A scale factor that is being applied to the texture in the slot.
     For example if Scale for textureMapA is set to 5 and Scale for
     textureMapB is set to 10, mapA will always be halve the size
     of MapB.

     HSV Shift Mix
     A Blend Factor on the HSV Shift Group determining how much of
     the HSV Shift is used on the texture Map.

     Edge Falloff
     Will cut the Alpha of the Map from the edges towards the center

     Edge Softness
     Determines the Softness & Length of the Edge Falloff. Lower
     Values will produce a more hard edged result

     Edge Roundness
     Determines if the Alpha Clipping is done as a Square Fade or
     Radial Fade. High Values will clip the Alpha more circular.



Requirements: =======================================================

- Mari 2.6 or above



History: ============================================================

# - 11/25/14
		1.0 Release




Credits: ============================================================================


 
        