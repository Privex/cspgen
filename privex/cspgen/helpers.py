import logging
import sys
import re
from privex.helpers import empty, empty_if, T, K
from typing import List, Optional, Union
log = logging.getLogger(__name__)

__all__ = [
    'read_stdin', 're_markers', '_re_markers', 'replace_markers', 'automark_str',
    'automark', '_dedup', 'dedup', 'dedup_dict', 'clean_dict', 'literal'
]


def read_stdin(auto_strip=True) -> List[str]:
    """Read STDIN into a list of :class:`.str`'s and then returns that list."""
    lines = []
    for ln in sys.stdin:
        lines.append(ln.strip() if auto_strip else ln)
    return lines


_re_markers = r'{{([a-zA-Z0-9._-]+)}}'
re_markers = re.compile(r'{{([a-zA-Z0-9._-]+)}}')


def replace_markers(data: str, groupsrc: dict, *markers) -> str:
    """
    Replace the markers ``markers`` in the form of ``{{marker}}`` which are present in the string ``data``,
    by looking up the marker names against ``groupsrc``, and recursively replacing any markers found in the
    replacement from ``groupsrc``.
    
    :param str data: The data to replace markers within
    :param dict groupsrc: A dictionary containing marker names mapped to their value, to be used for replacing markers in ``data``
    :param str markers: One or more markers to search for within ``data`` and replace.
    :return str new_data: The ``data`` after replacing all passed markers.
    """
    data = str(data)
    for m in markers:
        mk = '{{' + str(m) + '}}'
        if mk not in data: continue
        repd = ''
        if m in groupsrc:
            repd = groupsrc[m]
            log.debug(f"Found marker replacement: {m!r} = {repd!r}")
            repmks = re.compile(_re_markers).findall(repd)
            if len(repmks) > 0:
                log.debug(f"Marker replacement contains {len(repmks)} markers too! Replacing sub-markers...")
                repd = groupsrc[m] = replace_markers(repd, groupsrc, *repmks)
        data = data.replace(mk, repd)
        log.debug(f"Replaced data marker: {m!r} = {repd!r}")
        
    return data


def automark_str(data: str, groupsrc: dict):
    """Replace markers in the form of ``{{marker}}`` in ``data``, by looking up the marker name against ``groupsrc``"""
    log.debug(f" >>> Checking value for markers: {data!r}")
    gmarks = re.compile(_re_markers).findall(data)
    if len(gmarks) > 0:
        data = replace_markers(data, groupsrc, *gmarks)
    return data


def automark(data: dict, groupsrc: dict, inplace=False):
    """Replace markers in the form of ``{{marker}}`` in the values of ``data``, by looking up the marker name against ``groupsrc``"""
    data = data if inplace else {k: v for k, v in data.items()}
    for k, v in data.items():
        data[k] = automark_str(v, groupsrc)
    return data


def _dedup(data: Union[list, tuple]) -> list:
    """Remove duplicates from a list/tuple, then return a new clean list"""
    ndata = []
    for d in data:
        if d in ndata: continue
        ndata.append(d)
    return ndata


def dedup(data: Union[list, tuple, str, T], sep=None) -> T:
    """Remove duplicate entries from a list/tuple, or a string (split into a list using ``sep`` (default: any whitespace))"""
    if isinstance(data, str):
        sdt = data.split(sep)
        ndata = _dedup(sdt)
        sep = ' ' if sep is None else sep
        return sep.join(ndata)
    
    ndata = _dedup(data)
    return list(ndata) if isinstance(data, list) else tuple(ndata)


def dedup_dict(data: dict, sep=None, inplace=False) -> dict:
    """Same as :func:`.dedup` but de-duplicates the values in :class:`.dict`'s instead of list/tuple/str's """
    ndict = data if inplace else {}
    for k, v in data.items():
        ndict[k] = dedup(v, sep=sep)
    return ndict


def clean_dict(data: dict, groupsec: dict = None, inplace=False, do_automark=True, do_dedup=True, **kwargs) -> dict:
    """
    Extracts the contents of a dict-like object using ``dict(list(data.items()))``, replaces any markers present inside
    of the dict's values using :func:`.automark` (if do_automark is True), and then removes any duplicate entries
    within it's values, using :func:`.dedup` (if do_dedup is True).
    """
    ndata = dict(list(data.items()))
    groupsec = ndata if empty(groupsec) else groupsec
    if do_automark:
        ndata = automark(ndata, groupsec, inplace)
    if do_dedup:
        ndata = dedup_dict(ndata, inplace=inplace)
    return ndata


def literal(data: str) -> str:
    """Replaces ``\\n``, ``\\r`` and ``\\t`` in a string, with the real literal newline, carraige return, and tab characters."""
    return str(data).replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t")
