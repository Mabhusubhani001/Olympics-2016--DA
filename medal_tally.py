import numpy as np

def country_years_list(df):
    # We have added two more drop down menus in the web app for slecting the country and for selecting the year wise medal analysis
    years = df['Year'].unique().tolist()
    # lets sort them and add name "Overall" in the list at 0
    years.sort()
    years.insert(0, 'Overall')
    # Now let's do the same for conutry dropdown menu also
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country
# Now lets create a function for fetching medal details for drop down menu!
def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if year == 'Overall' and country != 'Overall':
        # But i want to get all the medals acquired in every year if Overall is selected in place of year!
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)
    x['total'] = x['total'].astype(int)

    return x
def medal_table(df):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    # let's finally find out how many gold,silver,bronze medals each country won in final medal_table!
    medal_df = medal_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
    medal_df['total']=medal_df['Gold'] + medal_df['Silver'] + medal_df['Bronze']
    medal_df['Gold'] = medal_df['Gold'].astype(int)
    medal_df['Silver'] = medal_df['Silver'].astype(int)
    medal_df['Bronze'] = medal_df['Bronze'].astype(int)
    medal_df['total'] = medal_df['total'].astype(int)

    return medal_df
#Helper Code block for plots that returns dataframes
def data_Over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition','count':col}, inplace=True)
    return nations_over_time
#Now let's create a table which contains most successful atheletes in a sport
def most_successful(df,sport):
    temp_df=df.dropna(subset=['Medal'])
    if sport!='Overall':
        temp_df=temp_df[temp_df['Sport']==sport]
    x=temp_df['Name'].value_counts().reset_index().rename(columns={'Name': 'index','count':'Name'}).head(15).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index')
    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    return x
def year_wise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['NOC', 'Games', 'Year', 'Sport', 'City', 'Event', 'Medal', 'Team'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df
def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['NOC', 'Games', 'Year', 'Sport', 'City', 'Event', 'Medal', 'Team'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt=new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int)
    return pt
#Now let's create a table which contains most successful atheletes in a country
def most_successful_countrywise(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df=temp_df[temp_df['region']==country]
    top10=temp_df['Name'].value_counts().reset_index().rename(columns={'Name': 'index','count':'Name'}).head(10).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport']].drop_duplicates('index')
    top10.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    return top10
def weightVSHeight(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport!='Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df
#Now lets plot one last one i.e, over the years how is the participation of men vs women
def menvswomen(df):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    men=athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women=athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
    final=men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    final.fillna(0,inplace=True)
    return final










