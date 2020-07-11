#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
import pandas as pd
import datetime as dt
import dash_bootstrap_components as dbc
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from cloudant import cloudant
from cloudant.client import Cloudant
from cloudant.result import Result, ResultByKey


# In[ ]:


client = Cloudant('47400d77-738e-4f53-af75-2724098f1441-bluemix', '566317acc09448f54f953a4d7cf344940b44447b297081d1a5d885bfd1e4479b', url='https://47400d77-738e-4f53-af75-2724098f1441-bluemix:566317acc09448f54f953a4d7cf344940b44447b297081d1a5d885bfd1e4479b@47400d77-738e-4f53-af75-2724098f1441-bluemix.cloudantnosqldb.appdomain.cloud', connect=True)
my_database = client["newtest"]
data=get_data()
positive_tweets=filter_tweets(data,'positive');
negative_tweets=filter_tweets(data,'negative');
natural_tweets=filter_tweets(data)
total_tweets=len(data)
positive_count=len(positive_tweets)
negative_count=len(negative_tweets)
natural_count=len(natural_tweets)

tcase , tdeath , trecovery = CaseCount()


# In[ ]:


def get_new_tweets():
    result_collection = Result(my_database.all_docs, include_docs=True)
    lst=[]
    for i in result_collection:
        lst.append([i['doc']['_id'], i['doc']['createdate'] , i['doc']['text'] , i['doc']['polarity'], i['doc']['subjectivity'],i['doc']['user_location'],i['doc']['longitude'],i['doc']['latitude'],i['doc']['hashtag']])
    return pd.DataFrame(lst,columns=['Tweet_id','Tweet_date','Tweet_text','polarity','subjectivity','user_location','longitude','latitude','hashtags'])


# In[ ]:


def corona_count(data):
        return  len(data[(data['hashtags'].str.contains("covid19"))|
                         (data['hashtags'].str.contains("coronavirus")) |
                         (data['hashtags'].str.contains("coronaviruspandemic"))|
                        (data['hashtags'].str.contains("covid_19"))])
 


# In[ ]:


def update_data():
    new_data=get_new_tweets()
    tcase , tdeath , trecovery = CaseCount()
    


# In[ ]:


def lockdown_count(data):
        return  len(data[(data['hashtags'].str.contains("lockdown"))])


# In[ ]:


def filter_tweets(data,filter="natural"):
    if filter == "positive":
        return data.loc[data['polarity'] > 0]
    elif filter == "negative":
        return data.loc[data['polarity'] < 0]
    else:
        return data.loc[data['polarity'] == 0]
    
        


# In[ ]:





# In[ ]:


def get_location_count(data,user_location):
    return  len(data[(data['user_location'].str.contains(user_location))])


# In[ ]:


def get_data():
    data=pd.read_csv("file_name.csv")
    return data


# In[ ]:


def CaseCount():
    import requests
    url = "https://api.rootnet.in/covid19-in/stats/latest"
    payload = {}
    headers= {}
    
    response = requests.request("GET", url, headers=headers, data = payload)
    data = response.json()
    totalcase  = data['data']['summary']['confirmedCasesIndian']
    totaldeaths = data['data']['summary']['deaths']
    totaldischarge  = data['data']['summary']['discharged'] 
    return totalcase,totaldeaths,totaldischarge


# In[ ]:


def generate_tweet_count_area():
    return html.Div(children=[
        html.Div(children=[
             html.Div(children=[
                  html.Div(children="Total Tweets",className='card-header'),
                  html.Div(children=[html.H5(children=str(total_tweets),id="total_count")],className='card-body'),                
                 
             ],className='card text-center text-white bg-info mb-3',style={'max-width': '14rem'})            
            
        ],className="col-md-2"),
        html.Div(children=[
            html.Div(children=[
                  html.Div(children="Positive Tweets",className='card-header'),
                  html.Div(children=[html.H5(children=str(positive_count),id="positive_count")],className='card-body'),                
                 
             ],className='card text-center text-white bg-success mb-3',style={'max-width': '14rem'})            
            
        ],className="col-md-2"),
        html.Div(children=[
             html.Div(children=[
                  html.Div(children="Negative Tweets",className='card-header'),
                  html.Div(children=[html.H5(children=str(negative_count),id="negative_count")],className='card-body'),                
                 
             ],className='card text-center text-white bg-danger mb-3',style={'max-width': '14rem'})            
            
        ],className="col-md-2"),
       
        html.Div(children=[
             html.Div(children=[
                  html.Div(children="Natural Tweets",className='card-header'),
                  html.Div(children=[html.H5(children=str(natural_count),id="natural_count")],className='card-body'),                
                 
             ],className='card text-center text-white bg-primary mb-3',style={'max-width': '14rem'})            
            
        ],className="col-md-2"), 
        
         html.Div(children=[
             html.Div(children=[
                  html.Div(children=[
                      html.H5(children="Total Confirmed Cases : " + str(tcase)),
                      html.H5(children="Total Deaths : " + str(tdeath)),
                      html.H5(children="Total Discharged : " + str(trecovery)),
                  ],className='card-body'),                
                 
             ],className='card text-black mb-6',style={'max-width': '28rem','height' : '121px'})            
            
        ],className="col-md-4")
        
    
        
        
    ],className='row')

#data.head()


#external scripts
external_scripts = [
    {
        'src': 'https://code.jquery.com/jquery-3.2.1.slim.min.js',
        'integrity': 'sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN',
        'crossorigin': 'anonymous'
    },
     {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
        'integrity': 'sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js',
        'integrity': 'sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl',
        'crossorigin': 'anonymous'
    }
    
]
# external CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm',
        'crossorigin': 'anonymous'
    }
]

app=dash.Dash(__name__, external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)
app.title="Corona Virus Tweet Sentiment Analysis"


def get_recent_tweet_ui(data):
     return dbc.Card(dbc.CardBody([
        html.Div("Recent Tweets Last updated at " +data['Tweet_date'][0] ,className="card-title"),
        html.Hr(),
        html.Div(children=[   
            get_recent_tweet(data['Tweet_text'][i],data['polarity'][i])  for i in range(3)]),

     ]))
    
def get_color_class(polarity):
    if polarity > 0:
        return "alert-success";
    elif polarity < 0:
        return "alert-danger";
    else:
        return "alert-primary"
    

def get_recent_tweet(text,polarity):
    return  html.Div(children=text,className="alert "+get_color_class(polarity) )
      


# In[ ]:


def get_hashtags_count(data,hashtag):
    return  len(data[(data['hashtags'].str.contains(hashtag))]);
                     
def update_hashtag_bar_chart(data):
    y=['covid19','covid_19','coronavirus','coronaviruspandemic','lockdown','socialdistancing']
    x={i:get_hashtags_count(data,i) for i in y} 
    x = dict(sorted(x.items(), key=lambda i: i[1]))
    hashtag_bar_fig = go.Bar(
            y=list(x.keys()),
            x=list(x.values()),
            text=list(x.values()),textposition='auto',
            orientation='h')
    return dbc.Card(dbc.CardBody([
            html.Div("Tweets Hashtags Count".upper(), className="card-title"),
            html.Hr(),
            html.Div(children=[dcc.Graph(figure={'data':[hashtag_bar_fig],'layout':{'width':'100%','display':'inline-block'}})],
                style={'margin-left':'0px'})
            ]))

   



    


# In[ ]:


def get_country_count(data,country):
    return len(data[(data['user_location'].str.contains(country))])
                     
def update_country_bar_chart(data):
    y=['india','london','united kingdom','united states','japan','new york','south africa','china','australia','canada','pakistan','england']
    x={i:get_country_count(data.dropna(subset=['user_location']),i) for i in y} 
    print(x)
    x = dict(sorted(x.items(), key=lambda i: i[1]))
    country_bar_fig = go.Bar(
            y=list(x.keys()),
            x=list(x.values()),
            text=list(x.values()),textposition='auto',
            orientation='h')
    return dbc.Card(dbc.CardBody([
            html.H4("Tweets Country Count".upper(), className="card-title"),
            html.Hr(),
            html.Div(children=[dcc.Graph(figure={'data':[country_bar_fig],'layout':{'width':'100%','display':'inline-block'}})],
                style={'margin-left':'0px'})
            ]))
   



# In[ ]:


def update_pie_corona(positive_tweets,negative_tweets):
    postive_tweet_corona=corona_count(positive_tweets)
    negative_tweet_corona=corona_count(negative_tweets)
    colors = ['rgb(0, 204,0)', 'rgb(255, 102, 102)']
    labels = ['Positive','Negative']
    corona_values = [postive_tweet_corona, negative_tweet_corona]
    corona_fig = go.Figure(data=[go.Pie(labels=labels, values=corona_values,marker_colors=colors,pull=[0, 0.1])])
        
    return dbc.Card(dbc.CardBody([
        html.Div("Behaviour Of People About Corona".upper(),className="card-title"),
        html.Hr(),
        html.Div(children=[dcc.Graph(figure=corona_fig)])
    ]))
    


# In[ ]:





# In[ ]:


def update_pie_lockdown(positive_tweets,negative_tweets):
    postive_tweet_lockdown=lockdown_count(positive_tweets)
    negative_tweet_lockdown=lockdown_count(negative_tweets)
    colors = ['rgb(0, 204,0)', 'rgb(255, 102, 102)']
    labels = ['Positive','Negative']
    lockdown_values=[postive_tweet_lockdown,negative_tweet_lockdown]
    lockdown_fig = go.Figure(data=[go.Pie(labels=labels, values=lockdown_values,marker_colors=colors,pull=[0, 0.1])])
    
    return dbc.Card(dbc.CardBody([
        html.Div("Behaviour Of People About Lockdown".upper(),className="card-title"),
        html.Hr(),
        html.Div(children=[dcc.Graph(figure=lockdown_fig)])
    ]))
                             
                        


# In[ ]:


def get_date_count(data,date):
    return  len(data[(data['Tweet_date'].str.contains(date))]);

def update_date_histogram(positive_tweets,negative_tweets):
    unique_date=set()
    for i in positive_tweets['Tweet_date'].str.split():
        unique_date.add(i[0])
    unique_date=tuple(unique_date)
    positive_date_count=[get_date_count(positive_tweets,i) for i in unique_date]
    negative_date_count=[get_date_count(negative_tweets,i) for i in unique_date]
    date_bar_fig = go.Figure(go.Bar(x=unique_date, y=positive_date_count,name="Positive Tweets"))
    date_bar_fig.add_trace(go.Bar(x=unique_date, y=negative_date_count,name="Negative Tweets"))
    date_bar_fig.update_layout(barmode='stack')
    
    return dbc.Card(dbc.CardBody([
        html.Div("Positive Tweets And Negative Tweet Based On Date".upper(),className="card-title"),
        html.Hr(),
        html.Div(children=[dcc.Graph(figure=date_bar_fig)])
    ]))
   


# In[ ]:


def plot_wordcloud(words):
    wc = WordCloud(background_color='black', width=400, height=360).generate(words)
    return wc.to_image()



def make_image(words):
    img = BytesIO()
    plot_wordcloud(words).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


def update_world_cloud(data):
    tokenized_tweet = data['Tweet_text'].apply(lambda x: str(x).split())
    stop_words = set(stopwords.words('english'))
    for i in tokenized_tweet:
        for j in list(i):
            if j in stop_words:
                i.remove(j)
    for i in range(len(tokenized_tweet)):
        tokenized_tweet[i] = ' '.join(tokenized_tweet[i])
    all_words = ' '.join([text for text in tokenized_tweet])

    return  dbc.Card(dbc.CardBody([
        html.Div("Tweets Word Cloud",className="card-title"),
        html.Hr(),
        html.Div(children=[
            html.Img(src=make_image(all_words))
            #html.Img(src="download.jpg")
            
        ])
    ]))
        


# In[ ]:


def update_map_count(positive_tweets,negative_tweets,natural_tweets):
    postive_map=positive_tweets.dropna()
    negative_map=negative_tweets.dropna()
    natural_map=natural_tweets.dropna()
    postive_map=postive_map.reset_index(drop=True)
    negative_map=negative_map.reset_index(drop=True)
    natural_map=natural_map.reset_index(drop=True)
    mapbox_access_token = "pk.eyJ1IjoiemFsYWRpZzk4IiwiYSI6ImNrYnMxa25kNDFnamwycXBuZG9mY21xMTkifQ.XF_6Tby0q6dC74U7gQjEYQ"

    map_fig = go.Figure()

    map_fig.add_trace(go.Scattermapbox(
            lat=postive_map['latitude'],
            lon=postive_map['longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=8,
                color='rgb(0,204, 0)',
                opacity=0.7
            ),
           text=postive_map['Tweet_text'],
            hoverinfo='text',name="Positive Tweets"
        ))

    map_fig.add_trace(go.Scattermapbox(
            lat=negative_map['latitude'],
            lon=negative_map['longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=8,
                color='rgb(255, 102, 102)',
                opacity=0.7
            ),
            text=negative_map['Tweet_text'],
            hoverinfo='text',name="Negative Tweeta"
        ))
    map_fig.add_trace(go.Scattermapbox(
            lat=natural_tweets['latitude'],
            lon=natural_tweets['longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=8,
                color='rgb(51, 152, 255)',
                opacity=0.7
            ),
            text=natural_tweets['Tweet_text'],
            hoverinfo='text',name="Natural Tweets"
        ))

    map_fig.update_layout(
        autosize=True,
        hovermode='closest',
        showlegend=True,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=20,
                lon=78
            ),
            pitch=0,
            zoom=2,
            style='light'
        ),
    )
   # map_fig.show()

    return  dbc.Card(dbc.CardBody([
            html.Div("Behaviour Of People About COVID-19",className="card-title"),
            html.Hr(),
            html.Div(children=[dcc.Graph(figure=map_fig)])
        ]))


# In[ ]:


app.layout=html.Div(children=[
    html.Div(children=[
        dbc.NavbarSimple(
        brand="COVID-19 TWEET SENTIMENT ANALYSIS",
        color="primary",
        dark=True),
        html.Hr(),
        #Tweet count panel
        generate_tweet_count_area(),
        #graph panel area
        html.Hr(),
      
        html.Div(children=[
            #first part of graph panel recet tweeet and word cloud
            html.Div(children=[
                get_recent_tweet_ui(data),
                html.Hr(),
                update_date_histogram(positive_tweets,negative_tweets),
                html.Hr()],
                #update_map_count(positive_tweets,negative_tweets,natural_tweets)],
            className="col-md-4"),
            
            #second part hashtag bar and countery bar chart
            html.Div(children=[
                update_pie_corona(positive_tweets,negative_tweets),
                html.Hr(),
                update_hashtag_bar_chart(data),
                html.Hr()],
            className="col-md-4"),
            
            #third part cororna pie and lockdown pie
            html.Div(children=[
                update_pie_lockdown(positive_tweets,negative_tweets),
                html.Hr(),
                update_country_bar_chart(data),
                html.Hr()],
            className="col-md-4")],className='row'),
    
    
        html.Div(children=[
            #first part of graph panel recet tweeet and word cloud
            html.Div(children=[
                update_world_cloud(data),
                html.Hr()],
                #update_map_count(positive_tweets,negative_tweets,natural_tweets)],
            className="col-md-4"),
            
            #second part hashtag bar and countery bar chart
            html.Div(children=[
                update_map_count(positive_tweets,negative_tweets,natural_tweets),
                html.Hr()],
            className="col-md-8")],className='row')
    
    ])],className='container-fluid',style={"background-color" : 'black'})


# In[ ]:


if __name__ == "__main__":
    app.run_server()
