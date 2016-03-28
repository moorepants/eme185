"""Constructs a single PDF from the report and the rubric that was generated
from Google Docs spreadsheet.

python merge_report_pdfs <directory>

"""

import os
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('directory')
args = parser.parse_args()

pdf_file_names = [f for f in os.listdir(args.directory) if f.endswith('.pdf')]

file_data = defaultdict(lambda: {'report': False, 'rubric': False,
                                 'graded': False})

for f in pdf_file_names:
    team_name, typ = os.path.splitext(f)[0].split('-')
    if typ in ['report', 'rubric', 'graded']:
        file_data[team_name][typ] = True

pathy = lambda x: os.path.join(args.directory, x)

# Remove any of the merged pdfs before creating a new one.
for team_name, typ_dict in file_data.items():
    graded_name = team_name + '-graded.pdf'
    if typ_dict['graded']:
        os.remove(pathy(graded_name))
        print('{} deleted.'.format(graded_name))

    if typ_dict['report'] and typ_dict['rubric']:
        os.system("pdftk {} {} cat output {}".format(
            pathy(team_name + '-rubric.pdf'), pathy(team_name + '-report.pdf'),
            pathy(graded_name)))
        print('{} created.'.format(graded_name))
