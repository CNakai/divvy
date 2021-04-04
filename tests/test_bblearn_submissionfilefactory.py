from pytest import fixture
from pytest import raises
from divvy.bblearn import SubmissionFileFactory as SFF


@fixture
def valid_bblearn_filename():
    return ("Homework 3_ Math quiz modifications_smp549_attempt_" +
            "2021-03-17-12-08-23_Math quiz documentation.pdf")


@fixture
def bblearn_submission_manifest_filename():
    return ("Homework 3_ Math quiz modifications_smp549_attempt_" +
            "2021-03-17-12-08-23.txt")


@fixture
def invalid_bblearn_filename(bblearn_submission_manifest_filename):
    return bblearn_submission_manifest_filename


def test_validates_valid_bblearn_filename(valid_bblearn_filename):
    assert SFF.is_valid_bblearn_filename(valid_bblearn_filename)


def test_invalidates_valid_bblearn_filename(invalid_bblearn_filename):
    assert not SFF.is_valid_bblearn_filename(invalid_bblearn_filename)


def test_creation_from_valid_bblearn_filename_succeeds(valid_bblearn_filename):
    SFF.from_bblearn_filename(valid_bblearn_filename)


def test_creation_from_invalid_bblearn_filename_fails(invalid_bblearn_filename):
    with raises(Exception):
        SFF.from_bblearn_filename(invalid_bblearn_filename)
