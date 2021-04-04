from pytest import fixture
from pytest import raises
from divvy.bblearn import filename
from divvy.bblearn.errors import InvalidFilenameError


def test_valid_bblearn_filename_is_segmentable(valid_bblearn_filename):
    assert filename.is_segmentable(valid_bblearn_filename)


def test_invalid_bblearn_filename_is_not_segmentable(invalid_bblearn_filename):
    assert not filename.is_segmentable(invalid_bblearn_filename)


def test_segment(valid_bblearn_filename, bblearn_filename_segments):
    segments = filename.segment(valid_bblearn_filename)
    assert segments == bblearn_filename_segments


def test_segment_raises_InvalidFilenameError_on_failure(
        invalid_bblearn_filename):
    with raises(InvalidFilenameError):
        filename.segment(invalid_bblearn_filename)
