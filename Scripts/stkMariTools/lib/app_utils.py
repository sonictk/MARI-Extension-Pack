#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" Module app_utils: This module contains useful methods for dealing with Mari. """

import mari


class MariAppUtils(object):
    """
    This class contains useful methods for interacting with the Mari application.
    """

    # Defining constants
    MARI_2_6v3_VERSION_NUMBER =   20603300 #MARI 2.6v3


    @classmethod
    def checkSupportedMariVersion(cls):
        """
        This method checks for a Mari version that is supported by the plugin.

        return: `bool` determining if the current Mari version is supported.
        rtype: `bool`
        """

        currentMariVersion = mari.app.version().number()

        if currentMariVersion >=  cls.MARI_2_6v3_VERSION_NUMBER:
            return True
        else:
            return False