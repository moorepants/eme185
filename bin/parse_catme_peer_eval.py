"""The CATME Peer evaluation results are provided in a non-standard CSV file.
There are multiple tables in the single file. The tables are separated by
double line returns and are as follows:

1. Extraneous metadata
2. Table of answers to the per team member rating questions (it has two header lines)
3. An aggregation table of the data in part 2

The next optional sections are a list of a set of question answers followed by
a table of the responses to those questions.

The final section are the private comments that the students provide.

"""

import os
import argparse
from io import StringIO

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

team_id_map = {
    "APB9": "Biodesiel Sclerosis Treatment",
    "APS1": "Self-tending chicken coop",
    "APS3": "Solar compost sterilizer",
    "APU6": "Urban greenhouse office shed",
    "BDD1": "Design of a Grape Roomba",
    "CFO6": "Optimal mountain bike rim design",
    "CNA7": "Adaptive target for jumping studies",
    "CWH0": "Floating Toilets: To Boldy 'Go' Where Noone has Been Able to Go Before",
    "DDL5": "Laparoscopic Field Hydraulic Surgery Table (Burro chute)",
    "DUM0": "Mobile microscope stand for wheelchair-bound students",
    "EDR4": "Recycler's Transportation Cart",
    "FMA5": "Automatic board feeder for custom saw/drill station",
    "FTC1": "Crimping device for refitting broken shovel heads",
    "FTR2": "Repurposing discarded 5 gallon vegetable oil jugs into nursery pots",
    "FUA7": "Automated native plant plug planting",
    "FUP6": "Pond Algae Removal",
    "GIS8": "Sports instrument inertial estimation device",
    "GSP6": "Pyrotechnic Actuator Installation Robot",
    "HWO8": "Low Cost DIY Powered Wheelchair",
    "JII6": "Instrumented Bicycle for Collision Reconstruction",
    "KM32": "3D Printing Micro-UAVs",
    "LLD5": "Design of Additively Manufactured (AM) Embedded Sensors for Structural Health Monitoring",
    "LLG6": "GUI or APP for Data Fitting of Constitutive Models",
    "LLP3": "Pressure sensor design development",
    "LMD2": "Design of a water table",
    "LPM7": "Portable Pasture Fencing",
    "LUR1": "Robotic Scarecrow",
    "MBD3": "Line Launcher",
    "MDA2": "Save the Bees through Engineering",
    "MDL2": "Instrumentation to Measure Equine Tail Pull Forces",
    "MDL9": "Large Animal Venipuncture Training Models"
}


def question_map(text):
    question_map = {}
    for q in text.split('\n')[1:]:
        key, question = q.split('","')
        question_map[key[1:]] = question[:-1]
    return question_map


def parse_answer_section(text, q_map):
    new_text = ''
    for line in text.split('\n')[1:]:
        if not line.startswith('"Team Stats'):
            new_text += line + '\n'
    df = pd.read_csv(StringIO(new_text))
    df = df.rename(columns=q_map)
    df = df.select(lambda x: not x.startswith('Mn') and not x.startswith('SD'), axis=1)
    df['Team Name'] = df['Team ID'].map(team_id_map)
    return df


def print_sorted(df, ascending=True):
    group = df.groupby('Team Name')
    results = group.mean()
    for col in results.columns:
        print(results[col].sort_values(ascending=ascending))
        print('\n\n')


def load_main_table(table_text):

    lines = table_text.split('\n')
    i = 1
    cols = []
    for thing in lines[1].split('","'):
        if thing in ['C ', 'I ', 'K ', 'E ', 'H ']:
            cols.append(thing.strip() + str(i) + ' ')
            if thing == 'H ':
                i += 1
        else:
            cols.append(thing)
    lines[1] = '","'.join(cols)
    text = "\n".join(lines[1:])
    #dtype = {'Student Name': str,
             #'Team ID': str,
             #'Note': str}
    df = pd.read_csv(StringIO(text)) #, dtype=dtype)
    # may have been needed in previous pandas versions
    #df['Student ID'] = df['Student ID'].str.split('-').str.join('')
    df.index = df['Student ID']

    return df


def merge_adjustment_factor(*dataframes, with_self=True):
    """Returns a data frame with student id as the index and the peer
    evaluation instances as the columns. The entry is the adjustment factor
    value. A numerical value is also computed in the column 'Improvement' that
    shows whether they were ranked higher or lower as time progressed."""

    if with_self:
        col = 'Adj Factor (w/ Self)'
    else:
        col = 'Adj Factor (w/o Self)'

    data = {}

    for i, df in enumerate(dataframes):
        data['P{}'.format(i + 1)] = df[col]

    data['Student Name'] = df['Student Name']

    data = pd.DataFrame(data)

    # calculate a slope value, improvement metric, that characterizes whether
    # the students' ranking improved over time or didn't, positive values are
    # improvements and negative means the got rated worse over time

    x_vals = range(4)
    slopes = []
    means = []
    stds = []
    adjusted_scores = []

    for idx, row in data.iterrows():
        y_vals = row[['P1', 'P2', 'P3', 'P4']].values.astype(float)

        # Weight the latter reviews more than the earlier reviews.
        mean = np.average(y_vals, weights=[0.85, 0.90, 0.95, 1.0])

        # Calculate a "slope" val that indicates how little or how much
        # improvement there was.
        opt, _ = curve_fit(lambda x, slope, intercept: slope * x + intercept,
                           x_vals, y_vals)
        improvement = opt[0]

        # If the student was rated low but improved over time, bump their
        # factor up based on the improvement. Also, don't allow any factor's
        # lower than 0.80.
        if mean < 0.95 and improvement > 0.0:
            adjusted_score = mean + 1.5 * improvement
        else:
            adjusted_score = max([0.80, mean])

        means.append(mean)
        stds.append(y_vals.std())
        slopes.append(improvement)
        adjusted_scores.append(adjusted_score)

    data['Improvement'] = slopes
    data['Mean Adj Factor'] = means
    data['STD Adj Factor'] = stds
    data['Final Adj Factor'] = adjusted_scores

    return data


def plot_student_adj(df, with_self=True):
    fig, axes = plt.subplots(3, sharex=True)
    df = df.sort_values('Final Adj Factor')
    df.plot(x='Student Name', y='Mean Adj Factor', kind='bar',
            yerr='STD Adj Factor', ylim=(0.6, 1.1), ax=axes[0])
    df.plot(x='Student Name', y='Improvement', kind='bar', ax=axes[1])
    df.plot(x='Student Name', y='Final Adj Factor', kind='bar',
            ylim=(0.75, 1.1), ax=axes[2])
    return axes


def load_catme_data_sections(path_to_file):

    with open(path_to_file, 'r') as f:
        text = f.read()

    sections = text.split('\n\n')

    return sections


def parse_catme_text(text_sections):

    metadata = pd.read_csv(StringIO(text_sections[0])).to_dict('records')[0]

    return


def create_team_factor(df):
    # TODO : What to do about note="over"
    df['Team Factor'] = df['Adj Factor (w/ Self)']
    unders = df['Note'] == 'Under'
    df['Team Factor'][unders] = df['Adj Factor (w/o Self)'][unders]
    df['Team Factor'][df['Team Factor'] > 1.05] = 1.05
    df['Team Factor'][(df['Team Factor'] >= 0.95) & (df['Team Factor'] < 1.0)] = 1.0
    if 'Manip' in df['Note']:
        df['Team Factor'][df['Team ID'] == df.loc[df['Note'] == 'Manip']['Team ID'].values[0]] = 1.0
    return df


def parse_conflict_text(question_map_text, score_text):

    # need to remove the first line because it is an extraneous header
    df = pd.read_csv(StringIO('\n'.join(score_text.split('\n')[1:])))

    # remove stats columns
    df = df.select(lambda x: not (x.startswith('Mn') or x.startswith('SD')),
                   axis=1)
    # remove rows with summary stats
    df = df[df['Student Name'] != 'Team Stats']

    # transform to long format
    long_df = pd.melt(df, id_vars=['Student ID', 'Student Name', 'Team ID'],
                      value_vars=['R1', 'R2', 'R3', 'T1', 'T2', 'T3', 'P1',
                                  'P2', 'P3'])

    long_df.index = long_df['Student ID'].astype(int)
    del long_df['Student ID']

    long_df = long_df.rename(columns={'variable': 'Question ID',
                                      "value": 'Score'})

    question_map = {}

    for line in question_map_text.split('\n')[1:]:
        code, question = line.split(',')
        question_map[code[1:-1]] = question.split(' (')[0][1:]

    long_df['Question'] = long_df['Question ID']

    long_df.replace({'Question': question_map}, inplace=True)

    return long_df

if __name__ == "__main__":

    #parser = argparse.ArgumentParser()
    #parser.add_argument('file')
    #args = parser.parse_args()
#
    #path = '/home/moorepants/Teaching/eme185'
#
    #file1 = 'Moore-EME_185A_Peer_Evaluation-EME_185-Winter_2016.csv'
    #file2 = 'Moore-Final_Peer_Evaluation-EME_185-Winter_2016.csv'
    #file3 = 'Moore-Spring_Midterm_Peer_Evaluation-EME_185-Winter_2016.csv'
#
    #sections1 = load_catme_data_sections(os.path.join(path, file1))
    #sections2 = load_catme_data_sections(os.path.join(path, file2))
    #sections3 = load_catme_data_sections(os.path.join(path, file3))
#
    #df1 = load_main_table(sections1[1])
    #df2 = load_main_table(sections2[1])
    #df3 = load_main_table(sections3[1])
#
    #df1 = create_team_factor(df1)
    #df2 = create_team_factor(df2)
    #df3 = create_team_factor(df3)
#
    #df = df3[['Student Name', 'Student ID', 'Team Factor']].copy()
    #df['Team Factor'] = (df1['Team Factor'] + df2['Team Factor'] + df3['Team Factor']) / 3
#
    #df[['Student ID', 'Team Factor']].to_csv('team_factor.csv')

    # Parse extra questions
    #q_map = question_map(sections[3])
    #conflict_df = parse_answer_section(sections[4], q_map)
    #print_sorted(conflict_df, False)
#
    #q_map = question_map(sections[5])
    #satis_df = parse_answer_section(sections[6], q_map)
    #print_sorted(satis_df, False)
#
    #q_map = question_map(sections[7])
    #satis_df = parse_answer_section(sections[8], q_map)
    #print_sorted(satis_df, False)

    path = '/home/moorepants/Drive/EME185/2017/peer-evaluations/Moore-Peer_Evaluation_{}-EME_185-Winter_2017.csv'
    dfs = []
    conflict_dfs = []

    for i in range(4):
        sections = load_catme_data_sections(path.format(i + 1))
        dfs.append(load_main_table(sections[1]))
        conflict_dfs.append(parse_conflict_text(sections[3], sections[4]))

    adj_fact_df = merge_adjustment_factor(*dfs)

    plot_student_adj(adj_fact_df)
