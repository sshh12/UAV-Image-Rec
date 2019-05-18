"""Testing that the files can be accessed and are non-empty."""

import os

import target_finder_model as tfm


def test_constants():
    """Test constants packaged with tfm"""
    assert tfm.CROP_SIZE[0] == tfm.CROP_SIZE[1]
    assert tfm.CROP_OVERLAP < tfm.CROP_SIZE[0]

    assert tfm.DETECTOR_SIZE[0] == tfm.DETECTOR_SIZE[1]
    assert tfm.PRECLF_SIZE[0] == tfm.PRECLF_SIZE[1]

    assert len(tfm.YOLO_CLASSES) > 0
    assert len(tfm.CLF_CLASSES) > 0
