"""Constructs a single PDF from the report and the rubric that was generated
from Google Docs spreadsheet."""

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('directory')
args = parser.parse_args()

files = [f for f in os.listdir(args.directory) if f.endswith('.pdf')]
graded = [f for f in files if f.endswith('graded.pdf')]

pathy = lambda x: os.path.join(args.directory, x)

for f in graded:
    os.remove(pathy(f))

files = [f for f in os.listdir(args.directory) if f.endswith('.pdf')]
rubrics = sorted([f for f in files if f.endswith('rubric.pdf')])
reports = sorted(list(set(files).difference(rubrics)))

for report, rubric in zip(reports, rubrics):
    name = os.path.splitext(report)[0] + '-graded.pdf'
    print(name)
    os.system("pdftk {} {} cat output {}".format(pathy(rubric), pathy(report),
                                                 pathy(name)))
