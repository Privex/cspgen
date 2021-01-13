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
import configparser
import sys
import textwrap
from colorama import Fore
from os import getenv as env
from privex.helpers import empty, empty_if, is_true, is_false, env_bool, T, K, ErrHelpParser

from privex.cspgen import version
from privex.cspgen.helpers import automark_str, clean_dict, dedup, literal, read_stdin

oprint = print
from rich import print
from pathlib import Path
import logging
import argparse
from privex.loghelper import LogHelper
from typing import Union, Optional, List, Tuple, Dict, Set

__all__ = [
    'CSPBuilder', 'get_builder', 'main', 'parser', 'log_level', 'PKG_DIR', 'EXAMPLE_DIR', 'EXAMPLE_INI'
]

PKG_DIR = Path(__file__).parent.resolve()
EXAMPLE_DIR = PKG_DIR / 'examples'
EXAMPLE_INI = EXAMPLE_DIR / 'example.ini'

log_level = env('LOG_LEVEL', 'WARNING')
_lh = LogHelper('privex.cspgen', handler_level=logging.getLevelName(log_level))
_lh.add_console_handler(stream=sys.stderr)

log = _lh.get_logger()

argc, argv = len(sys.argv), sys.argv


class CSPBuilder:
    def __init__(self, filename: str = None, file_handle = None, contents: Union[str, list, tuple] = None, **kwargs):
        self.config = configparser.ConfigParser()
        self.conf_file = None
        if not empty(filename):
            self.conf_file = Path(filename).resolve()
            self.config.read(self.conf_file)
        elif file_handle is not None:
            self.config.read_file(file_handle)
        elif not empty(contents, itr=True):
            if isinstance(contents, (tuple, list)):
                contents = "\n".join(contents)
            self.config.read_string(contents)
        else:
            raise ValueError(
                "CSPBuilder expects either a filename, file handle (open()), or config string "
                "contents to be passed. All 3 are None / empty. Nothing to parse."
            )

        self.groups = {}
        self.config_dict = {}
        self.flags = ''
        self.excluded = kwargs.get('excluded', ['flags', 'groups', 'DEFAULT'])
        self.cleaned = False

    @property
    def sections(self) -> list:
        return self.config.sections()

    @property
    def clean_sections(self) -> list:
        return [s for s in self.sections if s not in self.excluded]

    def clean(self):
        # First we extract 'groups' from the config, replace it's {{markers}}, and then deduplicate all group values
        if 'groups' in self.sections:
            self.groups = clean_dict(self.config['groups'])

        groups = self.groups
        # Next we iterate over the Config object and extract all sections into a standard dict
        config_dict = self.config_dict
        for k, v in self.config.items():
            v: configparser.SectionProxy
            sec_items = dict(v.items())
            config_dict[k] = sec_items
        
        # Remove auto-added 'DEFAULT' (not used), and 'groups' (already parsed and extracted into self.groups)
        if 'DEFAULT' in config_dict: del config_dict['DEFAULT']
        if 'groups' in config_dict: del config_dict['groups']

        # Extract 'flags' if present in the config, replace {{markers}}, and deduplicate it's contents.
        cflags = '' if 'flags' not in config_dict else config_dict['flags']['flags']
        cflags = dedup(automark_str(cflags, groups))
        
        # Then we can simply remove 'flags' from the config dict
        if 'flags' in config_dict: del config_dict['flags']

        # Finally we make sure all local variables are saved back to their appropriate instance attributes
        self.config_dict = {k: clean_dict(v, groups) for k, v in config_dict.items()}
        self.flags = cflags
        self.groups = groups
        self.cleaned = True
        return self

    def autoclean(self):
        if self.cleaned:
            return True
        return self.clean()

    def str_section(self, name: str):
        self.autoclean()
        sec = self.config_dict.get(name, None)
        if not sec: return None
        s = f"{name}: {sec.get('zones', '')}"
        if is_true(sec.get('unsafe-eval', False)): s += " 'unsafe-eval'"
        if is_true(sec.get('unsafe-inline', False)): s += " 'unsafe-inline'"
        s += ';'
        return s

    def generate(self, output='list', sep=' ', **kwargs):
        
        secs = [self.str_section(s) for s in self.clean_sections]
        secd = dict(zip(self.clean_sections, secs))
        secd['flags'] = [s + ';' for s in self.flags.split()]
        secs += secd['flags'] 
        output = output.lower()
        if output == 'list': return secs
        if output == 'tuple': return tuple(secs)
        if output in ['dict', 'dictionary', 'kv', 'keyval', 'map', 'mapping']: return secd
        if output in ['str', 'string']:
            sj = sep.join(secs)
            if not sj.endswith(';'): sj += ';'
            return sj
        raise ValueError(f"Supported: (str, string, list, tuple). Unsupported output type: {output}")

    def __str__(self):
        return self.generate(output='str')

    def __iter__(self):
        yield from self.generate(output='list')

    def __len__(self):
        return len(self.generate(output='list'))

    def __getitem__(self, item:str):
        self.autoclean()
        if item in self.sections:
            return self.config_dict[item]
        gend = self.generate(output='dict')
        if item in gend:
            return gend[item]
        if item in self.groups:
            return self.groups[item]
        raise KeyError(f"Item {item!r} not found in config sections, generated sections, or group keys...")


def get_builder(name: str = None, file_handle = None, contents: Union[str, list, tuple] = None, **kwargs) -> CSPBuilder:
    if empty(name) and file_handle is None and empty(contents, itr=True): name = argv[1]
    return CSPBuilder(name, file_handle, contents, **kwargs)


COPYRIGHT = f"""
    {Fore.GREEN}Content Security Policy (CSP) Generator{Fore.RESET}
        
        {Fore.CYAN}Version: v{version.VERSION}
        Github:  https://github.com/Privex/cspgen
        License: X11 / MIT
        
        (C) 2021 Privex Inc. ( https://www.privex.io ){Fore.RESET}
"""

parser = ErrHelpParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent(f"""
{COPYRIGHT}
    

    {Fore.YELLOW}Generates CSP's based off of one or more INI files, with each CSP "type" (default-src, style-src, etc.)
    as an INI header, a 'zones' key in each type, containing the various domains you want to allow,
    'unsafe-eval = true' / 'unsafe-inline = false' for more clear enabling/disabling unsafe-eval and unsafe-inline
    per "type", and two special headers:{Fore.RESET}
        {Fore.BLUE}
        'groups' - Groups of variables that can be used in each type's 'zones = ' key, AND can also include
                   other group names (as long as the included vars are defined higher up, and doesn't include
                   the var including it).

        'flags'  - Contains "flags", which are CSP strings that standalone, such as 'upgrade-insecure-requests',
                   instead of being a key with zones as a value.
        {Fore.RESET}

    {Fore.GREEN}Example INI file:{Fore.RESET}""" + """
    
        [groups]
        # First we define cdn, onions, and i2p
        cdn = https://cdn.privex.io cdn.privex.i2p files.privex.i2p files.privex.io https://www.privex.io
        onions = privex3guvvasyer6pxz2fqcgy56auvw5egkir6ykwpptferdcb5toad.onion privexqvhkwdsdnjofrsm7reaixclmzpbpveefiu4uctfm2l4mycnwad.onion
        i2p = privex.i2p www.privex.i2p pay.privex.i2p
        # Now we can add our main websites, PLUS the onions, and i2p variables
        websites = https://www.privex.io https://pay.privex.io https://privex.io {{onions}} {{i2p}}
        # While defaultsrc will contain 'self' + websites + cdn
        defaultsrc = 'self' {{websites}} {{cdn}}

        images = https://i.imgur.com https://ipfs.io https://cloudflare-ipfs.com
        video = https://youtube.com https://vimeo.com
        media = {{video}} {{images}}

        [default-src]
        # For default-src, we can simply set zones to use the defaultsrc var
        zones = {{defaultsrc}}
        # Enable unsafe-inline and disable unsafe-eval for default-src
        unsafe-inline = true
        unsafe-eval = false

        [img-src]
        zones = {{defaultsrc}} {{images}} {{trustpilot}}

        [media-src]
        zones = {{defaultsrc}} {{media}}

        [flags]
        # Special header 'flags'. We can set the independent CSP flag 'upgrade-insecure-requests' here.
        flags = upgrade-insecure-requests
    """ + f"""

    {Fore.GREEN}End of config{Fore.RESET}

    """),
)


def read_example_file() -> Tuple[str, Path]:
    with open(EXAMPLE_INI, 'r') as fh:
        data = fh.read()
    return data, EXAMPLE_INI


parser.add_argument('--section-sep', type=str, default=' ', dest='section_sep',
                    help="Separator between each CSP section (default-src, media-src, img-src etc.) - Textual \\n, \\r, and \\t will "
                         "be auto-converted into the literal characters for newline/carriage return/tab")
parser.add_argument('--file-sep', type=str, default='\n\n', dest='file_sep', help="Separator used between each file's config output")
parser.add_argument('--version', '-V', action='store_true', default=False, dest='show_version', help="Show version + copyright info")
parser.add_argument('--verbose', '-v', action='store_true', default=False, dest='verbose_mode', help="Verbose Mode - Show DEBUG logs")
parser.add_argument('--example', '-E', action='store_true', default=False, dest='show_example',
                    help="Output the template example.ini to STDOUT for use as a CSP INI config template")
parser.add_argument('filenames', nargs='*', default=[], help="One or more INI files to parse into CSP configs")


def main():
    global log
    try:
        vargs = parser.parse_args()
    except Exception as e:
        parser.error(f"{type(e)} - {str(e)}")
        return sys.exit(1)
    if vargs.verbose_mode:
        _lh2 = LogHelper('privex.cspgen', handler_level=logging.DEBUG)
        _lh2.add_console_handler(stream=sys.stderr)
        log = _lh2.get_logger()
        
    log.debug(f"parser args: {vargs!r}")
    if vargs.show_version:
        oprint(COPYRIGHT)
        return COPYRIGHT
    if vargs.show_example:
        exfile, expath = read_example_file()
        exnote = "#####", "#", "# Privex CSPGen example.ini file", f"# Original Location within Python Package: {expath}", "#", "#####\n"
        oprint(*exnote, exfile, *exnote, sep="\n")
        return sys.exit(0)
    filenames = vargs.filenames
    file_sep, sec_sep = literal(vargs.file_sep), literal(vargs.section_sep)
    str_secs = []
    list_secs = []
    if empty(filenames, itr=True):
        if sys.stdin.isatty():
            parser.error("No filenames specified, and no data piped to stdin")
            return sys.exit(1)
        log.debug("Assuming config piped via STDIN. Reading config from stdin.")
        confd = read_stdin()
        builder = get_builder(contents=confd)
        str_secs += [builder.generate('string', sep=sec_sep)]
        list_secs += [builder.generate('list')]
    else:
        for fn in filenames:
            if fn in ['-', '/dev/stdin', 'STDIN']:
                log.debug("Assuming config piped via STDIN. Reading config from stdin.")
                builder = get_builder(contents=read_stdin())
            else:
                builder = get_builder(fn)

            str_secs += [builder.generate('string', sep=sec_sep)]
            list_secs += [builder.generate('list')]

    # oprint('file_sep: ', repr(file_sep))
    # oprint('sec_sep: ', repr(sec_sep))
    oprint(file_sep.join(str_secs))
    return list_secs, str_secs


if __name__ == '__main__':
    main()

