#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" Module stk_MariTools: This module acts as the entry point for the toolkit.. """

# noinspection PyUnresolvedReferences
import mari
import logging
import sys
import traceback

from stkMariTools.lib.app_utils import MariAppUtils

# Setup logging and streamhandler
logging.basicConfig(level=logging.DEBUG)


def start():
    """
    This initializes the module and acts as the entry point.
    """
    logger = logging.getLogger(__name__)

    # Check for appropriate Mari version
    if MariAppUtils.checkSupportedMariVersion():
        logger.info('\n####################################\n'
                     'Intializing stkMariTools plugin...\n'
                     '####################################\n\n')

        # Add the menu items
        from stkMariTools import tools
        tools.import_submodules()

        logger.info('Successfully loaded stkMariTools plugin!')

    else:
        logger.error('### stkMariTools not supported on this version of Mari!!!')


if __name__ == '__main__':

    try: start()
    except Exception:
        sys.stderr.write('### Failed to initialize stkMariTools plugin!!!\n{0}'
                         .format(traceback.print_exc()))
