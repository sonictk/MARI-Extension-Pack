# ------------------------------------------------------------------------------
# Set Subdivision Levels
# ------------------------------------------------------------------------------
# SetSubdivisionLevels lets you apply global changes of subdivision display to
# all your objects or just visible object. It contains the actions:
# - Set all Objects to Highest level, Set all Objects to Lowest level
# - Set Visible Objects to Highest level, set Visible Objects to Lowest Level
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
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore


def setAllToHighest():
    """Sets all Geo to Highest SUBD Level"""

    geoList = mari.geo.list()
    locked = False
    locked_ignore = False

    #check if some geo is locked
    for geo in geoList:
        if geo.isLocked():
            locked = True

    if locked:
        info_dialog = Locked_InfoUI()
        info_dialog.exec_()
        info_reply = info_dialog.buttonRole(info_dialog.clickedButton())
        if info_reply is QtGui.QMessageBox.ButtonRole.YesRole:
            locked_ignore = True
        if info_reply is QtGui.QMessageBox.ButtonRole.NoRole:
            locked_ignore = False

    for geo in geoList:
        if locked_ignore and geo.isLocked():
            geo.setLocked(False)
            #Stepping through all subdLevels to get the highest
            geo.setSubdivisionLevel(0)
            geo.setSubdivisionLevel(1)
            geo.setSubdivisionLevel(2)
            geo.setSubdivisionLevel(3)
            geo.setLocked(True)
        if  geo.isLocked() is False:
            #Stepping through all subdLevels to get the highest
            geo.setSubdivisionLevel(0)
            geo.setSubdivisionLevel(1)
            geo.setSubdivisionLevel(2)
            geo.setSubdivisionLevel(3)


def setAllToLowest():
    """Sets all Geo to Lowest SUBD Level"""

    geoList = mari.geo.list()
    locked = False
    locked_ignore = False

    #check if some geo is locked
    for geo in geoList:
        if geo.isLocked():
            locked = True

    if locked:
        info_dialog = Locked_InfoUI()
        info_dialog.exec_()
        info_reply = info_dialog.buttonRole(info_dialog.clickedButton())
        if info_reply is QtGui.QMessageBox.ButtonRole.YesRole:
            locked_ignore = True
        if info_reply is QtGui.QMessageBox.ButtonRole.NoRole:
            locked_ignore = False


    for geo in geoList:
        if locked_ignore and geo.isLocked():
            geo.setLocked(False)
            geo.setSubdivisionLevel(0)
            geo.setLocked(True)
        if geo.isLocked() is False:
            geo.setSubdivisionLevel(0)

def setAllVisibleToHighest():
    """Sets all Visible Geo to Highest SUBD Level"""

    geoList = mari.geo.list()
    locked = False
    locked_ignore = False

    #check if some geo is locked
    for geo in geoList:
        if geo.isLocked() and geo.isVisible():
            locked = True

    if locked:
        info_dialog = Locked_InfoUI()
        info_dialog.exec_()
        info_reply = info_dialog.buttonRole(info_dialog.clickedButton())
        print info_reply
        if info_reply is QtGui.QMessageBox.ButtonRole.YesRole:
            locked_ignore = True
        if info_reply is QtGui.QMessageBox.ButtonRole.NoRole:
            locked_ignore = False

    for geo in geoList:
        if locked_ignore and geo.isLocked() and geo.isVisible():
            geo.setLocked(False)
            #Stepping through all subdLevels to get the highest
            geo.setSubdivisionLevel(0)
            geo.setSubdivisionLevel(1)
            geo.setSubdivisionLevel(2)
            geo.setSubdivisionLevel(3)
            geo.setLocked(True)
        if geo.isVisible() and (geo.isLocked() is False):
            #Stepping through all subdLevels to get the highest
            geo.setSubdivisionLevel(0)
            geo.setSubdivisionLevel(1)
            geo.setSubdivisionLevel(2)
            geo.setSubdivisionLevel(3)

def setAllVisibleToLowest():
    """Sets all Visible Geo to Lowest SUBD Level"""

    geoList = mari.geo.list()
    locked = False
    locked_ignore = False

    #check if some geo is locked
    for geo in geoList:
        if geo.isLocked() and geo.isVisible():
            locked = True

    if locked:
        info_dialog = Locked_InfoUI()
        info_dialog.exec_()
        info_reply = info_dialog.buttonRole(info_dialog.clickedButton())
        if info_reply is QtGui.QMessageBox.ButtonRole.YesRole:
            locked_ignore = True
        if info_reply is QtGui.QMessageBox.ButtonRole.NoRole:
            locked_ignore = False

    for geo in geoList:
        if locked_ignore and geo.isLocked() and geo.isVisible():
            geo.setLocked(False)
            geo.setSubdivisionLevel(0)
            geo.setLocked(True)
        if geo.isVisible() and (geo.isLocked() is False):
            geo.setSubdivisionLevel(0)


# ------------------------------------------------------------------------------

class Locked_InfoUI(QtGui.QMessageBox):
    """Informs the user that some Geo is locked and asks how to proceed"""
    def __init__(self,parent=None):
        super(Locked_InfoUI, self).__init__(parent)

        # Create info gui
        self.setWindowTitle('Some Objects are locked')
        self.setIcon(QtGui.QMessageBox.Warning)
        self.setText('Some Objects are currently locked. \n\n Do you wish to change locked Objects as well ?')
        self.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        self.setDefaultButton(QtGui.QMessageBox.Yes)


