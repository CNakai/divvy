import click
from .collate import collate
from .evaluate import evaluate
from .synthesize import synthesize
# from .send import send


@click.group(name='rubrics')
def __rubrics():
    """Commands for organizing, evaluating, and sending completed rubrics"""
    pass


__rubrics.add_command(collate)
__rubrics.add_command(evaluate)
__rubrics.add_command(synthesize)
# __rubrics.add_command(send)

command_group = [__rubrics]
