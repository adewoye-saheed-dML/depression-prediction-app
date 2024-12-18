
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.metrics import mutual_info_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score, precision_score, recall_score
from sklearn.metrics import roc_curve

from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import GridSearchCV

import warnings

warnings.filterwarnings('ignore')


df = pd.read_csv('C:/Users/WOYES/Downloads/students.csv')


# make the column names and values look uniform

df.columns = df.columns.str.lower().str.replace(' ','_')

cat_columns = list(df.dtypes[df.dtypes=='object'].index)

for c in cat_columns:
    df[c] = df[c].str.lower().str.replace(' ','_')

# recheck the dataset
df.head()


#  drop unnecessary column
df.drop(columns=['id'], inplace = True)


#  drop the missing values
df.dropna(subset= ['financial_stress'], inplace = True)


others = df[df['sleep_duration']=='others'].index
df.drop(others, inplace = True )


cat_map = {'5-6_hours': 0, 
           'less_than_5_hours':1,
           '7-8_hours':2,
           'more_than_8_hours':3
    }

df['sleep_duration'] = df['sleep_duration'].map(cat_map)

 
# We should remove least correlated feature from our dataset to optimize our model performance. Features like `work_pressure`, `job_satisfaction`, `gender`, `profession`, `family_history_of_mental_illness`, and `city` are less important to the response variable (`depression`)


df.drop(columns = ['work_pressure', 'job_satisfaction', 'gender','profession','family_history_of_mental_illness','city'], inplace=True)
df.head()


student= {'age':33.0, 'academic_pressure':5.0, 'cgpa':8.97, 'study_satisfaction':2.0, 'sleep_duration':0, 'dietary_habits':'healthy', 'degree':'b.pharm', 'have_you_ever_had_suicidal_thoughts_?':'yes', 'work/study_hours':3.0, 'financial_stress':1.0}


df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)

y_test = df_test.depression.values


# new numerical and categorical features 
num = ['age', 'academic_pressure', 'cgpa',
       'study_satisfaction','sleep_duration',
       'work/study_hours', 'financial_stress']

cat = ['dietary_habits', 'degree', 'have_you_ever_had_suicidal_thoughts_?']


def train(df_train, y_train, C=0.1):
    dicts = df_train[cat+num].to_dict(orient='records')

    dv = DictVectorizer(sparse = False)
    
    # fit and transform the dictionary vectorizer
    X_train = dv.fit_transform(dicts)

    model = LogisticRegression(C=0.1, solver='lbfgs', max_iter=1000) 
    model.fit(X_train, y_train) 

    return dv, model


def predict(df, dv, model):
    dicts = df[cat+num].to_dict(orient='records')
    
    # fit and transform the dictionary vectorizer
    X = dv.transform(dicts)

    y_pred = model.predict_proba(X)[:,1] 

    return y_pred


dv, model = train(df_full_train,df_full_train.depression.values, C=0.1)
y_pred = predict(df_test,dv, model)

auc =roc_auc_score(y_test,y_pred)
auc


import pickle


output_file = 'student.pkl'


with open(output_file,'wb') as f_out:
    pickle.dump((dv, model), f_out)


