from pytest import fixture

SF = "submitted_for"
SO = "submitted_on"
SB = "submitted_by"
SA = "submitted_as"

# PICKUP: Mas test data

@fixture(scope="session")
def valid_bblearn_filenames_and_segments():
    return [
        {
            "Homework 3_ Math quiz modifications_smp549_attempt_" +
            "2021-03-17-12-08-23_Math quiz documentation.pdf" }
    ]


@fixture(scope="session")
def bblearn_filename_segments():
    return {
        'submitted_for': 'Homework 3_ Math quiz modifications',
        'submitted_on': '2021-03-17-12-08-23',
        'submitted_by': 'smp549',
        'submitted_as': 'Math quiz documentation.pdf'
    }


@fixture(scope="session")
def invalid_bblearn_filename():
        # Happens to be the structure of a BBlearn submission manifest file
    return ("Homework 3_ Math quiz modifications_smp549_attempt_" +
            "2021-03-17-12-08-23.txt")

