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

Redistribution and use in source and binary forms, with or without modification, are permitted
provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions
and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse
or promote products derived from this software without specific prior written permission.

This Software Is Provided By The Copyright Holders And Contributors "as Is" and Any Express Or Implied
Warranties, Including, But Not Limited To, The implied Warranties Of Merchantability And Fitness For
A Particular Purpose are Disclaimed. In No Event Shall The Copyright Holder Or Contributors Be liable
For Any Direct, Indirect, Incidental, Special, Exemplary, Or consequential Damages (including, But Not
Limited To, Procurement Of substitute Goods Or Services; Loss Of Use, Data, Or Profits; Or Business
interruption) However Caused And On Any Theory Of Liability, Whether In contract, Strict Liability,
Or Tort (including Negligence Or Otherwise) arising In Any Way Out Of The Use Of This Software, Even If
Advised Of He possibility Of Such Damage.
