"""Testing that the files can be accessed and are non-empty."""

import os

import target_finder_model


def test_graph_file():
    assert os.path.getsize(target_finder_model.graph_file) > 0


def test_label_file():
    assert os.path.getsize(target_finder_model.labels_file) > 0
