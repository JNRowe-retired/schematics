import sys

PY3K = sys.version_info[0] == 3
if PY3K:
    basestring = str
    unicode = str
else:
    basestring = basestring
    unicode = unicode
