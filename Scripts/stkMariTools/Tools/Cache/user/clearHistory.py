#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" Module clearHistory """

import mari

def clearHistory():

    mari.history.clear()
    mari.ddi.garbageCollect()
    mari.clearMemoryCache()

clearHistory()