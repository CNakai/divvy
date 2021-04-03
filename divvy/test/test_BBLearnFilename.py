from ..bblearn import Filename
from pytest import fixture

class TestFilename:
    pass


NORMAL_FILENAME = TestFilename()
NORMAL_FILENAME.username = 'smp549'
NORMAL_FILENAME.assignment = 'Homework 3_ Math quiz modifications'
NORMAL_FILENAME.timestamp = '2021-03-17-12-08-23'
NORMAL_FILENAME.submitted_filename = 'Math quiz documentation.pdf'
NORMAL_FILENAME.bblearn_filename = "_".join([
    NORMAL_FILENAME.assignment,
    NORMAL_FILENAME.username,
    'attempt',
    NORMAL_FILENAME.timestamp,
    NORMAL_FILENAME.submitted_filename
])

MANIFEST_FILENAME = TestFilename()
MANIFEST_FILENAME.username = 'ams2952'
MANIFEST_FILENAME.assignment = 'Homework 3_ Math quiz modifications'
MANIFEST_FILENAME.timestamp = '2021-03-18-03-06-21'
MANIFEST_FILENAME.submitted_filename = ''
MANIFEST_FILENAME.bblearn_filename = "_".join([
    MANIFEST_FILENAME.assignment,
    MANIFEST_FILENAME.username,
    'attempt',
    MANIFEST_FILENAME.timestamp
]) + '.txt'

@fixture
def normal_filename():
    return Filename(NORMAL_FILENAME.bblearn_filename)


@fixture
def manifest_filename():
    return Filename(MANIFEST_FILENAME.bblearn_filename)


def test_normal_filename_as_bblearn(normal_filename):
    assert normal_filename.as_bblearn == NORMAL_FILENAME.bblearn_filename


def test_normal_filename_as_submitted(normal_filename):
    assert normal_filename.as_submitted == NORMAL_FILENAME.submitted_filename


def test_normal_filename_submitter_username(normal_filename):
    assert normal_filename.submitter_username == NORMAL_FILENAME.username


def test_normal_filename_attempt_timestamp(normal_filename):
    assert normal_filename.attempt_timestamp == NORMAL_FILENAME.timestamp


def test_normal_filename_for_assignment(normal_filename):
    assert normal_filename.for_assignment == NORMAL_FILENAME.assignment


def test_normal_filename_is_submission_manifest(normal_filename):
    assert not normal_filename.is_submission_manifest


def test_manifest_filename_as_bblearn(manifest_filename):
    assert manifest_filename.as_bblearn == MANIFEST_FILENAME.bblearn_filename


def test_manifest_filename_as_submitted(manifest_filename):
    assert manifest_filename.as_submitted == MANIFEST_FILENAME.submitted_filename


def test_manifest_filename_submitter_username(manifest_filename):
    assert manifest_filename.submitter_username == MANIFEST_FILENAME.username


def test_manifest_filename_attempt_timestamp(manifest_filename):
    assert manifest_filename.attempt_timestamp == MANIFEST_FILENAME.timestamp


def test_manifest_filename_for_assignment(manifest_filename):
    assert manifest_filename.for_assignment == MANIFEST_FILENAME.assignment


def test_manifest_filename_is_submission_manifest(manifest_filename):
    assert manifest_filename.is_submission_manifest


