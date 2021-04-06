from divvy.bblearn.errors import InvalidBBLearnFilenameError


def segment(bblearn_filename):
    """Returns the four constituent pieces a valid BBLearn filename

    The format of a valid filename is:
    <assignment name>_<username>_attempt_<timestamp>_<name as submitted>

    If the passed filename is not valid, an exception is raised

    """
    try:
        assignment_and_username, timestamp_and_filename = \
            bblearn_filename.split('_attempt_')
        assignment, username = assignment_and_username.rsplit('_',
                                                                maxsplit=1)
        timestamp, filename = timestamp_and_filename.split('_', maxsplit=1)
    except ValueError:
        raise InvalidBBLearnFilenameError(bblearn_filename)

    return {
        'submitted_for': assignment,
        'submitted_by': username,
        'submitted_on': timestamp,
        'submitted_as': filename
    }


def is_segmentable(bblearn_filename):
    try:
        segment(bblearn_filename)
        return True
    except Exception:
        return False

