#!/usr/bin/env python3.2
# -*- coding: utf-8 -*-
#
# GPL License and Copyright Notice =============================================
#  This file is part of Wrye Bash.
#
#  Wrye Bash is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  Wrye Bash is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Wrye Bash; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#  Wrye Bash copyright (C) 2005, 2006, 2007, 2008, 2009 Wrye
#
# ==============================================================================

"""This module starts Wrye Bash in GUI mode."""

# Import Hooks -----------------------------------------------------------------
import sys

if not hasattr(sys, 'frozen'):
    import os, types, importlib


    # When a Python application/module is located in a directory with unicode
    # characters, this causes problems with imports.  The full path is encoded
    # to MBCS before passing to the filesystem, so any characters that do not
    # encode properly to MBCS make Python unable to find the path for importing.
    # This doesn't normally affect standard or 3rd party modules, but it does
    # affect any module provided with said application/module.  To work around
    # this, we install an import hook that accesses the appropriate file
    # directly and loads it into Python.
    # Currently this is only implemented for Python mode, not frozen apps.
    class UnicodeImporter(object):
        def find_module(self, fullname, path=None):
            fullname = fullname.replace('.', '\\')
            exts = ('.pyc', '.pyo', '.py')
            if os.path.exists(fullname) and os.path.isdir(fullname):
                return self
            for ext in exts:
                if os.path.exists(fullname + ext):
                    return self

        def load_module(self, fullname):
            if fullname in sys.modules:
                return sys.modules[fullname]
            else:  # set to avoid reimporting recursively
                sys.modules[fullname] = types.ModuleType(fullname)
            filename = fullname.replace('.', '\\')
            ext = '.py'
            initfile = '__init__'
            try:
                if os.path.exists(filename + ext):
                    with open(filename + ext, 'U'):
                        mod = importlib.import_module(fullname)
                        sys.modules[fullname] = mod
                        mod.__loader__ = self
                else:
                    mod = sys.modules[fullname]
                    mod.__loader__ = self
                    mod.__file__ = os.path.join(os.getcwd(), filename)
                    mod.__path__ = [filename]
                    # init file
                    initfile = os.path.join(filename, initfile + ext)
                    if os.path.exists(initfile):
                        with open(initfile, 'U'):
                            code = fp.read()
                        codeobj = compile(code, initfile, 'exec') in mod.__dict__
                        exec(codeobj)
                return mod
            except Exception as e:  # wrap in ImportError a la python2 - will keep
                # the original traceback even if import errors nest
                print ('fail', filename + ext)
                raise ImportError(u'caused by ' + repr(e), sys.exc_info()[2])


    sys.meta_path.append(UnicodeImporter())
# Start Wrye Bash --------------------------------------------------------------
if __name__ == '__main__':
    from src import bash

    bash.main()
