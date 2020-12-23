import click
# from .collate import collate
# from .evaluate import evaluate
# from .send import send


@click.group(name='rubrics')
def __rubrics():
    """Commands for organizing, evaluating, and sending completed rubrics"""
    pass


# __grading.add_command(collate)
# __grading.add_command(evaluate)
# __grading.add_command(send)

command_group = [__rubrics]
