# ------------------------------------------------------------------------------
# Channel Template
# ------------------------------------------------------------------------------
# Get, set and create a channel template from a current channel, a template
# consists of the channel bit depth, and patch resolutions.
# coding: utf-8
# ------------------------------------------------------------------------------
# Written by Jorel Latraille, 2014
# ------------------------------------------------------------------------------
# http://www.jorel-latraille.com/
# http://www.thefoundry.co.uk
# ------------------------------------------------------------------------------
# DISCLAIMER & TERMS OF USE:
#
# Copyright (c) The Foundry 2014.
# All rights reserved.
#
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
import PySide.QtGui as QtGui

version = "0.01"
geo_dict = {}

# Mari 3 beta 6 has some problems with these class variables so defining them myself:

size_dict = {256:mari.ImageSet.SIZE_256,
             512:mari.ImageSet.SIZE_512,
             1024:mari.ImageSet.SIZE_1024,
             2048:mari.ImageSet.SIZE_2048,
             4096:mari.ImageSet.SIZE_4096,
             8192:mari.ImageSet.SIZE_8192,
             16384:mari.ImageSet.SIZE_16384,
             32768:mari.ImageSet.SIZE_32768
            }


# ------------------------------------------------------------------------------

def _isProjectSuitable():
    """Checks project state."""
    MARI_3_0v1_VERSION_NUMBER = 30001202    # see below
    if mari.app.version().number() >= MARI_3_0v1_VERSION_NUMBER:

        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False, False

        if mari.app.version().number() >= 30001202:
            return True, True

        return True, False

    else:
        mari.utils.message("You can only run this script in Mari 3.0v1 or newer.")
        return False, False


# ------------------------------------------------------------------------------
def getChannelTemplate():
    "Get current channel's patch resolutions and create a template."
    suitable = _isProjectSuitable()
    if not suitable[0]:
          return
    mari.history.startMacro('Save Channel Resolution')
    global geo_dict
    geo = mari.geo.current()
    channel = mari.current.channel()
    geo_dict[geo] = []
    geo_dict[geo].append(channel.depth())
    for patch in geo.patchList():
        geo_dict[geo].append([channel.width(patch.uvIndex()), patch.uvIndex()])
    mari.history.stopMacro()

# ------------------------------------------------------------------------------
def setChannelFromTemplate():
    "Set current channel's patch resolutions from a template."
    suitable = _isProjectSuitable()
    if not suitable[0]:
          return
    mari.history.startMacro('Load Channel Resolution')
    geo = mari.geo.current()
    if not geo_dict.has_key(geo):
        mari.utils.message('There is no Channel Resolution saved for the current geometry, please use "/Channel/Resize/Save Channel Resolution" to save one')
        mari.history.stopMacro()
        return
    channel = mari.current.channel()
    for item in geo_dict[geo]:
        if item == geo_dict[geo][0]:
            continue
        try:
            channel.resize(size_dict[item[0]], [item[1],])
        except Exception, e:
            print(e)
    mari.history.stopMacro()
# ------------------------------------------------------------------------------
def createChannelFromTemplate():
    "Create a channel from a template."
    suitable = _isProjectSuitable()
    if not suitable[0]:
          return
    mari.history.startMacro('Create Channel from Saved Resolution')
    geo = mari.geo.current()
    if not geo_dict.has_key(geo):
        mari.utils.message('There is no Channel Resolution saved for the current geometry, please use "/Channel/Resize/Save Channel Resolution" to save one')
        mari.history.stopMacro()
        return
    name = (u'', True)
    while name == (u'', True):
        iD = QtGui.QInputDialog()
        name = iD.getText(iD, 'Channel Name','Channel name e.g. COL_skin')
    if name[1] == False:
        return
    channel = geo.createChannel(name[0], geo_dict[geo][1][0], geo_dict[geo][1][0], geo_dict[geo][0])
    for item in geo_dict[geo]:
        if item == geo_dict[geo][0]:
            continue
        try:
            channel.resize(size_dict[item[0]], [item[1],])
        except Exception, e:
            print(e)
    mari.history.stopMacro()

# ------------------------------------------------------------------------------
