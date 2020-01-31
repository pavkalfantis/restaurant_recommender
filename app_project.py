from flask import Flask, render_template, request, redirect
import os
import requests
from datetime import date,timedelta
from requests.auth import HTTPBasicAuth
import simplejson as json
import pandas as pd

from bokeh.tile_providers import get_provider, Vendors
from bokeh.plotting import figure,show
from bokeh.embed import components
from bokeh.util.string import encode_utf8
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import output_file, show, output_notebook


app = Flask(__name__)

@app.route('/')
def index():
  return render_template('request.html')

@app.route('/about')
def about():
  return render_template('about.html')

LV_restaurants=pd.read_csv('dataset-capstone/LV_restaurants.csv')
LV_restaurants=LV_restaurants.drop(columns=['Unnamed: 0'])

def create_map():
    tile_provider = get_provider(Vendors.CARTODBPOSITRON_RETINA)

    # range bounds supplied in web mercator coordinates
    p = figure(#x_range=(lv_merc_coord[0]-map_range, lv_merc_coord[0]+map_range),
               #y_range=(lv_merc_coord[1]-map_range, lv_merc_coord[1]+map_range),
               x_axis_type="mercator", y_axis_type="mercator")
    p.add_tile(tile_provider)

    p.circle(x = LV_restaurants['merc_x'],
             y = LV_restaurants['merc_y'])
    return p

def create_map_hover():
    tile_provider = get_provider(Vendors.CARTODBPOSITRON_RETINA)
    source = ColumnDataSource(data=dict(
                            x=list(LV_restaurants['merc_x']), 
                            y=list(LV_restaurants['merc_y']),
                            categories=list(LV_restaurants['categories']),
                            stars=list(LV_restaurants['stars']),
                            restaurant_name=list(LV_restaurants['name'])))
    hover = HoverTool(tooltips=[
        ("name", "@restaurant_name"),
        ("stars","@stars"),
        ("categories","@categories")

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
def index2():
    if request.method=='GET':
        return render_template('request.html')
    else:
        food=request.form['food']
      
    p=create_map_hover()
    script, div = components(p)
    return render_template("chart.html", div=div, script=script)

if __name__ == '__main__':
  app.run(port=33507,debug=True)
