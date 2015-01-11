# ------------------------------------------------------------------------------
# Mari Extension Pack Importer
# Copyright (c) 2014 Mari Ideascale. All Rights Reserved.
# ------------------------------------------------------------------------------
# File: initExtensionPack.py
# Description: Main script to import Tools and Shaders and check MARI compatibility
# ------------------------------------------------------------------------------
# Author: Jens Kafitz, 2015
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
import os, sys, time
import fileinput
from PySide import QtGui


# EXTENSION PACK VERSION
current_extension_pack = "2.0"


# SCRIPT DIRECTORY PATH(S)
base_path = os.path.abspath(mari.resources.path(mari.resources.USER_SCRIPTS))
if mari.app.version().isWindows():
    base_path = base_path.split(';')
else:
    base_path = base_path.split(':')



######################################################################

# BLACKLIST FOR VERSION CONFLICTS:


# Blacklist of PY Files in Script Directories - any one of these will throw an error since they are included in the extension pack
illegalFiles = ["bnChanLayer.py","bnChanLayer.pyc","bnMaskFromSelection.py","bnMaskFromSelection.pyc",
				"patch_bake.py","patch_bake.pyc","toggle_layer_visibility_lock.py","toggle_layer_visibility_lock.pyc",
				"ak_unprojectChannelToImageman_v1-ab0cd4.py","ak_unprojectChannelToImageman_v1-ab0cd4.pyc",
				"ak_unprojectLayerToImageman_v1-4c13d7.py","ak_unprojectLayerToImageman_v1-4c13d7.pyc",
				"ak_unprojectChannelToImageman_v1.py","ak_unprojectChannelToImageman_v1.pyc",
				"ak_unprojectLayerToImageman_v1.py","ak_unprojectLayerToImageman_v1.pyc",
				"mergeDuplicateLayers.py","mergeDuplicateLayers.pyc",
				"screenshotAllChannels.py","screenshotAllChannels.pyc",
				"channel_template.py","channel_template.pyc","convert_selected_to_paintable.py",
				"convert_selected_to_paintable.pyc","export_image_manager_images.py","export_image_manager_images.pyc",
				"export_selected_channels.py","export_selected_channels.pyc","export_uv_masks.py","export_uv_masks.pyc",
				"flatten_selected_channels.py","flatten_selected_channels.pyc","layer_visibility.py","layer_visibility.pyc"
				]

# Blacklist of Shader Files in Script Directories - any one of these will throw an error since they are included in the extension pack
illegalShaders = ["JK_AlbedoWarning.xml","initShaders.py","initShaders.pyc"]

# Blacklist of Modules within JTOOLS __INIT__ - any of these will cause an error after the original file was renamed
illegal_Modules = ["import channel_template","import convert_selected_to_paintable","import export_image_manager_images",
				"import export_selected_channels","import export_uv_masks","import flatten_selected_channels","import layer_visibility"
			    ]


# Blacklist of Functions within JTOOLS INIT
illegal_Func = ["def convertSelectedToPaintable(self):","convert_selected_to_paintable.convertSelectedToPaintable()",
				"def createChannelFromTemplate(self):","channel_template.createChannelFromTemplate()",
				"def exportImageManagerImages(self):","export_image_manager_images.exportImageManagerImages()",
				"def exportSelectedChannels(self):","export_selected_channels.exportSelectedChannels()",
				"def flattenMaskStacks(self):","flatten_mask_stacks.flattenMaskStacks()",
				"def flattenSelectedChannels(self):","flatten_selected_channels.flattenSelectedChannels()",
				"def getChannelTemplate(self):","channel_template.getChannelTemplate()",
				"def layerVisibility(self):","layer_visibility.layerVisibility()",
				"def setChannelFromTemplate(self):","channel_template.setChannelFromTemplate()"]


######################################################################

# Functions in order:

# checkMariVersion()
# detectScriptConflict()
# versionConflictCheck()
# detectJTOOLS()
# resolveScriptConflict(input_paths)
# resolveJToolsConflict(jtools_path)
# versionConflictUI(QtGui.QDialog)
# extPackLoad()


######################################################################


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

	script_error_dict = {}
	shader_error_dict = {}
	script_conflict = False
	shader_conflict = False

	for scriptpath in base_path:

		for path, subdirs, files in os.walk(scriptpath):
	
			path_str = path.replace("\\", "/")
	
			for name in files:
	
				for script_name in illegalFiles:
	
					if name.startswith(script_name) and name.endswith(script_name) :
		
						script_error_dict[name] = path_str + '/' + script_name
						script_conflict = True

				for shader_name in illegalShaders:
					
					if name.startswith(shader_name) and name.endswith(shader_name) :
						
						shader_error_dict[name] = path_str + '/' + shader_name
						shader_conflict = True

	
	return script_conflict, shader_conflict, script_error_dict, shader_error_dict     


# ------------------------------------------------------------------------------



def versionConflictCheck():
	'''Outputs Version Conflicts to Python Console'''
	version_conflict = detectScriptConflict()

	# Script Conflict Dict
	# [0] Script Conflict
	# [1] Shader Conflict
	# [2] Script Error Paths
	# [3] Shader Error Paths

	script_pathLib = version_conflict[2]
	shader_pathLib = version_conflict[3]
	script_pathDict = {}
	shader_pathDict = {}

	if version_conflict[0] or version_conflict[1]:

			print '#####################################################'
			print '           VERSION CONFLICT DETECTED '
			print '#####################################################'
			print 'The following files in your Script Directory are'
			print 'in conflict with the Extension Pack (old version)'

			if version_conflict[0]:
				print ''
				print 'Please remove or rename the following from your Script Directory:'
				print ''
				for script_path in script_pathLib:
					script_path_edit = script_pathLib[script_path]
					script_path_str = script_path_edit.replace("\\", "/")
					script_pathDict[script_path_str] = script_path_str
					print script_path_str
				print ''
			if version_conflict[1]:
				print 'Please remove the following conflicting shader or node versions:'
				print ''
				for shader_path in shader_pathLib:
					shader_path_edit = shader_pathLib[shader_path]
					shader_path_str = shader_path_edit.replace("\\", "/")
					shader_pathDict[shader_path_str] = shader_path_str
					print shader_path_str
				print ''

			print '-----------------------------------------------------'
			print ''

			return True, script_pathDict, shader_pathDict, version_conflict[0], version_conflict[1]


	else:

		return False, script_pathDict, shader_pathDict,  version_conflict[0], version_conflict[1]


# ------------------------------------------------------------------------------

def detectJTOOLS():
	''' Will scan for old JTOOLS Versions. If found it usually means some modules need to be removed 
		from its init file'''

	module_wrong = False
	module_path = ''

	for scriptpath in base_path:
		for root, dirs, files in os.walk(scriptpath):
			for dir in dirs:
				if dir == 'jtools':
					jtools_path =  os.path.join(root, dir)
					init_path = jtools_path + '\\' + '__init__.py'
					file_exists = os.path.exists(init_path)
					if not file_exists:
						init_path = init_path.replace("\\", "/")
						file_exists = os.path.exists(init_path)
					if file_exists:
						module_path = ''
						module_wrong = False
						for line in fileinput.input(init_path):
							for module in illegal_Modules:
								VersionName = -1
								Commented = -1
								Commented = line.find('#')
								VersionName = line.find(module)
								# If module is found and is not commented out:
								if VersionName is not -1 and Commented is -1:
									print module
									module_path = init_path
									module_wrong = True
					else:
						print 'JTOOLS __init__.py could not be found.'
						print 'If you encounter an error in the Python Console'
						print 'it is recommended to download the latest version from'
						print 'http://mari.ideascale.com'

					print ''


	return module_wrong, module_path
								

# ------------------------------------------------------------------------------
 
def resolveScriptConflict(script_input_state):
	''' Will rename any offending files'''

	print ''
	print '      Trying automatic conflict resolve'
	print ''
	print '#####################################################'

	script_success_state = False
	shader_success_state = False

	script_input_paths = script_input_state[1]
	shader_input_paths = script_input_state[2]


	# Script_Input_state dict
	# [0] General Conflict (Scripts or Shaders)
	# [1] Script Error Paths
	# [2] Shader Error Paths
	# [3] Script Conflict Exists
	# [4] Shader Conflict Exists
	
	# Fixing conflicting scripts
	for script_files in script_input_paths:
		script_success_state = False
		file_exists = os.path.exists(script_files) 
		# tests if a .VersionConflict file exists as well:
		file_conflict_exists = os.path.exists(script_files+'.VersionConflict') 
		if file_exists:
				if file_conflict_exists:
					os.remove(script_files+'.VersionConflict')
				os.rename(script_files,script_files+'.VersionConflict')
				time.sleep(1)
				print 'Renamed conflicting file, (.VersionConflict):'
				print script_files
				print ''
				script_success_state = True

		else:
				script_files = script_files.replace("/", "\\")
				file_conflict_exists = os.path.exists(script_files+'.VersionConflict') 
				if file_conflict_exists:
					os.remove(script_files+'.VersionConflict')
				os.rename(script_files,script_files+'.VersionConflict')
				time.sleep(1)
				print 'Renamed conflicting file, (.VersionConflict):'
				print script_files
				print ''
				script_success_state = True


	for shader_files in shader_input_paths:
			shader_success_state = False
			file_exists = os.path.exists(shader_files) 
			if file_exists:
					os.remove(shader_files)
					time.sleep(1)
					print ''
					print 'Removed old shader file:'
					print shader_files
					print ''
					shader_success_state = True
	
			else:
					shader_files = shader_files.replace("/", "\\")
					os.remove(shader_files)
					time.sleep(1)
					print ''
					print 'Removed old shader file:'
					print shader_files
					print ''
					shader_success_state = True


	return script_success_state, shader_success_state, script_input_state[3], script_input_state[4]

	
# ------------------------------------------------------------------------------

def resolveJToolsConflict(jtools_path):
	''' Will edit jtools __init__ file to remove modules and functions '''

	try: 
		f1 = open(jtools_path, 'r')
		f2 = open(jtools_path + '._tmp', 'w')
		for line in f1:
			line_write = False
			for module in illegal_Modules:
				if module in line:
					f2.write("# " + line)
					line_write = True
			for function in illegal_Func:
				if function in line:
					f2.write("# " + line)
					line_write = True
	
			if not line_write:
				f2.write(line)
	
	
		f1.close()	
		f2.close()
	
		# Rename old __init__ to __init__.py.VersionConflict, check if exists before
		file_conflict_exists = False
		file_conflict_exists = os.path.exists(jtools_path+'.VersionConflict') 
		if file_conflict_exists:
			os.remove(jtools_path+'.VersionConflict')
	
		os.rename(jtools_path,jtools_path+'.VersionConflict')
	
		# Rename new __init__ to __init__.py
		os.rename(jtools_path + '._tmp',jtools_path)

		return True

	except Exception:

		return False
		

# ------------------------------------------------------------------------------



class versionConflictUI(QtGui.QDialog):
	'''Dialog listing Scripts in conflict with Extension Pack'''
	def __init__(self,script_input_state,jtools_path):
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
		self.DescrD =  QtGui.QLabel("Choosing to Fix Automatically will try to rename the offending files")
		self.cancelBtn = QtGui.QPushButton('Cancel')
		self.resolveBtn = QtGui.QPushButton('Fix')
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
		self.resolveBtn.clicked.connect(lambda: self.closeResolveDialog(script_input_state,jtools_path))
		self.raise_()
		self.activateWindow()

	def excepDialog(self):
		''' Closes Dialog and throws a warning message '''
		self.close()
		mari.utils.message("MARI Extension Pack did NOT LOAD:\nVersion Conflict\nCheck Python Console for Details")

	def closeResolveDialog(self,script_input_state,jtools_path):
		''' Attempts to rename offending files and edit JTOOLS-INIT '''
		scriptResolve = resolveScriptConflict(script_input_state)

		# Script_Resolve dict
		# [0] script fix success
		# [1] shader fix success
		# [2] script problem existed
		# [3] shader problem existed

		jtoolsresolve = True
		tools_resolve = True
		shaders_resolve = True

		if scriptResolve[2]: #if there was a problem at all
			if scriptResolve[0]: #if it was fixed
				print 'Script File Rename:  Successful'
				print ''
				tools_resolve = True
			else:
				print 'Script File Rename Failed: You may not have write permissions to the folder'
				print ''
				tools_resolve = False
		else:
			tools_resolve = True

		if scriptResolve[3]: #if there was a problem at all
			if scriptResolve[1]: #if it was fixed
				print 'Old Shaders removed:  Successful'
				print ''
				shaders_resolve = True
			else:
				print 'Removal of old Shaders failed: You may not have write permissions to the folder'	
				print ''
				shaders_resolve = False
		else:
			shaders_resolve = True
	
		if jtools_path != '':
			jtoolsresolve = resolveJToolsConflict(jtools_path)
			if jtoolsresolve:
				print 'JTOOLS __INIT__ File successfully patched'
				print ''
			else:
				print 'Error occurred during edit of JTOOLS __INIT__.py:'
				print 'You may not have write permissions to the folder'
				print ''

		if tools_resolve and shaders_resolve and jtoolsresolve:
			mari.utils.message('Conflicts successfully fixed. Please restart MARI')

		else:
			mari.utils.message('An error occured during the automatic fix.\nYou may not have write permissions to the Script Folder\nCheck Python Console for details.')
			
		self.close()



# ------------------------------------------------------------------------------

def extPackLoad():
	'''Loads MARI Extension Pack'''

	# Checking MARI Version, if False Error
	mari_version = checkMariVersion()		
	if not mari_version[0]:
		print ' '
		print '  Mari Extension Pack ' + current_extension_pack
		print '     DID NOT LOAD'
		print ' '
		print 'Reason: Incompatible Mari Version'	
		print ' '
		return

	# Checking Script Conflicts & jtools init state
	script_version = versionConflictCheck()

	# Script Version Check Dict
	# [0] General Conflict (Scripts or Shaders)
	# [1] Script Error Paths
	# [2] Shader Error Paths
	# [3] Script Conflict Exists
	# [4] Shader Conflict Exists

	jtools = detectJTOOLS()


	if script_version[0] or jtools[1]:
		# Location of JTOOLS INIT, empty if it doesn't exist
		jtools_path = jtools[1]

		# if JTOOLS Check returns TRUE means that there are Modules
		# within its __init__ file that need to be disabled 
		if jtools[0]:
			print 'Conflicting Modules from JTOOLS above need to be removed from'
			print 'File: ' + jtools[1]
			print ''


		print ''
		print '#####################################################'
		print ''
		print '	       MARI EXTENSION PACK DID NOT LOAD'
		print '         See printout above to resolve'
		print ''
		print '#####################################################'
			

		versionConflictUI(script_version,jtools_path).exec_()

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