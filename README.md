IDEASCALE SHADER/NODE MIRROR
=====================================================================================
Copyright (c) 2013-2014 www.mari.ideascale.com. All Rights Reserved.

Version:
-----------
Nodepack :  1.20 master //  MARI Function Library: 1.07

     
Info
-----------------
General Development Area for custom nodes, custom shaders and Python scripts
Mirroring www.mari.ideascale.com.

This includes all User Content including Python Scripts and user created Nodes

A collabarative space for development is available here:

https://github.com/campi3d/IdeascaleNodePack


GIT Workflow
-----------------
We have adopted the git flow branching model. 

A demo video is available here: https://vimeo.com/86492303

SUBBRANCH -> DEV -> RELEASE CANDIDATE (Optional) -> MASTER

MASTER is always a released version. 
DEV is the sum of all Development (more or less stable)
Development Branches (referred to as "sub branch" in this document)  are branched off DEV. 

Once a sub branch is completed, a pull request is made to DEV. 
If many changes are made to DEV from different Collaborators,
a RELEASE CANDIDATE Branch may be created from DEV before merged into MASTER.

In order to keep track of things it would be good if major new features just get noted down in the release notes within the DEV Branch
so we have some sort of easy way to assemble release information.


Installation
-----------------

Take scripts and put them into your user preference script directory. Or any startup
script path that Mari has set. Once these are in place, Mari on startup will run through
the scripts folder and load the procedural library. Going to the Python tab and showing
the console will allow you to see the modules loading up. This is where if in any case
the loading fails it will let you know. 

Example:
  • On Linux+Mac: ~/Mari/Scripts/
  • On Windows: Documents/Mari/Scripts/ 

  After Installation and Mari Restart please check your Python Console under "Python/Show Console" Menu
  for any errors.



Conflicts with previous Nodepack Versions
-----------------

On version 1.10  of this Nodepack the structure has been changed by moving
all Nodes into a Subfolder /Shaders/. 
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

- Nicholas Breslow www.nbreslow.com // nick@nbreslow.com

- Jens Kafitz www.campi3d.com // info@campi3d.com

- Ben Neall www.bneall.blogspot.co.nz //  bneall@gmail.com

- Antonio Neto

- Orlando Esponda

- Antoni Kujawa


Thank you
-----------------

Yasin Hasanian for MAC QA


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
 
        