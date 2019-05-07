#!/usr/bin/env python

"""Script that parses CATME peer evaluation data and plots summary plots and
statistics.

The CATME Peer evaluation results are provided in a CSV file which contains
more than one table and mixed in metadata. The data are separated by double
line returns and are as follows:

1. Extraneous metadata
2. Table of answers to the per team member rating questions (it has two header
   lines)
3. An aggregation table of the data in part 2

The next optional sections are a list of a set of question answers followed by
a table of the responses to those questions. Here are the options for these
sets of questions that are tied to a score of 1, 2, 3, 4, or 5.

Team Conflict
=============

1. None or Not at all
2. Little or Rarely
3. Some
4. Much or Often
5. Very Much or Very Often

Team Satisfaction and Team Perspectives
=======================================

1. Strongly Disagree
2. Disagree
3. Neither Agree Nor Disagree
4. Agree
5. Strongly Agree

The final section are the private comments that the students provide.

"""

# TODO : Report which students are not filling out the peer eval.

import os
import textwrap
from io import StringIO

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import seaborn as sns


def load_main_table(table_text):
    """Returns a data frame with the peer to peer ratings for a single CATME
    peer evaluation given the text from the CSV export."""

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
    df = pd.read_csv(StringIO(text))
    df.index = df['Student ID']

    return df


def find_deliquent_students(df):
    """Returns a list of student names who did not fill out the survey."""

    def is_int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    deliquent_students = []

    for name, group in df.groupby('Team ID'):
        na_cols = group.columns[group.isna().any()].tolist()
        num_members = len(group)
        deliquent_rater_nums = set([int(name.strip()[-1]) for name in na_cols
                                    if is_int(name.strip()[-1])])
        deliquent_students += [group['Student Name'][group['Rater #'] == num].values[0]
                               for num in deliquent_rater_nums if num <= num_members]

    return deliquent_students


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

    data = data.dropna()  # if student drops and is deleted after peer eval

    # calculate a slope value, improvement metric, that characterizes whether
    # the students' ranking improved over time or didn't, positive values are
    # improvements and negative means the got rated worse over time

    x_vals = list(range(len(dataframes)))
    slopes = []
    means = []
    stds = []
    adjusted_scores = []

    eval_names = ['P1', 'P2', 'P3', 'P4']
    weights = [0.85, 0.90, 0.95, 1.0]

    for idx, row in data.iterrows():
        y_vals = row[eval_names[:len(dataframes)]].values.astype(float)

        # Weight the latter reviews more than the earlier reviews.
        mean = np.average(y_vals, weights=weights[:len(dataframes)])

        # Calculate a "slope" val that indicates how little or how much
        # improvement there was.
        opt, _ = curve_fit(lambda x, slope, intercept: slope * x + intercept,
                           x_vals, y_vals)
        improvement = opt[0]

        # If the student was rated low but improved over time, bump their
        # factor up based on the improvement. Also, don't allow any factor's
        # lower than 0.75.
        if mean < 0.95 and improvement > 0.0:
            adjusted_score = mean + 1.5 * improvement
        else:
            adjusted_score = max([0.75, mean])

        adjusted_score = mean

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
    """Returns three axes. The first is a bar plot of the adjustment factor for
    each student. The second is a bar plot showing the improvement value. And
    the third is a bar plot of the adjustment factor modified by the
    improvement score."""
    fig, axes = plt.subplots(3, sharex=True)
    df = df.sort_values('Final Adj Factor')
    df.plot(x='Student Name', y='Mean Adj Factor', kind='bar',
            yerr='STD Adj Factor', ylim=(0.6, 1.1), ax=axes[0])
    df.plot(x='Student Name', y='Improvement', kind='bar', ax=axes[1])
    df.plot(x='Student Name', y='Final Adj Factor', kind='bar',
            ylim=(0.75, 1.1), ax=axes[2])
    return axes


def load_catme_data_sections(path_to_file):
    """Returns a list of text sections from the CATME csv export."""

    with open(path_to_file, 'r') as f:
        text = f.read()

    sections = text.split('\n\n')

    return sections


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


def parse_team_questions(question_map_text, score_text):
    """Returns a data frame with each asked question in a row.

    Team Conflict
    =============

    Example text that maps an ID to the actual question::

       "T1","How much conflict of ideas is there in your work group? (Task Conflict)"
       "T2","How frequently do you have disagreements within your work group about the task of the project you are working on? (Task Conflict)"
       "T3","How often do people in your work group have conflicting opinions about the project you are working on? (Task Conflict)"
       "R1","How much relationship tension is there in your work group? (Relationship Conflict)"
       "R2","How often do people get angry while working in your group? (Relationship Conflict)"
       "R3","How much emotional conflict is there in your work group? (Relationship Conflict)"
       "P1","How often are there disagreements about who should do what in your work group? (Process Conflict)"
       "P2","How much conflict is there in your group about task responsibilities? (Process Conflict)"
       "P3","How often do you disagree about resource allocation in your work group? (Process Conflict)"

    This text is then followed by the scores for those questions::

       ,,,"Relationship Conflict",,,,,"Task Conflict",,,,,"Process Conflict",,,,,"Overall",,
       "Student Name","Student ID","Team ID","R1","R2","R3","Mn","SD","T1","T2","T3","Mn","SD","P1","P2","P3","Mn","SD","Mn","SD"
       "Surname01, Firstname01","12345","team01","1","1","1","1.00","0.00","1","1","1","1.00","0.00","1","1","1","1.00","0.00","1.00","0.00"
       "Surname02, Firstname02","12346","team01","2","1","1","1.33","0.58","3","2","3","2.67","0.58","2","3","2","2.33","0.58","2.11","0.78"
       "Surname03, Firstname03","12347","team01","1","1","1","1.00","0.00","2","1","1","1.33","0.58","1","1","1","1.00","0.00","1.11","0.33"
       "Surname04, Firstname04","12348","team01","1","1","1","1.00","0.00","2","2","2","2.00","0.00","2","2","1","1.67","0.58","1.56","0.53"

    Team Satisfaction
    =================

    "Q1","I am satisfied with my present teammates"
    "Q2","I am pleased with the way my teammates and I work together"
    "Q3","I am very satisfied with working in this team"

    ,,,"Team Satisfaction",,,,,
    "Student Name","Student ID","Team ID","Q1","Q2","Q3","Mn","SD"
    "Surname01, Firstname01","12345","team01","4","4","4","4.00","0.00"
    "Surname02, Firstname02","12346","team01","4","4","3","3.67","0.58"

    Team Perspectives
    =================

    "TA1","Being part of the team allows team members to do enjoyable work (Task Attraction)"
    "TA2","Team members get to participate in enjoyable activities (Task Attraction)"
    "TA3","Team members like the work that the group does (Task Attraction)"
    "IC1","Team members like each other (Interpersonal Cohesiveness)"
    "IC2","Team members get along well (Interpersonal Cohesiveness)"
    "IC3","Team members enjoy spending time together (Interpersonal Cohesiveness)"
    "TC1","Our team is united in trying to reach its goals for performance (Task Commitment)"
    "TC2","I'm unhappy with my team's level of commitment to the task (Task Commitment) [scale reversed]"
    "TC3","Our team members have conflicting aspirations for the team's performance (Task Commitment) [scale reversed]"

    ,,,"Interpersonal Cohesiveness",,,,,"Task Commitment",,,,,"Task Attraction",,,,,"Overall",,
    "Student Name","Student ID","Team ID","IC1","IC2","IC3","Mn","SD","TC1","TC2","TC3","Mn","SD","TA1","TA2","TA3","Mn","SD","Mn","SD"
    "Surname01, Firstname01","12345","team01","5","5","4","4.67","0.58","5","1","2","4.67","0.58","5","4","4","4.33","0.58","4.56","0.53"
    "Surname02, Firstname02","12346","team01","4","4","3","3.67","0.58","4","3","4","3.00","1.00","4","3","4","3.67","0.58","3.44","0.73"
    "Surname03, Firstname03","12347","team01","5","5","5","5.00","0.00","5","1","2","4.67","0.58","5","5","5","5.00","0.00","4.89","0.33"


    """

    # need to remove the first line because it is an extraneous header and any
    # lines with summary stats
    lines = [l for l in score_text.split('\n')[1:] if 'Team Stats' not in l]
    df = pd.read_csv(StringIO('\n'.join(lines)))

    # remove stats columns
    df = df.select(lambda x: not (x.startswith('Mn') or x.startswith('SD')),
                   axis=1)

    # transform to long format
    question_cols = [s for s in df.columns if s[-1].isdigit()]
    long_df = pd.melt(df, id_vars=['Student ID', 'Student Name', 'Team ID'],
                      value_vars=question_cols)

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

    # 2017
    DIR = '/home/moorepants/Drive/Teaching/EME185/2017/peer-evaluations'
    FNAME_TEMP = 'Moore-Peer_Evaluation_{}-EME_185-Winter_2017.csv'

    # 2018
    DIR = '/home/moorepants/Drive/Teaching/EME185/2018/peer-evaluations'
    FNAME_TEMP = 'Moore-2018_EME185_Peer_Evaluation_#{}-EME_185-Winter_2018.csv'

    # 2019
    DIR = '/home/moorepants/Drive/Teaching/EME185/2019/peer-evaluations'
    FNAME_TEMP = 'Moore-Peer_Evaluation_{}-EME_185-Winter_2019.csv'

    if not os.path.exists(os.path.join(DIR, 'charts')):
        os.makedirs(os.path.join(DIR, 'charts'))

    files = os.listdir(DIR)

    dfs = []
    team_ques_dfs = []

    # TODO : The range should adjust based on the number of files in the
    # directory.

    for i in range(3):

        path = os.path.join(DIR, FNAME_TEMP.format(i + 1))

        sections = load_catme_data_sections(path)

        dfs.append(load_main_table(sections[1]))

        conflict_df = parse_team_questions(sections[3], sections[4])
        conflict_df['Evaluation'] = i + 1
        conflict_df['Question Page'] = 'Team Conflict'

        satisfaction_df = parse_team_questions(sections[5], sections[6])
        satisfaction_df['Evaluation'] = i + 1
        satisfaction_df['Question Page'] = 'Team Satisfaction'

        perspectives_df = parse_team_questions(sections[7], sections[8])
        perspectives_df['Evaluation'] = i + 1
        perspectives_df['Question Page'] = 'Team Perspectives'

        team_ques_dfs.append(pd.concat([conflict_df, satisfaction_df,
                                        perspectives_df], ignore_index=True))

    team_questions_df = pd.concat(team_ques_dfs, ignore_index=True)
    team_questions_df['Question Group'] = team_questions_df['Question ID'].apply(lambda x: x[:-1])

    questions = team_questions_df[['Question ID', 'Question']].drop_duplicates()
    q_id_map = dict(zip(questions['Question ID'], questions['Question']))

    for i, df in enumerate(dfs):
        names = find_deliquent_students(df)
        print('Missing survey {}:'.format(i + 1))
        print(names)
        print('\n')

    for team_id in team_questions_df['Team ID'].unique():
        subset = team_questions_df[team_questions_df['Team ID'] == team_id]
        facet = sns.catplot(x='Question ID', y='Score', hue='Evaluation',
                            col='Question Page', data=subset, kind='bar',
                            ci='sd', sharey=False, sharex=False,
                            legend_out=False)
        facet.axes[0, 0].set_title(team_id + ': ' +
                                   facet.axes[0, 0].get_title(), fontsize=12)
        facet.axes[0, 0].set_ylim((0, 5))
        facet.axes[0, 0].set_yticks(range(6))
        facet.axes[0, 0].set_yticklabels(['',
                                          'None or Not\nat all',
                                          'Little or\nRarely',
                                          'Some',
                                          'Much or\nOften',
                                          'Very Much or\nVery Often'])
        facet.axes[0, 0].set_xlim((-0.5, 8.5))

        facet.axes[0, 1].set_title(team_id + ': ' +
                                   facet.axes[0, 1].get_title(), fontsize=12)
        facet.axes[0, 1].set_ylim((0, 5))
        facet.axes[0, 1].set_yticks(range(6))
        facet.axes[0, 1].set_yticklabels(['',
                                          'Strongly\nDisagree',
                                          'Disagree',
                                          'Neither Agree\nNor Disagree',
                                          'Agree',
                                          'Strongly\nAgree'])
        facet.axes[0, 1].set_xlim((8.5, 11.5))

        facet.axes[0, 2].set_title(team_id + ': ' +
                                   facet.axes[0, 2].get_title(), fontsize=12)
        facet.axes[0, 2].set_ylim((0, 5))
        facet.axes[0, 2].set_yticks(range(6))
        facet.axes[0, 2].set_yticklabels(['',
                                          'Strongly\nDisagree',
                                          'Disagree',
                                          'Neither Agree\nNor Disagree',
                                          'Agree',
                                          'Strongly\nAgree'])
        facet.axes[0, 2].set_xlim((11.5, 20.5))

        new_labs = ['\n'.join(textwrap.wrap(q_id_map[lab.get_text()], width=40))
                    for lab in facet.axes[0, 0].get_xticklabels()]
        facet.set_xticklabels(new_labs, rotation=-90)
        plt.gcf().set_size_inches(20.0, 10.0)
        plt.tight_layout()
        plt.savefig(os.path.join(DIR, 'charts', team_id + '.png'))
        plt.close()

    adj_fact_df = merge_adjustment_factor(*dfs)

    plot_student_adj(adj_fact_df)

    plt.gcf().set_size_inches(20.0, 15.0)
    plt.tight_layout()
    plt.savefig(os.path.join(DIR, 'charts', 'adjustment.png'))
