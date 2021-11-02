#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""
version 0.1
10 august 2012
Program for LCMSMS data Analysis
"""
#
#
import wx
import wx.lib.mixins.listctrl as listmix
#
#
def cmp(a, b):
    """cmp disappeared on py3k"""

    return (a > b) - (a < b)
#
#
class TestListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id_, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, id_, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
#
#
class ProteinList(wx.Panel, listmix.ColumnSorterMixin):
    def __init__(self, parent, id_):
        wx.Panel.__init__(self, parent, id_, style=wx.WANTS_CHARS)
        self.items = ()
        sizer = wx.BoxSizer(wx.VERTICAL)
        #
        tid = wx.NewIdRef()
        #
        self.list = TestListCtrl(self, tid, style=wx.LC_REPORT | wx.BORDER_NONE)
        sizer.Add(self.list, 1, wx.EXPAND)
        listmix.ColumnSorterMixin.__init__(self, 6)
        #
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        #
    #
    def GetColumnSorter(self):
        return self.custom_sorter
    #
    # noinspection PyUnresolvedReferences
    def custom_sorter(self, key1, key2):
        """Sort numerically if a string contains only digits"""
        col = self._col
        ascending = self._colSortFlag[col]
        #
        item1 = self.itemDataMap[key1][col]
        item2 = self.itemDataMap[key2][col]
        #
        try:
            item1 = float(item1)
            item2 = float(item2)
        except ValueError:
            pass
        #
        cmp_val = cmp(item1, item2)
        #
        # If the items are equal then pick something else
        # to make the sort value unique
        if cmp_val == 0:
            cmp_val = cmp(*self.GetSecondarySortValues(col, key1, key2))

        if ascending:
            return cmp_val
        else:
            return -cmp_val
    #
    def populate(self):
        """"""
        self.list.ClearAll()
        #
        self.list.InsertColumn(0, "#")
        self.list.InsertColumn(1, "ID", wx.LIST_FORMAT_RIGHT)
        self.list.InsertColumn(2, "Name")
        self.list.InsertColumn(3, "Coverage")
        self.list.InsertColumn(4, "Mr (KDa)")
        self.list.InsertColumn(5, "pI")

        for key, data in self.items:
            index = self.list.InsertItem(self.list.GetItemCount(), data[0])
            #
            for idx in range(1, 6):
                self.list.SetItem(index, idx, data[idx])
            #
            self.list.SetItemData(index, key)

        self.list.SetColumnWidth(0, 30)
        self.list.SetColumnWidth(1, -1)
        self.list.SetColumnWidth(2, 400)
        self.list.SetColumnWidth(3, 70)
        self.list.SetColumnWidth(4, 70)
        self.list.SetColumnWidth(5, -1)

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    # noinspection PyPep8Naming
    def GetListCtrl(self):
        return self.list

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return -1, -1


#
if __name__ == '__main__':

    items = {
        1: ("1", "sp", "PROQ PROQ", "89.08", "01", "02"),
        2: ("2", "P37754", "6-phosphoglucon, decarbo", "33.97", "10", "14"),
        3: ("3", "P00350", "6-phosphogluconate dehydro", "59.40", "11", "15"),
        4: ("4", "B7ULP0", "6-phosphogluconolactonase", "35.65", "12", "16"),
        5: ("5", "P00509", "Aspartate aminotransferase", "52.02", "13", "17")
    }

    class AFrame(wx.Frame):
        def __init__(self, *args, **kwargs):
            Panel = kwargs.pop('panel')
            wx.Frame.__init__(self, *args, **kwargs)
            self.panel = Panel(self, -1)
            self.panel.itemDataMap = items
            self.panel.items = items.items()
            self.panel.populate()
            self.panel.list.Focus(2)
            self.panel.list.Select(2)

    app = wx.PySimpleApp()
    AFrame(None, panel=ProteinList).Show()
    # noinspection PyUnresolvedReferences
    app.MainLoop()
