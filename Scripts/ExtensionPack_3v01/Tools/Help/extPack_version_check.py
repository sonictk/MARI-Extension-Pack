# ------------------------------------------------------------------------------
# MARI Extension Pack Version Check
# ------------------------------------------------------------------------------
# Check if installed version is the most up to date version
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


try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
import mari


def get_version(url):
    """Receive the content of ``url``, parse it as JSON and return the
       object.
    """

    try:
        response = urlopen(url)
        data = str(response.read())
        return data
    except Exception:
        mari.utils.message('Unable to connect to server', 'Unable to connect')
        return

def check_version():
    """ Check current version against installed version """

    INSTALLED_VERSION = '3.0.01'

    url = 'http://www.campi3d.com/External/MariExtensionPack/VersionCheck/ExtensionPackVersion.json'
    CURRENT_VERSION = get_version(url)

    if CURRENT_VERSION != None:

        if INSTALLED_VERSION != CURRENT_VERSION:
            mari.utils.message('A newer version of Mari Extension Pack is available: ' + CURRENT_VERSION + '\n\nDownload at www.MariExtensionPack.org', 'Newer Version available')
        else:
            mari.utils.message('Your MARI Extension Pack is up to date', 'No new version found')