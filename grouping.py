import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json

# Json 파일 읽기
origin1 = pd.read_json('./m1_filter_realscore.json')
origin2 = pd.read_json('./m2_filter_realscore.json')
origin3 = pd.read_json('./m3_filter_realscore.json')

errata = pd.read_json('./1_문항정오답표.json')

print(type(origin1))
print(type(errata))
print(len(origin1))
print(len(origin2))
print(len(origin3))
print(len(errata))
print("=========================")
print("start separation", end="\n\n")

# 정오표 데이터 분류
m1 = {}
m2 = {}
m3 = {}
idx_1 = 0
idx_2 = 0
idx_3 = 0


def addRow(col_idx, group, data):
    if (group == 1):
        m1[col_idx] = data
    elif (group == 2):
        m2[col_idx] = data
    elif (group == 3):
        m3[col_idx] = data


for idx, row in errata.iterrows():

    if (row.answerCode == 1):
        profile = row.learnerProfile
        data = {"testID": row.testID, "assessmentItemID": row.assessmentItemID}

        if (profile == "F;S01;7" or profile == "M;S01;7"):
            addRow(idx_1, 1, data)
            idx_1 += 1

        elif (profile == "F;S01;8" or profile == "M;S01;8"):
            addRow(idx_2, 2, data)
            idx_2 += 1

        elif (profile == "F;S01;9" or profile == "M;S01;9"):
            addRow(idx_3, 3, data)
            idx_3 += 1

    if (idx % 50000 == 0):
        print(idx)
    elif (idx % 5000 == 0):
        print(".", end=" ")

print("====================================")
print(len(errata_m1))
print(len(errata_m2))
print(len(errata_m3))

errata_m1 = json.dumps(m1)
errata_m2 = json.dumps(m2)
errata_m3 = json.dumps(m3)

with open('errata_m1.txt', 'w') as outfile:
    outfile.write(errata_m1)
with open('errata_m2.txt', 'w') as outfile:
    outfile.write(errata_m2)
with open('errata_m3.txt', 'w') as outfile:
    outfile.write(errata_m3)