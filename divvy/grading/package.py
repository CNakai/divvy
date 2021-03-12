from ..bblearn_submission_utils import refile_files_by_submitter
import click
from json import load
from os import mkdir, scandir, rename
from os.path import abspath, basename, exists, join, split
from shutil import copy, copytree, make_archive, rmtree
from sys import exit
from zipfile import is_zipfile, ZipFile


unassigned_gradees_notice = """
NOTICE: There were {0} students who had a submission in the submission file but
        who were not listed in the grading assignment file as a gradee.

        This likely due to either:

            1) running the 'package' command with a submission file or a
            grading assignment file that are mismatched, i.e. using a 'hwk1'
            submission file but a 'hwk2' grading assignment file or vice versa;
            this is likely if the number of unassigned gradees is high.

            2) running the 'package' command with a "fresher" version of the
            submission file than was used to generate the grading assignment
            file; you can either regenerate the grading assignment file (if you
            want to include the unassigned gradees in the grading process) or
            ignore this warning (if those students, say, made their submissions
            after the due date and you want to exclude them).
"""


@click.command()
@click.argument('submission-zip')
@click.argument('grading-assignment-file')
@click.option(
    '--rubric', '-r', 'rubrics',
    multiple=True,
    type=click.Path(exists=True, dir_okay=False,
                    readable=True, resolve_path=True),
    help="""
    A path to a file containing a rubric.  This file will be copied into every
    student submission directory in every zipfile.  When it is copied, the
    filename will be changed according to the following scheme:

    Original:    "rubric1.extension"
    After copy:  "rubric1__gradee_<id of student being graded>.extension"

    This option can be given multiple times.
    """
)
@click.option(
    '--grading-instructions', '-i',
    type=click.Path(exists=True, dir_okay=False,
                    readable=True, resolve_path=True),
    help="""
    A path to a file containing grading instructions.  This is different from
    rubric files.  Grading instructions are more general and apply to the whole
    assignment.

    If specified, this file will be placed at the top level of every created
    zipfile.
    """
)
@click.option(
    '--output-dir', '-d',
    type=click.Path(file_okay=False, writable=True, resolve_path=True),
    help="""
    The directory into which the zipfiles should be placed.  It must be empty.

    By default, the program will create a directory with the same name as the
    SUBMISSION-ZIP minus the file extension in the working directory of the
    script.
    """
)
def package(submission_zip, grading_assignment_file, rubrics,
            grading_instructions, output_dir):
    """
    The files for each student's submission in the BBLearn assignment
    submission zipfile indicated by SUBMISSION-ZIP are placed into their own
    directories labelled with the student's id.  Any specified RUBRICs are then
    copied into these directories.

    A new set of directories is created to contain all the student submission
    directories for a given grader.  These directories are labelled according
    to the following scheme:

        <grader's id>_grading_for_<assignment_name>

    Where the assignment name comes from the name of the BBLearn submission
    file minus the file extension.

    The GRADING-ASSIGNMENT-FILE is then used to move the appropriate student
    submission directories into the assigned grader's directory.

    Finally, any grading instructions are copied into the grader directories
    and then the grader directories are zipped.

    The directory tree for a grader's zipfile might look like this:

    \b
    jkl321_grading_for_hwk1.zip
    └── jkl321_grading_for_hwk1
        ├── GRADING_INSTRUCTIONS.txt
        ├── ghi789
        │   ├── submission_file3.txt
        │   ├── submission_file2.txt
        │   ├── submission_file1.txt
        │   ├── rubric_1__gradee_ghi789.json
        │   └── rubric_2__gradee_ghi789.json
        ├── def456
        │   ├── submission_file3.txt
        │   ├── submission_file2.txt
        │   ├── submission_file1.txt
        │   ├── rubric_1__gradee_def456.json
        │   └── rubric_2__gradee_def456.json
        └── abc123
            ├── submission_file3.txt
            ├── submission_file2.txt
            ├── submission_file1.txt
            ├── rubric_1__gradee_abc126.json
            └── rubric_2__gradee_abc126.json

    """
    if not is_zipfile(submission_zip):
        print(f"Whoops, it seems that there is no zipfile at {submission_zip}")
        exit(1)

    if not output_dir:
        (submission_path, submission_filename) = split(abspath(submission_zip))
        # This is technically incorrect because the first "." is not guaranteed
        # to be the file extension separator in any filename, but it should
        # suffice for the submission filenames generated by BBLearn assuming
        # instructors aren't including dots in their assignment names
        output_dir = submission_filename.split('.')[0]

    if not exists(output_dir):
        print(f"Creating directory {output_dir}")
        mkdir(output_dir)
        print("Done!")
    elif len(list(scandir(output_dir))) != 0:
        print(f"The directory {output_dir} is not empty!")
        exit(1)

    print("\nUnzipping submission archive...")
    with ZipFile(submission_zip) as z:
        z.extractall(output_dir)
        print("Done!")

    print("Refiling submitted files into student submission directories...")
    refile_files_by_submitter(output_dir)
    print("Done!")

    print("Distributing rubric files...")
    assignment_name = basename(submission_zip).split('.')[0]
    distribute_rubrics(output_dir, rubrics, assignment_name)
    print("Done!")

    print("Refiling student submission directories into grader directories...")
    with open(grading_assignment_file, 'r') as gaf:
        grading_assignments = load(gaf)
    gradee_to_graders = grading_assignments['gradee_to_graders']
    unassigned_gradees = refile_submissions_by_grader(output_dir,
                                                      gradee_to_graders,
                                                      assignment_name)
    print("Done!")

    print("Packaging grader directories...")
    package_grader_dirs(output_dir, grading_instructions)
    print("Done!\n")

    if unassigned_gradees != []:
        print(unassigned_gradees_notice.format(len(unassigned_gradees)))


def distribute_rubrics(output_dir, rubrics, assignment_name):
    for gradee_entry in scandir(output_dir):
        for rubric in rubrics:
            (rubric_name, extensions) = basename(rubric).split('.', maxsplit=1)
            rubric_copy_path = join(
                gradee_entry.path,
                f"{rubric_name}__gradee_{gradee_entry.name}.{extensions}"
            )
            copy(rubric, rubric_copy_path)


def refile_submissions_by_grader(output_dir, gradee_to_graders,
                                 assignment_name):
    unassigned_gradees = []
    for gradee_entry in scandir(output_dir):
        gradee_id = gradee_entry.name
        grader_ids = gradee_to_graders.get(gradee_id)

        if not grader_ids:
            unassigned_gradees.append(gradee_id)
            rmtree(gradee_entry.path)
            continue

        for grader_id in grader_ids:
            grader_dir_name = f"{grader_id}_grading_for_{assignment_name}"
            grader_dir_path = join(output_dir, grader_dir_name)
            if not exists(grader_dir_path):
                mkdir(grader_dir_path)
            copytree(gradee_entry.path,
                     join(grader_dir_path, gradee_entry.name))
        rmtree(gradee_entry.path)

    return unassigned_gradees


def package_grader_dirs(output_dir, grading_instructions):
    for grader_entry in scandir(output_dir):
        if grading_instructions:
            copy(grading_instructions, grader_entry.path)
        make_archive(
            grader_entry.path,
            'zip',
            root_dir=output_dir,
            base_dir=grader_entry.name
        )
        rmtree(grader_entry.path)
