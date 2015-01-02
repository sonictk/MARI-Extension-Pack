# ------------------------------------------------------------------------------
# Export Images from Image Manager
# ------------------------------------------------------------------------------
# Will Export selected Images from the Image Manager
# If Images have a file format, the file format will be used for export,
# otherwise TIF Format is used.
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
from PythonQt import QtGui, QtCore
import os

class ProgressDialog(QtGui.QDialog):

	def __init__(self, maxStep):
		super(ProgressDialog, self).__init__()
		self.setWindowTitle('Exporting Images...')

		self.cancelCpy = False

		layout = QtGui.QVBoxLayout()
		self.setLayout(layout)
		self.pbar = QtGui.QProgressBar(self)
		self.pbar.setRange(0, maxStep)
		self.pbar.setGeometry(30, 40, 200, 25)

		self.pbar.connect("valueChanged (int)", self.status)
		layout.addWidget(self.pbar)

		self.cBtn = QtGui.QPushButton("cancel")
		self.cBtn.connect('clicked()', lambda: self.cancelCopy())
		layout.addWidget(self.cBtn)
	
	def status(self):
		if self.pbar.value == self.pbar.maximum:
			self.close()
		
	def cancelCopy(self):
		self.pbar.value = self.pbar.maximum
		self.cancelCpy = True

def exportSelImgs():
	''' export the selected images to the given path '''
	if not mari.projects.current():
		mari.utils.message("No project currently open")
		return

	path = mari.utils.getExistingDirectory()
	if not os.path.exists(path):
		mari.utils.message("Not a valid path")
		return
	else:
		path = path + '/'

	images = mari.images.selected()

	if len(images) == 0:
		mari.utils.message("No images currently selected")
		return
	
	formats = [ str(i) for i in mari.images.supportedWriteFormats() ]

	maxStep = len( images )

	progressDiag = ProgressDialog(maxStep)
	progressDiag.show()

	progStep = 0
	for image in images:

		if progressDiag.cancelCpy == True:
			progressDiag.close()
			return

		imageName = ( image.filePath() ).split("/")[-1]

		try:
			format = imageName.split(".")[-1]

			# check if the format is valid...
			if format in formats:
				image.saveAs( path + imageName )
			else:
				format = ".tif"
				image.saveAs( path + imageName + format)
		except:
			pass

		progStep += 1
		progressDiag.pbar.setValue(progStep)

