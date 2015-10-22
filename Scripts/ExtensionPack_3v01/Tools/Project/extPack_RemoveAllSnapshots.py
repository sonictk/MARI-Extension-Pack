# ------------------------------------------------------------------------------
# Remove All Project Snapshots
# ------------------------------------------------------------------------------
# Removes all saved snapshots (channels, layers) from your project
# Same as using it from your Snapshot Menu but just added for convenience
# when optimizing a project.
# ------------------------------------------------------------------------------
# Written by Jens Kafitz, 2015
# ------------------------------------------------------------------------------
# http://www.jenskafitz.com
# ------------------------------------------------------------------------------
# Last Modified: 16 October 2015
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



class WarningUI(QtGui.QMessageBox):
    """Informs the user that this is not undoable"""
    def __init__(self,parent=None):
        super(WarningUI, self).__init__(parent)
        # Create info gui
        self.setWindowTitle('Warning !')
        self.setIcon(QtGui.QMessageBox.Warning)
        self.setText('Removing all Snapshots will \n\n- remove ALL snapshots from your project\n- clear the history\n- Save the project\n\nYou will not be able to undo this action or any before it.')
        self.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        self.setDefaultButton(QtGui.QMessageBox.Cancel)



def removeAllSnapshots():
    ''' Removes all Snapshots from your Project'''

    warning = WarningUI()
    warning.exec_()
    warning_reply = warning.buttonRole(warning.clickedButton())
    if warning_reply is QtGui.QMessageBox.ButtonRole.AcceptRole:
        mari.system.snapshots.deleteAll(False)
        project = mari.current.project()
        project.save()
        mari.history.clear(False)
        mari.utils.message('All Snapshots removed','Snapshots')

    else:
        return