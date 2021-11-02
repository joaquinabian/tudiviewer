#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""
version 0.1
10 august 2012
Program for LCMSMS data Analysis
"""
#
#
#
from matplotlib import use
use('WXAgg')

import wx
import os
import configparser
import pandas as p
from commons.iconic import Iconic
from commons.info import About
from commons.warns import tell
from matplotlib import rcParams as rcp
from tudi_frame import TudiFrame
from tudi_ico import ICON
# noinspection PyUnresolvedReferences
from matplotlib.cm import jet
from matplotlib.colors import Normalize
#
#
rcp['figure.subplot.left'] = 0.12
rcp['figure.subplot.right'] = 0.96
rcp['figure.subplot.top'] = 0.92
rcp['figure.subplot.bottom'] = 0.10
rcp['xtick.labelsize'] = 'medium'
rcp['ytick.labelsize'] = 'medium'
rcp['axes.labelsize'] = 'medium'
rcp['font.size'] = 10.0
#
#
class MyFileDropTarget(wx.FileDropTarget):
    """"""
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    # noinspection PyMethodOverriding
    def OnDropFiles(self, x, y, filename):
        self.window.notify(filename)
#
# noinspection PyArgumentList,PyUnusedLocal
class TudiViewer(TudiFrame, Iconic):
    def __init__(self, title):
        TudiFrame.__init__(self, None, -1, title=title, size=(600, 350))
        Iconic.__init__(self, icon=ICON)
        self.colorbar = None
        self.default_dir = 'test'
        self.xvals = []
        self.yvals = []
        self.size = []
        self.color = []
        self.search_hits = []
        self.search_term = None
        self.cross = {}
        self.threshold = None
        self.keep_warning = 1
        self.ini_file = 'tudi.ini'
        #
        self.id = ''
        self.name = ''
        self.psm = ''
        self.coverage = ''
        self.mr = ''
        self.pi = ''
        #
        self.new_path = self.DEMO = 'test/test_short.tsv'
        self.datafile_path = ""
        #
        self.Bind(wx.EVT_CLOSE, self.on_close_window)
        self.Bind(wx.EVT_SIZE, self.on_size)
        #
        self.Bind(wx.EVT_BUTTON, self.on_about, self.bt_about)
        self.Bind(wx.EVT_BUTTON, self.on_file, self.bt_file)
        self.Bind(wx.EVT_BUTTON, self.on_search, self.bt_search)
        self.Bind(wx.EVT_BUTTON, self.on_clear_list, self.bt_clear_list)
        #
        self.Bind(wx.EVT_COMBOBOX, self.on_file_choice, self.cbx_file)
        #
        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio, self.rb_id)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio, self.rb_name)
        #
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,
                  self.on_protein_selected, self.proteins.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                  self.on_protein_deselected, self.proteins.list)
        #
        self.Bind(wx.EVT_BUTTON, self.on_refresh, self.view.bt_refresh)
        #
        self.view.canvas.mpl_connect('pick_event', self.on_pick)
        #
        dt1 = MyFileDropTarget(self)
        self.cbx_file.SetDropTarget(dt1)
        #
        self.get_config()
        self.get_file_data()
        #
        self.SetMinSize((700, 500))          # frame min size
        self.SetSize((1100, 650))
    #
    def get_config(self):
        """Read defaults from INI file.
        """
        config = configparser.ConfigParser()
        dirname = os.path.dirname(__file__)

        try:
            config.read(os.path.join(dirname, self.ini_file))

            self.id = config.get('columns', 'id')
            self.name = config.get('columns', 'name')
            self.psm = config.get('columns', 'psm')
            self.coverage = config.get('columns', 'coverage')
            self.mr = config.get('columns', 'mr')
            self.pi = config.get('columns', 'pi')

        # NoOptionError: no option.
        # NoSectionError: ini file does not exists.
        except (configparser.NoOptionError, configparser.NoSectionError):
            tell(("Error occurred reading %s INI file.\n"
                  "Will get defaults instead\n"
                  "Note your file must have at least 3 columns with\n"
                  "the following default column names:\n"
                  "'Accession'       'calc. pI'      'MW [kDa]'\n"
                  "For full functionality you will also need columns:\n"
                  "'Description'   'Sum(# PSMs)'   'Sum(Coverage)'\n"
                  ) % self.ini_file
                 )
            self.id = 'Accession'
            self.name = 'Description'
            self.psm = 'Sum(# PSMs)'
            self.coverage = 'Sum(Coverage)'
            self.mr = 'MW [kDa]'
            self.pi = 'calc. pI'
    #
    def on_size(self, evt):
        """"""
        self.Refresh()
        evt.Skip()
    #
    def get_num(self, x):
        """Removes last char of a string and converts to float.

        Used by pandas to map to floats columns with cells of the type "99%"

        """
        x = x[:-1]
        return float(x)
    #
    def read_data(self):
        """Loads selected data file columns into a pandas dataframe.

        Reads tsv, csv, xls and xlsx files.
        Only requirement is a header in row 0 with at least 3 (marked with an
        asterisk) and better all 6 columns with the following names:
                         'Accession'*     'Description'
                         'Sum(# PSMs)'   'Sum(Coverage)'
                         'calc. pI'*      'MW [kDa]'*
        These column names can be modified in tudi.ini configuration file

        """
        #
        (root, ext) = os.path.splitext(self.datafile_path)
        if ext in ('.xls', '.xlsx'):
            xls = p.ExcelFile(self.datafile_path)
            df = xls.parse(xls.sheet_names[0], header=0, index_col=None)
        elif ext == '.csv':
            df = p.read_csv(self.datafile_path, sep=',')
        else:
            df = p.read_csv(self.datafile_path, sep='\t')
        #
        if len(df) == 0:
            tell('File is empty')
            return 0
        #
        if not self.minimal_column_set_exist(df.columns):
            return 0

        df = self.fill_failing_columns(df)
        #
        coverage = self.coverage
        format_ = self.sniff_coverage(df[coverage])

        if format_ == 'per_one':
            df[coverage] = df[coverage] * 100
        elif format_ == 'symbolic':
            df[coverage] = df[coverage].map(self.get_num)
        elif format_ == 'percentage':
            pass
        else:
            tell('unknown format for coverage')
            return 0

        self.dataframe = df[[self.id, self.name, coverage,
                             self.psm, self.pi, self.mr]]
        return 1
    #
    def minimal_column_set_exist(self, columns):
        """Check if the absolutely necessary columns exist.

        At least three columns are needed:
          - index column     (protein id)
          - x,y coordinates ( Mr and pI of the protein )

        """
        expected = (self.id, self.mr, self.pi)
        not_found = [column for column in expected if column not in columns]

        if not_found:
            text = ('The %(type)s file will not be loaded\n'
                    'because the column names set in your INI file:\n'
                    ' %(col)s \n'
                    'do not correspond to any column in the %(type)s file\n\n'
                    'Either check and modify column names in the %(type)s'
                    ' file\n< %(file)s >\n'
                    'or set their actual name in %(ini)s')

            if self.DEMO == self.datafile_path:
                tell(text % ({'type': 'DEMO', 'col': not_found,
                              'file': self.DEMO, 'ini': self.ini_file})
                     )
            else:
                tell(text % ({'type': 'Selected', 'col': not_found,
                              'file': self.datafile_path, 'ini': self.ini_file})
                     )
            return False
        return True
    #
    def fill_failing_columns(self, df):
        """Create and fill secondary columns with data"""
        warn_about = []
        for column in (self.coverage, self.psm):
            if not column in df.columns:
                df[column] = p.Series([10] * len(df.index), index=df.index)
                warn_about.append(column)

        if self.name not in df.columns:
            df[self.name] = df[self.id]
            warn_about.append(self.name)

        if self.keep_warning and warn_about:
            text = ('Some required data is being given a default value'
                    ' because the corresponding column names set in your'
                    ' INI file:\n%(col)s\n'
                    ' do not correspond to any column in the %(type)s file\n\n'
                    'You can either:\n'
                    ' - check and modify column names in the %(type)s'
                    ' file\n<%(file)s>\n'
                    ' - set their actual column names in %(ini)s\n'
                    ' - continue as it is (Press Cancel to remove this'
                    ' warning)'
                    )

            if self.DEMO == self.datafile_path:
                self.keep_warning = tell(text % ({'type': 'DEMO',
                                                  'col': warn_about,
                                                  'file': self.DEMO,
                                                  'ini': self.ini_file}),
                                         level='question'
                                         )
            else:
                self.keep_warning = tell(text % ({'type': 'Selected',
                                                  'col': warn_about,
                                                  'file': self.datafile_path,
                                                  'ini': self.ini_file}),
                                         level='question'
                                         )
        return df
    #
    def sniff_coverage(self, series):
        """Ascertain coverage format.

        Coverage has to be an integer representing a percentage.
        Protein Discoverer excel files and derived tsv and csv can show protein
        coverage in different formats which are read by pandas in different
        ways (i.e. as percentage / 100 or in the form xy%).

        """

        if '%' in str(series[0]):
            return 'symbolic'

        if max(series) <= 1:
            format_ = 'per_one'
        elif max(series) <= 100:
            format_ = 'percentage'
        else:
            format_ = None

        return format_
    #
    def filter_data(self):
        """Filter and process dataframe values (zoom, threshold and transforms)

        There are three transforms types:
            -None-
            -squared root
            -squared
            -log2

        """
        self.equalize_type = self.view.ch_type.GetSelection()
        self.zoom = float(self.view.cbx_zoom.GetValue())
        psms = self.psm
        #
        threshold = self.view.sp_threshold.GetValue()
        self.threshold_changed = threshold !=\
                                 self.threshold and self.threshold is not None
        self.threshold = threshold
        #
        try:
            # get only proteins with minimum scans
            df = self.dataframe[self.dataframe[psms] > self.threshold]
        except (KeyError, AttributeError):
            tell('%s not a tsv file or wrong column names' % self.datafile_path)
            return
        #
        if len(df) == 0:
            tell('threshold %f too high' % self.threshold)
            return
        #
        x = df['calc. pI']
        y = df['MW [kDa]']
        #
        if self.equalize_type == 1:                  # square root
            size = p.np.sqrt(df[psms])
        elif self.equalize_type == 2:                # power
            size = df[psms] ** 2
        elif self.equalize_type == 3:                # log2
            size = p.np.log2(df[psms])
        else:
            size = df[psms]
        #
        # noinspection PyAugmentAssignment
        size = size * self.zoom
        color = df[self.coverage]
        accession = df[self.id]
        desc = df['Description']

        # convert panda series to list seems necessary to work
        self.index = df.index.tolist()
        self.xvals = x.tolist()
        self.yvals = y.tolist()
        # noinspection PyUnresolvedReferences
        self.size = size.tolist()
        self.color = color.tolist()
        self.accession = accession.tolist()
        self.desc = desc.tolist()
    #
    def fill_list(self):
        """Populate ListCtrl with protein data."""
        items = {}
        for key, (idx, acc, desc, cov, mr, pi) in enumerate(
                                            zip(self.index, self.accession,
                                                self.desc, self.color,
                                                self.yvals, self.xvals)):
            items[key + 1] = (str(idx + 1), acc,
                              desc, str(cov),
                              str(mr), str(pi))
        #
        self.proteins.itemDataMap = items
        self.proteins.items = items.items()
        self.proteins.populate()
    #
    def draw_view(self, hold=True, refresh=False):
        """Produces a clickable scatter plot of the data with titles."""
        if refresh:
            y_win = (6, 290)
            x_win = (3, 12)
        else:
            x_win = tuple(self.view.axes.viewLim.intervalx)
            y_win = tuple(self.view.axes.viewLim.intervaly)

        norm = Normalize(vmin=1, vmax=95)
        #
        # clear scatter points
        self.view.axes.clear()
        self.scx = self.view.axes.scatter(self.xvals, self.yvals, s=self.size,
                                          c=self.color, marker='o', cmap=jet,
                                          norm=norm, linewidth=0.2, alpha=0.8,
                                          picker=2)
        #
        file_name = os.path.split(self.datafile_path)[-1]
        title = "Abundance (radius) of Proteins\n %s" % file_name

        self.view.xlabel = 'theoretical pI'
        self.view.ylabel = 'Mass (KDa)'
        self.view.axes.set_title(title)
        self.view.axes.set_yscale('log')

        if not self.colorbar:
            self.colorbar = self.view.figure.colorbar(self.scx)
            self.colorbar.ax.set_ylabel('sequence coverage (%)')
        self.view.axes.set_xlim(x_win)
        self.view.axes.set_ylim(y_win)
        self.view.draw(hold=hold)
    #
    #noinspection PyArgumentEqualDefault
    def on_protein_selected(self, evt):
        """Marks in the scatter plot the protein selected in the protein list.

        """
        protein_index = int(self.proteins.list.GetItemData(evt.Index)) - 1

        mass = self.yvals[protein_index]
        pi = self.xvals[protein_index]
        #
        cross = self.view.axes.plot([pi], [mass], 'b+', markersize=20)
        self.cross[protein_index] = cross
        self.view.draw(hold=True)
    #
    def on_protein_deselected(self, evt):
        """Unmarks in the scatter plot a previously selected protein.

        When a new protein is selected in the ctrl list with a Left click,
        the previous selected protein is deselected.
        """
        self.currentItem = evt.Index
        protein_index = int(
            self.proteins.list.GetItemData(self.currentItem)) - 1
        cross = self.cross.pop(protein_index)[0]
        #after a refresh, deselecting an item gives error
        try:
            cross.remove()
        except ValueError:
            return
        self.view.draw(hold=True)
    #
    def on_file(self, evt):
        """dialog for selecting files. Updates listbox"""
        fd = wx.FileDialog(None, defaultDir=self.default_dir)
        #
        if fd.ShowModal() == wx.ID_OK:
            self.new_path = fd.GetPath()
            self.get_file_data()
    #
    def notify(self, afile):
        """Update text control after drag and drop"""
        self.new_path = afile[0]
        self.get_file_data()
    #
    def on_file_choice(self, evt):
        """Update text control after selecting a choice from drop box"""
        self.new_path = self.cbx_file.GetStringSelection()
        self.get_file_data()
    #
    def on_refresh(self, evt):
        """Recalculate data and refresh scatter plot"""
        self.filter_data()
        if self.threshold_changed:
            self.fill_list()
        self.draw_view(hold=True, refresh=False)
    #
    def get_file_data(self, hold=True, refresh=True):
        """Read data from input file and plot scatter"""
        path = os.path
        if not path.exists(self.new_path):
            tell('%s file does not exist' % self.new_path)
            return
        if path.abspath(self.new_path) == path.abspath(self.datafile_path):
            return
        self.datafile_path = self.new_path
        self.cbx_file.SetValue(self.datafile_path)
        if self.datafile_path not in self.cbx_file.GetItems():
            self.cbx_file.Append(self.datafile_path)

        if self.read_data():
            self.filter_data()
            self.fill_list()
            self.draw_view(hold=hold, refresh=refresh)
    #
    def on_radio(self, evt):
        """Clear hits and restart search protocol when changing search type"""
        self.search_term = None
        self.on_clear_list(None)
    #
    def on_search(self, evt):
        """Search for a term and highlight and show hits in list"""
        term = self.tc_search.GetValue()
        self.background_color = self.proteins.list.GetBackgroundColour()

        search_column = self.accession if self.rb_id.GetValue() else self.desc
        #
        if term == self.search_term:
            self.pos += 1
            if self.pos == len(self.search_hits):
                self.pos = 0
            self.proteins.list.Focus(self.search_hits[self.pos])
        else:
            self.pos = 0
            search_hits = [self.index[index] + 1
                           for index, item in enumerate(search_column)
                           if item.find(term) > -1]
            #
            self.search_hits = [self.proteins.list.FindItem(-1, str(hit))
                                for hit in search_hits]
            if self.search_hits:
                self.tc_search.SetBackgroundColour(wx.NullColour)
                self.tc_search.Refresh()
                self.proteins.list.Focus(self.search_hits[self.pos])
                for index in self.search_hits:
                    self.proteins.list.SetItemBackgroundColour(index, 'red')
                self.search_term = term
            else:
                self.tc_search.SetBackgroundColour('red')
                self.tc_search.Refresh()
                self.search_term = None
    #
    def on_clear_list(self, evt):
        """Clear highlighted terms in list and get ready for a new search"""
        for index in self.search_hits:
            self.proteins.list.SetItemBackgroundColour(index,
                                                       self.background_color)
        self.search_term = None
    #
    def on_pick(self, event):
        """writes in grid table the data from the protein selected in canvas"""
        n = len(event.ind)
        if not n:
            self.adjust_rows(0)
            return True
        self.adjust_rows(len(event.ind))

        for row, index in enumerate(event.ind):
            description = self.desc[index].split('OS=')
            self.grid_picked.SetCellValue(row, 0, str(self.index[index] + 1))
            self.grid_picked.SetCellValue(row, 1, self.accession[index])
            self.grid_picked.SetCellValue(row, 2, description[0][:60])

        return True
    #
    def adjust_rows(self, number):
        """Prepares a blank table with <number> rows"""
        actual = self.grid_picked.GetNumberRows()
        if actual > 1:
            #noinspection PyArgumentList
            self.grid_picked.DeleteRows(1, actual)
            #
        if number > 0:
            self.grid_picked.AppendRows(number - 1)
        else:
            self.grid_picked.SetCellValue(0, 0, "")
            self.grid_picked.SetCellValue(0, 1, "")
            self.grid_picked.SetCellValue(0, 2, "")
    #
    def on_close_window(self, evt):
        self.Destroy()
#
    def on_about(self, evt):
        """Show documentation."""
        if not About.exists:
            self.about = About()
            self.about.Show()
        else:
            self.about.SetFocus()
#
#
#
if __name__ == '__main__':

    app = wx.PySimpleApp()
    TudiViewer(title='module').Show()
    #noinspection PyUnresolvedReferences
    app.MainLoop()
