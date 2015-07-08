# ------------------------------------------------------------------------------
# Unproject Channel To Image Manager
# ------------------------------------------------------------------------------
# Will do a Quick Unprojection of the current Channel based on Paint Buffer Dimensions and
# place the result in the Image Manager
# ------------------------------------------------------------------------------
# http://mari.ideascale.com
# ------------------------------------------------------------------------------
# Originally written by Antoni Kujawa, 2014
# Extended by Jens Kafitz, 2015
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


import os
import mari
from time import gmtime, strftime



def unprojChanPaint():
    '''Unprojects current Channel to image manager'''

    curGeo = mari.geo.current()
    curChan = curGeo.currentChannel()
    curCam = mari.current.canvas().camera()
    buffer_ident = 0
    stage = "Information not available"


    mari.history.startMacro('Unproject Channel to Image Manager')
    projectionCamera = mari.actions.get ("/Mari/Canvas/Projection/Create Projector")
    projectionCamera.trigger()

    # Get Buffer Resolution,Channel Depth and Channel Colorspace
    paint_buffer = mari.canvases.paintBuffer()
    buffer_res_U = paint_buffer.resolution().width()*2
    buffer_res_V = paint_buffer.resolution().height()*2
    buffer_scale_X = paint_buffer.scale().width()
    buffer_scale_Y = paint_buffer.scale().height()

    # MARI is being a little bitch about the Class variables after Pyside Change
    # since they no longer can be called by number ...
    if curChan.depth() is mari.Image.DEPTH_BYTE:
        buffer_depth = mari.Projector.BitDepth.DEPTH_BYTE
        buffer_ident = 0
    elif curChan.depth() is mari.Image.DEPTH_HALF:
        buffer_depth = mari.Projector.BitDepth.DEPTH_HALF
        buffer_ident = 1
    elif curChan.depth() is mari.Image.DEPTH_FLOAT:
        buffer_depth = mari.Projector.BitDepth.DEPTH_FLOAT
        buffer_ident = 2

    colorSpace = curChan.colorspaceConfig()


    try:
        channel_projector = mari.projectors.current()
        timestamp = strftime("%Hh%Mm%Ss_%m%d%Y", gmtime())
        channelNameString = curChan.name()
        channelNameString = channelNameString.replace(" ", "")
        projectorName = channel_projector.setName("CurrentChannel_" + channelNameString + "_" + timestamp)
        channel_projector = mari.projectors.current()
        channel_projector.setUseShader("Current Channel")
        channel_projector.setLightingMode(channel_projector.FLAT)
        channel_projector.setSize (buffer_res_U,buffer_res_U)
        channel_projector.setScale(mari.VectorN(buffer_scale_X,buffer_scale_X))
        channel_projector.setBitDepth (buffer_depth)
        channel_projector.setExportColorspaceConfig(colorSpace)
        unprojDir = os.path.expanduser('~') + "/"
        filename = channel_projector.name()
        filename = filename.replace(":", "_")

        # Determining File Format based on buffer depth
        if buffer_ident > 0:
            unprojectFileLoc = "{1}{0}.exr".format(channel_projector.name(), unprojDir)
        else:
            unprojectFileLoc = "{1}{0}.png".format(channel_projector.name(), unprojDir)

        stage = "Saving File"
        channel_projector.unprojectToFile(unprojectFileLoc)

        stage = "Removing temporary projector"
        mari.projectors.remove(mari.projectors.current().name())

        stage = "Loading file from disc"
        mari.images.open(unprojectFileLoc)

        stage = "Setting unprojected Image as Paint Through"
        mari.tools.setCurrent("Paint Through")

        stage = "Resetting Camera"
        # Resetting Camera
        if curCam.type() is mari.Camera.ORTHOGRAPHIC:
            cam_action = mari.actions.find('/Mari/Canvas/Camera/Ortho Camera')
            cam_action.trigger()
        elif curCam.type() is mari.Camera.PERSPECTIVE:
            cam_action = mari.actions.find('/Mari/Canvas/Camera/Perspective Camera')
            cam_action.trigger()
        elif curCam.type() is mari.Camera.UV:
            cam_action = mari.actions.find('/Mari/Canvas/Camera/UV Camera')
            cam_action.trigger()
        else:
            pass
        print "Successfully unprojected Channel to Image Manager"


        mari.history.stopMacro()

    except Exception:
        print 'Something bad happened, Channel Quick Unproject did not complete the last stage: '+ stage
        mari.utils.message("Channel Unproject did not complete: " + stage, "Quick Channel Unproject")

    return


def _isProjectSuitable():
    """Checks project state."""
    MARI_2_0V1_VERSION_NUMBER = 20001300    # see below
    if mari.app.version().number() >= MARI_2_0V1_VERSION_NUMBER:

        if mari.projects.current() is None:
            mari.utils.message("Please open a project before running.")
            return False, False

        if mari.app.version().number() >= 20603300:
            return True, True

        return True, False

    else:
        mari.utils.message("You can only run this script in Mari 2.6v3 or newer.")
        return False, False



def unproject_channel_to_imageman():
  suitable = _isProjectSuitable()
  if not suitable[0]:
        return

  unprojChanPaint()