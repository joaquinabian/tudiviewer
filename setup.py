# exWx/setup.py
#
## python setup.py py2exe
#
from distutils.core import setup
import os
import sys
import ConfigParser
import matplotlib
#noinspection PyUnresolvedReferences
import py2exe
#
sys.argv.append('py2exe')
config = ConfigParser.ConfigParser()
config.readfp(open('install.ini'))
#
PyName = config.get('Setup', 'pyname')
AppVersion = config.get('Common', 'version')
AppName = config.get('Common', 'name')
Icondir = config.get('Common', 'icondir')
Icon = config.get('Common', 'big_icon')
#
Icon = os.path.join(Icondir, Icon)
#
def get_docs():
    folder = 'doc'
    docs = []
    for arch in os.listdir(folder):
        docs.append(os.path.join(folder, arch))
    return [("doc", docs)]

#
#
####################################
#
#      tudi.pyw
#
####################################
#
#
setup(
    windows=[
             {'script': PyName,
              'icon_resources': [(0, Icon)],
              'dest_base': AppName,
              'version': AppVersion,
              'company_name': "JoaquinAbian",
              'copyright': "No Copyrights",
              'name': AppName
              }
             ],

    options={
        'py2exe': {
            'packages': ['matplotlib', 'pytz'],
            #'includes':     [],
            'excludes': ['bsddb', 'curses', 'pywin.debugger',
                         'pywin.debugger.dbgcon', 'pywin.dialogs',
                         'tcl', 'Tkconstants', 'Tkinter', 'pygtk',
                         'pydoc', 'doctest', 'test', 'sqlite3',
                         'bsddb', 'curses', 'themail', '_fltkagg',
                         '_gtk', '_gtkcairo', '_agg2', '_gtkagg',
                         '_tkagg', '_cairo'
                         ],
            'ignores': ['wxmsw26uh_vc.dll'],
            'dll_excludes': ['libgdk-win32-2.0-0.dll',
                             'libgobject-2.0-0.dll',
                             'tcl84.dll', 'tk84.dll',
                             'libgdk_pixbuf-2.0-0.dll',
                             'libgtk-win32-2.0-0.dll',
                             'libglib-2.0-0.dll',
                             'libcairo-2.dll',
                             'libpango-1.0-0.dll',
                             'libpangowin32-1.0-0.dll',
                             'libpangocairo-1.0-0.dll',
                             'libglade-2.0-0.dll',
                             'libgmodule-2.0-0.dll',
                             'libgthread-2.0-0.dll',
                             'QtGui4.dll', 'QtCore.dll',
                             'QtCore4.dll'
                             ],
            'compressed': 1,
            'optimize': 2,
            'bundle_files': 1
        }
    },
    zipfile=None,
    #Additional files I want in folder  'dist'.
    #The packer (inno) can go to the main dir to get them but then
    #they would not be in 'dist' and the program.exe there would not work.
    data_files=get_docs() +\
               matplotlib.get_py2exe_datafiles() + [
        ("", ["INSTALL.txt", #Installation final page
              "README.txt", #README and help (English)
              "LICENCE.TXT", #Licence File (GPL v3)
              "msvcp90.dll",
              "C:\\Python27/Lib/site-packages/wx-2.8-msw-unicode/wx/gdiplus.dll",
              "C:\\Python27/lib/site-packages/scipy/integrate/_quadpack.pyd",
              "C:\\Python27/lib/site-packages/numpy/fft/fftpack_lite.pyd",
              "C:\\Python27/lib/site-packages/Pythonwin\mfc90.dll",
              "C:\\Python27/lib/site-packages/scipy/optimize/minpack2.pyd",
              ]
        ),
        ("test", ["test/test_short.csv",
                  "test/test_short.tsv", "test/test_short.xlsx"]
        ),
        #("images", [Sicon, Icon])
    ]
)
