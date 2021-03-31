from os import mkdir
from shutil import move, rmtree
from zipfile import is_zipfile, ZipFile

# PICKUP: Refactor to use pathlib and alias_map


def refile_files_by_submitter(submission_directory, alias_map=None,
                              unpack_submitted_zips=False):
    """
    Creates per student subdirectories within the submission_directory and
    moves each student's files into their directory.

    If there is no alias map the per student subdirectories will be named
    according to their BBLearn username, otherwise their username will be
    looked up in the alias map and the alias will be used instead.

    If unpack_submitted_zips is true, after the submitted files have been moved
    into the created per student subdirectories, those subdirectories will be
    visited and any zip files found in them will be extracted into them and
    then the zip file will be deleted.
    """
    submission_file_paths = sorted(
        list(submission_directory.iterdir()),
        key=lambda path: extract_student_id(path.name)
    )

    for path in submission_file_paths:
        username = extract_bblearn_username(path.name)
        alias = alias_map[username] if alias_map else username
        student_directory = submission_directory.joinpath(alias)
        if not student_directory.exists():
            mkdir(student_directory)

        file_name_as_submitted = remove_bblearn_prefix(path.name)
        move(path, student_directory.joinpath(file_name_as_submitted))

    for student_directory_path in submission_directory.iterdir():
        # Clean up metadata files
        for cruft in ['__MACOSX', '.DS_store']:
            rmtree(student_directory_path.joinpath(cruft), ignore_errors=True)

        if unpack_submitted_zips:
            for submitted_file_path in student_directory_path.iterdir():
                if is_zipfile(submitted_file_path):
                    with ZipFile(submitted_file_path) as z:
                        z.extractall(student_directory_path)


def extract_bblearn_username(bblearn_submitted_filename):
    return extract_student_id(bblearn_submitted_filename)


# TODO: Document the BBLearn prefix format so these make sense
def extract_student_id(bblearn_filename):
    front = bblearn_filename.split(sep='_attempt_', maxsplit=2)[0]
    return front[front.rindex('_') + 1:]


def remove_bblearn_prefix(bblearn_filename):
    back = bblearn_filename.split(sep='_attempt_', maxsplit=2)[1]
    return back[back.find('_') + 1:]
