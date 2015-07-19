#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" Module ui_utils: This module contains useful classes for dealing with
the Mari UI."""

import logging
import mari
import traceback


class MariToolsMenuManager(object):
    """
    This class will add a Mari menu item
    """

    logger = logging.getLogger(__name__)


    def __init__(self):
        """
        The constructor.

        """

        # Call base class
        super(MariToolsMenuManager, self).__init__()


    def addMenuItemsFromScripts(self):
        """
        This method searches through the existing modules and adds any
        valid MenuItems to the main Mari menu.

        :return:
        """

        pass


class MariToolsMenuItem(object):
    """
    This base class is used for adding a Mari action.
    """

    logger = logging.getLogger(__name__)

    def __init__(self):
        """
        The constructor.

        :return:
        """

        self.actionIdentifier = None
        self.actionCommand = None
        self.actionPath = None
        self.addBefore = ''


    def addMariToolsMenuItem(self):
        """
        This method should be overriden in subclasses to add a Mari menu item.

        :return:
        """

        try:
            mari.menus.addAction(
                mari.actions.create(
                    self.actionIdentifier,
                    self.actionCommand
                    ),
                self.actionPath,
                self.addBefore
            )

        except ValueError:
            self.logger.error('### Could not add action:{0}!!!\n{1}'
                              .format(self.actionIdentifier, traceback.print_exc()))


