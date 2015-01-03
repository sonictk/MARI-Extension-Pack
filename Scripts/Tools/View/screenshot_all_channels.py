# ------------------------------------------------------------------------------
# Screenshot All Channels
# ------------------------------------------------------------------------------
# Will do Screenshots of all Channels and export them based on the path provided
# in Screenshot Settings
# ------------------------------------------------------------------------------
# http://mari.ideascale.com
# http://cg-cnu.blogspot.in/
# ------------------------------------------------------------------------------
# Written by Sreenivas Alapati, 2014
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

def screenshotAllChannels():
    '''Take screenshot of all the channels for the current view '''

    if mari.projects.current() == None:
        mari.utils.message("No project currently open", title = "Error")
        return

    mari.utils.message("Snapshotting multiple Channels requires Incremental Screenshot Setting to be enabled")

    mari.history.startMacro('Snapshot all Channels')
    curGeo = mari.geo.current()
    curChannel = curGeo.currentChannel()
    chanList = curGeo.channelList()
    curCanvas = mari.canvases.current()

    mari.app.setWaitCursor()

    for chan in chanList:
        curGeo.setCurrentChannel(chan)
        curCanvas.repaint()
        snapAction = mari.actions.find ('/Mari/Canvas/Take Screenshot')
        snapAction.trigger()

    curGeo.setCurrentChannel(curChannel)
    curCanvas.repaint()
    mari.app.restoreCursor()
    mari.history.stopMacro()

    return

