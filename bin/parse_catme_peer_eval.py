import os
import argparse
from io import StringIO

import pandas as pd

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
    df = pd.read_csv(StringIO(text))
    df['Student ID'] = df['Student ID'].str.split('-').str.join('')
    df.index = df['Student ID']

    return df


def load_catme_data_sections(path_to_file):

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


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    path = '/home/moorepants/Teaching/eme185'

    file1 = 'Moore-EME_185A_Peer_Evaluation-EME_185-Winter_2016.csv'
    file2 = 'Moore-Final_Peer_Evaluation-EME_185-Winter_2016.csv'
    file3 = 'Moore-Spring_Midterm_Peer_Evaluation-EME_185-Winter_2016.csv'

    sections1 = load_catme_data_sections(os.path.join(path, file1))
    sections2 = load_catme_data_sections(os.path.join(path, file2))
    sections3 = load_catme_data_sections(os.path.join(path, file3))

    df1 = load_main_table(sections1[1])
    df2 = load_main_table(sections2[1])
    df3 = load_main_table(sections3[1])

    df1 = create_team_factor(df1)
    df2 = create_team_factor(df2)
    df3 = create_team_factor(df3)

    df = df3[['Student Name', 'Student ID', 'Team Factor']].copy()
    df['Team Factor'] = (df1['Team Factor'] + df2['Team Factor'] + df3['Team Factor']) / 3

    df[['Student ID', 'Team Factor']].to_csv('team_factor.csv')

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
