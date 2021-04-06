import click
import divvy.grading
import divvy.rubrics

sources = [
    divvy.grading.command_group,
    divvy.rubrics.command_group
]

@click.group()
def cli():
    pass


for command in sources:
    cli.add_command(command)
