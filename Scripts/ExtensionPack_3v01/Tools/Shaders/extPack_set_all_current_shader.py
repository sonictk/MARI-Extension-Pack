# ------------------------------------------------------------------------------
# Set all Objects to current shader
# ------------------------------------------------------------------------------
# Will set all objects to the same shader
# coding: utf-8
# ------------------------------------------------------------------------------
# Written by Jorel Latraille, 2014
# ------------------------------------------------------------------------------
# http://mari.ideascale.com
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

version = "0.01"

# ------------------------------------------------------------------------------
def setAllCurrentShader():
    "Set all geometry shaders to selected shader"
    if not isProjectSuitable(): #Check if project is suitable
        return False

    deactivateViewportToggle = mari.actions.find('/Mari/Canvas/Toggle Shader Compiling')
    deactivateViewportToggle.trigger()

    geo = mari.geo.current()
    geo_list = mari.geo.list()
    shader = geo.currentShader()
    shader_list = list(geo.shaderList())
    sIndex = shader_list.index(shader)

    for geo in geo_list:
        if len(geo.shaderList()) == len(shader_list):
            geo_shader_list = geo.shaderList()
            geo_shader = geo_shader_list[sIndex]
            geo.setCurrentShader(geo_shader)
        elif sIndex < len(geo.shaderList()):
            geo_shader_list = geo.shaderList()
            geo_shader = geo_shader_list[sIndex]
            geo.setCurrentShader(geo_shader)

    deactivateViewportToggle.trigger()

# ------------------------------------------------------------------------------
def isProjectSuitable():
    "Checks project state and Mari version."
    MARI_3_0V1_VERSION_NUMBER = 30001202    # see below
    if mari.app.version().number() >= MARI_3_0V1_VERSION_NUMBER:

        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False

        geo = mari.geo.current()
        if geo is None:
            mari.utils.message("Please select an object to set shader from.")
            return False

        shader = mari.geo.current().currentShader()
        if shader is None:
            mari.utils.message("Please select a shader to set shader from.")
            return False

        return True

    else:
        mari.utils.message("You can only run this script in Mari 2.0v1 or newer.")
        return False



