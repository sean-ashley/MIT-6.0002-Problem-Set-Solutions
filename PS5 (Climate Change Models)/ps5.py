# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
from sklearn.metrics import r2_score
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import itertools
# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    for i in degs:
        models.append(np.polyfit(x,y,i))
    return models

    


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    return r2_score(y,estimated)

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    

    for model in models:
        
        #plot real values
        plt.plot(x,y,label = 'Real Values',color = 'blue',linestyle = 'None',marker = '.')
        #create range of estimated values with the same x values
        estYVals = pylab.polyval(model,x)
        
        #plot the model
        plt.plot(x,estYVals,label= 'Model',color = 'red', linestyle = 'solid')
        #calculate r^2 value
        r2_val = round(r_squared(y,estYVals),6)
        #if its a linear model
        if len(model) == 2:
            #generate se/sslope and put it in the title
            se_over_slp = se_over_slope(pylab.array(x),pylab.array(y),estYVals,model)
            se_over_slp = round(se_over_slp,6)
            se_over_slp = str(se_over_slp)
            plt.title('Real Data vs Degree ' + str(len(model)-1) + ' Model.' + '\n' + 'R^2 Value: ' + str(r2_val) + '\n' + 'SE/Slope: ' + se_over_slp )
        else:
            #otherwise dont
            plt.title('Real Data vs Degree ' + str(len(model)-1) + ' Model.' + '\n' + 'R^2 Value: ' + str(r2_val))
        #generate tile and axis labels
        plt.xlabel('Years')
        plt.ylabel('Temperatures in Celsius')
        #show the plot
        plt.show()
        #clewar the plot
        plt.clf()






def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    #initialize return array and avg to append
    averages = []
    running_avg = 0
    #iterate through years
    for year in years:
        #iterate through each city per year
        for city in multi_cities:
            #get the average of all the settings
            running_avg += ((climate.get_yearly_temp(city,year).sum() / len((climate.get_yearly_temp(city,year)))) / len(multi_cities))
        #append the avg to the array
        averages.append(running_avg)
        #re initalize average to zero for next year
        running_avg = 0
        
    

    return averages


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """

    #initlialize list of averages
    moving_averages = []
    #loop through data
    for i in range(len(y)):
        
            #for the first few data points, have a shifting window length

        if i < window_length-1:
            moving_averages.append(sum(y[:i+1]) / len(y[:i+1]))
            #find the moving averages with the stable window length
        else:
            moving_averages.append(sum(y[i-window_length+1:i+1])/window_length)
                
        
    return pylab.array(moving_averages)





def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    return np.sqrt((((y-estimated)**2).sum())/len(y))

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    #initialize empty list of standard deviations
    std_devs = []

    #iterate thru years
    for year in years:
        #iterate thru cities
        for city in range(len(multi_cities)):
            #if its the first city create the array
            if city == 0:
                city_list = np.array(climate.get_yearly_temp(multi_cities[city],year))
            #otherwise add up the arrays
            else:
                city_list += climate.get_yearly_temp(multi_cities[city],year)
        #find the average temp at each date
        city_list = city_list / len(multi_cities)
        #compute the std and append to the back of the list
        std = np.std(city_list)

        std_devs.append(std)
        
    
    return pylab.array(std_devs)


            


        
    

    

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        
        #plot real values
        plt.plot(x,y,label = 'Real Values',color = 'blue',marker = '.', linestyle = 'None')
        #create range of estimated values with the same x values
        estYVals = pylab.polyval(model,x)
        #plot the model
        plt.plot(x,estYVals,label= 'Model',color = 'red', linestyle = 'solid')
        #make the plot title
        plt.title('Real Data vs Degree ' + str(len(model)-1) + ' Model.' + '\n' + 'RMSE: ' + str(rmse(y,estYVals)))
        #generate tile and axis labels
        plt.xlabel('Years')
        plt.ylabel('Temperatures in Celsius')
        #show the plot
        plt.show()
        #clewar the plot
        plt.clf()

if __name__ == '__main__':

    

    # Part A.4
    def partAI():
        y_vals = []
        #create climate object
        climate = Climate('data.csv')
        #loop thru years
        for year in TRAINING_INTERVAL:
            #get daily temps for jan 10
            y_vals.append(climate.get_daily_temp('NEW YORK',1,10,year))
        #generate the linear model
        model = generate_models(list(TRAINING_INTERVAL),y_vals,[1])
        #evaluate the models
        evaluate_models_on_training(list(TRAINING_INTERVAL),y_vals, model)
    
    def partAII():
        
        #create climate object
        climate = Climate('data.csv')
        #Get averages from helper function
        averages = gen_cities_avg(climate,['NEW YORK'],list(TRAINING_INTERVAL))

        #generate model
        model = generate_models(list(TRAINING_INTERVAL),averages,[1])
        #evaluate model
        evaluate_models_on_training(list(TRAINING_INTERVAL),averages, model)

    # Part B
    def partB():
         
         
        #create climate object
        climate = Climate('data.csv')
        #get averages from helper functions
        averages = gen_cities_avg(climate,CITIES,list(TRAINING_INTERVAL))

        #generate model
        model = generate_models(list(TRAINING_INTERVAL),averages,[1])
        #evaluate model
        evaluate_models_on_training(list(TRAINING_INTERVAL),averages, model)
    


    

   


    

    # Part C
    def partC():
         #create climate object
        climate = Climate('data.csv')
        #get moving averages from helper functions
        moving_averages = moving_average(gen_cities_avg(climate,CITIES,list(TRAINING_INTERVAL)),5)
        #generate model
        model = generate_models(list(TRAINING_INTERVAL),moving_averages,[1])
        #evaluate model
        evaluate_models_on_training(list(TRAINING_INTERVAL),moving_averages, model)

  


    # Part D.2
    def partDI():
        #create climate object
        climate = Climate('data.csv')
        #get moving averages from helper functions
        moving_averages = moving_average(gen_cities_avg(climate,CITIES,list(TRAINING_INTERVAL)),5)
        #generate models
        models = generate_models(list(TRAINING_INTERVAL),moving_averages,[1,2,20])
        #evaluate models
        evaluate_models_on_training(list(TRAINING_INTERVAL),moving_averages, models)
    

    def partDII():
        #create climate object
        climate = Climate('data.csv')
        #get moving averages from helper funcitons
        moving_averages_training = moving_average(gen_cities_avg(climate,CITIES,list(TRAINING_INTERVAL)),5)
        moving_averages_testing = moving_average(gen_cities_avg(climate,CITIES,list(TESTING_INTERVAL)),5)
        

        #generate models
        models = generate_models(list(TRAINING_INTERVAL),moving_averages_training,[1,2,20])
        #evaluate
        evaluate_models_on_testing(list(TESTING_INTERVAL),moving_averages_testing,models)
        


    # Part E
    def partE():
        #create climate object
        climate = Climate('data.csv')
        #get std's from helper functions
        std_devs_training = gen_std_devs(climate,CITIES,list(TRAINING_INTERVAL))
     
        #find moving averages
        moving_averages_training = moving_average(std_devs_training,5)
        
        #generate model
        model = generate_models(list(TRAINING_INTERVAL),moving_averages_training,[1])
        #evaluate
        evaluate_models_on_training(list(TRAINING_INTERVAL),moving_averages_training,model)
    partE()
    

