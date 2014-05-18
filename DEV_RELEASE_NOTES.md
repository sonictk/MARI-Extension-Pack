Release Notes for Shader/Nodepack 1.30
=====================================================================================

Release Date
-----------
TBA


Added Features:
-----------
- Cylindrical Projection - a full Cylindrical Projection Node, optimized for easy setup in 3D Space.
- Color Range to Mask - a powerful Adjustment Shader similar to Photoshop's Select Color Range
- Squid Skin Procedural - organic Noise Pattern
- Cavity Map from Tangent Space Normal - Using a Tangent space normal map will output you a pseudo cavity map

Feature Improvements:
-----------
- Military Camo - a more flexible Camo procedural was added allowing for 3 color steps. Layer them up by setting Color A to transparent for more elaborate effects
- The original Camo Procedural with 2 Colors has been deprecated. You can use the new Military Camo with a Spacing of 0 for the same effect.
- A variety of interface improvements have been made, collapsing less used node groups by default (Mari 2.6v2 only)


Bugfixes:
-----------
- A missing Library Name File within the FunctionLibrary Directory could cause the Nodepack to not load when mixed with
  single node releases from Ideascale.
- various fixes for MAC configurations that had issues with the Nodepack before
- Turning on Displacement in Shaders no longer causes a Shader Error when the Nodepack is installed
- UV Mode for Noises that broke in Nodepack 1.21 Maintenance release is now fixed
- Baking Paint with the Falloff Map active in a Channel Mask no longer causes the baked paint to shift 
- Depth Mode on the Falloff Map has been removed due to instability. Use the Depth mask in the Projection Palette instead
- Custom Object Normal, Axis Mask, Paintable Gabor and PolysurfaceCurvature will no longer show an 
  error when used in a displacement preview channel


Known Issues & Workarounds:
-----------
- When a Nodepack Node is used in a Channel, that is plugged into the ChannelMask (Projection Palette), 
projecting Paint from the Paintbuffer will throw an error. This is related to a MARI Bug that we will
need the Foundry to fix.
The current workaround is to cache any Nodepack Node in the Channel, at which point the Channel Mask will work.

- the paintableGabor can crash nvidia display drivers when used in a Displacement Preview Channel. 
  The current workaround is to cache the GaborNoise.


Developer Notes:
-----------
- As of this version of the Nodepack <DefaultName> is used for Node names in the Mari Interface.
  <ID> will no longer be called but is required by Mari to ensure Version consistency. Please refer
  to the SDK Docs within your Script_Docs/SDK/ Folder for more information




Release Notes for Shader/Nodepack 1.20
=====================================================================================

Release Date
-----------
5 March 2014


Best bits of 1.20:
-----------
- a shader mimicking Mental Ray's mia_material_x in look and handling
- new procedurals Dots, Stripes, Weave, superEllipse + superShape
- Noises and Procedurals can now be optionally evaluated in UV Space


Requirements:
-----------
- This Node+Shader Pack requires MARI 2.5v2 or higher.


Added Features:
-----------
- new BRDF Standalone Shader "MIA Material BRDF" mimicking very closely results and handling of Mental Ray's mia_material_x
- new BRDF Difuse Shaders with Energy Conservation such as OrenNayar Difuse
- new BRDF Specular Shaders with Energy Conservation such as WardAnisotropic and WardIsotropic
- new procedural superShape. A complex procedural with an large amount of shape variations based on the "Superformula"
  (http://en.wikipedia.org/wiki/Superformula). Can for example be used to create clothing patterns such as chainmail, denim, star patterns etc.
- new procedural Weave. Cloth/Weave Pattern that you might know from Maya.
- new procedural superEllipse. A procedural creating anything from rounded rectangles to ellipses.
- new procedural Dot Pattern. An improved Dot Procedural which a lot of cool extras
- new procedural Stripes. An improved Stripes Procedural which a lot of cool extras
- new environment Falloff Map with options for Fresnel, Distance etc.. This is not bakeable/convert to paintable but for visual enhancements + channel masking

Feature Improvements:
-----------
- previously existing noise and fractal nodes can now be switched to UV Space via the "Space/UV Space" Checkbox. 
- UI improvements have been made for a variety of nodes to give a more unified user experience between nodes
- Color A/B has been added to "Spotify" Node.
- various Bugfixes in Library
- Adjustment "NormalMapMerge" was deprecated since Mari now has this functionality build in


Development:
-----------
- Documentation improvements in Script_Docs/SDK Folder for new Developers
- new Functions for modifying UV Space have been added. Refer to section 7) of the Function Overview in the SDK Documentation
- new Distance Functions have been added. Refer to section 10)  of the Function Overview in the SDK Documentation
- new Value Functions have been added. Refer to section 8)  of the Function Overview in the SDK Documentation



Credits:
-----------

- Miguel A Santiago Jr., Nicholas Breslow, Jens Kafitz, Ben Neall, Antonio Neto, Orlando Esponda, Antoni Kujawa



License
-----------------

This program is free software: you can redistribute it and/or modify it under the terms 
of the GNU General Public License as published by the Free Software Foundation, either 
version 3 of the License, or (at your option) any later version.                    
                                      
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details.                
                                      
You should have received a copy of the GNU General Public License along with this program.  
If not, see <http://www.gnu.org/licenses/>.
 
        