# ColorRangeToMask - A powerful color selection adjustment mimicking 
# Photoshop's Select Color Range
#
# Copyright (c) 2014 Jens Kafitz. All Rights Reserved.
# ---------------------------------------------------------------
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com
# Web: www.mari.ideascale.com
# Email: MariIdeas@campi3d.com
# ---------------------------------------------------------------
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

Information: ========================================================

The ColorRangeToMask node provided a powerful toolset to create 
Masks. Simply add the Adjustment layer, select the color ranges then
bake it down or use in a channel mask.


Options: ===========================================================

Disclaimer: 
Please note due to the size and complexity of the node we recommend
merging/flattening changes - even the ones made with the new Grade
Mode. It is not recommended to keep this node live.


--- COLOR PICKING ---

ShowBackground:
Allows you to show the result of the Channel without the Adjustment
applied. This is useful for color picking.

Wipe:
A viewport wipe between picked Colors and Background

Reverse Wipe:
Invert the Screenwipe

Preview:
Multiple options for the way the selection is previewed. For a solid
Mask set the dropdown to "Grayscale"  (same result as turning off 
"Show background"). The default Option "Stencil" willscreen the mask 
over the background. "BlackMatte" + "WhiteMatte" are conistent with
Photoshops Preview Modes, overlaying Black or white over unselected
areas.
				

--- GLOBAL ---

Additive Slots:
The Amount of Colors to be sampled for additive selection (max 4)

Subtr. Slots:
The Amount of Colors to be sampled for additive selection (max 4)

+/- Bias:
Will overpower the Additive Selection (negative values) or 
Subtr.Selection (pos. values)

Gain:	
The higher the value the more you will blow out your selection

Invert:
Will Invert the selection result


--- Enhance SELECTION ---


Enhance:
With Enhance ticked on all color evaluations will be run on saturated
versions. This can help to fill gaps in your selection

Min/Max:
Will set the minimum values for the curve along which the saturation
is increased.


--- ADDITIVE SELECTION ---

Color A,B,C,D
The Color Picker Slots for additive selection. By default only A is 
active unless you change the value in the "Global"/Additive Slots"
Section

Expand A,B,C,D
Will expand the selection of color


--- SUBTRACTIVE SELECTION ---

Color E,F,G,H
The Color Picker Slots for subtractive selection. By default 
deactivated unless you change the value in the 
"Global"/Subtractive Slots" Section

Expand A,B,C,D
Will expand the selection of color


--- GRADE MODE ---

Grade Mode
Will turn on the option to directly color correct the selected colors.
This will override any Preview Settings from the "Preview" Group

Hue/Saturation/Value Shift
Will apply an HSV Shift to the selected colors.
This behaves identical to the HSV Adjustment Layer inside of MARI

Gamma/Contrast/Contrast Pivot
Will apply an Gamma/Contrast/Contrast Pivot Shift to the selected
colors. This behaves identical to the respectively named adjustments
Gamme & Contract inside of Mari




Requirements: =======================================================

- Mari 2.5 or above (2.0 Version available as well)

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

The new node is located under  Adjustments /Custom/


History: ============================================================

# History:

# - 04/21/14
    1.0 Release for Mari 2.0,2.5,2,6

# - 06/23/14
    1.05 Release. Added in different preview modes to be more in 
    line with photoshop

# - 11/23/14
    A simple Grade Module was added to allow users to Grade selected
    colors directly



Credits: ============================================================

Based on work done for ColorToMask by the foundry.

 
        