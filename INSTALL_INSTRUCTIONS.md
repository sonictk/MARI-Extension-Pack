INSTALL INSTRUCTIONS
=====================================================================================
Copyright (c) 2013-2014 www.mari.ideascale.com. All Rights Reserved.

     
Installation
-----------------

Take contents of script directory and put them into your user preference script directory. Or any startup
script path that Mari has set. Once these are in place, Mari on startup will run through
the scripts folder and load the procedural library. Going to the Python tab and showing
the console will allow you to see the modules loading up. This is where if in any case
the loading fails it will let you know. 

Example:

  • On Linux+MAC: ~/Mari/Scripts/

  • On Windows: /Documents/Mari/Scripts/ 

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
 
        