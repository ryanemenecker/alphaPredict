"""
short description of alphaPredict.

Predict confidence scores of alphaFold2
"""

# Add imports here
from .alpha import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
