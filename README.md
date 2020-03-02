# Capstone Project for the TDI

My capstone project for the [Data Incubator](https://www.thedataincubator.com/) fellowship.

## Requirements of Capstone project

1. Business Objective

The business objective of this capstone project is to build a product for consumers, a custom web application that will recommend restaurants in the city of Las Vegas. The web application will be used by visitors and residents of Las Vegas in order to help them decide where to dine out.

2. Data Ingestion

The dataset used for this project is provided by [Yelp](https://www.yelp.com/dataset).
The whole dataset is more than 6GB in size and contains information on various businesses,  users and business reviews and tips. The data were loaded and ingested in pandas by joining the different dataframes in order to build the dataframes used by the web app. The main analysis of the project is done on the Jupyter notebook. The output of the notebook is then loaded from the app.py file to build the website

3. Visualizations

Exploratory Data Analysis Visualizations are created with [matplotlib](https://matplotlib.org/), interactive maps that map restaurant recommendations are created with [Bokeh](https://docs.bokeh.org/en/latest/index.html) and review and tips wordclouds that show what people are talking about for a specific restaurant are created with [wordcloud](https://pypi.org/project/wordcloud/).

4. Interactive Website

The [interactive website](http://restaurants-lv.herokuapp.com/index) which serves as the project deliverable is created with Flask and deployed through Heroku. Users can input the desired cuisine and then the app will map restaurant recommendations and show their score, review counts and other information on the map. The template for the website that was used was obtained from [w3schools](https://www.w3schools.com/w3css/w3css_templates.asp). Html files are located in the /templates directory and static files used on the website (like plots, pictures and wordclouds) are found on /static directory

5. Deliverable

The website along with the README document describe the deliverable for this project
