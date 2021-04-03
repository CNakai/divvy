# TODO: do interface test for these a la Sandi Metz?
from ..bblearn import SubmissionFile
from pytest import fixture

class SubmissionFileDouble:
    submitted_for = 'Homework 3_ Math quiz modifications'
    submitted_on = '2021-03-17-12-08-23'
    submitted_by = 'smp549'
    submitted_as = 'Math quiz documentation.pdf'


    @property
    def name(self):
        return "_".join([self.submitted_for, self.submitted_by, 'attempt',
                         self.submitted_on, self.submitted_as])


@fixture
def test_double():
    return SubmissionFileDouble()


@fixture
def test_submission_file(test_double):
    return SubmissionFile(test_double.name)


def test_retrieves_bblearn_name(test_submission_file, test_double):
    assert test_submission_file.name == test_double.name


def test_retrieves_name_as_submitted(test_submission_file, test_double):
    assert test_submission_file.submitted_as == test_double.submitted_as


def test_retrieves_submitter_username(test_submission_file, test_double):
    assert test_submission_file.submitted_by == test_double.submitted_by


def test_retrieves_submission_timestamp(test_submission_file, test_double):
    assert test_submission_file.submitted_on == test_double.submitted_on


def test_retrieves_assignment_submitted_for(test_submission_file, test_double):
    assert test_submission_file.submitted_for == test_double.submitted_for
