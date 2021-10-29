TUDI VIEWER vs 1.0.0 (version september 5, 2012)

TUDI_VIEWER is a tool for the visualization of protein collections obtained
from Thermo Protein Discoverer.


Table of contents
-----------------
1.- DEPENDENCIES
2.- INSTALLATION
3.- INPUT FILE FORMAT
4.- FEATURES AND CHANGELOG
5.- TODO
6.- CONTRIBUTE


DEPENDENCIES
----------------
If you work with TudiViewer source you need Python installed (tested with Python
version 2.7.2) as well as the following dependencies:
    Matplotlib
    Pandas 
    wxPython 2.8.11.2
    commons (from lpcsicuab googlecode repository)

Note for developpers:
Installation from source requires some small quirks in pandas modules.
Check also dll dependencies in INSTALL.txt


INSTALLATION
----------------
 Tested in windows XP 32 bits and win7 64 bits

a) Install TudiViewer FROM WINDOWS INSTALLER
    a.- Download TudiViewer_x.y_setup.exe installer from repository.
    b.- Double click on the installer in any directory.
    c.- Run TudiViewer by double-clicking on a TudiViewer direct access you can
        manually locate in your desktop or from the START-PROGRAMS application
        created by the installer.

b) Install TudiViewer FROM SOURCE (when available)
    a.- Download TudiViewer and commons zip archives from repository
    b.- Unzip in python site-packages or in another folder in the python path
    c.- Run TudiViewer by double-clicking on the tudi_viewer.pyw module.

c) Install TudiViewer FROM MERCURIAL (when available)
    a.- Get a copy of the TudiViewer and commons repositories from mercurial:
        https://bitbucket.org/jabianmonux/_tudiviewer
        http://code.google.com/p/lp-csic-uab/source/checkout?repo=commons
    b.- Locate de folders and run the application as indicated in b.



INPUT FILE FORMAT
-------------------------------------

TudiViewer accepts input files in CSV, TSV, XLS and XLSX formats
It works with Thermo Protein Discovered reports but the only requirement is
a header in row 0 with at least 6 columns with the following headers:

'Accession', 'Description', 'Sum(# PSMs)', 'Sum(Coverage)', 'calc. pI', 'MW [kDa]'


FEATURES AND CHANGELOG
-----------------------

1.1.0 September 2012
- Some few bugs fixed

1.0.0 September 2012
- First version. Executable build successfully.

TODO
--------

- test
- finish about/readme
- upload executable
- make accept less than five columns


CONTRIBUTE
-----------

These programs are made to be useful. If you use them and don't work
entirely as you expect, let me know about features you think are needed, and
I'll try to include them in future releases.

Joaquin Abian September 2012