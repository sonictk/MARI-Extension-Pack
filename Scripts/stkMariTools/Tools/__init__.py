#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" Module __init__.py: This module acts to import all files in subdirectories
 to sys.modules """

import os
import logging
import traceback
import imp


def import_submodules():
    """
    This method will import all submodules from this folder into
    the module namespace.

    :return:
    """

    logger = logging.getLogger(__name__)

    # Grab all modules in subdirectories recursively
    modules = []

    # Normalize the base path
    basePath = os.path.dirname(os.path.abspath(__file__))

    logger.debug('Searching directory:\n{0}\nrecursively for modules...'
                 .format(basePath))

    for root, dirs, filenames in os.walk(basePath):
        for filename in filenames:

            # Only grab .py files and not files like __init__.py
            if filename.endswith('.py') and not filename.startswith('__'):

                # Filter out broken symlinks and directories called 'dir.py/'
                if os.path.isfile(os.path.join(root, filename)):
                    modules.append((filename, os.path.join(root, filename)))

    # Define all module names in the package namespace
    __all__ = [os.path.basename(module[0])[:-3] for module in modules]

    logger.debug('Successfully set the following modules to {0} namespace: \n{1}'
                 .format(__name__, __all__))

    for module in modules:
        try:
            print module[0]
            print 'first'
            print module[1]
            print 'sec'

            loaded_module = imp.load_source(module[0], module[1])
            loaded_module.registerMenuItem()

        except RuntimeWarning:
            logger.warning('# Absolute import was handled incorrectly!\n{0}'
                           .format(traceback.print_exc()))
            continue

        except ImportError:
            logger.error('### Could not find module!!!\n{0}'.format(traceback.print_exc()))
            continue

        except AttributeError:
            logger.error('### Module does not have required registerMenuItem() method!!!\n{0}'
                         .format(traceback.print_exc()))
            continue

        except Exception:
            logger.error('### Importing tools modules failed!!!\n{0}'.format(traceback.print_exc()))
            continue
