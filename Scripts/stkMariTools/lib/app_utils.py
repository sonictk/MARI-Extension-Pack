#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" Module app_utils: This module contains useful methods for dealing with Mari. """

import mari
import os

from stkMariTools.tools.cache.clearHistory import ClearHistoryMenuItem


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

    @classmethod
    def addMenuItems(cls):
        """
        This method adds all valid menu items to the Mari main menu.

        :return:
        """

        # Scrape all directories and find valid menu item modules
        basePath = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))

        for root, dirs, filenames in os.walk(basePath, followlinks=True):
            for filename in filenames:
                if filename.endswith('.py'):
                    pass


        # hardcoded add menu items for now
        ClearHistoryMenuItem()


