# ------------------------------------------------------------------------------
# Mari Extension Pack Importer
# Copyright (c) 2014 Mari Ideascale. All Rights Reserved.
# ------------------------------------------------------------------------------
# File: initExtensionPack.py
# Description: Main script to import Tools and Shaders and check MARI compatibility
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
import os
import xml.etree.ElementTree as ET
import time
from PySide import QtGui


# EXTENSION PACK VERSION
current_extension_pack = "2.0"



# SCRIPT DIRECTORY PATH(S)
base_path = os.path.abspath(mari.resources.path(mari.resources.USER_SCRIPTS))
if mari.app.version().isWindows():
    base_path = base_path.split(';')
else:
    base_path = base_path.split(':')

# ------------------------------------------------------------------------------

def checkMariVersion():
    "Checks if Mari Version is compatible"
    MARI_2_6v3_VERSION_NUMBER =   20603300 #MARI 2.6v3

    if mari.app.version().number() >=  MARI_2_6v3_VERSION_NUMBER:

	return True, True
    
    else:
        mari.utils.message("Mari Version not compatible with MARI Extension Pack 2.0")
        return False, False

# ------------------------------------------------------------------------------

def detectScriptConflict():
	'''Finds existing copies from the blacklist of script files from ideascale'''

	# This is the Blacklist of Files that are being looked for
	# If one of these is found, the ExtensionPack will refuse to load
	# to avoid Version Conflicts 
	illegalFiles = ['bnChanLayer.py','bnChanLayer.pyc','bnMaskFromSelection.py','bnMaskFromSelection.pyc',
					'patch_bake.py','patch_bake.pyc','toggle_layer_visibility_lock.py','toggle_layer_visibility_lock.pyc',
					'ak_unprojectChannelToImageman_v1-ab0cd4.py','ak_unprojectChannelToImageman_v1-ab0cd4.pyc',
					'ak_unprojectLayerToImageman_v1-4c13d7.py','ak_unprojectLayerToImageman_v1-4c13d7.pyc',
					'mergeDuplicateLayers.py','mergeDuplicateLayers.pyc',
					'screenshotAllChannels.py','screenshotAllChannels.pyc',
					'channel_template.py','channel_template.pyc','convert_selected_to_paintable.py',
					'convert_selected_to_paintable.pyc','export_image_manager_images.py','export_image_manager_images.pyc',
					'export_selected_channels.py','export_selected_channels.pyc','export_uv_masks.py','export_uv_masks.pyc'
					'flatten_selected_channels.py','flatten_selected_channels.pyc','layer_visibility.py','layer_visibility.pyc'
					]

	errorDict = {}
	conflict = False

	for scriptpath in base_path:

		for path, subdirs, files in os.walk(scriptpath):
	
			path_str = path.replace("\\", "/")
	
			for name in files:
	
				for FileName in illegalFiles:
	
					if name.startswith(FileName) and name.endswith(FileName) :
		
						errorDict[name] = path_str + '/' + FileName
						conflict = True
		

	return conflict, errorDict      
 
# ------------------------------------------------------------------------------


def versionConflictCheck():
	'''Outputs Version Conflicts to Python Console'''
	version_conflict = detectScriptConflict()
	pathLib = version_conflict[1]
	pathDict = {}

	if version_conflict[0]:

			print '#####################################################'
			print '           VERSION CONFLICT DETECTED '
			print 'The following files in your Script Directory are'
			print 'in conflict with the Extension Pack (old version)'
	
			print ''
			print 'Please remove the following from your Script Directory:'
			print ''
			for path in pathLib:
				path_edit = pathLib[path]
				path_str = path_edit.replace("\\", "/")
				pathDict[path_str] = path_str
				print path_str
			print ''
			print '#####################################################'
			print ''
			print '	       MARI EXTENSION PACK DID NOT LOAD'
			print '         See printout above to resolve'
			print ''
			print '#####################################################'
			return False, pathDict

	else:

		return True, pathDict

# ------------------------------------------------------------------------------

def resolveScriptConflict(input_paths):
	''' Will rename any offending files and edit JTOOLS-INIT File if found to remove imports '''

	print ''
	print '	        MARI EXTENSION PACK CONFLICT  '
	print '      Trying automatic conflict resolve'
	print ''

	for files in input_paths:
		file_exists = os.path.exists(files)
		if file_exists:
				os.rename(files,files+'.VersionConflict')
				time.sleep(1)
				print 'Renamed conflicting file, (.VersionConflict):'
				print files
				print ''
		else:
				files = files.replace("/", "\\")
				os.rename(files,files+'.VersionConflict')
				time.sleep(1)
				print 'Renamed conflicting file, (.VersionConflict):'
				print files
				print ''


	

	mari.utils.message("Please restart MARI to complete automatic resolve")
	


# ------------------------------------------------------------------------------



class versionConflictUI(QtGui.QDialog):
	'''Dialog listing Scripts in conflict with Extension Pack'''
	def __init__(self,input_paths):
		super(versionConflictUI, self).__init__()
		# Dialog Settings
		self.setFixedSize(550, 200)
		self.setWindowTitle('EXTENSION PACK VERSION CONFLICT')
		# Layouts
		layoutV1 = QtGui.QVBoxLayout()
		layoutH1 = QtGui.QHBoxLayout()
		self.setLayout(layoutV1)
		# Widgets
		self.DescrA =  QtGui.QLabel("A Version Conflict was detected in your Script Directory")
		self.DescrB =  QtGui.QLabel("You have files installed that have newer versions in MARI Extension Pack")
		self.DescrC =  QtGui.QLabel("Please open your Console via the PYTHON Menu for a list of files ")
		self.DescrD =  QtGui.QLabel("Choosing to Resolve Automatically will try to remove the offending files")
		self.cancelBtn = QtGui.QPushButton('Close')
		self.resolveBtn = QtGui.QPushButton('Resolve')
		# Populate 
		layoutV1.addWidget(self.DescrA)
		layoutV1.addWidget(self.DescrB)
		layoutV1.addWidget(self.DescrC)
		layoutV1.addWidget(self.DescrD)
		layoutV1.addLayout(layoutH1)
		layoutH1.addWidget(self.cancelBtn)
		layoutH1.addWidget(self.resolveBtn)
		# Connections
		self.cancelBtn.clicked.connect(self.excepDialog)
		self.resolveBtn.clicked.connect(lambda: self.closeResolveDialog(input_paths))
		self.raise_()
		self.activateWindow()

	def excepDialog(self):
		''' Closes Dialog and throws a warning message '''
		self.close()
		mari.utils.message("MARI Extension Pack did NOT LOAD: Version Conflict")

	def closeResolveDialog(self,input_paths):
		''' Attempts to rename offending files and edit JTOOLS-INIT '''
		resolveScriptConflict(input_paths)
		self.close()



# ------------------------------------------------------------------------------

def extPackLoad():
	'''Loads MARI Extension Pack'''

	# Checking MARI Version
	mari_version = checkMariVersion()
		

		
	if not mari_version[0]:
		print ' '
		print '  Mari Extension Pack ' + current_extension_pack
		print '     DID NOT LOAD'
		print ' '
		print 'Reason: Incompatible Mari Version'	
		print ' '
		return

	# Checking Script Conflicts
	script_version = versionConflictCheck()

	if not script_version[0]:
		paths = script_version[1]
		versionConflictUI(paths).exec_()
		return
	
	else:
	
		import Tools
		import Shaders.RegisterCustomShaders
	
	# End Console Printout success:
		   
	print '#####################################################'
	print 'Mari Extension Pack ' + current_extension_pack + ' finished loading successfully'
	print '#####################################################'
	print '            http://mari.ideascale.com'
	print ''





# ------------------------------------------------------------------------------
# Start Console Printout
# ------------------------------------------------------------------------------

print '-----------------------------------------'
print "MARI Extension Pack: "+ current_extension_pack
print '-----------------------------------------'
print "http://mari.ideascale.com"
print '-----------------------------------------'

extPackLoad()