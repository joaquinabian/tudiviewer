#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""
version 0.1
10 august 2012
Program for LCMSMS data Analysis
"""
TITLE = ' TudiViewer v1.1'
#
#
#
import wx
from tudi_viewer import TudiViewer

app = wx.PySimpleApp()
TudiViewer(title=TITLE).Show()
#noinspection PyUnresolvedReferences
app.MainLoop()
