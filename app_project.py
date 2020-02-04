from flask import Flask, render_template, request, redirect
import os
#import requests
#from datetime import date,timedelta
#from requests.auth import HTTPBasicAuth
#import simplejson as json
import pandas as pd

from bokeh.tile_providers import get_provider, Vendors
from bokeh.plotting import figure,show
from bokeh.embed import components
from bokeh.util.string import encode_utf8
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import output_file, show, output_notebook

app = Flask(__name__)

#@app.route('/')
#def index():
#  return render_template('request.html')

@app.route('/about')
def about():
  return render_template('about.html')

#Load Data
LV_restaurants=pd.read_csv('dataset-capstone/LV_restaurants.csv')
LV_restaurants=LV_restaurants.drop(columns=['Unnamed: 0'])
LV_restaurants['categories_list']=LV_restaurants.categories.str.split(', ')

def restaurant_selection(selection = ['Mexican']):
    mask = LV_restaurants.categories_list.apply(lambda x: any(item for item in selection if item in x))
    df = LV_restaurants[mask]
    return df.sort_values(['stars','review_count'],ascending=[False, False]).head(10)

def create_map_hover(df):
    tile_provider = get_provider(Vendors.CARTODBPOSITRON_RETINA)
    source = ColumnDataSource(data=dict(
                            x=list(df['merc_x']), 
                            y=list(df['merc_y']),
                            categories=list(df['categories']),
                            stars=list(df['stars']),
                            restaurant_name=list(df['name'])))
    hover = HoverTool(tooltips=[
        ("name", "@restaurant_name"),
        ("stars","@stars"),
       # ("categories","@categories")

    ])
    # range bounds supplied in web mercator coordinates
    p = figure(x_axis_type="mercator", 
               y_axis_type="mercator",
               tools=[hover, 'wheel_zoom','save'])
    p.add_tile(tile_provider)
    p.circle(x='x',
             y='y', 
             source=source,
             #size='stars',
             line_color="red", 
             fill_color="red",
             fill_alpha=0.1)
    return p

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('request.html')
    else:
        food=request.form['food'].split(' ')
        
    #check if food in availabe categories
    if food[0] not in LV_restaurants.categories_list.apply(pd.Series).stack().value_counts().index:
        #render error page eventually
        food=['Mexican']
        
    p=create_map_hover(restaurant_selection(food))
    script, div = components(p)
    return render_template("chart.html", div=div, script=script)

if __name__ == '__main__':
  app.run(port=33507,debug=True)
