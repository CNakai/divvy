import click
import divvy.assignment
import divvy.grading
import divvy.rubrics


sources = [
    divvy.assignment.command_group,
    divvy.grading.command_group,
    divvy.rubrics.command_group
]


@click.group()
def cli():
    pass


for command in sources:
    cli.add_command(command)
