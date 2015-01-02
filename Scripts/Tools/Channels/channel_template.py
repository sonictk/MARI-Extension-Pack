# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Get, set and create a channel template from a current channel, a template
# consists of the channel bit depth, and patch resolutions.
# coding: utf-8
# Written by Jorel Latraille
# ------------------------------------------------------------------------------
# DISCLAIMER & TERMS OF USE:
#
# Copyright (c) The Foundry 2014.
# All rights reserved.
#
# This software is provided as-is with use in commercial projects permitted.
# Redistribution in commercial projects is also permitted
# provided that the above copyright notice and this paragraph are
# duplicated in accompanying documentation,
# and acknowledge that the software was developed
# by The Foundry.  The name of the
# The Foundry may not be used to endorse or promote products derived
# from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

import mari

version = "0.01"
geo_dict = {}

# ------------------------------------------------------------------------------
def getChannelTemplate():
    "Get current channel's patch resolutions and create a template."
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
    mari.history.startMacro('Load Channel Resolution')
    geo = mari.geo.current()
    if not geo_dict.has_key(geo):
        mari.utils.message('There is no Channel Resolution saved for the current geometry, please use "/Channel/Resize/Save Channel Resolution" to save one')
        return
    channel = mari.current.channel()
    for item in geo_dict[geo]:
        if item == geo_dict[geo][0]:
            continue
        try:
            channel.resize(item[0], [item[1],])
        except Exception, e:
            print(e)
    mari.history.stopMacro()
# ------------------------------------------------------------------------------
def createChannelFromTemplate():
    "Create a channel from a template."
    mari.history.startMacro('Create Channel from Saved Resolution')
    geo = mari.geo.current()
    if not geo_dict.has_key(geo):
        mari.utils.message('There is no Channel Resolution saved for the current geometry, please use "/Channel/Resize/Save Channel Resolution" to save one')
        return
    channel = geo.createChannel(name, geo_dict[geo][1][0], geo_dict[geo][1][0], geo_dict[geo][0])
    for item in geo_dict[geo]:
        if item == geo_dict[geo][0]:
            continue
        try:
            channel.resize(item[0], [item[1],])
        except Exception, e:
            print(e)
    mari.history.stopMacro()

# ------------------------------------------------------------------------------
