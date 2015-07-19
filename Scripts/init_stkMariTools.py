#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" Module stk_MariTools: This module acts as the entry point for the toolkit.. """

# noinspection PyUnresolvedReferences
import mari
import logging

from stkMariTools.lib.app_utils import MariAppUtils

# Setup logging and streamhandler
logging.basicConfig(level=logging.DEBUG)


def start():
    """
    This initializes the module and acts as the entry point.

    :return: `None`
    """
    logger = logging.getLogger(__name__)

    # Check for appropriate Mari version
    if MariAppUtils.checkSupportedMariVersion():
        logger.debug('\n####################################\n'
                     'Intializing stkMariTools plugin...\n'
                     '####################################\n\n')

        # Add the menu items
        MariAppUtils.addMenuItems()

    else:
        logger.error('### stkMariTools not supported on this version of Mari!!!')


start()

