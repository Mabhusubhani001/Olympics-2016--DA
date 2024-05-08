import streamlit as st
import pandas as pd
import preprocessor,medal_tally
import scipy
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)
st.sidebar.title('Olympic Analysis Project 📊')
st.sidebar.image('https://maven-uploads.s3.amazonaws.com/47407087/projects/001.jpg')
menu=st.sidebar.radio('Select an Option',
                      ('Medal Analysis','Overall Analysis','Country-wise Analysis','Athlete Wise Analysis'))
# st.dataframe(df)
if menu == 'Medal Analysis':
    st.sidebar.header('Medal Analysis')
    years,country=medal_tally.country_years_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)
    medal=medal_tally.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and  selected_country=='Overall':
        st.title('Overall Medal Analysis')
    if selected_year=='Overall' and selected_country!='Overall':
        st.title('Overall Analysis of '+str(selected_country))
    if selected_year!='Overall' and selected_country=='Overall':
        st.title('Medal Analysis of all countries in '+str(selected_year))
    if selected_year!='Overall' and selected_country!='Overall':
        st.title('Medal Analysis of '+str(selected_country)+' in '+str(selected_year))
    st.table(medal)
if menu=='Overall Analysis':
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    atheletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    st.title('Overall Statistics')
    col1,col2,col3=st.columns(3)

    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(atheletes)
    with col3:
        st.header('Nations')
        st.title(nations)
    nations_over_time=medal_tally.data_Over_time(df,'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title('Participating Nations Over the Years')
    st.plotly_chart(fig)
    events_over_time=medal_tally.data_Over_time(df,'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title('Event Over the Years')
    st.plotly_chart(fig)
    atheletes_over_time=medal_tally.data_Over_time(df,'Name')
    fig = px.line(atheletes_over_time, x='Edition', y='Name')
    st.title('Athletes Over the Years')
    st.plotly_chart(fig)
    st.title('No of Events Over the Years(Every Sport)')
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)
    st.title('Most Successful Athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox("Select Sport",sport_list)
    x=medal_tally.most_successful(df,selected_sport)
    st.table(x)
if menu=='Country-wise Analysis':
    st.sidebar.title('Country wise Analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox("Select Country",country_list)
    country_wise=medal_tally.year_wise_medal_tally(df,selected_country)
    fig=px.line(country_wise,x='Year',y='Medal')
    st.title(selected_country+' Medal Tally Over the Years')
    st.plotly_chart(fig)

    st.title(selected_country+' has the following performance:')
    pt=medal_tally.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title(selected_country+' Top 10 Athletes')
    x=medal_tally.most_successful_countrywise(df,selected_country)
    st.table(x)

if menu=='Athlete Wise Analysis':
    st.title('Distribution of Age Over Medals')
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)
    # Now lets plot the same plot pdf for age and sport wrt gold medals only
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x,name,show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age wrt Sports(Only Gold)')
    st.plotly_chart(fig)

    st.title('Height vs Weight')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox("Select Sport", sport_list)
    temp_df=medal_tally.weightVSHeight(df,selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=50)
    st.pyplot(fig)

    st.title('Men vs Women Participation Over the Years!')
    finalplot=medal_tally.menvswomen(df)
    fig = px.line(finalplot, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)







