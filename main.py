import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#Json 파일 읽기
origin = pd.read_json('./resource/3_candidateIRT.json')

print(len(origin))
print("=========================")
print("start separation", end="\n\n")

#학년별 dataframe 만들기
m1 = pd.DataFrame(columns=['learnerID', 'learnerProfile', 'testID', 'theta', 'realScore', 'TimeStamp'])
m2 = pd.DataFrame(columns=['learnerID', 'learnerProfile', 'testID', 'theta', 'realScore', 'TimeStamp'])
m3 = pd.DataFrame(columns=['learnerID', 'learnerProfile', 'testID', 'theta', 'realScore', 'TimeStamp'])

for idx, row in origin.iterrows():

    profile = row.learnerProfile
    if(profile == "F;S01;7" or profile == "M;S01;7"):
        m1 = m1.append(row, ignore_index=True)
    elif(profile == "F;S01;8" or profile == "M;S01;8"):
        m2 = m2.append(row, ignore_index=True)
    elif(profile == "F;S01;9" or profile == "M;S01;9"):
        m3 = m3.append(row, ignore_index=True)

    if (idx % 300 == 0):
        print(idx)
    elif (idx % 10 == 0):
        print(".", end='')



print("=========================")
#print(m1)
#print(m2)
#print(m3)


#각 학년별 진점수, 이해력 그래프 그리기
matplotlib.rcParams['axes.unicode_minus'] = False

#이해력 시각화
plt.hist(m1['theta'], bins=20)
plt.xlabel("theta")
plt.ylabel("count")

plt.grid()
plt.show()

#진점수 시각화

plt.hist(m1['realScore'], bins=20)
plt.xlabel("realScore")
plt.ylabel("count")

plt.grid()
plt.show()
