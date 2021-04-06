from pytest import fixture
from pytest import raises
from divvy.bblearn import filename
from divvy.bblearn.errors import InvalidBBLearnFilenameError


def test_valid_bblearn_filename_is_segmentable(valid_bblearn_filename):
    assert filename.is_segmentable(valid_bblearn_filename)


def test_invalid_bblearn_filename_is_not_segmentable(invalid_bblearn_filename):
    assert not filename.is_segmentable(invalid_bblearn_filename)


def test_segment(valid_bblearn_filename, bblearn_filename_segments):
    segments = filename.segment(valid_bblearn_filename)
    assert segments == bblearn_filename_segments


def test_segment_raises_error_with_invalid_filename(invalid_bblearn_filename):
    with raises(InvalidBBLearnFilenameError):
        filename.segment(invalid_bblearn_filename)
