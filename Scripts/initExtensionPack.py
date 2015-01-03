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

current_extension_pack = "1.7"

# ------------------------------------------------------------------------------
# Start Console Printout
# ------------------------------------------------------------------------------

print '-----------------------------------------'
print "MARI Extension Pack: "+ current_extension_pack
print '-----------------------------------------'
print "http://mari.ideascale.com"
print '-----------------------------------------'


# ------------------------------------------------------------------------------
# Checking Mari Version
# ------------------------------------------------------------------------------

def isMariSuitable():
    "Checks Mari Version"
    MARI_2_6v3_VERSION_NUMBER =   20603300 #MARI 2.6v3

    if mari.app.version().number() >=  MARI_2_6v3_VERSION_NUMBER:

        import Tools
        import Shaders.RegisterCustomShaders

	return True, True
    
    else:
        mari.utils.message("Mari Version not compatible with MARI Extension Pack 1.7")
        return False, False

# ------------------------------------------------------------------------------

def ExtensionPackInit():
	suitable = isMariSuitable()

# End Console Printout Failure

	if not suitable[0]:
		print ' '
		print '  Mari Extension Pack ' + current_extension_pack
		print '     DID NOT LOAD'
		print ' '
		print 'Reason: Incompatible Mari Version'	
		print ' '
		return

# End Console Printout success:
   
	print '#####################################################'
	print 'Mari Extension Pack ' + current_extension_pack + ' finished loading successfully'
	print '#####################################################'
	print '            http://mari.ideascale.com'
	print ''


ExtensionPackInit()