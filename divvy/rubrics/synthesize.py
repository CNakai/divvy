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
    "_grades.csv" to the end.  This file will be created in the working
    directory of the script.
    """
)
def synthesize(rubrics_dir, bblearn_column_name, grade_file):
    """
    TODO
    """
    if not grade_file:
        grade_file = pathlib.Path(rubrics_dir).stem.split('_rubrics')[0] + '_grades.csv'

    assignment_grades = {}
    gradee_paths = [p for p in pathlib.Path(rubrics_dir).iterdir()
                    if p.is_dir() and '_rubrics' in p.name]
    for gradee_path in gradee_paths:
        gradee_id = gradee_path.stem.split('_rubrics')[0]
        grade_props = {
            'score': 0,
            'status': 'good',
            'good_rubrics': [],
            'bad_rubrics': [],
        }

        for rubric_path in gradee_path.iterdir():
            try:
                with open(rubric_path) as rubric_file:
                    rubric = toml.load(rubric_file)
                grade_props['good_rubrics'].append((rubric_path.name,
                                                    score(rubric)))
            except (toml.TomlDecodeError, UnicodeDecodeError):
                grade_props['bad_rubrics'].append(rubric_path.name)

        if not grade_props['good_rubrics']:
            grade_props['status'] = 'bad'

        # TODO add in avg/median choice
        for _, rubric_score in grade_props['good_rubrics']:
            grade_props['score'] += rubric_score

        # Prevent div by 0
        grade_props['score'] /= len(grade_props['good_rubrics']) or 1
        grade_props['score'] = round(grade_props['score'], 2)

        assignment_grades[gradee_id] = grade_props

    with open(grade_file, 'w') as grades_csv_file:
        grade_writer = csv.writer(grades_csv_file, delimiter=',',
                                  quotechar='"', quoting=csv.QUOTE_ALL)
        grade_writer.writerow(('Username', bblearn_column_name))
        for username, grade_props in assignment_grades.items():
            if grade_props['status'] == 'good':
                grade_writer.writerow((username, grade_props['score']))
            else:
                print(f'Something went wrong with {username}\'s grade:')
                print(json.dumps(grade_props, indent=4) + '\n')


# Recursively walk the dictionaries in the rubric adding up the values of any
# keys named score
def score(rubric_part):
    if not isinstance(rubric_part, dict):
        return 0

    return (rubric_part.get('score', 0) +
            sum([score(subpart) for subpart in rubric_part.values()]))
