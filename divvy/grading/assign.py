from .util import extract_student_id
import click
from json import dump
from os.path import abspath, exists, join, split
from random import shuffle
from sys import exit
from zipfile import is_zipfile, ZipFile


@click.command()
@click.argument('submission_zip')
@click.option('--number_to_grade', '-n', type=int, default=1, help="""
    The number of students that each student will grade.

    Defaults to 1.
    """
              )
@click.option(
    '--outfile_name', '-o',
    type=click.Path(dir_okay=False, writable=True, resolve_path=True),
    help="""
    The name for the grading assignment file to be created by this program.
    The file extension ".json" is suffixed to name provided.

    If none is specified, the name of the file will default to the name of the
    submission zipfile plus "_grading_groups.json"
    """
)
def assign(submission_zip, number_to_grade, outfile_name):
    """
    The BBLearn assignment submission zipfile indicated by SUBMISSION_ZIP is
    scanned to determine the ids of students who submitted the assignment.
    These are the ids used to construct the grading assignment file which this
    program outputs.

    The grading assignment file is a JSON file containing two dictionaries: the
    first maps the ids of graders to the ids of the students whose submissions
    they will grade and the second maps the inverse relationship.
    """
    if not is_zipfile(submission_zip):
        print(f"Whoops, it seems that there is no zipfile at {submission_zip}")
        exit(1)

    if not outfile_name:
        (submission_path, submission_filename) = split(abspath(submission_zip))
        # This is technically incorrect because the first "." is not guaranteed
        # to be the file extension separator in any filename, but it should
        # suffice for the submission filenames generated by BBLearn assuming
        # instructors aren't including dots in their assignment names
        submission_name = submission_filename.split('.')[0]
        outfile_name = join(submission_path,
                            submission_name + "_grading_groups")

    outfile_name += ".json"

    if exists(outfile_name):
        print(f"The file {outfile_name} already exists!")
        click.confirm("Would you like to OVERWRITE this file and continue?",
                      abort=True)

    with ZipFile(submission_zip) as z:
        submission_filenames = z.namelist()

    ids = []
    for filename in submission_filenames:
        ids.append(extract_student_id(filename))
        ids = list(set(ids))
        shuffle(ids)

    grader_to_gradees = {}
    gradee_to_graders = {}
    # The trick with the next line and the for loop simulates "looped slicing"
    ids = ids[-number_to_grade:] + ids + ids[:number_to_grade]
    for (i, id) in list(enumerate(ids))[number_to_grade:-number_to_grade]:
        grader_to_gradees[id] = ids[i+1:i+number_to_grade+1]
        gradee_to_graders[id] = ids[i-number_to_grade:i]

    with open(outfile_name, 'w') as grading_assignment_file:
        dump(
            {
                'grader_to_gradees': grader_to_gradees,
                'gradee_to_graders': gradee_to_graders
            },
            grading_assignment_file,
            indent=4
        )
