# --------------------------------------------------------------------
# Disable Viewport
# Copyright (c) 2015 MARI Extension Pack. All Rights Reserved.
# --------------------------------------------------------------------
# Written by Jens Kafitz, 2015
# --------------------------------------------------------------------
# http://www.campi3d.com
# --------------------------------------------------------------------
# Description: Repackaging toggleShaderCompile action written by the
# foundry so I can add it to the interface with custom icons & tooltips
# --------------------------------------------------------------------
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
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS
# IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF HE POSSIBILITY OF SUCH DAMAGE.
# --------------------------------------------------------------------


import mari


def _isProjectSuitable():
    if mari.projects.current() is None:
        mari.utils.message("Please open a project before running.")
        return False, False

    else:
        return True,True



def toggleViewport():
    """Disables or enables Viewport"""

    suitable = _isProjectSuitable()

    action = mari.actions.find("/Mari/MARI Extension Pack/Shading/Pause Viewport Update")

    if not suitable[0]:
        action.setChecked(False)
        return

    if action.isChecked() is False:
            mari.canvases.setPauseShaderCompiles(False)
    else:
            mari.canvases.setPauseShaderCompiles(True)


def toggleDisableViewportIcon():
    """This is triggered directly by the viewport signal to ensure icon state is always correct"""

    iconAction = mari.actions.find('/Mari/MARI Extension Pack/Shading/Pause Viewport Update')
    if iconAction.isChecked() is True:
        iconAction.setChecked(False)
    else:
        iconAction.setChecked(True)


def disableViewport(mode):
    """Determine if only icon needs changing or full action"""

    if mode == 'iconOnly':
        toggleDisableViewportIcon()
    else:
        toggleViewport()


