import click
import csv
from itertools import chain
import json
import toml
from pathlib import Path
from sys import exit

from divvy.assignment import Assignment


@click.command()
@click.argument('rubrics-dir')
@click.argument('bblearn-column-name')
@click.argument('grading-map')
@click.argument('exemplar-rubric')
@click.argument('output-file')
def synthesize(rubrics_dir, bblearn_column_name, grading_map, exemplar_rubric, output_file):
    """
    TODO
    """
    grading_attempts = Assignment.from_divvy_assignment_dir(rubrics_dir)
    gm = json.load(Path(grading_map).open())
    max_rubrics = len(list(gm.values())[0])
    exemplar_rubric = toml.load(exemplar_rubric)
    max_score = max_possible_score(exemplar_rubric)

    gradee_to_rubrics_map = {}
    for attempt in grading_attempts.latest_attempts:
        grader = attempt.submitted_by
        for gradee in gm[grader]:
            if not gradee_to_rubrics_map.get(gradee):
                gradee_to_rubrics_map[gradee] = []

            try:
                rubric_file = [
                    file for file in attempt.files
                    if '__gradee_' + gradee in file.name
                ][0]
            except IndexError:
                print(f"Grader {grader} did not submit a rubric for {gradee}")
                continue

            try:
                rubric_data = toml.loads(rubric_file.get_data().decode())
            except toml.TomlDecodeError:
                print(f"Bad rubric file {rubric_file.name} by {grader}")
                continue

            try:
                rubric_file.score = score(rubric_data, exemplar_rubric)
            except KeyError as e:
                print(f"Incomplete rubric {rubric_file.name} by {grader}")
                print(e)
                continue

            gradee_to_rubrics_map[gradee].append(rubric_file)

    print()
    print()
    print()

    assignment_grades = {}
    for gradee, rubrics in gradee_to_rubrics_map.items():
        if len(rubrics) == 0:
            print(f"No good rubrics for {gradee}!  Please review!")
            grade = ""
        else:
            m = sum([r.score for r in rubrics]) / len(rubrics)
            variance = sum([(r.score - m)**2 for r in rubrics]) / len(rubrics)
            std_dev = variance**0.5
            std_dev_grade_value = round((std_dev / max_score) * 100, 2)
            percent_grade = round((m / max_score) * 100, 2)

            if len(rubrics) < max_rubrics / 2 and percent_grade < 70:
                print(f"{gradee}: Only {len(rubrics)} good rubric(s)!  Please review!")
            elif std_dev_grade_value >= 15 and percent_grade < 70:
                print(f"{gradee}: Std. Dev. was whack {std_dev_grade_value}%!  Please review!")

            grade = round(m)

        assignment_grades[gradee] = grade

    output_file = Path(output_file)
    if output_file.exists():
        keep_only_best_scores(assignment_grades, bblearn_column_name, output_file)
        output_file.rename(output_file.parent / Path(f"old_{output_file.name}"))

    with output_file.open('w') as grades_csv_file:
        grade_writer = csv.writer(grades_csv_file, delimiter=',',
                                  quotechar='"', quoting=csv.QUOTE_ALL)
        grade_writer.writerow(('Username', bblearn_column_name))
        for username, grade in assignment_grades.items():
            grade_writer.writerow((username, grade))


# Recursively walk the dictionaries in the rubric adding up the values of any
# keys named score
def score(rubric_part, exemplar_part):
    if not isinstance(exemplar_part, dict):
        return 0

    exemplar_max_score = exemplar_part.get('max_score')
    if exemplar_max_score:
        return min(rubric_part['score'], exemplar_max_score)

    return sum([score(rubric_part[k], exemplar_part[k])
                for k in sorted(exemplar_part.keys())])


def max_possible_score(exemplar_part):
    if not isinstance(exemplar_part, dict):
        return 0

    return exemplar_part.get('max_score', 0) + sum([
        max_possible_score(next_part) for next_part in exemplar_part.values()
    ])


def keep_only_best_scores(usernames_and_scores, column_title, path):
    with open(path, newline="") as g:
        reader = csv.DictReader(g)
        for row in reader:
            username = row['Username']
            new_score = usernames_and_scores.get(username, 0)
            try:
                old_score = int(float(row[column_title]))
            except ValueError:
                old_score = 0
            if old_score > new_score:
                usernames_and_scores[username] = old_score
