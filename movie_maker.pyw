#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""
version 0.1
10 august 2012
Program for LCMSMS data Analysis
MovieMaker is a helper class to automate generation of many figures
"""

import os
import wx
import datetime
from tudi_viewer import TudiViewer


class MovieStarter(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: TudiFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.bt_starter = wx.Button(self, wx.ID_ANY,
                                    "- start batch creation -  ",
                                    style=wx.NO_BORDER)
        self.SetSize((200, 200))


class MovieMaker(TudiViewer):
    """A TudiViewer for batch generation of images"""
    def __init__(self):
        TudiViewer.__init__(self, 'MovieMaker. Press File to start generation')
        self.archives = []
        #self.SetSize((1100, 650)) # fig of size 673x632
        #self.SetSize((1500, 800)) # fig of size 923x819
        self.SetSize((1607, 808))  # fig of size 990x830 like the originals
        self.bt_file.Label = 'select file'
        self.starter = MovieStarter(self)
        self.Bind(wx.EVT_BUTTON, self.on_start, self.starter.bt_starter)
    #
    #noinspection PyUnusedLocal
    def on_start(self, evt):
        """Start batch image generation from files in current dir
        """
        path = self.cbx_file.GetValue()
        print path
        dirname = os.path.dirname(path)
        files = os.listdir(dirname)
        self.outdir = os.path.join(dirname, 'output')
        if not os.path.exists(self.outdir):
            os.mkdir(self.outdir)

        for fname in files:
            fpath = os.path.join(dirname, fname)

            if os.path.isfile(fpath):
                self.new_path = fpath
                self.archives.append(fpath)
                self.get_file_data()

                name, ext = os.path.splitext(fname)
                img_name = '%s.png' % name
                self.outpath = os.path.join(self.outdir, img_name)
                self.view.figure.savefig(self.outpath)

        self.save_log()

    def save_log(self):
        """Save a log file with conditions used for figure generation

        To be done
        """
        archives = '\n'.join(self.archives)
        today = datetime.date.today()
        today = today.ctime()
        format = '%s\n%s\n\nThreshold = %s\nZoom x%s\nEqualizer = %s'
        values = (today, archives,
                  self.threshold, self.zoom, self.equalize_type)
        text = format % values

        logfile = os.path.join(self.outdir, 'log.log')
        with open(logfile, 'w') as f:
            f.write(text)

#
#
#
if __name__ == '__main__':

    app = wx.PySimpleApp()
    mm = MovieMaker()
    mm.Show()
    mm.starter.Show()
    app.MainLoop()