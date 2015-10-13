# ------------------------------------------------------------------------------
# Transform Paint Options
# ------------------------------------------------------------------------------
# Adds a variety of options to the 'Transform paint' Tool properties toolbar
# such as
#   - Buffer Resolution
#   - Buffer Res Halve / Double
#   - Bit Depth
#   - Link BitDepth to Channe
#   - Flip X/Y
#   - Color Clamp
# ------------------------------------------------------------------------------
# Written by Jens Kafitz, 2015
# ------------------------------------------------------------------------------
# http://www.campi3d.com
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
import PySide.QtGui as QtGui


# Variables need to be declared as globals or else the scoping
# doesn't work due to a PySide Bug resulting in the widgets not being added to the toolbar
g_buffer_size_label = None
g_buffer_size = None
g_halve_size = None
g_double_size = None
g_buffer_depth_label = None
g_buffer_depth = None
g_buffer_clamp = None
g_buffer_sync = None
g_flip_x = None
g_flip_y = None

g_depth_var_dict = {'8 Bit (Byte)': mari.PaintBuffer.BufferDepth.DEPTH_BYTE ,
                    '16 Bit (Half)': mari.PaintBuffer.BufferDepth.DEPTH_HALF ,
                    '32 Bit (Float)': mari.PaintBuffer.BufferDepth.DEPTH_FLOAT
                    }

version = '3.0'


class paintBufferToolbar(object):
    "Adds new items to the TransformPaint Tool Properties Toolbar"
    def __init__(self, parent=None):

        #  Global Vars. Need to use Globals because Objects are being destroyed otherwise
        self.paintBuffer = mari.canvases.paintBuffer()

        global g_buffer_size_label
        global g_buffer_size
        global g_halve_size
        global g_double_size
        global g_buffer_depth_label
        global g_buffer_depth
        global g_buffer_clamp
        global g_buffer_sync
        global g_flip_x
        global g_flip_y

        self.settings = mari.Settings()

        # Create Widgets

        g_buffer_size_label = QtGui.QLabel("  Resolution ")
        g_buffer_size = QtGui.QComboBox()

        # determine allowed resolutions
        for resolution in self.paintBuffer.supportedResolutions():
            size = resolution.width()
            g_buffer_size.addItem(str(size) + ' x ' + str(size), resolution)

        g_halve_size = QtGui.QPushButton("Halve")
        g_double_size = QtGui.QPushButton("Double")

        g_buffer_depth_label = QtGui.QLabel("  Depth ")
        g_buffer_depth = QtGui.QComboBox()
        g_buffer_depth.addItem("8 Bit (Byte)", mari.PaintBuffer.BufferDepth.DEPTH_BYTE)
        g_buffer_depth.addItem("16 Bit (Half)", mari.PaintBuffer.BufferDepth.DEPTH_HALF)
        g_buffer_depth.addItem("32 Bit (Float)", mari.PaintBuffer.BufferDepth.DEPTH_FLOAT)
        g_buffer_clamp = QtGui.QCheckBox('Clamp')
        g_buffer_sync = QtGui.QCheckBox('Link Depth to Channel')

        g_flip_x = QtGui.QPushButton("Flip X")
        g_flip_y = QtGui.QPushButton("Flip Y")


        # set currents for widgets from active Paintbuffer
        self._setBufferResolutionItem()
        self._setBufferDepthItem()
        self._setBufferClampItem()


        # Add to Toolbar
        toolbar = mari.app.findToolBar('Tool Properties')
        toolbar.setLocked(False)
        toolbar.addWidget(g_buffer_size_label)
        toolbar.addWidget(g_buffer_size)
        toolbar.addWidget(g_halve_size)
        toolbar.addWidget(g_double_size)
        # toolbar.addSeparator()
        # toolbar.addSeparator()
        toolbar.addWidget(g_buffer_depth_label)
        toolbar.addWidget(g_buffer_depth)
        # toolbar.addSeparator()
        toolbar.addWidget(g_buffer_clamp)
        toolbar.addWidget(g_buffer_sync)
        # toolbar.addSeparator()
        # toolbar.addSeparator()
        toolbar.addWidget(g_flip_x)
        toolbar.addWidget(g_flip_y)
        toolbar.setLocked(True)

        # reading existing buffer sync setting in config file

        sync_setting = readBufferSyncSetting()
        if sync_setting != None:
            if sync_setting == 'false':
                checkstate = False
            elif sync_setting == 'true':
                checkstate = True
            else:
                checkstate = True
            g_buffer_sync.setChecked(checkstate)


        # connect to signals so widgets change when settings are changed in Painting Palette
        #  1 - Signals from Painting Palette to Toolbar
        mari.utils.connect(self.paintBuffer.resolutionChanged, lambda: self._setBufferResolutionItem())
        mari.utils.connect(self.paintBuffer.depthChanged, lambda: self._setBufferDepthItem())
        #  2 - Signals from Toolbar to Painting Palette
        mari.utils.connect(g_buffer_size.currentIndexChanged, lambda: self._changeBufferResolution())
        mari.utils.connect(g_buffer_depth.currentIndexChanged, lambda: self._changeBufferDepth())
        mari.utils.connect(g_buffer_clamp.stateChanged, lambda: self._changeBufferClamp())
        mari.utils.connect(g_double_size.clicked, lambda: self._doubleRes())
        mari.utils.connect(g_halve_size.clicked, lambda: self._halveRes())
        mari.utils.connect(g_flip_x.clicked, lambda: self._flipX())
        mari.utils.connect(g_flip_y.clicked, lambda: self._flipY())
        mari.utils.connect(g_buffer_sync.stateChanged, self._BufferSyncSettingChanged)



    def _checkTool(self):
        ''' Checks if the current Tool is the right tool '''
        if mari.tools.currentTool().name() == 'Transform Paint':
            return True
        else:
            return False


    def _BufferSyncSettingChanged(self):
        ''' Turns the Signal Connection on and off '''
        state = g_buffer_sync.isChecked()
        if state == True:
            connectBufferSync()
        if state == False:
            disconnectBufferSync()


    def _setBufferResolutionItem(self):
        ''' Reads the current Buffer resolution and sets the Toolbar Dropdown accordingly '''
        if not self._checkTool():
            return
        else:
            cur_buffer_res = self.paintBuffer.resolution().width()
            g_buffer_size.setCurrentIndex( g_buffer_size.findText( str(cur_buffer_res) + ' x ' + str(cur_buffer_res) ) )


    def _setBufferDepthItem(self):
        ''' Reads the current Buffer depth and sets the Toolbar Dropdown accordingly '''
        if not self._checkTool():
            return
        else:
            cur_buffer_depth =  self.paintBuffer.depth()
            g_buffer_depth.setCurrentIndex( g_buffer_depth.findData( cur_buffer_depth))

    def _setBufferClampItem(self):
        ''' Reads the current Buffer clamp settings and sets the Toolbar Chckbox accordingly '''
        cur_buffer_clamp = self.paintBuffer.clampColors()
        g_buffer_clamp.setChecked(cur_buffer_clamp)


    def _changeBufferResolution(self):
        '''Changes the Paint Buffer Resolution'''
        index = g_buffer_size.currentIndex()
        data = g_buffer_size.itemData(index)
        self.paintBuffer.setResolution(data)


    def _changeBufferDepth(self):
        '''Changes the Paint Buffer Depth'''
        index = g_buffer_depth.currentIndex()
        data = g_buffer_depth.itemText(index)
        depth = g_depth_var_dict[data]
        self.paintBuffer.setDepth(depth)

    def _changeBufferClamp(self):
        '''Changes the Paint Buffer Clamping'''
        checkedState = g_buffer_clamp.isChecked()
        self.paintBuffer.setClampColors(checkedState)

    def _doubleRes(self):
        ''' Doubles the Size of the paintBuffer Res'''
        cur_buffer_res = self.paintBuffer.resolution().width()
        cur_buffer_res *= 2
        if cur_buffer_res > 32768:
            cur_buffer_res = 32768
        g_buffer_size.setCurrentIndex( g_buffer_size.findText( str(cur_buffer_res) + ' x ' + str(cur_buffer_res) ) )

    def _halveRes(self):
        ''' Doubles the Size of the paintBuffer Res'''
        cur_buffer_res = self.paintBuffer.resolution().width()
        cur_buffer_res /= 2
        if cur_buffer_res < 256:
            cur_buffer_res = 256
        g_buffer_size.setCurrentIndex( g_buffer_size.findText( str(cur_buffer_res) + ' x ' + str(cur_buffer_res) ) )


    def _flipX(self):
        ''' Flips the Buffer horizontally'''
        scale = self.paintBuffer.scale()
        scale_x = self.paintBuffer.scale().width() * (-1.0)
        scale.setWidth(scale_x)
        self.paintBuffer.setScale(scale)

    def _flipY(self):
        ''' Flips the Buffer horizontally'''
        scale = self.paintBuffer.scale()
        scale_y = self.paintBuffer.scale().height() * (-1.0)
        scale.setHeight(scale_y)
        self.paintBuffer.setScale(scale)



def syncBufferBitDepth():
    '''Keeps the Paint Buffer Depth in sync with the current paint target'''

    paintBuffer = mari.canvases.paintBuffer()
    cur_channel = mari.current.channel()

    if cur_channel is None:
        return

    channel_depth_var_dict = {mari.Image.Depth.DEPTH_BYTE : mari.PaintBuffer.BufferDepth.DEPTH_BYTE ,

                              mari.Image.Depth.DEPTH_HALF : mari.PaintBuffer.BufferDepth.DEPTH_HALF ,

                              mari.Image.Depth.DEPTH_FLOAT : mari.PaintBuffer.BufferDepth.DEPTH_FLOAT

                             }


    cur_depth = cur_channel.depth()
    buffer_depth = channel_depth_var_dict[cur_depth]
    paintBuffer.setDepth(buffer_depth)


def connectBufferSync():
    ''' Connects the BufferSyncing to Paint Target Changes'''
    cur_geo = mari.current.geo()
    syncBufferBitDepth()
    settings = mari.Settings()
    mari.utils.connect(cur_geo.channelMadeCurrent,syncBufferBitDepth)
    settings.beginGroup('SyncPaintBuffer_BitDepth_'+ version)
    name = 'Buffer_Sync'
    settings.setValue(name,'true')
    settings.endGroup()


def disconnectBufferSync():
    ''' Disconnects the BufferSyncing from Paint Target Changes'''
    cur_geo = mari.current.geo()
    settings = mari.Settings()
    settings.beginGroup('SyncPaintBuffer_BitDepth_'+ version)
    name = 'Buffer_Sync'
    settings.setValue(name,'false')
    settings.endGroup()
    mari.utils.disconnect(cur_geo.channelMadeCurrent,syncBufferBitDepth)


def readBufferSyncSetting():
    ''' Reads the Buffer Sync Setting in the Config file '''
    settings = mari.Settings()
    settings.beginGroup('SyncPaintBuffer_BitDepth_'+ version)
    value = settings.value('Buffer_Sync')
    settings.endGroup()
    return value


def initBufferSyncOnNewProject():
    ''' Turns on Buffer Sync on a new session if it was active on previous session close'''
    savedState = readBufferSyncSetting()
    if savedState == 'true':
        connectBufferSync()


def initToolbar():
    ''' Initalizes toolbar connection'''
    bufferAction = mari.actions.get('/Mari/Tools/General/Transform Paint')
    mari.utils.connect(bufferAction.triggered, paintBufferToolbar)

