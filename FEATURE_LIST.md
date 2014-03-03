FEATURE DESCRIPTION
=====================================================================================


INFORMATION:
----------
The Ideascale Shader/Nodepack is an open-source compilation of shaders, adjustments and procedurals for Mari.
Core features include a vast array of custom noises and fractals as well as new shaders matching offline render packages.


Requirements:
----------
- This Shader/Node Pack requires MARI 2.5v2 or higher.


FEATURE LIST
=====================================================================================


Adjustment Layers:
-----------
- Grade+

A Grade Node with more nuke like functionality such as color picking, limit to color channels etc.

- Normal Map Intensity

An Adjustment Layer that let's you easily and mathematically correct adjust the scale of your normal mao

- Threshold

A Threshold Adjustment similar to Photoshop's Threshold Function. Added functionality includes support for color thresholding and
soft clipping

- setRange

A remap node that let's you enter specific values to remap to. This is similar in behavior to Maya's SetRange Node

- Vibrance

A Vibrancy Adjustment Layer. Changing the Vibrance of colors affects their saturation. However other than a regular Saturation change
values are changes based on a curve, saturating lower saturated values first so not to clip colors.



Geometry Procedurals:
-----------
- Axis Mask

A simple Node allowing you to mask based on a direction. 

- Custom Object Normal

Outputs the Object Normal, however other than Mari's standard Normal Node it allows you to modify the the Normals

- polySurface Curvature

A curvature detection Node. This node is currently in Beta stages and gives tesselated results. It is best to bake the node to textures and run a 
blur filter on it after to get smooth results.




Environment Procedurals:
-----------
- Falloff Map

A Node that allows you to add colors based on effects such as Facing Ratio, ZDepth and Surface Luminance. This node is not bakeable and should
be used for visual enhancement or in conjunction with Channel Masking via the Projection Palette.


Noise/Fractal Procedurals:
-----------
- Brownian Motion, FBM

Two nodes creating fractals based on the Brownian Motion Algorithm.

-  multiFBM

Similar to the previous two nodes, this node offers more complexity by letting you map other noises to any value of the main noise.

- vector FBM

A fractal brownian motion with a vector component giving you more organic results

- ridged MultiNoise + Spotify

Two nodes giving you distinct ridge lines in your noises. Useful for terrain, marble etc.

- Cellular Noise

An advanced voronoi noise implementation offering you many more options than the Celluar that comes with MARI by default

- Inigo,Perlin & Turbulence Noise

3 Noises with different implementations of Perlin, Simplex and Value Noise.

- Legacy Cloud, Squiggle, Turbulence, Cellular & Perlin

Modifications of the Nodes that ship with MARI including options such as seed, transformations, Color A/B etc.

- Camo Pattern

A procedural giving you a military camo pattern

- Dots

A procedural generating a variety of Dot patterns with a lot of options to modify the look

- Stripes

A procedural generating a variety of Stripe patterns with a lot of options to modify the look

- superEllipse2d

A procedural generating things like rectangles, rounded rectangles, pyramids and ellipses

- superShape2d

An implementation of the "Superformula" allowing for a huge array of different geometric forms. Useful for clothing patterns for example

- Weave

A procedural weave pattern


Shaders:
-----------
- MIA Material BRDF (standalone)

A energy conserving shader mimicking mental ray's mia_material_x in look and handling

- Reflection/Refraction (standalone)

A shader with an implementation of reflection and refraction for things like glass

- OrenNayar (difuse)

A difuse component shader using the Oren Nayar Shading Model

- Anisotropic / Isotropic (specular)

Two specular component shaders adding specular anisotropy/isotropy
