#!/usr/bin/python
# Copyright (C) 2012 Alex Nitz
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


"""
setup.py file for PyCBC package
"""
import os
import fnmatch
import sys
import subprocess
import commands
from trace import fullmodname
import unittest
from distutils import sysconfig,file_util
from distutils.core import setup,Command,Extension


# ======== DISTUTILS CONFIGURATION AND BUILD SCRIPTS ==========================        
# Run all of the testing scripts
class test(Command):
    
    user_options = []
    test_modules = []
    def initialize_options(self):
        self.build_dir = None
    def finalize_options(self):
        #Populate the needed variables
        self.set_undefined_options('build',('build_lib', 'build_dir'))
        
    def find_test_modules(self,pattern):
       # Find all the unittests that match a given string pattern
        modules= []
        for path, dirs, files in os.walk("test"):
            for filename in fnmatch.filter(files, pattern):
                #add the test directories to the path
                sys.path.append(os.path.join(path))
                #save the module name for importing
                modules.append(fullmodname(filename))
        return modules
        
    def run(self):
        # Get the list of cpu test modules
        self.test_modules+= self.find_test_modules("test*.py")     
        # Run from the build directory
        sys.path.insert(0,self.build_dir)

        results = []
        cuda_results = []
        opencl_results = []
        for test in self.test_modules:
            a = subprocess.call(['python','test/'+test+'.py','-s', 'cpu'])
            results.append([test,a])
            a = subprocess.call(['python','test/'+test+'.py','-s', 'cuda'])
            cuda_results.append([test,a])
            a = subprocess.call(['python','test/'+test+'.py','-s', 'opencl'])
            opencl_results.append([test,a])
        
        print "\n-----CPU Results-----"
        for test in results:
            print test[0] + " status - "+str(test[1])
        if len(cuda_results) != 0:
            print "\n-----CUDA Results-----"
            for test in cuda_results:
                print test[0] + " status - "+str(test[1])
        if len(opencl_results) != 0:
            print "\n-----OpenCL Results-----"
            for test in opencl_results:
                print test[0] + " status - "+str(test[1])


# do the actual work of building the package
setup (
    name = 'PyCBC',
    version = '0.1',
    description = 'Gravitational wave CBC analysis toolkit',
    author = 'Ligo Virgo Collaboration - PyCBC team',
    url = 'https://sugwg-git.phy.syr.edu/dokuwiki/doku.php?id=pycbc:home',
    cmdclass = { 'test'  : test ,},
    ext_modules = [],
	requires = ['swiglal'],
    packages = ['pycbc','pycbc.fft','pycbc.types'],
    scripts = [],
)

