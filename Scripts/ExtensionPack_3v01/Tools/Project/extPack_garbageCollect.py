# ------------------------------------------------------------------------------
# mari.ddi.garbageCollect
# ------------------------------------------------------------------------------
# Removes junk from your Project
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
        self.setWindowTitle('Warning: Your history will be cleared !')
        self.setIcon(QtGui.QMessageBox.Warning)
        self.setText('Please be advised, this process will:\n\n\
- save your project\n\
- clear your history.\n\n\
You will not be able to undo any action from before running\n\
garbage Collection\n\n\
For best results, please close & reopen your project after the process completes.\n\n\
There is no success mesage. Depending on the amount of unnecessary data on disc and speed of your HD\n\
allow a few minutes of idle time for the process to complete.\n')
        self.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        self.setDefaultButton(QtGui.QMessageBox.Cancel)



def cleanUp():
    ''' Removes all Snapshots from your Project'''

    warning = WarningUI()
    warning.exec_()
    warning_reply = warning.buttonRole(warning.clickedButton())
    # If User chooses to Ignore problematic paths, we will remove the prolematic ones from the dictionary
    if warning_reply is QtGui.QMessageBox.ButtonRole.AcceptRole:
        project = mari.current.project()
        project.save()
        mari.history.clear(False)
        mari.ddi.garbageCollect()
        project.save()

    else:
        return