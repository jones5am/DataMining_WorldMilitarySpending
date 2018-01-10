# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 17:24:00 2017

@author: Andrew Jones
"""

#%% Reading in all data from current directory and importing packages
import pandas as pd
import matplotlib.pyplot as plt

#Military Spending in constant year 2015 $USD
Military2015 = pd.read_excel('SIPRI-Milex-data-1949-2016_v4.xlsx', sheetname = 'Constant (2015) USD', headers = True, index_col = 'Country')

#Military Spending as a percentage of the countries GDP
ShareGDP = pd.read_excel('SIPRI-Milex-data-1949-2016_v4.xlsx', sheetname = 'Share of GDP', headers = True, index_col = 'Country')

#Military Spending per capita in current $USD
PerCapitaMilitary = pd.read_excel('SIPRI-Milex-data-1949-2016_v4.xlsx', sheetname = 'Per capita', headers = True, index_col = 'Country')

#Military Spending in current $USD
MilitaryCurrent = pd.read_excel('SIPRI-Milex-data-1949-2016_v4.xlsx', sheetname = 'Current USD', headers = True, index_col = 'Country')

#%% Creating all DataFrames

#Create DataFrames for: The military spending of at least the top 10 nations (in military spending)
Military2015['Total'] = Military2015.sum(axis=1)
Military2015 = Military2015.sort_values(by = 'Total', ascending = False)

Top_10 = Military2015.head(n=10)
Top_10 = Top_10.T

Top_10_CountryNames = list(Top_10)


#Create DataFrames for: Inputs to other questions
TotalGDP = Military2015.div(ShareGDP)
Top_10GDP = Top_10[Top_10_CountryNames]
Population = MilitaryCurrent.div(PerCapitaMilitary)
PerCapitaGDP = TotalGDP.div(Population)

#Create DataFrames for: Compare the data to that country's GDP
ShareGDP = ShareGDP.sort_values(by = 2016, ascending = False)

ShareGDP_forTop10Fixed = ShareGDP.loc[Top_10_CountryNames]
ShareGDP_forTop10Fixed = ShareGDP_forTop10Fixed.T

#Create DataFrames for: Compare the data to the overall military spending of the all 10+ countries
Top10_vs_RestofWorld = Military2015.iloc[10:]
Top10_vs_RestofWorld = Top10_vs_RestofWorld.T
Top10_vs_RestofWorld['RestOfWorld'] = Top10_vs_RestofWorld.sum(axis=1)
Top10_vs_RestofWorld = Top10_vs_RestofWorld[['RestOfWorld']]
Top10_vs_RestofWorld = Top10_vs_RestofWorld.join(Top_10)

Top10_vs_RestofWorld_Totals = Top10_vs_RestofWorld.iloc[[-1]]


#Create DataFrames for: Bonus question - which countries are currently spending the most as a percent of their GDP
Top_10ShareGDP = ShareGDP.head(n=10)
Top_10ShareGDP = Top_10ShareGDP.T


#Create DataFrames for: Compare the per person military spending to the per person GDP
PerCapitaGDP_vs_PerCapitaSpending = PerCapitaGDP.subtract(PerCapitaMilitary)
Top_10PerCapitaGDP_vs_PerCapitaSpending = PerCapitaGDP_vs_PerCapitaSpending.loc[Top_10_CountryNames]
Top_10PerCapitaGDP_vs_PerCapitaSpending = Top_10PerCapitaGDP_vs_PerCapitaSpending.drop('Total', 1)
Top_10PerCapitaGDP_vs_PerCapitaSpending = Top_10PerCapitaGDP_vs_PerCapitaSpending.T

#Create DataFrames for: Single out the fastest growing countries in military spending in fixed value and in percentage
MilitaryGrowthPercentage = MilitaryCurrent.pct_change(axis = 1)
MilitaryGrowthPercentage['Average Growth'] = MilitaryGrowthPercentage.mean(axis = 1)
MilitaryGrowthPercentage = MilitaryGrowthPercentage.sort_values(by = 'Average Growth', ascending = False)

Top_10_MilitaryGrowthPercentage = MilitaryGrowthPercentage.head(n = 11)
Top_10_MilitaryGrowthPercentage = Top_10_MilitaryGrowthPercentage.drop('Equatorial Guinea') #remove Equatorial Guinea because it has too much null & seemingly outlier data for an average to be valid
Top_10_MilitaryGrowthPercentage = Top_10_MilitaryGrowthPercentage.T.drop('Average Growth')

Top_10_MilitaryGrowthFixed = MilitaryCurrent.diff(axis =1)
Top_10_MilitaryGrowthFixed['Total'] = Top_10_MilitaryGrowthFixed.sum(axis = 1)
Top_10_MilitaryGrowthFixed = Top_10_MilitaryGrowthFixed.sort_values(by = 'Total', ascending = False)
Top_10_MilitaryGrowthFixed = Top_10_MilitaryGrowthFixed.head(n = 10).T
#%%

#Line Chart Function - created a function because many line charts are created for the presentation
def linechart(df, ylabel = 'Dollars', xlabel = 'Year', title = 'Military Spending'):
    try:
        df.drop('Total', inplace = True)
    except ValueError:
        pass
    
    df.plot(legend = True)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.legend(loc = 'upper center', bbox_to_anchor=(0.5 , -0.15), ncol = 3, fancybox = True, shadow = True)
    plt.show()
    



#%% Section 1 for Constructing USA vs. China forecast
# created two sections & trigger variable so that this could be rerun without the
# forecast continuing to compound

US_Growth = MilitaryGrowthPercentage.loc['USA','Average Growth']
China_Growth = MilitaryGrowthPercentage.loc['China, P.R.', 'Average Growth']


US_Forecast = Top_10['USA']
China_Forecast = Top_10['China, P.R.']

try:
    US_Forecast.drop('Total', inplace = True)
    China_Forecast.drop('Total', inplace = True)
except:
    pass


Forecast_Years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
trigger = True

#%% Section 2 for Constructing USA vs. China forecast

if trigger == False:
    pass
else:
    for fy in Forecast_Years:
        US_StartingPoint = US_Forecast[2016]
        China_StartingPoint = China_Forecast[2016]
       
        if trigger == True:
            US_Cumulative = US_StartingPoint * (1 + US_Growth)
            China_Cumulative = China_StartingPoint * (1+China_Growth)
        else:
            US_Cumulative = US_Cumulative * (1 + US_Growth)
            China_Cumulative = China_Cumulative * (1 + China_Growth)
            
        US_Forecast[fy] = US_Cumulative
        China_Forecast[fy] = China_Cumulative
        trigger = False
        USandChina_Forecast = US_Forecast.to_frame().join(China_Forecast.to_frame())
        

linechart(USandChina_Forecast, title = 'US vs. China Military Spending')

#%% Stacked Bar Chart for "Compare top 10 countries to the rest of the world"

try:
    Top10_vs_RestofWorld.drop('Total', inplace = True)
except ValueError:
    pass

Top10_vs_RestofWorld.plot.bar(stacked = True, legend = True)
plt.ylabel('Dollars')
plt.title('Top 10 vs Rest of World Military Spending')
plt.legend(loc = 'center left', bbox_to_anchor=(1 , 0.5), ncol = 1, fancybox = True, shadow = True)
plt.show()


#%% Pie Chart for "Compare top 10 countries to the rest of the world"
Top10_vs_RestofWorld_Totals = Top10_vs_RestofWorld_Totals.T
Top10_vs_RestofWorld_Totals['Total'].plot.pie()
plt.title('Top 10 vs Rest of World Military Spending')
plt.show()


    

#%% Creating all line charts to be used in presentation

linechart(Top_10, title = 'Top 10 Countries by Military Spending')
linechart(ShareGDP_forTop10Fixed, ylabel = 'Percent', title = 'Military Spending as % of GDP' )
linechart(Top_10ShareGDP, ylabel = 'Percent', title = 'Military Spending as Percent of GDP (2016)')
linechart(Top_10PerCapitaGDP_vs_PerCapitaSpending, title = 'GDP per Capita - Military Spending per Capita')
linechart(Top_10_MilitaryGrowthFixed, ylabel = 'Dollar Change Since Previous Year',title = 'Top 10 Countries for Military Spending Growth (Fixed $)')
linechart(Top_10_MilitaryGrowthPercentage, ylabel = 'Percentage', title = 'Fastest Growing Military Spending (Avg %)')

