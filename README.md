#MARI EXTENSION PACK 1.7

Copyright (c) 2015 www.mari.ideascale.com. All Rights Reserved.


##Version:
Extension Pack :  1.7  //  MARI Function Library: 1.11


##Info
General Development Area for custom nodes, custom shaders and Python scripts
Mirroring www.mari.ideascale.com.

This includes all User Content including Python Scripts and user created Nodes

A collabarative space for development is available here:

https://github.com/campi3d/IdeascaleNodePack


##GIT Workflow

We have adopted the git flow branching model.

A comprehensive Step-by-Step is available on the Twiki: 
https://github.com/campi3d/IdeascaleNodePack/wiki/Making-a-change---step-by-step-Tutorial


SUBBRANCH -> DEV -> RELEASE CANDIDATE (Optional) -> MASTER

MASTER is always a released version.
DEV is the sum of all Development (more or less stable)
Development Branches (referred to as "sub branch" in this document)  are branched off DEV.

Once a sub branch is completed, a pull request is made to DEV.
If many changes are made to DEV from different Collaborators,
a RELEASE CANDIDATE Branch may be created from DEV before merged into MASTER.

In order to keep track of things it would be good if major new features just get noted down in the release notes within the DEV Branch
so we have some sort of easy way to assemble release information.


##Adding new nodes, shaders, functions & Python Scripts

Refer to the contents of the Script_Docs/SDK folder for information



##Contributors


###PYTHON DEVELOPMENT

- Jorel Latraille, http://www.jorel-latraille.com
- Ben Neall www.bneall.blogspot.co.nz //  bneall@gmail.com
- Sreenivas Alapati http://cg-cnu.blogspot.in // sreenivas9alapati@gmail.com
- Miguel A Santiago Jr. www.digiteck3d.com // miguel@digiteck3d.com
- Jens Kafitz, www.campi3d.com // MariIdeas@campi3d.com
- Antoni Kujawa


###NODE DEVELOPMENT

- Jens Kafitz www.campi3d.com // MariIdeas@campi3d.com
- Miguel A Santiago Jr. www.digiteck3d.com // miguel@digiteck3d.com
- Nicholas Breslow www.nbreslow.com // nick@nbreslow.com
- Antoni Kujawa
- Orlando Esponda
- Antonio Neto


###SHADER DEVELOPMENT

- Miguel A Santiago Jr. www.digiteck3d.com // miguel@digiteck3d.com
- Nicholas Breslow www.nbreslow.com // nick@nbreslow.com


###MAC QA

- Yasin Hasanian
- Dave Girard


##License


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


