# TODO: do interface test for these a la Sandi Metz?
from pytest import fixture
from divvy.attempts import AttemptFile
from divvy.bblearn import filename

@fixture
def test_double(valid_bblearn_filename, bblearn_filename_segments):
    class AttemptFileDouble:
        submitted_for = bblearn_filename_segments['submitted_for']
        submitted_on = bblearn_filename_segments['submitted_on']
        submitted_by = bblearn_filename_segments['submitted_by']
        submitted_as = bblearn_filename_segments['submitted_as']
        bblearn_name = valid_bblearn_filename

    return AttemptFileDouble()


@fixture
def test_attempt_file(bblearn_filename_segments):
    return AttemptFile(**bblearn_filename_segments)


def test_retrieves_bblearn_name(test_attempt_file, test_double):
    assert test_attempt_file.bblearn_name == test_double.bblearn_name


def test_retrieves_name_as_submitted(test_attempt_file, test_double):
    assert test_attempt_file.submitted_as == test_double.submitted_as


def test_retrieves_submitter_username(test_attempt_file, test_double):
    assert test_attempt_file.submitted_by == test_double.submitted_by


def test_retrieves_submission_timestamp(test_attempt_file, test_double):
    assert test_attempt_file.submitted_on == test_double.submitted_on


def test_retrieves_assignment_submitted_for(test_attempt_file, test_double):
    assert test_attempt_file.submitted_for == test_double.submitted_for
