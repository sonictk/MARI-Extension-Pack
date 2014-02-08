IDEASCALE SCRIPT & NODE MIRROR
=====================================================================================
Copyright (c) 2013-2014 www.mari.ideascale.com. All Rights Reserved.

Version: 1.10 master
-----------------


     
Info
-----------------
General Development Area for custom nodes, custom shaders and Python scripts
Mirroring www.mari.ideascale.com.

This includes all User Content including Python Scripts and user created Nodes

A collabarative space for development is available here:

https://github.com/campi3d/IdeascaleNodePack


History
-----------------

 - 01/03/14 Initial commit
 - 01/07/14 Fixes for MAC+Linux, recommited with Capital S in Script Directory so Linux is happy
 - 01/08/14 RegisterSetRange.py was missing final registerSetRange() so Node wasn't loaded
 - 02/08/14 A new loading structure has been implemented to clean up the clutter in the script directory



Installation
-----------------

Take scripts and put them into your user preference script directory. Or any startup
script path that Mari has set. Once these are in place, Mari on startup will run through
the scripts folder and load the procedural library. Going to the Python tab and showing
the console will allow you to see the modules loading up. This is where if in any case
the loading fails it will let you know. 

Example:
  • On Linux: /Mari/Scripts/
  • On Windows: Documents/Mari/Scripts/ 

  After Installation and Mari Restart please check your Python Console under "Python/Show Console" Menu
  for any errors.



Conflicts with previous Nodepack Versions
-----------------

 With version 1.10 of this Nodepack the structure has been changed by moving
all Nodes into aSubfolder /Shaders/. 
If you have previous versions of the Nodes or FunctionLibraries
installed they will conflict.

 After Installation and Mari Restart please check your Python Console under Python/Show Console
 for any errors.

PLEASE UNINSTALL PREVIOUS VERSIONS BY:

- deleting Folder /scripts/FunctionLibrary
- deleting Folder /scripts/NodeLibrary
- deleting any previous RegisterNODENAME.py file in the /script/ directory.


Adding new nodes, shaders and functions
-----------------
Refer to the contents of the Script_Docs/SDK folder for information



Contributors
-----------------

- Miguel A Santiago Jr. www.digiteck3d.com // miguel@digiteck3d.com

- Jens Kafitz www.campi3d.com // info@campi3d.com

- Ben Neall www.bneall.blogspot.co.nz //  bneall@gmail.com

- Orlando Esponda

- Antoni Kujawa


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
 
        