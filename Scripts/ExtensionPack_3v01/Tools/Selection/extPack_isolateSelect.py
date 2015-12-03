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
    selVisibleAction = mari.actions.find('/Mari/Geometry/Selection/Select Visible')
    hideSelAction =  mari.actions.find('/Mari/Geometry/Selection Group/Hide Selection Group')
    showSelAction = mari.actions.find('/Mari/Geometry/Selection Group/Show Selection Group')
    deselectAction = mari.actions.find('/Mari/Geometry/Selection/Select None')


    if mari.selection_groups.sceneSelectionMode() != OBJ_Mode:
        if mari.selection_groups.sceneSelectionMode() == PATCH_Mode or FACE_Mode:
            deactivateViewportToggle.trigger()
            mari.history.startMacro('Toggle Isolate Selection')

            isolate_cur_set = None
            isolate_trig_set = None
            isolate_vis_set = None

            vis_set_found = False
            cur_set_found = False

            if len(sel_groups) != 0:
                for item in sel_groups:
                    if item.name() == "zz_IsolateSelect_current":
                        isolate_cur_set = item
                        isolateSelectState = True
                        cur_set_found = True
                    if item.name() == "zz_IsolateSelect_visible":
                        isolate_vis_set = item
                        isolateSelectState = True
                        vis_set_found = True


            if isolateSelectState:
                # since users potentially changes selections while Isolate Select is active
                # I am saving the new selection so it doesn't change
                mari.selection_groups.createSelectionGroupFromSelection('zz_IsolateSelect_trigger')
                sel_groups = mari.selection_groups.list()
                trigger_found = False
                if len(sel_groups) != 0:
                    for item in sel_groups:
                        if item.name() == 'zz_IsolateSelect_trigger':
                            isolate_trig_set = item
                            trigger_found = True

                if vis_set_found:
                    mari.selection_groups.select(isolate_vis_set)
                    showSelAction.trigger()
                    mari.selection_groups.removeSelectionGroup(isolate_vis_set)
                if cur_set_found:
                    mari.selection_groups.select(isolate_cur_set)
                    mari.selection_groups.removeSelectionGroup(isolate_cur_set)
                if trigger_found:
                    mari.selection_groups.select(isolate_trig_set)
                    mari.selection_groups.removeSelectionGroup(isolate_trig_set)

            else:

                mari.selection_groups.createSelectionGroupFromSelection('zz_IsolateSelect_current')
                selVisibleAction.trigger()
                mari.selection_groups.createSelectionGroupFromSelection('zz_IsolateSelect_visible')

                sel_groups = mari.selection_groups.list()
                vis_set_found = False
                cur_set_found = False

                if len(sel_groups) != 0:
                    for item in sel_groups:
                        if item.name() == "zz_IsolateSelect_visible":
                            isolate_vis_set = item
                            vis_set_found = True
                        if item.name() == "zz_IsolateSelect_current":
                            isolate_cur_set = item
                            cur_set_found = True

                if cur_set_found:
                    mari.selection_groups.select(isolate_cur_set)
                    hideSelAction.trigger()
                if vis_set_found and cur_set_found:
                    mari.selection_groups.select(isolate_vis_set)
                    hideSelAction.trigger()
                if cur_set_found:
                    mari.selection_groups.select(isolate_cur_set)
                    showSelAction.trigger()
                if vis_set_found and not cur_set_found:
                    mari.selection_groups.select(isolate_vis_set)
                    mari.selection_groups.removeSelectionGroup(isolate_vis_set)
                    deselectAction.trigger()
                    mari.utils.message('No selection found','Isolate Selection')


            mari.history.stopMacro()
            deactivateViewportToggle.trigger()

    else:
        mari.utils.message('Isolate Selection in Object Mode is currently not supported','Isolate Selection')


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    isolateSelect()