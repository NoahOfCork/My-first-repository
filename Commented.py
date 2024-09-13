import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
 
# Read the csv and write it to the variable content
f = open('^SPX.csv', 'r')
content = pd.read_csv(f)
 
# Get a list with the dates and prices. Open is what the price of a unit of stock was at the start of a day
dates = content['Date']
prices = content['Open']
 
# Format the dates to plot on the x-axis and the prices on the y-axis
x = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in dates]
y = prices
 
# lists every date within groups of four
months = [dates[n*4:n*4+4] for n in range(int(len(dates)/4))]
#months is a dataframe, so the indexes of the lists within it still have the indexes from dates
month_start = [dt.datetime.strptime(months[n][n*4],'%d/%m/%Y').date() for n in range(len(months))]

#loc accesses specific rows by name. .index returns the index of the first appearance of the index of the month. This gives us a list of lists representing the range of prices that were within the same month
month_prices = [prices.loc[months[n].index].tolist() for n in range(len(months))]

#The sum of the prices in each week within a month, divided by four. There are always 4 weeks within each month, so this is always the average
average_month_prices = [sum(month_prices[n])/4 for n in range(len(months))]
#lambda creates unnamed functions that can be used on one line. map() uses a function for every element of a given list
#the amount that the value of a unit of stock has grown by since the start
amp_at0 = list(map(lambda x: x - average_month_prices[0], average_month_prices))
 
percent_change = [round(((average_month_prices[n+1]/average_month_prices[n])-1)*100, 2) for n in range(len(average_month_prices)) if n+1 < len(average_month_prices)]

#the amount of money that is has been invested
investments_1, investments_2, investments_3, investments_4, investments_5 = 100, 100, 100, 100, 100
#the value of the stocks that the investor owns
portfolio_1, portfolio_2, portfolio_3, portfolio_4, portfolio_5 = 100, 100, 100, 100, 100

#of this grouping, variables ending in _i represent how much money was invested. variables ending in _p is the value of the money now
#dca represents investing equal amounts every month
dca_i, dca_p = [], []
up5_i, up5_p = [], []
down5_i, down5_p = [], []
up4_i,up4_p = [], []
down4_i, down4_p = [], []


# Invests equal amounts at regular intervals
#My comments here apply to all investor loops
for i in range(len(percent_change)):
    #Updates the value of the investments already made
    portfolio_1 *= 1 + (percent_change[i]/100)
    # Records the amount invested and the value if sold now to the lists that will be plotted at the end
    dca_i.append(investments_1)
    dca_p.append(portfolio_1)
    # Invests
    investments_1 += 20
    portfolio_1 += 20
    

    
for i in range(len(percent_change)):
    portfolio_2 *= 1 + (percent_change[i]/100)
    up5_i.append(investments_2)
    up5_p.append(portfolio_2)
    if percent_change[i] > 5:
        investments_2 += 100
        portfolio_2 += 100
        

 
for i in range(len(percent_change)):
    portfolio_3 *= 1 + (percent_change[i]/100)
    down5_i.append(investments_3)
    down5_p.append(portfolio_3)
    if percent_change[i] < -5:
        investments_3 += 100
        portfolio_3 += 100
        

 
for i in range(len(percent_change)):
    portfolio_4 *= 1 + (percent_change[i]/100)
    up4_i.append(investments_4)
    up4_p.append(portfolio_4)
    if all(a < b for a, b in zip(month_prices[i], month_prices[i][1:])):
        investments_4 += 100
        portfolio_4 += 100
 

 
for i in range(len(percent_change)):
    portfolio_5 *= 1 + (percent_change[i]/100)
    down4_i.append(investments_5)
    down4_p.append(portfolio_5)
    if all(a > b for a, b in zip(month_prices[i], month_prices[i][1:])):
        investments_5 += 100
        portfolio_5 += 100
 

    
 
# Plot the graph
plt.plot(x,y)
plt.plot(month_start, amp_at0)
#plots the value gained by investing equal amounts at regular intervals
plt.plot(month_start[:-1], dca_i, linestyle='dashed', color='green')
plt.plot(month_start[:-1], dca_p, color='green')
#Plots the value gained by investing when the value drops by 5% over a month
plt.plot(month_start[:-1], down5_i, linestyle='dashed', color='blue')
plt.plot(month_start[:-1], down5_p, color='blue')
#Plots the value gained by investing when the value raises by 5% over a month
plt.plot(month_start[:-1], up5_i, linestyle='dashed', color='red')
plt.plot(month_start[:-1], up5_p, color='red')
#Plots the value gained by investing when the value increases every week over a month
plt.plot(month_start[:-1], up4_i, linestyle='dashed', color='yellow')
plt.plot(month_start[:-1], up4_p, color='yellow')
#Plots the value gained by investing when the value drops every week over a month
plt.plot(month_start[:-1], down4_i, linestyle='dashed', color='brown')
plt.plot(month_start[:-1], down4_p, color='brown')


roi_1 = round(portfolio_1/investments_1, 2)
roi_2 = round(portfolio_2/investments_2, 2)
roi_3 = round(portfolio_3/investments_3, 2)
roi_4 = round(portfolio_4/investments_4, 2)
roi_5 = round(portfolio_5/investments_5, 2)
 
print(f'Green: Dollar Cost Averaging ROI: {roi_1}')
print(f'Blue: Up 5% ROI: {roi_2}')
print(f'Red: Down 5% ROI: {roi_3}')
print(f'Yellow: Up 4 weeks in a row ROI: {roi_4}')
print(f'Brown: Down 4 weeks in a row ROI: {roi_5}')

plt.show()