import click
import divvy.grading
# import divvy.rubrics


@click.group()
def cli():
    pass


def __build_command_groups():
    command_groups = [
        divvy.grading.command_group,
        # divvy.rubrics.command_group,
    ]

    for command_group in command_groups:
        for command in command_group:
            cli.add_command(command)


__build_command_groups()
