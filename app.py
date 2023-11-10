import streamlit as st
from streamlit_option_menu import option_menu
from log_reg import log_reg
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from matplotlib import colors as c
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Indicators of Heart Disease",
    page_icon="🏥",
)

if 'data' not in st.session_state:
    data = pd.read_csv('heart_2020_cleaned.csv')
    st.session_state["data"] = data
else:
    data = st.session_state["data"]

if "user" not in st.session_state:
    log_reg()
else:
    with st.sidebar:
        selected = option_menu(None, ["Numerical feature analysis", "Categorical features analysis"],
                               icons=["bar-chart-line-fill", "pie-chart-fill"], default_index=0)
        if st.sidebar.button("Log out", type="primary"):
            st.session_state.pop('user')
            st.experimental_rerun()
    if selected == 'Numerical feature analysis':
        # st.text_area(
        #     "desc1",
        #     "AgeCategory shouldn't be categorical, so I will apply a function to calculate the mean age and make it a continuous feature",
        #     disabled=True, label_visibility='hidden', key='desc1'
        # )

        age_category={
            "18-24":18,"25-29":25,"30-34":30,"35-39":35,"40-44":40, 
            "45-49":45,"50-54":50,"55-59":55,"60-64":60,"65-69":65,
            "70-74":70,"75-79":75,"80 or older":80
        }

        heartDisease = "HeartDisease"
        temp=data[[heartDisease,"Sex","AgeCategory","Race"]]
        temp["AgeCategory"]=temp["AgeCategory"].apply(lambda x : age_category[x])
        tempAge=temp[temp[heartDisease]=="Yes"].groupby(["AgeCategory"])[[heartDisease]].count().rename(columns={heartDisease:f"{heartDisease}_count"})
        tempAge["total_count"]=temp.groupby(["AgeCategory"])[[heartDisease]].count()
        tempAge[f'{heartDisease}_ratio'] = tempAge[f'{heartDisease}_count'] / tempAge['total_count']
        tempAge[f'{heartDisease}_cumratio_total'] = tempAge[f'{heartDisease}_count'].cumsum() / tempAge['total_count'].cumsum()
        tempAge[f'{heartDisease}_cumratio_yes'] = tempAge[f'{heartDisease}_count'].cumsum() / len(temp[temp[heartDisease]=='Yes'])

        fig=make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(x=tempAge.index,y=tempAge[f"{heartDisease}_ratio"],marker=dict(color=["lightcoral"]*9+["darkred"]*10),name="The Ratio of Heart Disease in Age"),secondary_y=False)
        fig.add_trace(go.Scatter(x=tempAge.index, y=tempAge[f'{heartDisease}_cumratio_yes'],line=dict(color="black") ,name='The Cumulative Sum of Ratio of Heart Diseas by Age'),secondary_y=True)
        fig.update_layout(title='<b>THE PERCENTAGE of HEART DISEASE by AGE</b>', template="simple_white")
        fig.update_layout(legend=dict(x=0, y=1.4), margin=dict(l=20, r=20, t=200, b=70))
        fig.update_yaxes(title="Ratio", rangemode="tozero", secondary_y=False)
        fig.update_yaxes(title="Cumulative Sum of Ratio", rangemode="tozero", secondary_y=True)
        fig.update_xaxes(title="AgeCategory")
        st.plotly_chart(fig, theme='streamlit', use_container_width=True)

        c1 = c.to_rgba('#F0073B')
        c3 = c.to_rgba("#DE1E5A")
        c5 = c.to_rgba("#CB3579")
        c7 = c.to_rgba('#B94C98')
        # st.text_area(
        #     "desc2",
        #     "AgeCategory shouldn't be categorical, so I will apply a function to calculate the mean age and make it a continuous feature",
        #     disabled=True, label_visibility='hidden', key='desc2'
        # )
        cont_col = st.multiselect("Please select columns 👇", ['BMI','PhysicalHealth','MentalHealth','SleepTime'], ['BMI','PhysicalHealth'])
        
        boxplot_color = [c1,c3,c5,c7]

        with st.spinner("Drawing..."):
            for i in range(0,len(cont_col)):
                plt.figure(figsize=(10,1),dpi=120)
                sns.boxplot(x= data[cont_col[i]], y=data['HeartDisease'], data=data, orient="h", color=boxplot_color[i])
                plt.title(cont_col[i] + " Distribution", fontweight='bold')
                st.pyplot(plt)


    elif selected == 'Categorical features analysis':
        c1 = c.to_rgba('#F0073B')
        c5 = c.to_rgba("#CB3579")
        # st.text_area(
        #     "desc3",
        #     "The boxplot showed whether there were significant differences in BMI, sleep duration and mental health between adults with and without heart disease",
        #     disabled=True, label_visibility='hidden', key='desc3'
        # )
        
        binary_col = use_col = st.selectbox("Please select column 👇", ['Sex','Smoking','AlcoholDrinking','Stroke',
            'Asthma', 'DiffWalking','PhysicalActivity','KidneyDisease','SkinCancer'])

        plt.figure(figsize=(10,4), dpi=120)
        
        ax1 = plt.subplot(1,2,1)
        data[data['HeartDisease'] == 'Yes'].groupby(data[binary_col]).HeartDisease.count().plot(kind='pie', autopct='%.1f%%', colors=[c1, c5],
                                                                                            wedgeprops = { 'linewidth' : 7, 'edgecolor' : 'white', 'width':0.45 })
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.title("With heart disease")
        
        ax2 = plt.subplot(1,2,2)
        data[data['HeartDisease'] == 'No'].groupby(data[binary_col]).HeartDisease.count().plot(kind='pie',  autopct='%.1f%%', colors=[c1, c5],
                                                                                         wedgeprops = { 'linewidth' : 7, 'edgecolor' : 'white', 'width':0.45 })
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.title("Without heart disease")
        plt.suptitle("Patient with/without Heart Disease distribution by " + binary_col + " status", fontweight='bold')
        st.pyplot(plt)
