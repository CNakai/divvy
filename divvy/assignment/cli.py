import click
from os import mkdir
from pathlib import Path
from shutil import rmtree
from sys import exit

from .assignment import Assignment


def set_up_command_group():
    global command_group
    __attempts.add_command(unpack)
    command_group = __attempts


@click.group(name='attempts')
def __attempts():
    """Commands for querying and unpacking assignment attempts"""
    pass


@click.command()
@click.argument('assignment-download-zip')
@click.option(
    '--unpacking-dir', '-d',
    type=click.Path(file_okay=False, writable=True, resolve_path=True),
    help="""
    The directory into which the ASSIGNMENT-DOWNLOAD-ZIP will be initially
    unpacked and in which the student submission directories will be created.

    The provided directory must be empty.  If it is not, the operation will
    terminate.

    By default, the program will create a directory with the same name as the
    ASSIGNMENT-DOWNLOAD-ZIP minus the file extension in the working directory
    of the script.
    """
)
def unpack(assignment_download_zip, unpacking_dir):
    """
    Unpack BBLearn assignment submission zips.

    """
    assignment = Assignment.from_bblearn_assignment_download_zip(
        assignment_download_zip
    )
    unpacking_dir = Path(unpacking_dir) if unpacking_dir else Path('.')
    if not unpacking_dir.exists():
        mkdir(unpacking_dir)

    save_path = assignment.save_path(unpacking_dir)
    if save_path.exists():
        print("ATTENTION: the path the bblearn zip file will be unpacked at",
              f"already exists:\n\t{save_path}\nContinuing will delete what",
              "is there.  Do you want to continue?")
        choice = input("[y/N]: ").lower()[0:1]

        if choice != 'y':
            exit()

        rmtree(save_path)

    assignment.save(unpacking_dir)


set_up_command_group()
