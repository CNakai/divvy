from ..bblearn_submission_utils import refile_files_by_submitter
import click
from json import dump, load
from os import mkdir, remove, rename
from os.path import abspath, basename, exists, join, split
import pathlib
from shutil import copy, copytree, make_archive, rmtree
from sys import exit
from zipfile import is_zipfile, ZipFile


# TODO
extraneous_rubrics_notice = """
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
@click.argument('rubrics-zip')
@click.argument('grading-assignment-file')
@click.option(
    '--output-dir', '-d',
    type=click.Path(file_okay=False, writable=True, resolve_path=True),
    help="""
    The directory where the student rubric folders will be created.  It must be
    empty.

    By default, the program will create a directory with the same name as the
    SUBMITTED-RUBRICS-ZIP minus the file extension in the working directory of
    the script.
    """
)
@click.option(
    '--report-file', '-r',
    type=click.Path(dir_okay=False, writable=True, resolve_path=True),
    help="""
    The name of the report file to generate.

    By default, the program will create a file with a name based on the
    GRADING-ASSIGNMENT-FILE.  It will remove the "_grading_groups" ending
    if present and add "_rubric_collation_report" to the end instead.  This
    file will be created in the working directory of the script.
    """
)
def collate(rubrics_zip, grading_assignment_file, output_dir, report_file):
    """
    The rubrics for each gradee student in the BBLearn assignment submission
    zipfile indicated by SUBMITTED-RUBRICS-ZIP are placed into their own
    directories labelled with the gradee student's id.  In order to prevent
    naming collisions, the rubrics may be renamed by appending consecutive
    integers to the end of the filename.

    Next, a report is generated stating for which students rubrics were
    missing and whose responsibility those rubrics were.

    Finally, all the rubrics in each gradee's directory are added to a zipfile
    which can be mailed to the gradee with the 'rubrics send' command.
    """
    if not is_zipfile(rubrics_zip):
        print(f"Whoops, it seems that there is no zipfile at {rubrics_zip}")
        exit(1)

    if not output_dir:
        (rubrics_zip_path, rubrics_zip_filename) = split(abspath(rubrics_zip))
        # This is technically incorrect because the first "." is not guaranteed
        # to be the file extension separator in any filename, but it should
        # suffice for the submission filenames generated by BBLearn assuming
        # instructors aren't including dots in their assignment names
        output_dir = rubrics_zip_filename.split('.')[0]

    if not exists(output_dir):
        print(f"Creating directory {output_dir}")
        mkdir(output_dir)
        print("Done!")
    elif len(scandir(output_dir)) != 0:
        print(f"The directory {output_dir} is not empty!")
        exit(1)

    print("\nUnzipping rubrics archive...")
    with ZipFile(rubrics_zip) as z:
        z.extractall(output_dir)
        print("Done!")

    print("Intermediately refiling submitted rubrics by submitter...")
    refile_files_by_submitter(output_dir)
    print("Done!")

    print("Refiling rubrics into gradee directories...")
    with open(grading_assignment_file, 'r') as gaf:
        grading_assignments = load(gaf)
    missing_rubrics = refile_rubrics_by_gradee(output_dir, grading_assignments)
    print("Done!")

    print("Packaging rubrics into sendable zips for the gradees...")
    package_rubrics(output_dir)
    print("Done!\n")

    if missing_rubrics:
        print("Uh oh, some rubrics were missing!")
        print(missing_rubrics)
        with open('missing_rubrics.json', 'w') as mr:
            dump(missing_rubrics, mr, indent=4)


def refile_rubrics_by_gradee(output_dir, grading_assignments):
    output_path = pathlib.Path(output_dir)
    grader_to_gradees = grading_assignments['grader_to_gradees']
    missing_rubrics = grading_assignments['gradee_to_graders']
    for grader_id, gradee_ids in grader_to_gradees.items():
        grader_path = output_path.joinpath(grader_id)
        if not grader_path.exists():
            continue

        for file_path in grader_path.iterdir():
            gradee_id = file_path.stem.split('__gradee_')[-1]
            if gradee_id not in gradee_ids:
                remove(file_path)
                continue

            try:
                missing_rubrics[gradee_id].remove(grader_id)
            except ValueError:
                print('There was an attempt to double-remove the rubric',
                      f'submitted by {grader_id} for {gradee_id}')
                continue

            gradee_rubrics_path = output_path.joinpath(gradee_id + '_rubrics')
            if not gradee_rubrics_path.exists():
                mkdir(gradee_rubrics_path)
            file_count = len(list(gradee_rubrics_path.iterdir()))
            new_file_name = (f'{file_path.stem}_{file_count}' +
                             ''.join(file_path.suffixes))
            copy(file_path, gradee_rubrics_path.joinpath(new_file_name))
            # print(f'{gradee_id} \t {missing_rubrics[gradee_id]} \t {grader_id}')

        # rmtree(grader_path)

    for gradee_id, graders in list(missing_rubrics.items()):
        if not graders:
            missing_rubrics.pop(gradee_id)

    return missing_rubrics

# TODO: Make util with similar function passing in 'remove_dirs'
# TODO: Make it take in a list of paths to dirs
def package_rubrics(output_dir):
    for gradee_rubrics_path in pathlib.Path(output_dir).iterdir():
        make_archive(
            gradee_rubrics_path,
            'zip',
            root_dir=output_dir,
            base_dir=gradee_rubrics_path.name
        )