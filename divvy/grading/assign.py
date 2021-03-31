import click
from json import dump
from pathlib import Path
from random import shuffle
from sys import exit


@click.command()
@click.argument(
    'submission_dir',
    type=click.Path(file_okay=False, readable=True, resolve_path=True)
)
@click.option(
    '--number-to-grade', '-n',
    type=int, default=1,
    help="""
    The number of students that each student will grade.

    Defaults to 1.
    """
)
@click.option(
    '--output_file', '-o',
    type=click.Path(dir_okay=False, writable=True, resolve_path=True),
    help="""
    The name for the grading assignment file to be created by this program.
    The file extension ".json" is suffixed to name provided.

    If none is specified, the name of the file will default to the name of the
    submission zipfile plus "_grading_assignments.json"
    """
)
def assign(submission_dir, number_to_grade, output_file):
    """
    SUBMISSION-DIR must be a directory where a BBLearn submission zip has been
    unpacked with the 'unpack-submission' command.

    The SUBMISSION-DIR is scanned to determine the aliases of students who
    submitted the assignment.  These are then used to construct the grading
    assignment file which this program outputs.

    The grading assignment file is a JSON file containing two dictionaries: the
    first maps the ids of graders to the ids of the students whose submissions
    they will grade and the second maps the inverse relationship.

    """
    submission_dir = Path(submission_dir)

    if not submission_dir.is_dir():
        print(f"Whoops!  It seems that {submission_dir} is not a directory.")
        exit(1)

    if not output_file:
        output_file = Path(f"{submission_dir.name}_grading_assignments.json")

    if output_file.exists():
        print(f"The file {output_file} already exists!")
        click.confirm("Would you like to OVERWRITE this file and continue?",
                      abort=True)

    aliases = [submitter_dir.name for
               submitter_dir in
               submission_dir.iterdir()]
    shuffle(aliases)

    # The trick with the next line and the for loop simulates "looped slicing":
    # Starting list:
    #                 [abc123, def456, ..., uvw456, xyz789]
    #                    0       1            n       n+1
    # List capable of looped slicing:
    # [uvw456, xyz789, abc123, def456, ..., uvw456, xyz789, abc123, def456]
    #    0       1       2       3            n-1     n       n+1     n+2
    #
    # If you iterate over the slice of the list from [2:n+1], you can access
    # the items two below that slice and two above to simulate looping around
    # to the other end of the list.
    #
    # The code below uses "number_to_grade" to determine the maximum depth of
    # looped access rather than a fixed number.
    aliases = aliases[-number_to_grade:] + aliases + aliases[:number_to_grade]
    grader_to_gradees = {}
    gradee_to_graders = {}
    for (i, alias) in list(enumerate(aliases))[number_to_grade:-number_to_grade]:
        # The next number_to_grade after the current alias are those who will
        # be graded by the current alias
        grader_to_gradees[alias] = aliases[i+1:i+number_to_grade+1]
        # And those three before are the ones who will grade the current alias
        gradee_to_graders[alias] = aliases[i-number_to_grade:i]

    with open(output_file, 'w') as grading_assignment_file:
        dump(
            {
                'grader_to_gradees': grader_to_gradees,
                'gradee_to_graders': gradee_to_graders
            },
            grading_assignment_file,
            indent=4
        )
