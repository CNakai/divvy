from os import mkdir, rename, scandir
from os.path import exists, join
from shutil import rmtree

def refile_files_by_submitter(submission_directory):
    """
    Creates per student subdirectories within the submission_directory and
    moves each students files into their directory
    """
    submission_file_entries = sorted(
        list(scandir(submission_directory)),
        key=lambda entry: extract_student_id(entry.name)
    )

    for entry in submission_file_entries:
        id = extract_student_id(entry.name)
        student_directory = join(submission_directory, id)

        if not exists(student_directory):
            mkdir(student_directory)

        new_path = join(student_directory, remove_bblearn_prefix(entry.name))
        rename(entry.path, new_path)

    for student_directory_entry in scandir(submission_directory):
        student_directory = student_directory_entry.path
        for cruft in ['__MACOSX', '.DS_store']:
            rmtree(join(student_directory, cruft), ignore_errors=True)


def extract_student_id(bblearn_filename):
    front = bblearn_filename.split(sep='_attempt_', maxsplit=2)[0]
    return front[front.rindex('_') + 1:]


def remove_bblearn_prefix(bblearn_filename):
    back = bblearn_filename.split(sep='_attempt_', maxsplit=2)[1]
    return back[back.find('_') + 1:]
