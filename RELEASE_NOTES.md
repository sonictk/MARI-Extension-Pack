Release Notes for Node/Shader Pack 1.20
=====================================================================================

Release Date
-----------
4 March 2014


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
- new environment Falloff Map with options for Fresnel, Distance etc.. This is a visual helper only and is not bakeable/convert to paintable.

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
 
        