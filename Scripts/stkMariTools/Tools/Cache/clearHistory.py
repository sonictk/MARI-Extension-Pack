#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" Module clearHistory """

# noinspection PyUnresolvedReferences
import logging
import mari
import traceback
from PySide.QtGui import QMessageBox

from stkMariTools.lib.ui_utils import MariToolsMenuItem


class ClearHistoryMenuItem(MariToolsMenuItem):
    """
    This class adds a Clear History action.
    """

    logger = logging.getLogger(__name__)

    def __init__(self):
        """
        The constructor.

        :return:
        """
        super(ClearHistoryMenuItem, self).__init__()

        mari.ClearHistoryMenuItem = self
        self.actionIdentifier = 'Clear cached history'
        self.actionCommand = 'mari.ClearHistoryMenuItem.clearHistory()'
        self.actionPath = 'MainWindow/&Scripts/&Cache'

        self.addMariToolsMenuItem()


    def clearHistory(self):
        """
        This method clears the Mari undo stack and cache.

        :return:
        """

        try: mari.history.clear()
        except RuntimeError:
            self.logger.error('### Could not clear the project history!!!\n{0}'
                              .format(traceback.print_exc()))
            # Display user prompt
            mari.utils.message(text='Could not clear the project history!\n'
                               'Check if there is no project open, '
                               'or if the current project requires saving.',
                               title='Could not clear project history!',
                               icon=QMessageBox.Icon.Warning)

            return

        mari.ddi.garbageCollect()
        mari.ddi.clearMemoryCache()