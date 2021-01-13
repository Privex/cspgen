#!/usr/bin/env python3
import sys


def _err(*args, file=sys.stderr, **kwargs):
    return print(*args, file=file, **kwargs)


def _failed_msg(obj: str, modl: str, pkg: str):
    return f"Failed to import " + (f"'{obj}' from '{modl}'." if obj != '' else f"'{obj}'.") + \
           f"You may need to run 'pip3 install -U {pkg}' " \
           f"or 'python3 -m pip install -U {pkg}'\n"


def cli():
    has_rich = False
    
    try:
        from rich import print
        has_rich = True
    except ImportError as e:
        _err(f" [!!!] " + _failed_msg('', 'rich', 'rich'))
        _err(f" [!!!] Exception was: {type(e)} - {str(e)} \n\n")
    
    try:
        from privex.cspgen.builder import main
    except ImportError as e:
        xmsg = _failed_msg('main', 'privex.cspgen.builder', 'privex-cspgen')
        _err(("[red] \[!!!] " + xmsg + '[/]') if has_rich else f" [!!!] {xmsg}")
        _err(
            "[red] \[!!!]" if has_rich else " [!!!]",
            f"Exception was: {type(e)} - {str(e)}",
            "[\]\n\n" if has_rich else "\n\n"
        )
        return sys.exit(1)
    
    main()
