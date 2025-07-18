import datetime
from statistics import stdev
from tqdm import tqdm

import warnings
warnings.filterwarnings('ignore')

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, auc, classification_report,
                             confusion_matrix, precision_recall_curve,
                             roc_auc_score, roc_curve)
from sklearn.model_selection import (GridSearchCV, RepeatedStratifiedKFold,
                                     cross_val_score, train_test_split)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

df = pd.read_csv("/content/drive/MyDrive/WA_Fn-UseC_-HR-Employee-Attrition.csv")

df

df.shape

df.info

df.isnull()

df.isnull().sum()

df.head()

df.describe()

import pandas as pd
import matplotlib.pyplot as plt
plt.figure(figsize=(8,6))
x=df["DailyRate"]
y=df["Attrition"]
plt.bar(x,y)
plt.show()

import matplotlib.pyplot as plt

# Sample data
x=df["DailyRate"]
y=df["Attrition"]


# Create lollipop chart
plt.stem(x,y,markerfmt='o', linefmt='k-', basefmt=' ')

# Add title and labels
plt.title('Lollipop Chart Example')
plt.xlabel('Categories')
plt.ylabel('Values')

# Display the plot
plt.show()

plt.figure(figsize=(8, 6))
sns.violinplot(x='DailyRate', y='Attrition', data=df)
plt.title('DailyRate vs Attrition')
plt.xlabel('DailyRate')
plt.ylabel('Attirtion')
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(x='MonthlyIncome', y='Attrition', data=df)
plt.title('Income vs Attrition')
plt.xlabel('MonthlyIncome')
plt.ylabel('Attirtion')
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(x='HourlyRate', y='Attrition', data=df)
plt.title('HourlyRate vs Attrition')
plt.xlabel('HourlyRate')
plt.ylabel('Attirtion')
plt.show()

num_cols = ['Age', 'DistanceFromHome','MonthlyIncome','NumCompaniesWorked', 'PercentSalaryHike',
       'TotalWorkingYears', 'TrainingTimesLastYear',
       'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion',
       'YearsWithCurrManager']

for col in num_cols:
    plt.figure(figsize=(12,6))
    sns.violinplot(x=col, hue='Attrition', data=df)
    plt.title("Attrition distrition by " + col)
    plt.show()

df['Attrition'].value_counts()

df['MaritalStatus'].value_counts().plot(kind = 'pie' , autopct = "%1.1f%%")
plt.show()

df['MonthlyIncome'].value_counts().plot(kind = 'pie' , autopct = "%1.1f%%")
plt.show()

df.groupby('Attrition').EducationField.value_counts().plot(kind = "pie",autopct = "%1.1f%%")
plt.show()

fact_cols=["Gender","DistanceFromeHome","OverTime","JobRole"]

df.groupby('Attrition').OverTime.value_counts().plot(kind = "pie",autopct = "%1.1f%%")
plt.show()

df.groupby('Attrition').JobRole.value_counts().plot(kind = "pie",autopct = "%1.1f%%")
plt.show()

df.groupby('Attrition').Over18.value_counts().plot(kind = "pie",autopct = "%1.1f%%")
plt.show()

"""DATA TRANSFORMATION"""

df['Over18'].value_counts()

df['BusinessTravel'].value_counts()

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()

df['EducationField'] = encoder.fit_transform(df['EducationField'])

df['Gender'] = encoder.fit_transform(df['Gender'])

df['JobRole'] = encoder.fit_transform(df['JobRole'])

df['MaritalStatus'] = encoder.fit_transform(df['MaritalStatus'])

df['OverTime'] = encoder.fit_transform(df['OverTime'])

df.info()

from sklearn.preprocessing import MinMaxScaler

df.head()

obj=df.select_dtypes('object')
num=df.select_dtypes(['int64','float64'])

obj.head()

num.head()

obj=pd.get_dummies(obj,drop_first=True)
obj.head()

d=num.corr()
plt.figure(figsize=(15,10))
sns.heatmap(d[(d>0.2) | (d<-0.2)],annot=True)

mm=MinMaxScaler()
numScale=mm.fit_transform(num)
num=pd.DataFrame(numScale,columns=num.columns)
num.head()

final = pd.concat([obj.reset_index(drop=True),num.reset_index(drop=True)], axis=1)
final.head()

"""MODEL TRAINING"""

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import RandomOverSampler,SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.preprocessing import StandardScaler
import xgboost as xgb

x=final.drop(['Attrition_Yes'],axis=1)
y=final['Attrition_Yes']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
sns.kdeplot(y_train)

x=final.drop(['Attrition_Yes'],axis=1)
y=final['Attrition_Yes']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
sns.catplot(y_train)

from sklearn.metrics import accuracy_score
p = model.predict(x_test)
print(accuracy_score(y_test,p))

from sklearn.metrics import accuracy_score
models = {
    "Logistic regression":LogisticRegression(),
    "Tree ":DecisionTreeClassifier(),
    "Ensambled":RandomForestClassifier(),
    "xg":xgb.XGBClassifier(),
    'SVC':SVC(),
    'KNN':KNeighborsClassifier(),
}
for name,model in models.items():
    model.fit(x_train,y_train)
    p = model.predict(x_test)
    print("Model: " , name)
    print("Model:",accuracy_score(y_test,p))

"""The above models have accuracy score more than 85% except Decision Tree classifier"""

print("CONCLUSION:")
print("The employee attrition due to various factors have been visualized and analysed")
print("The prediction of attrition with various machine learning algorithms have been demonstrated and founded")
print("The accuracy score of prediction through machine learning algorithms have been predicted")

print("Project by:")
print("1.JayaPrakash.K")
print("2.Vijay.S")
print("3.Manish.P")
print("4.SanthoshKumar.M")

print("THANK YOU")

