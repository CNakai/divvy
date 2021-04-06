import click
from os import mkdir
from pathlib import Path
from sys import exit
from zipfile import is_zipfile, ZipFile
from .bblearn_submission_utils import refile_files_by_submitter
from .bblearn.submissionfile import SubmissionFile


@click.command()
@click.argument('submission-zip')
@click.option(
    '--unpacking-dir', '-d',
    type=click.Path(file_okay=False, writable=True, resolve_path=True),
    help="""
    The directory into which the SUBMISSION-ZIP will be initially unpacked and
    in which the student submission directories will be created.

    The provided directory must be empty.  If it is not, the operation will
    terminate.

    By default, the program will create a directory with the same name as the
    SUBMISSION-ZIP minus the file extension in the working directory of the
    script.
    """
)
@click.option(
    '--alias-map', '-m', 'alias_map',
    type=click.Path(dir_okay=False, readable=True, resolve_path=True),
    help="""
    Submission directories are named according to the ALIAS-MAP which should
    be a .csv file with two columns.  One column must be named "Username", and
    the other column must be named "Alias" (case-insensitive).

    The "Username" column should contain BBLearn usernames for students (for
    NAU this is their CAS id, the prefix of their NAU e-mail) and the "Alias"
    column should contain whatever alias you want to map those usernames to,
    e.g. full names, student id numbers, a secret id, etc.
    """
)
def unpack_submission(submission_zip, unpacking_dir, alias_map):
    """
    Unpack BBLearn assignment submission zips.

    First, the SUBMISSON-ZIP is unzipped into the UNPACKING-DIR.  Then, for
    each file, the username of the file's submitter is discerned from the
    username.  If a directory already exists for that student's submission, the
    file is moved to that directory.  If not, a directory for that student's
    submission is created and then the file is moved there.  These per
    submitter directories are called *(student) submission directories*

    When the files are moved into their submission directory, the prefix that
    was added to the filename by BBLearn is removed.  This means that when the
    unpacking operation is finished, the UNPACKING-DIR will contain only
    student submission directories--since each file will have been moved into
    one--and that each submission directory will hold the files submitted by a
    single student and that those files will have the name they had when the
    student submitted them.
    """
    submission_zip = Path(submission_zip)

    if not is_zipfile(submission_zip):
        print(f"Whoops, it seems that {submission_zip} is not a zip file")
        exit(1)

    # This is technically incorrect because the first "." is not guaranteed
    # to be the file extension separator in any filename, but it should
    # suffice for the submission filenames generated by BBLearn assuming
    # instructors aren't including dots in their assignment names
    unpacking_dir = (Path(submission_zip.stem)
                     if not unpacking_dir
                     else Path(unpacking_dir))

    if not unpacking_dir.exists():
        print(f"Creating directory {unpacking_dir}... ", end="")
        mkdir(unpacking_dir)
        print("Done!")
    elif len(list(unpacking_dir.iterdir())) != 0:
        print(f"The directory {unpacking_dir} is not empty!")
        exit(1)

    print("\nUnzipping submission archive... ", end="")
    with ZipFile(submission_zip) as z:
        z.extractall(unpacking_dir)
        print("Done!")

    print("Refiling submitted files into student submission directories...",
          end="")
    if alias_map:
        # TODO: Create dictionary from info in .csv file
        pass
    refile_files_by_submitter(unpacking_dir, alias_map)
    print("Done!")
