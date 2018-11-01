from Tkinter import *
import pandas
from pandas.plotting import scatter_matrix
import easygui
from images2gif import writeGif
from PIL import Image
import os
import csv
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn import metrics
import numpy as np
import pdb
import plotly.plotly as py
import plotly.graph_objs as go
top = Tk()
top.geometry("420x320")
top.wm_title("SMART FARMING")
top.configure(background="BLACK")
lst=[]
L2 = Label(top, text="TEMPERATURE :-",fg='white',bg='black')
L2.grid(row=0, column=0,padx=20,pady=(40,0))
L21 = Label(top, text="**",fg='white',bg='black')
L21.grid(row=0, column=1,padx=20,pady=(40,0))
#
L3 = Label(top, text="HUMIDITY :-",fg='white',bg='black')
L3.grid(row=1, column=0,padx=20,pady=(10,0))
L31 = Label(top, text="**",fg='white',bg='black')
L31.grid(row=1, column=1,padx=20,pady=(10,0))
#
L4 = Label(top, text="Rain Today ?",fg='white',bg='black')
L4.grid(row=2, column=0,padx=20,pady=(10,0))
E4 = Entry(top, bd = 5)
E4.grid(row=2, column=1,padx=20,pady=(10,0))
##
#L5 = Label(top, text="entry4")
#L5.grid(row=3, column=0,padx=20,pady=(10,0))
#E5 = Entry(top, bd = 5)
#E5.grid(row=3, column=1,padx=20,pady=(10,0))
##
#L6 = Label(top, text="entry5")
#L6.grid(row=4, column=0,padx=20,pady=(10,0))
#E6 = Entry(top, bd = 5)
#E6.grid(row=4, column=1,padx=20,pady=(10,0))
##
#L7 = Label(top, text="entry6")
#L7.grid(row=5, column=0,padx=20,pady=(10,0))
#E7 = Entry(top, bd = 5)
#E7.grid(row=5, column=1,padx=20,pady=(10,0))
##
#L8 = Label(top, text="entry7")
#L8.grid(row=6, column=0,padx=20,pady=(10,0))
#E8 = Entry(top, bd = 5)
#E8.grid(row=6, column=1,padx=20,pady=(10,0))
##
#L9 = Label(top, text="entry8")
#L9.grid(row=7, column=0,padx=20,pady=(10,0))
#E9 = Entry(top, bd = 5)
#E9.grid(row=7, column=1,padx=20,pady=(10,0))


#textPad = ScrolledText(top, width=50, height=40)
# textPad.pack()

########################################################################
#names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
print 'enter location 1 or 2'
if int(raw_input())==1:
    DATA_SET_PATH = "loc1.csv"
else:
    DATA_SET_PATH = "loc2.csv"

logistic_regression_model = LogisticRegression()
py.sign_in('premith', 'lR59CSvbi4TqZsyV8Uac')
def dataset_headers(dataset):
    """
    To get the dataset header names
    :param dataset: loaded dataset into pandas DataFrame
    :return: list of header names
    """
    return list(dataset.columns.values)
 
 
def unique_observations(dataset, header, method=1):
    """
    To get unique observations in the loaded pandas DataFrame column
    :param dataset:
    :param header:
    :param method: Method to perform the unique (default method=1 for pandas and method=0 for numpy )
    :return:
    """
    try:
        if method == 0:
            # With Numpy
            observations = np.unique(dataset[[header]])
        elif method == 1:
            # With Pandas
            observations = pd.unique(dataset[header].values.ravel())
        else:
            observations = None
            print "Wrong method type, Use 1 for pandas and 0 for numpy"
    except Exception as e:
        observations = None
        print "Error: {error_msg} /n Please check the inputs once..!".format(error_msg=e.message)
    return observations
 
 
def feature_target_frequency_relation(dataset, f_t_headers):
 
    """
    To get the frequency relation between targets and the unique feature observations
    :param dataset:
    :param f_t_headers: feature and target header
    :return: feature unique observations dictionary of frequency count dictionary
    """
 
    feature_unique_observations = unique_observations(dataset, f_t_headers[0])
    unique_targets = unique_observations(dataset, f_t_headers[1])
 
    frequencies = {}
    for feature in feature_unique_observations:
        frequencies[feature] = {unique_targets[0]: len(
            dataset[(dataset[f_t_headers[0]] == feature) & (dataset[f_t_headers[1]] == unique_targets[0])]),
            unique_targets[1]: len(
                dataset[(dataset[f_t_headers[0]] == feature) & (dataset[f_t_headers[1]] == unique_targets[1])])}
    return frequencies
 
 
def feature_target_histogram(feature_target_frequencies, feature_header):
    """
 
    :param feature_target_frequencies:
    :param feature_header:
    :return:
    """
    keys = feature_target_frequencies.keys()
    y0 = [feature_target_frequencies[key][0] for key in keys]
    y1 = [feature_target_frequencies[key][1] for key in keys]
 
    trace1 = go.Bar(
        x=keys,
        y=y0,
        name='no rain'
    )
    trace2 = go.Bar(
        x=keys,
        y=y1,
        name='rain'
    )
    data = [trace1, trace2]
    layout = go.Layout(
        barmode='group',
        title='Feature :: ' + feature_header + ' rain fall',
        xaxis=dict(title="Feature :: " + feature_header + " classes"),
        yaxis=dict(title="rain predict")
    )
    fig = go.Figure(data=data, layout=layout)
    # plot_url = py.plot(fig, filename=feature_header + ' - Target - Histogram')
    py.image.save_as(fig, filename=feature_header + '_Target_Histogram.png')
 
 
def train_logistic_regression(train_x, train_y):
    """
    Training logistic regression model with train dataset features(train_x) and target(train_y)
    :param train_x:
    :param train_y:
    :return:
    """
 
    
    logistic_regression_model.fit(train_x, train_y)
    return logistic_regression_model
 
 
def model_accuracy(trained_model, features, targets):
    """
    Get the accuracy score of the model
    :param trained_model:
    :param features:
    :param targets:
    :return:
    """
    accuracy_score = trained_model.score(features, targets)
    return accuracy_score
 
def main12():
    file_names = sorted((fn for fn in os.listdir('.') if fn.endswith('.png')))
    for hg in range(0,len(file_names)):
        #print file_names[hg]
        img = Image.open(str(file_names[hg]))
        img.show()
def predict():
    array = []
    array1=[]
    rn=E4.get()
    print rn
    qw=open('d1.txt')
    sd1=qw.read()
    f=sd1.split('\n')
    for line in f:
        if ('Temperature' in line):
            bsdk=line.split(':')
            array.append(float(bsdk[len(bsdk)-1]))
        if ('Humidity' in line):
            b1=line.split(':')
            array1.append(float(b1[len(b1)-1]))
    tmp=sum(array) / float(len(array))
    hum=sum(array1) / float(len(array1))
    L21.configure(text=str(tmp))
    L31.configure(text=str(hum))
    ######################################
    qs1=open('azxs.txt','r+')
    
    sd=qs1.read()
    qs1.close()
    #print sd
    #pu=[]
    lstk=sd.split(',')
    print lstk
    for i1 in range(0,len(lstk)-1):
        lstk[i1]=float(lstk[i1])
    #print fincoffx
    #print lstk
    sumi=0
    pr=[0,tmp,	0,	1.6	,hum,	1020,	1017.3	,1	,2	,int(rn)]
    #pr=[0,tmp,	0,	4	,59,	1026.1,	1022.7	,7	,7	,0]
    for ij in range(1,len(lstk)-1):
        #print pr[ij]
        sumi=sumi+(lstk[ij]*pr[ij])
    sumi=sumi+float(lstk[0])
    print sumi
    #sumi=1
    strf=''
    if sumi>-3.0:
        strf= "probability of rain is yes!"
    else:
        strf= "no rain !"
    L41.configure(text=strf ,font=("Courier", 10))
    print strf
    
    ##############################################
    
    
    
    
def main():
    """
    Logistic Regression classifier main
    :return:
    """
    # Load the data set for training and testing the logistic regression classifier
    dataset = pd.read_csv(DATA_SET_PATH)
    print "Number of Observations :: ", len(dataset)
    fincoff=[]
 
    # Get the first observation
    print dataset.head()
 
    headers = dataset_headers(dataset)
    #print "Data set headers :: {headers}".format(headers=headers)
 
    training_features = headers[0:len(headers)-1]
    print training_features
    target ='RainTomorrow'
 
    # Train , Test data split
    train_x, test_x, train_y, test_y = train_test_split(dataset[training_features], dataset[target], train_size=0.7)
    print "train_x size :: ", train_x.shape
    print "train_y size :: ", train_y.shape
 
    print "test_x size :: ", test_x.shape
    print "test_y size :: ", test_y.shape
 
    #print "edu_target_frequencies :: ", feature_target_frequency_relation(dataset, [training_features[3], target])
    
 
    for feature in training_features:
        feature_target_frequencies = feature_target_frequency_relation(dataset, [feature, target])
        ###################   must consider this  #########################
        #feature_target_histogram(feature_target_frequencies, feature)
 
    # Training Logistic regression model
    trained_logistic_regression_model = train_logistic_regression(train_x, train_y)
    #print trained_logistic_regression_model

    train_accuracy = model_accuracy(trained_logistic_regression_model, train_x, train_y)
 
    # Testing the logistic regression model
    test_accuracy = model_accuracy(trained_logistic_regression_model, test_x, test_y)
    fincoff.append(float(logistic_regression_model.intercept_[0]))
    for jk in range(0,len(logistic_regression_model.coef_[0])):
        fincoff.append(float(logistic_regression_model.coef_[0][jk]))
    
    print fincoff
    qas=open('azxs.txt','w+')
    asd=''
    qas.write(asd)
    for kj in range(0,len(fincoff)):
        #print type(fincoff[kj])
        qas.write(str(fincoff[kj])+',')
        #asd=asd+str(fincoff[kj])+" "
    #print asd
    #qas.write(asd)
    qas.close()
    
    #19,	0	,3.4,	76,	41,	1019.8,	1015.8,	6,	5,	0
    #16.8	,0,	2.8,	70,	53,	1018,	1013.8,	7	,7	,0
    #17.5,	0	,1.6,	81,	48,	1025.5,	1021.8,	1,	5,	0
    #18.5	,3.8,	2,	99,	50,	1026.6,	1023.1,	7,	4	,1
    
    
 
    print "Train Accuracy :: ", train_accuracy
    print "Test Accuracy :: ", test_accuracy
    #easygui.msgbox(strf, title="simple gui")
 
#if __name__ == "__main__":
#    main()
DB1=Button(top, text="RUN ML", width=20,command=main,bg='cyan')
DB1.grid(row=8, column=1,padx=20,pady=10)
DB2=Button(top, text="SHOW DATA ANALYSIS", width=20,command=main12,bg='cyan')
DB2.grid(row=9, column=1,padx=20,pady=10)
DB3=Button(top, text="GET DATA/PREDICT NOW", width=20,command=predict,bg='cyan')
DB3.grid(row=10, column=1,padx=20,pady=10)
L41 = Label(top, text="----",fg='white',bg='black')
L41.grid(row=11, column=1,padx=20,pady=(10,0))
top.mainloop()