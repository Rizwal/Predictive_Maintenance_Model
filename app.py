import streamlit as st
import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

data=pickle.load(open('data.pkl','rb'))
model=pickle.load(open('model.pkl','rb'))

st.set_page_config(page_title="MyApp")
tab_titles=[
    'Description',
    'Predict',
    'EDA',
    'Perdormance Measures'
]

tabs=st.tabs(tab_titles)
with tabs[0]:
    st.title("PREDICTIVE MAINTAINENCE")
    st.write('Predictive maintenance is a technique that uses data analysis tools and techniques to detect anomalies in your operation and possible defects in equipment and processes so you can fix them before they result in failure')
    st.title("DATASET INFORMATION")
    st.write('The dataset consists of 10 000 data points stored as rows with 14 features in columns')   
    st.write('UID: unique identifier ranging from 1 to 10000') 
    st.write('product ID: consisting of a letter L, M, or H for low (50% of all products), medium (30%) and high (20%) as product quality variants and a variant-specific serial number')
    st.write('air temperature [K]: generated using a random walk process later normalized to a standard deviation of 2 K around 300 K process temperature [K]: generated using a random walk process normalized to a standard deviation of 1 K, added to the air temperature plus 10 K.')
    st.write('rotational speed [rpm]: calculated from a power of 2860 W, overlaid with a normally distributed noise torque [Nm]: torque values are normally distributed around 40 Nm with a Ïƒ = 10 Nm and no negative values. ')
    st.write('tool wear [min]: The quality variants H/M/L add 5/3/2 minutes of tool wear to the used tool in the process. and a ''machine failure'' label that indicates, whether the machine has failed in this particular datapoint for any of the following failure modes are true.')
    
    st.title('MACHINE FAILURE TYPES')
    st.write('Tool wear failure (TWF): the tool will be replaced of fail at a randomly selected tool wear time between 200 â€“ 240 mins (120 times in our dataset). At this point in time, the tool is replaced 69 times, and fails 51 times (randomly assigned).')
    st.write('Heat dissipation failure (HDF): heat dissipation causes a process failure, if the difference between air- and process temperature is below 8.6 K and the toolâ€™s rotational speed is below 1380 rpm. This is the case for 115 data points.')
    st.write('Power failure (PWF): the product of torque and rotational speed (in rad/s) equals the power required for the process. If this power is below 3500 W or above 9000 W, the process fails, which is the case 95 times in our dataset.')
    st.write('Overstrain failure (OSF): if the product of tool wear and torque exceeds 11,000 minNm for the L product variant (12,000 M, 13,000 H), the process fails due to overstrain. This is true for 98 datapoints.')
    st.write('Random failures (RNF): each process has a chance of 0,1 % to fail regardless of its process parameters. This is the case for only 5 datapoints, less than could be expected for 10,000 datapoints in our dataset.')
    
with tabs[1]:
    def prediction(airtemp,proctemp,rotspeed,torque,toolwear,Type_H,Type_L,Type_M):
        datatopred=pd.DataFrame({
            'Air temperature [K]': airtemp,
            'Process temperature [K]': proctemp,
            'Rotational speed [rpm]': rotspeed,
            'Torque [Nm]': torque,
            'Tool wear [min]': toolwear,
            'Type_H': Type_H,
            'Type_L': Type_L,
            'Type_M': Type_M

        },index=[0])
        pred=model.predict(datatopred)
        print(pred)
        return pred

    st.title("Predictive Maintainence")
        
    html_temp = """
    <div style="background-color:blue;padding:2px">
    <h2 style="color:white;text-align:center;font-size:20px">Write the value of given points</h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)   

    airtemp=st.number_input("Enter Air Temperature in K",key='airtemp')
    proctemp=st.number_input("Enter Process temperature in K",key='proctemp')
    rotspeed=st.number_input("Enter Rotational Speed in rpm",step=1,key='rotspeed')
    torque=st.number_input("Enter torque in Nm",key='torque')
    toolwear=st.number_input("Enter minimum Tool wear ",step=1,key='toolwear')
    Type_H=st.selectbox("Enter 1 if Product Quality is high(20% of all products)",data['Type_H'].unique(),key='Type_H')
    Type_L=st.selectbox("Enter 1 if Product Quality is Low(50% of all products)",data['Type_L'].unique(),key='Type_L')
    Type_M=st.selectbox("Enter 1 if Product Quality is medium(30% of all products)",data['Type_M'].unique(),key='Type_M')

    if(st.button("RESULT")):
        result=prediction(airtemp,proctemp,rotspeed,torque,toolwear,Type_H,Type_L,Type_M)
        if(result==0):
            st.write('Machine Failure : Yes')
            st.write('Failure Type : Heat Dissipation')
        
        elif(result==1):
            st.write('Machine Failure : No')
            st.write('Failure Type : No Failure')
            
        elif(result==2):
            st.write('Machine Failure : Yes')
            st.write('Failure Type : Power Failure')
            
        elif(result==3):
            st.write('Machine Failure : Yes')
            st.write('Failure Type : Random Failure')
            
        elif(result==4):
            st.write('Machine Failure : Yes')
            st.write('Failure Type : Tool wear Failure')
            
        elif(result==5):
            st.write('Machine Failure : Yes')
            st.write('Failure Type : Overstrain Failure')
            
            
        user_data = {
            'Air temperature [K]': airtemp,
            'Process temperature [K]': proctemp,
            'Rotational speed [rpm]': rotspeed,
            'Torque [Nm]': torque,
            'Tool wear [min]': toolwear,
            'Type_H': Type_H,
            'Type_L': Type_L,
            'Type_M': Type_M,
            'Failure Type':int(result)
            
        }
        new_data=pd.DataFrame([user_data],columns=['Air temperature [K]', 'Process temperature [K]',
       'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]', 'Type_H','Type_L','Type_M','Failure Type'])
        
        if pd.io.common.file_exists('user_data.csv'):
            new_data.to_csv('user_data.csv', mode='a', header=False, index=False)
        else:
            new_data.to_csv('user_data.csv', mode='w', header=True, index=False)
    
        st.success('Data Submitted')
    
    
            
with tabs[2]:
    fig=plt.figure(figsize=(12,12))
    col=['Air temperature [K]', 'Process temperature [K]',
       'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]', 'Target']
    l=list(enumerate(col))

    for i in l:
        plt.subplot(3,3,i[0]+1)
        sns.histplot(data[i[1]],kde=True)
        
    st.pyplot(fig)
    
    fig2=plt.figure(figsize=(12,12))
    col=['Air temperature [K]', 'Process temperature [K]',
       'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']
    l=list(enumerate(col))

    for i in l:
        plt.subplot(3,3,i[0]+1)
        sns.boxplot(data[i[1]])
        plt.xlabel(i[1])
        
    st.pyplot(fig2)
    
    fig3=plt.figure(figsize=(12,12))
    sns.heatmap(data.corr(),annot=True)
    st.pyplot(fig3)

    
    fig4=plt.figure(figsize=(10,5))
    st.write(data['Failure Type'].value_counts())
    st.write('Heat Dissipation : 0')
    st.write('No Failure : 1')
    st.write('Power Failure : 2')
    st.write('Random Failure : 3')
    st.write('Tool wear Failure : 4')
    st.write('Overstrain Failure : 5')
    plt.xticks(rotation=40)
    sns.countplot(x='Failure Type',data=data,order=data['Failure Type'].value_counts().index)
    st.pyplot(fig4)
    
    
    
with tabs[3]:
    st.subheader('Random Forest')
    st.image('rf.png')
    
    st.subheader('SVC')
    st.image('svc.png')
    
    st.subheader('Logistic Regression')
    st.image('lr.png')
    
    st.subheader('K-nearest neighbours')
    st.image('knn.png')
    
    st.subheader('Adaboost Classifier')
    st.image('ada.png')
    
    st.subheader('Neural Network')
    st.image('ann.png')
    
    st.subheader('Report')
    st.image('all.png')
    