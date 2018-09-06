"""Entrypoint for the target_finder_model library.

This module contains the filenames used for target-finder so they can
be encapsulated in a single python library that can be fetched.
"""

from pkg_resources import resource_filename

from .version import __version__


graph_file = resource_filename(__name__, 'data/graph.pb')
labels_file = resource_filename(__name__, 'data/labels.txt')
