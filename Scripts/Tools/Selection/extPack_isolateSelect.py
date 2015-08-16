# ------------------------------------------------------------------------------
# Isolate Selection
# ------------------------------------------------------------------------------
# Isolate Selection will only show the current selection.
# By executing it again the old visibility states will be restored
# ------------------------------------------------------------------------------
# Written by Jens Kafitz, 2015
# ------------------------------------------------------------------------------
# http://www.jenskafitz.com
# ------------------------------------------------------------------------------
# Last Modified: 17 August 2015
# ------------------------------------------------------------------------------
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF HE POSSIBILITY OF SUCH DAMAGE.
# ------------------------------------------------------------------------------

import mari

def isolateSelect():
    """Isolate Selected Face or Patches"""

    OBJ_Mode = mari.selection_groups.SELECTION_MODE_OBJECTS
    PATCH_Mode = mari.selection_groups.SELECTION_MODE_PATCHES
    FACE_Mode = mari.selection_groups.SELECTION_MODE_FACES

    selectionSet = None
    sel_groups = mari.selection_groups.list()
    isolateSelectState = False
    deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
    selInvertAction = mari.actions.find('/Mari/Geometry/Selection/Select Invert')
    hideSelAction =  mari.actions.find('/Mari/Geometry/Selection Group/Hide Selection Group')
    showSelAction = mari.actions.find('/Mari/Geometry/Selection Group/Show Selection Group')


    if mari.selection_groups.sceneSelectionMode() != OBJ_Mode:
        if mari.selection_groups.sceneSelectionMode() == PATCH_Mode or FACE_Mode:
            deactivateViewportToggle.trigger()

            for item in sel_groups:
                if item.name() == "zz_IsolateSelect":
                    selectionSet = item
                    isolateSelectState = True

            if isolateSelectState:

                mari.selection_groups.select(selectionSet)
                showSelAction.trigger()
                mari.selection_groups.removeSelectionGroup(selectionSet)

            else:

                selInvertAction.trigger()
                mari.selection_groups.createSelectionGroupFromSelection('zz_IsolateSelect')

                sel_groups = mari.selection_groups.list()

                for item in sel_groups:
                    if item.name() == "zz_IsolateSelect":
                        mari.selection_groups.select(item)
                        hideSelAction.trigger()

                selInvertAction.trigger()

            deactivateViewportToggle.trigger()

    else:
        mari.utils.message('Isolate Selection in Object Mode is currently not supported','Isolate Selection')


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    isolateSelect()