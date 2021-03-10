import click
from .assign import assign
from .package import package
from .send import send


@click.group(name='grading')
def __grading():
    """Commands for preparing and sending grading assignments"""
    pass


__grading.add_command(assign)
__grading.add_command(package)
__grading.add_command(send)

command_group = [__grading]
