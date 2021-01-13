#!/usr/bin/env python3
"""
+===================================================+
|                 © 2021 Privex Inc.                |
|               https://www.privex.io               |
+===================================================+
|                                                   |
|    CSPGen - Python Content Sec Policy Generator   |
|    License: X11/MIT                               |
|                                                   |
|      Core Developer(s):                           |
|                                                   |
|        (+)  Chris (@someguy123) [Privex]          |
|                                                   |
+===================================================+

CSPGen - A Python tool for generating Content Security Policies without constantly repeating yourself.
Copyright (c) 2021    Privex Inc. ( https://www.privex.io )

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, 
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name(s) of the above copyright holders shall not be used in advertising or 
otherwise to promote the sale, use or other dealings in this Software without prior written authorization.
"""

from setuptools import setup, find_packages
from privex.cspgen.version import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='privex_cspgen',

    version=VERSION,

    description='A Python tool for generating Content Security Policies without constantly repeating yourself',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Privex/cspgen",
    author='Chris (Someguy123) @ Privex',
    author_email='chris@privex.io',

    license='MIT',
    install_requires=[
        'privex-helpers>=3.2.0', 'privex-loghelper>1.0.0', 'rich', 'colorama'
    ],
    packages=find_packages(),
    scripts=['bin/csp-gen', 'bin/cspgen', 'bin/gen-csp'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
