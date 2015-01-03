# -------------------------------------------------------------------
# Requirements: This Node Library requires MARI FunctionLibary 
                 1.08 or higher,available at mari.ideascale.com
# -------------------------------------------------------------------
# Voronoi Popcorn
# Copyright (c) 2015 Jens Kafitz. All Rights Reserved.
# -------------------------------------------------------------------
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com      
# Web: www.mari.ideascale.com   
# Email: MariIdeas@campi3d.com
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

Sample Settings are available here: https://vimeo.com/103744817
... or in your Script_docs/samples folder.

A voronoi based Fractal useful for veins, soft gravel like 
displacements etc.

A base voronoi is created then offset but secondary noises (large
Edge Detail & Small Edge Detail.)
Both Voronoi and Edge Detail are run through a fractalization 
(multiple octaves) for further randomness.


     -------------------- Color ------------------------

     Color A/B
     Self explanatory, assign two colors. Transparency/Alpha is
     supported

     Invert
     Invert the result of the Noise before Color A/B is applied

     ---------------- Voronoi Procedure ------------------------ 
     Popcorn
     Generates Soft round cells

     Coffee Bean
     Generates cells with hard geometric shapes

     Sparse Corn
     Soft cells with a very sparse distribution

     Crumpled Paper
     Cells with an outline but a soft centre


      ---------------- Voronoi Base ------------------------ 

     Primary Scale
     This is the main Scale Factor for all noise operations run
     in this procedural.


     Seed
     A random Offset applied o the noise(s)

     ---------------- Threshold ------------------------  

     Threshold
     Defines the 'tipping point' at which point color A vs color B is
     applied. Please note since the incoming noise has a very large 
     range the Threshold is ranged far greater than 0-1 to allow
     for maximum fidelity for bump/displacments without plateau
     effects.

     Soft Clip
     Applies a outer/inner bound to the Threshold to soften
     transitions.Please note since the incoming noise has a very large 
     range the Soft Clip is ranged far greater than 0-1 to allow
     for maximum fidelity for bump/displacments without plateau
     effects.


     Contrast
     Contrast acts like a "Gain" on the end result of the noise
     operation. Basically it is Noiseresult * contrast, sharpening
     the result.


    ---------------- Relationship Color A/B -------------------

    Density
    Density will affect how much Color B you are likely to see.
    Under the hood it is the amount of octaves run at the final
    fractalization process. Please note that this works
    off full number (1,2,3 etc.) which is why you are seeing
    stepping when moving the slider

    In pseudo code it runs:
    For each number until B Density is reached run the 
    voronoiPopcorn times the B Density Gain.

   Density Gain
   DensityGain will affect how much Color B you are likely to see
    and acts as a multiplier of Density for each octave of the
    noise.
    For each number untilDensity is reached run the 
    voronoiPopcorn times the Density Gain.



    ---------------- Secondary Noise -------------------


     Secondary Scale
     The secondary Scale (also called "Lacunarity") affects the
     fractalization that is run at the end of this procedural.
     When it is set to 0 (or 1) it will be as if it is turned off.
     It will affect the scale of the B Density/B Density Gain under
     the Color A/B Relationship Group. For smoother less noisy
     results leave this off (at 0).


     Density
     Density will affect how much Color A you are likely tosee    .
     It is run as part of the voronoiPopcorn process.
   
     Density Gain
     Density will affect how much Color A you are likely tosee    .
     It acts as a clipping value of the popcornVoronoi (maximum
     value) but can generally be treated as a multiplier of A   Density.



     ---------------- Large Edge Detail -------------------

     The Large Edge Detail Group generates a Noise that is used
     to offset any voronoi cells, giving the veiny feeling

     Large Edge Detail Amount
     The octaves (iterations) at which the offset noise is generated

     Large Edge Detail Amplitute
     The strength (amount of offset from original point) the noise
     has. 

     Large Edge Detail Scale
     The scale the noise is generated at. Please note this value
     is kept always higher than the small edge detail scale by
     adding the two values together.


     ---------------- Small Edge Detail -------------------

     The small Edge Detail Group generates a Noise that is used
     to offset any voronoi cells, giving the veiny feeling

     small Edge Detail Amount
     The octaves (iterations) at which the offset noise is generated

     small Edge Detail Amplitute
     The strength (amount of offset from original point) the noise
     has. 

     small Edge Detail Scale
     The scale the noise is generated at. Please note this value
     is kept always lower than the large edge detail scale by
     adding the two values together.

     ---------------- Space -------------------

     UV Space
     By default the procedural will work in world space, using
     world space coordinates to generate seamless noises.
     When UV Space is ticked, UVs will be used as base values for the
     noises. This has the benefit of allowing the transformations
     (see below) to work relative to your uv tiles instead of relative
     to the object centre.

   ---------------- Transform Scale/Translate/Rotate---------------

   Allows for transformations of the noise. Please note that this
   does not work on the finished noise result but on each stage
   of noise that contributes to the end result. Therefore features
   will change when you offset, scale and rotate.
   When UV Space is ticked on, Rotate Z will rotate around the centre
   of your UDIM.




Requirements: =======================================================

- Mari 2.5v2 or above
- MARI Function Library 1.08 or above (http://mari.ideascale.com/)


Installation: =======================================================


Please download and install the MARI Function Library V1.08 or higher
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

The new nodes are located under the /Procedurals/Custom/MultiFractal/
folder.


History: ============================================================


# - 08/14/14
    released for Mari 2.5v2 and higher


Credits: ============================================================



 
        