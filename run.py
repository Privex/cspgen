#!/usr/bin/env python3
"""
This script can be used to run the CSPGen CLI directly from the Github repo modules.
"""
from pathlib import Path
import sys
BASE_DIR = Path(__file__).parent.resolve()
sys.path.extend([str(BASE_DIR)])

from privex.cspgen.cli import cli

if __name__ == '__main__':
    cli()
