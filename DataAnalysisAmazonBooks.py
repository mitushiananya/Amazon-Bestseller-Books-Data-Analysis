import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.io import curdoc
curdoc().clear()
from bokeh.io import show
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.palettes import Dark2_5 as palette
import itertools
from bokeh.palettes import d3
#colors has a list of colors which can be used in plots
colors = itertools.cycle(palette)


df = pd.read_csv("amazonbooks.csv")
print("Datatypes before preprocessing the data:")
print(df.dtypes)
# All the datatypes are of Object type

# 1. DATA CLEANING
# Just keep the rating. That is 4.5 out of 5 stars. Keep only '4.5' remove the rest
df['Rating'] = df['Rating'].apply(lambda x: x.split()[0])  # Remove the extra part from the rating.
df['Rating'] = pd.to_numeric(df['Rating'])  # Convert the rating into numeric type data
df["Price"] = df["Price"].str.replace('$', '')  # Remove the dollar sign. Just keep the price
df["Price"] = df["Price"].str.replace(',', '')  # Remove commas from the price.
df['Price'] = df['Price'].apply(lambda x: x.split('.')[0])  # Split the price by dot
df['Price'] = df['Price'].astype(int)  # Convert the price into int datatype
df["Customers_Rated"] = df["Customers_Rated"].str.replace(',', '')  # Remove the commas from the number of customer who rated
df['Customers_Rated'] = pd.to_numeric(df['Customers_Rated'], errors='ignore')  # Convert the customer rated to int datatype
print("Shape of the data: ", df.shape)
print("\nFirst 5 rows of the dataset")
print(df.head(5))
print("Datatypes of the dataset: ")
print(df.dtypes)  # Datatypes after the preprocessing of data

# 2. DEALING WITH NAN VALUES
# Replace the zero values (both int and string) to NaN
df.replace(str(0), np.nan, inplace=True)
df.replace(0, np.nan, inplace=True)

# Count the number of NaN values
count_nan = len(df) - df.count()
print("\nNumber of Nan Values:")
print(count_nan)

# Drop the NaN values
df = df.dropna()

# 3. DATA ANALYSIS AND VISUALISATION
# Authors with the highest-priced book
highpricedbook = df.sort_values(["Price"], axis=0, ascending=False)[:15]
print("\nHighest Priced Books:")
print(highpricedbook)
# plot showing the highest priced books
priceybook = df.groupby(by='Book Name')['Price'].sum().sort_values(ascending =False).head(20).reset_index()
plt.figure(figsize=(8,6))
plt.xlabel('Price',fontsize=10)
plt.ylabel('Book Name',fontsize=10)
plt.title('Highest Priced Books',fontsize = 15)
ax = sns.barplot(x= priceybook['Price'],y = priceybook['Book Name'], palette='icefire')
for i ,(value,name) in enumerate (zip(priceybook['Price'], priceybook['Book Name'])):
    ax.text(value, i-.05,f'{value:,.0f}',size = 8,ha='left',va='center')
ax.set(xlabel='Price',ylabel='Book Name')
plt.show()

# Authors have the top-rated books and which books of those authors are top rated
# Filter out those authors in which less than 1000 customers rated
ratingthousand = df[df['Customers_Rated'] > 1000]
topratedbook = ratingthousand.sort_values(['Rating'],axis=0, ascending=False)[:15]
print("\nTop-Rated Books:")
print(topratedbook)

# Top Rated Author
bestbookauthor = df.sort_values(["Customers_Rated"], axis=0, ascending=False)[:20]
print("\nBest Rated Author and Book")
print(bestbookauthor)
# Plot showing the top rated author
bestauthor = df.groupby(by='Author')['Customers_Rated'].sum().sort_values(ascending =False).head(20).reset_index()
plt.figure(figsize=(8,6))
plt.xlabel('Customers_Rated',fontsize=10)
plt.ylabel('Author',fontsize=10)
plt.title('Best Author',fontsize = 15)
ax = sns.barplot(x= bestauthor['Customers_Rated'],y = bestauthor['Author'], palette='vlag')
for i ,(value,name) in enumerate (zip(bestauthor['Customers_Rated'], bestauthor['Author'])):
    ax.text(value, i-.05,f'{value:,.0f}',size = 8,ha='left',va='center')
ax.set(xlabel='Customers_Rated',ylabel='Author')
plt.show()

# Rating vs Books and Author
# Bokeh Plot
palette = d3['Category20'][20]
index_cmap = factor_cmap('Author', palette=palette,
                         factors=bestbookauthor["Author"])
p = figure(plot_width=700, plot_height=700, title = "Top Authors: Rating vs. Customers Rated")
p.scatter('Rating','Customers_Rated',source=bestbookauthor,fill_alpha=0.6, fill_color=index_cmap,size=20,legend='Author')
p.xaxis.axis_label = 'RATING'
p.yaxis.axis_label = 'CUSTOMERS RATED'
p.legend.location = 'top_left'
show(p)