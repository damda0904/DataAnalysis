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
        data = {"learnerID": row.learnerID, "testID": row.testID, "assessmentItemID": row.assessmentItemID}

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

errata_m1 = json.dumps(m1)
errata_m2 = json.dumps(m2)
errata_m3 = json.dumps(m3)

print("====================================")
print(len(m1))
print(len(m2))
print(len(m3))

with open('each_errata_m1.txt', 'w') as outfile:
    outfile.write(errata_m1)
with open('each_errata_m2.txt', 'w') as outfile:
    outfile.write(errata_m2)
with open('each_errata_m3.txt', 'w') as outfile:
    outfile.write(errata_m3)

from ast import literal_eval

# 필터링된 문항 데이터셋과 비교해서
# 해당되는 맞은 문항을 학생별로 묶어서 저장

# 학생별로 맞은 문항을 묶을 딕셔너리
# 딕셔너리는 학년별로 구분
s1 = {}
s2 = {}
s3 = {}

# 문항 데이터셋을 위한 딕셔너리
q1 = {}
q2 = {}
q3 = {}

# Json 파일 읽기
question1 = literal_eval(open('./m1_filter_guessLevel.txt', 'r').readline())
question2 = literal_eval(open('./m2_filter_guessLevel.txt', 'r').readline())
question3 = literal_eval(open('./m3_filter_guessLevel.txt', 'r').readline())

# 각 문항 데이터셋을 딕셔너리로 전처리
for row in question1:
    q1[row['assessmentItemID']] = json.dumps(row)
for row in question2:
    q2[row['assessmentItemID']] = json.dumps(row)
for row in question3:
    q3[row['assessmentItemID']] = json.dumps(row)

print(len(q1))
print(len(q2))
print(len(q3))
print("====================================")
print("start grouping")

# 필터링 및 그룹핑
for key, value in m1.items():
    learner = value['learnerID']
    assessmentItem = value['assessmentItemID']

    # 문항 데이터셋에 들어있는 문항이 아닐 경우
    if (not (assessmentItem in q1)):
        continue

    if (learner in s1):
        tmp = s1[learner]
        tmp.add(assessmentItem)
        s1[learner] = tmp
    else:
        tmp = set()
        tmp.add(assessmentItem)
        s1[learner] = tmp

for key, value in m2.items():
    learner = value['learnerID']
    assessmentItem = value['assessmentItemID']

    # 문항 데이터셋에 들어있는 문항이 아닐 경우
    if (not (assessmentItem in q2)):
        continue

    if (learner in s2):
        tmp = s2[learner]
        tmp.add(assessmentItem)
        s2[learner] = tmp
    else:
        tmp = set()
        tmp.add(assessmentItem)
        s2[learner] = tmp

for key, value in m3.items():
    learner = value['learnerID']
    assessmentItem = value['assessmentItemID']

    # 문항 데이터셋에 들어있는 문항이 아닐 경우
    if (not (assessmentItem in q3)):
        continue

    if (learner in s3):
        tmp = s3[learner]
        tmp.add(assessmentItem)
        s1[learner] = tmp
    else:
        tmp = set()
        tmp.add(assessmentItem)
        s3[learner] = tmp

print("")
print("====================================")
print(len(s1))
print(len(s2))
print(len(s3))

for key, value in s1.items():
    tmp = list(value)
    s1[key] = tmp

for key, value in s2.items():
    tmp = list(value)
    s2[key] = tmp

for key, value in s3.items():
    tmp = list(value)
    s3[key] = tmp

s1_assessmentItemSet = json.dumps(s1)
s2_assessmentItemSet = json.dumps(s2)
s3_assessmentItemSet = json.dumps(s3)

with open('studentGroup_m1.txt', 'w') as outfile:
    outfile.write(s1_assessmentItemSet)
with open('studentGroup_m2.txt', 'w') as outfile:
    outfile.write(s2_assessmentItemSet)
with open('studentGroup_m3.txt', 'w') as outfile:
    outfile.write(s3_assessmentItemSet)