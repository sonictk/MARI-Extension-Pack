# ------------------------------------------------------------------------------
# Available at: http://mari.ideascale.com/
# ------------------------------------------------------------------------------
# ColorRangeToMask - A powerful color selection adjustment mimicking Photoshop's Select Color Range
# Copyright (c) 2014 Jens Kafitz. All Rights Reserved.
# ------------------------------------------------------------------------------
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com
# Web: www.mari.ideascale.com
# Email: info@campi3d.com
# ------------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------


Information: ==============================================================

The ColorRangeToMask node provided a powerful toolset to create Masks.
Simply add the Adjustment layer, select the color ranges then bake it down or use in a
channel mask.


Node Description: ==============================================================

--- COLOR PICKING ---

ShowBackground:		Allows you to show the result of the Channel without the Adjustment applied.
				This is useful for color picking.

Wipe:			A viewport wipe between picked Colors and Background

Reverse Wipe:	Invert the Screenwipe

Preview: 		Multiple options for the way the selection is previewed. For a solid Mask set the dropdown to
				"Grayscale" (same result as turning off "Show background"). The default Option "Stencil" will
				screen the mask over the background. "BlackMatte" + "WhiteMatte" are conistent with Photoshops
				Preview Modes, overlaying Black or white over unselected areas.
				

--- GLOBAL ---

Additive Slots:	The Amount of Colors to be sampled for additive selection (max 4)

Subtr. Slots:	The Amount of Colors to be sampled for additive selection (max 4)

+/- Bias:		Will overpower the Additive Selection (negative values) or Subtr. Selection (pos. values)

Gain:			The higher the value the more you will blow out your selection

Invert:			Will Invert the selection result


--- Enhance SELECTION ---


Enhance:		With Enhance ticked on all color evaluations will be run on saturated versions.
		 	This can help to fill gaps in your selection

Min/Max:		Will set the minimum values for the curve along which the saturation is increased.


--- ADDITIVE SELECTION ---

Color A,B,C,D 	The Color Picker Slots for additive selection. By default only A is active unless
				you change the value in the "Global"/Additive Slots" Section

Expand A,B,C,D  Will expand the selection of color


--- SUBTRACTIVE SELECTION ---

Color E,F,G,H 	The Color Picker Slots for subtractive selection. By default deactivated unless
				you change the value in the "Global"/Subtractive Slots" Section

Expand A,B,C,D  Will expand the selection of color






Requirements: =======================================================================

- Mari 2.5 or above (2.0 Version available as well)


Installation: =======================================================================

Take scripts and put them into your user preference script directory. Or any startup
script path that Mari has set. Once these are in place, Mari on startup will run through
the scripts folder and load the procedural library. Going to the Python tab and showing
the console will allow you to see the modules loading up. This is where if in any case
the loading fails it will let you know. 


Example:
	• On Linux+Mac: ~/Mari/Scripts/
	• On Windows: Documents/Mari/Scripts/	



Where to find the nodes: ============================================================

The new node is located under  Adjustments /Custom/


History: ============================================================================

# History:
# - 04/21/14		1.0 Release for Mari 2.0,2.5,2,6


Credits: ============================================================================

Based on work done for ColorToMask by the foundry.

 
        