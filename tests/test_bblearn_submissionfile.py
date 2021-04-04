# TODO: do interface test for these a la Sandi Metz?
from divvy.bblearn import SubmissionFile as SF
from pytest import fixture
from pytest import raises

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


@fixture
def test_double():
    class SubmissionFileDouble:
        submitted_for = 'Homework 3_ Math quiz modifications'
        submitted_on = '2021-03-17-12-08-23'
        submitted_by = 'smp549'
        submitted_as = 'Math quiz documentation.pdf'
        bblearn_name = (
            f"{submitted_for}_{submitted_by}_attempt_{submitted_on}_{submitted_as}"
        )

    return SubmissionFileDouble()


@fixture
def test_submission_file(test_double):
    return SF(submitted_as=test_double.submitted_as,
              submitted_by=test_double.submitted_by,
              submitted_on=test_double.submitted_on,
              submitted_for=test_double.submitted_for)


def test_validates_valid_bblearn_filename(valid_bblearn_filename):
    assert SF.is_valid_bblearn_filename(valid_bblearn_filename)


def test_invalidates_valid_bblearn_filename(invalid_bblearn_filename):
    assert not SF.is_valid_bblearn_filename(invalid_bblearn_filename)


def test_creation_from_valid_bblearn_filename_succeeds(valid_bblearn_filename):
    SF.from_bblearn_filename(valid_bblearn_filename)


def test_creation_from_invalid_bblearn_filename_fails(invalid_bblearn_filename):
    with raises(Exception):
        SF.from_bblearn_filename(invalid_bblearn_filename)

def test_retrieves_bblearn_name(test_submission_file, test_double):
    assert test_submission_file.bblearn_name == test_double.bblearn_name


def test_retrieves_name_as_submitted(test_submission_file, test_double):
    assert test_submission_file.submitted_as == test_double.submitted_as


def test_retrieves_submitter_username(test_submission_file, test_double):
    assert test_submission_file.submitted_by == test_double.submitted_by


def test_retrieves_submission_timestamp(test_submission_file, test_double):
    assert test_submission_file.submitted_on == test_double.submitted_on


def test_retrieves_assignment_submitted_for(test_submission_file, test_double):
    assert test_submission_file.submitted_for == test_double.submitted_for
