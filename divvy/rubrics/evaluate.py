import click
import csv
import json
import toml
import pathlib
from sys import exit


@click.command()
@click.argument('rubrics-dir')
@click.argument('bblearn-column-name')
@click.option(
    '--grade-file', '-r',
    type=click.Path(dir_okay=False, writable=True, resolve_path=True),
    help="""
    The name of the BBLearn uploadable grade .csv file to generate.

    By default, the program will create a file with a name based on the
    RUBRICS-DIR.  It will remove the "_rubrics" ending if present and add
    "_grading_grades.csv" to the end.  This file will be created in the working
    directory of the script.
    """
)
def evaluate(rubrics_dir, bblearn_column_name, grade_file):
    """
    TODO
    """
    if not grade_file:
        grade_file = pathlib.Path(rubrics_dir).stem.split('_rubrics')[0] + '_grading_grades.csv'

    assignment_grades = {}
    grader_paths = [p for p in pathlib.Path(rubrics_dir).iterdir()
                    if p.is_dir() and '_rubrics' not in p.name]
    for grader_path in grader_paths:
        grader_id = grader_path.name

        score = 0
        for rubric_path in grader_path.iterdir():
            try:
                with open(rubric_path) as rubric_file:
                    toml.load(rubric_file)
                score += 1
            except (toml.TomlDecodeError, UnicodeDecodeError):
                print(f"{grader_id}: Bad rubric: {rubric_path.name}")

        assignment_grades[grader_id] = score

    with open(grade_file, 'w') as grades_csv_file:
        grade_writer = csv.writer(grades_csv_file, delimiter=',',
                                  quotechar='"', quoting=csv.QUOTE_ALL)
        grade_writer.writerow(('Username', bblearn_column_name))
        for username, score in assignment_grades.items():
            grade_writer.writerow((username, score))
