#######################
#### DATA Cleaning ####
#######################

#%% Imports
import pandas as pd
import seaborn as sns
import matplotlib as plt
import numpy as np

#%% importing required files
df = pd.read_csv('C:/Users/bryan/Documents/Uni/Intro to Programming/Group Project/ip_project/Clean Files/CSV/Scraped_Data_2311.csv')

zip_codes = pd.read_csv('C:/Users/bryan/Documents/Uni/Intro to Programming/data_with_zipcode.csv')

df['zip_code_scraped'] = zip_codes['ZipCode']

original_rows = df.shape[0]
original_columns = df.shape[1]

##%% Data Analysis, getting first insights
#check for null values
null_values = df.isnull().sum()

#check for datatypes in the frame
df.dtypes

##getting an initial statistical summary
stats_summary = df.describe()

##%% Data Cleaning
# Show columns
df.columns

# Renaming columns
df.columns=['Unnamed', 	
'admin_fee_exact_value', 
'admin_fee',
'admin_fee_currency',
'commission_rate', 	
'deposit_type_drop', 	
'deposit_type', 	
'deposit_amount', 	
'deposit_currency', 	
'exclusive', 	
'cost_per_extra_guest', 	
'cost_per_extra_guest_currency', 	
'instant_booking', 	
'contract_type', 	
'electricity_included', 	
'gas_included', 	
'internet_included', 	
'water_included', 	
'cleaning_period', 	
'offer_id', 	
'offer_price', 	
'offer_price_currency', 	
'cancellation_policy', 	
'max_guests', 	
'minimum_no_night', 	
'creation_date', 	
'landlord_prev_accepted_bookings', 	
'landlord_prev_confirmed', 	
'landlord_prev_rejected_bookings', 	
'landlord_prev_requested_bookings', 	
'offer_id_drop', 	
'city',
'neighborhood_id',
'neighborhood',
'property_floors_accum', 	
'property_id', 	
'landlord_residant_age', 	
'landlord_residant_gender', 	
'landlord_residant_occupation', 	
'postal_code', 	
'latitude', 	
'longitude', 
'neighborhood_id_drop', 	
'property_rules_cum', 	
'accomodation_type', 	
'accomodation_area', 	
'number_of_bathrooms', 	
'number_of_bedrooms', 	
'property_type', 	
'property_verified', 	
'units_cum', 	
'kitchen_balcony', 
'kitchen_window',
'bathroom_bathtub',
'pets_allowed',
'smoking_allowed',
'overnight_guests_allowed',
'bedroom_balcony',
'single_beds', 
'double_beds',
'kitchen_chairs', 
'kitchen_dishes_cutlery',
'kitchen_dishwasher', 
'kitchen_dryer',
'kitchen_freezer',
'kitchen_fridge',
'kitchen_microwave',
'kitchen_oven',
'kitchen_stove',
'kitchen_table',
'kitchen_washing-machine',
'bedroom_chairs',
'bedroom_desk',
'bedroom_sofa',
'bedroom_sofa_bed',
'bedroom_wardrobe', 
'bedroom_window', 
'neighborhood_drop',
'living_room_window',
'bedroom_chest_of_drawers',
'living_room_balcony',
'living_room_chairs',
'living_room_sofa',
'living_room_coffee_table',
'kitchen_pots_pans',
'bedroom_lock',
'bedroom_tv',
'living_room_table',
'living_room_desk',
'living_room_sofa_bed',
'living_room_tv',
'bedroom_bed_linen',
'bedroom_towels',
'private_bathroom',
'females_only',
'international_only',
'males_only',
'postgraduates_only',
'students_only',
'offer_id_drop2',
'rental_type',
'title',
'zip_code_scraped']


##Dropping columns that are unnessecary (such as: duplicates, empty columns,..)
df = df.drop(
        columns= ['Unnamed', 	
'admin_fee_exact_value', 
'admin_fee_currency',
'deposit_type_drop', 	
'deposit_currency', 		
'cost_per_extra_guest_currency', 	
'offer_price_currency', 	 	
'offer_id_drop', 	
'city',
'property_floors_accum', 	
'neighborhood_id_drop', 	
'property_rules_cum', 	
'units_cum', 	
'neighborhood_drop',
'offer_id_drop2'])

# Drop duplicate offer_id's
df.drop_duplicates(subset=['offer_id'], keep=False)

# Check number of rows in the dataframe: 2938
df.shape[0]

# Check for total nullvalues and relative amount of null values in relation to row number
null_values = df.isnull().sum().to_frame()
null_values['NaN percentage']=null_values.values/df.shape[0]
null_values

# Correcting monetary values
df['admin_fee'] = df['admin_fee']/100
df['deposit_amount'] = df['deposit_amount']/100
df['cost_per_extra_guest'] = df['cost_per_extra_guest']/100
df['offer_price'] = df['offer_price']/100

# Create new column for cleaning T/F - we are more interested in whether or not there is cleaning than in the regularity
for i in df.index:
    if df.at[i,'cleaning_period'] is not np.nan:
        df.at[i,'cleaning'] = True

df.drop(columns='cleaning_period',inplace=True)

# Set deposit amount for listings where deposit amount is equal to first payment equal to first rent payment 
for i in df.index:
    if df.at[i,'deposit_type'] == 'equal-to-first-payment':
        df.at[i,'deposit_amount'] = df.at[i,'offer_price']
        
df.drop(columns = 'deposit_type', inplace=True)

#Set monthly commission rate
df['commission_amount'] = df['commission_rate'] * df['offer_price']

# Aggregate landlord response information to a single value: landlord response rate
df['landlord_response_rate'] = ( df['landlord_prev_accepted_bookings'] + df['landlord_prev_rejected_bookings'] ) / df['landlord_prev_requested_bookings'] 
# Drop the old columns
df = df.drop(['landlord_prev_accepted_bookings' , 'landlord_prev_rejected_bookings' , 'landlord_prev_requested_bookings'], axis = 1)

## Format creation date to a DATE
## NEEDS TO BE CONVERTED TO YEAR!
df['creation_date'] = df['creation_date'].astype(str).str[:-8]
df['creation_date'] = pd.to_datetime(df['creation_date'])

## Create boolean for double bed y/n
for idx, values in df.iterrows():
    if df.at[idx,'double_beds'] >0:
        df.at[idx,'double_bed'] = True
    if df.at[idx,'double_beds'] == 0:
        df.at[idx,'double_bed'] = False
 
# Create a log_price variable
df['log_offer_price'] = df['offer_price'].apply(np.log)    

#%% Encoding certain variables for exploration purposes
# Contract type
dict_contract_type = {'fortnight':1, 'nightly':2, 'monthly':3, 'fixed-unitary':4, 'fixed':5}
df['contract_type'].replace(dict_contract_type, inplace=True)

# Cancellation policy
dict_cancellation_policy={'flexible':1,'moderate':2, 'strict':3,'super-strict':4}
df['cancellation_policy'].replace(dict_cancellation_policy, inplace=True)

# Accomodation type
dict_accomodation_type={'private':1,'hostel':2, 'residence':3,}
df['accomodation_type'].replace(dict_accomodation_type, inplace=True)

# Building type
df['property_type'].unique()
dict_building_type={'house':1,'apartment':2, 'studio':3,}
df['property_type'].replace(dict_building_type, inplace=True)

# Rental type
df['rental_type'].unique()
dict_rental_type = {'property':1,'unit':2,'subunit':3}
df['rental_type'].replace(dict_rental_type, inplace=True)

# Fix units

# Aggregate landlord information to a single field indicating whether landlord lives in the flat
#--> not working
#df['landlord_residant'] = df['landlord_residant_age'] 
#df.loc[df['landlord_residant'] != np.nan]['landlord_residant'] = 'True'
#
#df = df.drop(['landlord_residant_age','landlord_residant_occupation','landlord_residant_gender'],axis=1)


# Aggregate energy expenses (water,electricity,gas) to a single field noting whether all expenses are included in the price
for idx, values in df.iterrows():
    if df.at[idx,'electricity_included'] == True and df.at[idx,'gas_included'] == True and df.at[idx,'water_included'] == True:
        df.at[idx,'all_expenses_included'] = True
    else:
        df.at[idx,'all_expenses_included'] = False

df.drop(columns=['electricity_included','gas_included','water_included'], inplace=True)

# Drop columns with too many null values, as it is difficult to make any inference about these value
null_values
df.drop(null_values[null_values['NaN percentage']>=0.3].index,inplace=True,axis=1)


df.dtypes

# Inspect amount of values that are 0 in dataframe per column
zeros = (df == 0).sum(axis=0).to_frame()
zeros['NaN percentage']=zeros.values/df.shape[0]
zeros

# Drop columns with too many 0's - assuming that this is not useful for our analysis as data are too similarly distributed
df.drop(zeros[zeros['NaN percentage']>=0.9].index,inplace=True,axis=1)

# Drop non-boolean with too many 0's
df.drop(columns = ['accomodation_area','admin_fee','exclusive'], inplace=True)


# Scrape Lisbon zip-codes
from bs4 import BeautifulSoup as soup
from requests import get

url='https://worldpostalcode.com/portugal/lisboa/'
response = get(url)
print(response.text)
html_soup = soup(response.text,'lxml')
type(html_soup)
zip_codes=html_soup.find_all('div', {'class' : 'rightc'})
zip_codes
lisbon_zipcodes = zip_codes[0].text
lisbon_zipcodes=[lisbon_zipcodes[i:i+8] for i in range(0, len(lisbon_zipcodes), 8)]
lisbon_zipcodes

# if scraped zip code is null, take original zip code
df['zip_code_scraped']=df['zip_code_scraped'].fillna(df['postal_code'])

#Check whether zip-code is in lisbon_zipcodes and flag rows
df['Lisbon'] = df['zip_code_scraped'].isin(lisbon_zipcodes)

# Drop all data where zip code is not in Lisbon
df= df[df['Lisbon']==True]

df.drop(columns = ['Lisbon','postal_code'],inplace=True)


#test = df[['double_bed','rental_type']]
#
#df[(df['double_bed']==True) & (df['rental_type']=='subunit')]


# Change in dataset size
# Rows
row_change = (df.shape[0] - original_rows)/original_rows
row_change
# columns
column_change = (df.shape[1] - original_columns)/original_columns
column_change


df.to_csv('C:/Users/jojo/Documents/Uni/Intro to Programming/Group Project/ip_project/Clean Files/CSV/Cleaned_Data_2311.csv')

##############################
#### Geopy Data Inclusion ####
##############################

#%% 
#### Find Lisbon ZIP Codes####
from bs4 import BeautifulSoup as soup
from requests import get

#url='https://worldpostalcode.com/portugal/lisboa/'
#response = get(url)
#print(response.text)
#html_soup = soup(response.text,'lxml')
#type(html_soup)
#zip_codes=html_soup.find_all('div', {'class' : 'rightc'})
#zip_codes
# n = 8 
#lisbon_zipcodes = zip_codes[0].text
#lisbon_zipcodes=[lisbon_zipcodes[i:i+n] for i in range(0, len(lisbon_zipcodes), n)]
#

# Check whether zip-code is in lisbon_zipcodes and flag rows
#df['Lisbon'] = df['postal_code'].isin(lisbon_zipcodes)

# Drop all data where zip code is not in Lisbon
#df= df[df['Lisbon']==True]
#df.shape[0]

df = pd.read_csv('C:/Users/jojo/Documents/Uni/Intro to Programming/Group Project/ip_project/Clean Files/CSV/Cleaned_Data_2311.csv')

### Closeness to subway station #####
# Create raw string of subway stations from wikipedia
subways_raw = 'Reboleira Blue Line,Amadora Este Blue Line,Alfornelos Blue Line,Pontinha Blue Line,Carnide Blue Line,Colégio Militar/Luz Blue Line,Alto dos Moinhos Blue Line,Laranjeiras Blue Line,Jardim Zoológico Blue Line,Praça de Espanha Blue Line,Parque Blue Line,Marquês de Pombal Blue Line,Avenida Blue Line,Restauradores Blue Line,Baixa/Chiado Blue Line,Terreiro do Paço Blue Line,Santa Apolónia Blue Line,Odivelas Yellow Line,Senhor Roubado Yellow Line,Ameixoeira Yellow Line,Lumiar Yellow Line,Quinta das Conchas Yellow Line,Campo Grande Yellow Line,Cidade Universitária Yellow Line,Entrecampos Yellow Line,Campo Pequeno Yellow Line,Saldanha Yellow Line,Picoas Yellow Line,Rato Yellow Line,Telheiras Green Line,Alvalade Green Line,Roma Green Line,Areeiro Green Line,Alameda Green Line,Arroios Green Line,Anjos Green Line,Intendente Green Line,Martim Moniz Green Line,Rossio Green Line,Cais do Sodré Green Line,Olaias Red Line,Bela Vista Red Line,Chelas Red Line,Olivais Red Line,Cabo Ruivo Red Line,Oriente Red Line,Moscavide Red Line,Encarnação Red Line,Aeroporto Red Line,São Sebastião'

# convert string to list
subways_raw = subways_raw.split(",")

import unicodedata
# encode ascii to utf-8 in order to be able to pass them into the url
subways_clean = []
for i in subways_raw:
    i = unicodedata.normalize('NFD', i).encode('ascii', 'ignore').decode("utf-8")
    subways_clean.append(i)

# Scrape subway addresses from google maps for each subway station into list
import json
subways = []

for i in subways_clean:
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=Estacao+'+i.replace(' ','+')+'Lisbon+Metro+Station&key=AIzaSyB8DK7OZa7y-zYlBMKAhYWOuUidUeHw4ec'
    from urllib.request import urlopen
    jsonurl = urlopen(url)

    text = json.loads(jsonurl.read())
    subways.append({'name':i.replace('+',' '), 'neighborhood':text['results'][0]['formatted_address'],'lat':text['results'][0]['geometry']['location']['lat'], 'lng':text['results'][0]['geometry']['location']['lng']})
    

# Calculate distance of each appartment with all subway stations
import geopy.distance


for idx, value in df.iterrows():
    coords_apartm = (df.at[idx,'latitude'],df.at[idx,'longitude'])
    for i in range(len(subways)):
        coords_sub = (subways[i]['lat'],subways[i]['lng'])
        df.at[idx,subways[i]['name']] = geopy.distance.distance(coords_apartm, coords_sub).km

df_subways = df.iloc[:,53:]
    
df['subways within 0.5 km'] = df_subways[df_subways<= 0.5].count(axis=1)
df['closest subway'] = df_subways.min(axis=1)


##### Distances to universities
universities_raw='University of Lisbon,Nova University of Lisbon,Nova School of Business and Economics, Universidade Católica Portuguesa,Instituto Politécnico de Lisboa,Universidade Lusófona de Humanidades e Tecnologias,ISCTE – University Institute of Lisbon,Instituto Superior Técnico'
universities_raw =universities_raw.split(",")

# encode ascii to utf-8 in order to be able to pass them into the url
universities_clean = []
for i in universities_raw:
    i = unicodedata.normalize('NFD', i).encode('ascii', 'ignore').decode("utf-8")
    universities_clean.append(i)

# Scrape university addresses from google maps for each subway station into list
import json
universities = []

for i in universities_clean:
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+i.replace(' ','+')+'Lisbon+address&key=AIzaSyB8DK7OZa7y-zYlBMKAhYWOuUidUeHw4ec'
    from urllib.request import urlopen
    jsonurl = urlopen(url)

    text = json.loads(jsonurl.read())
    universities.append({'name':i.replace('+',' '), 'neighborhood':text['results'][0]['formatted_address'],'lat':text['results'][0]['geometry']['location']['lat'], 'lng':text['results'][0]['geometry']['location']['lng']})


for idx, value in df.iterrows():
    coords_apartm = (df.at[idx,'latitude'],df.at[idx,'longitude'])
    for i in range(len(universities)):
        coords_uni = (universities[i]['lat'],universities[i]['lng'])
        df.at[idx,universities[i]['name']] = geopy.distance.distance(coords_apartm, coords_uni).km

df_universities = df.iloc[:,105:]
       
df['universities within 0.5 km'] = df_universities[df_universities<= 0.5].count(axis=1)
df['closest university'] = df_universities.min(axis=1)


## Distance to attractions
attractions_raw='Belém Tower,Jerónimos Monastery,São Jorge Castle,Praça do Comércio,Rossio Square,Santa Justa Lift,Lisbon Oceanarium,Padrão dos Descobrimentos,Christ the King,Carmo Convent,Church of Santa Engrácia,Lisbon Cathedral,Eduardo VII Park,Lisbon Zoo,Miradouro de São Pedro de Alcântara,Miradouro da Senhora do Monte,Ascensor da Glória,LxFactory'

attractions_raw =attractions_raw.split(",")

# encode ascii to utf-8 in order to be able to pass them into the url
attractions_clean = []
for i in attractions_raw:
    i = unicodedata.normalize('NFD', i).encode('ascii', 'ignore').decode("utf-8")
    attractions_clean.append(i)

# Scrape university addresses from google maps for each subway station into list
import json
attractions = []

for i in attractions_clean:
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+i.replace(' ','+')+'Lisbon+address&key=AIzaSyB8DK7OZa7y-zYlBMKAhYWOuUidUeHw4ec'
    from urllib.request import urlopen
    jsonurl = urlopen(url)

    text = json.loads(jsonurl.read())
    attractions.append({'name':i.replace('+',' '), 'neighborhood':text['results'][0]['formatted_address'],'lat':text['results'][0]['geometry']['location']['lat'], 'lng':text['results'][0]['geometry']['location']['lng']})


for idx, value in df.iterrows():
    coords_apartm = (df.at[idx,'latitude'],df.at[idx,'longitude'])
    for i in range(len(attractions)):
        coords_attr = (attractions[i]['lat'],attractions[i]['lng'])
        df.at[idx,attractions[i]['name']] = geopy.distance.distance(coords_apartm, coords_attr).km

df_attractions = df.iloc[:,115:]
       
df['attractions within 0.5 km'] = df_attractions[df_attractions<= 0.5].count(axis=1)
df['closest attraction'] = df_attractions.min(axis=1)


df.iloc[:,52]

df_final =df.iloc[:,:52]
df_distances=df[['subways within 0.5 km','closest subway','universities within 0.5 km','closest university','attractions within 0.5 km','closest attraction']]


df_final['subways within 0.5 km']=df_distances['subways within 0.5 km']
df_final['universities within 0.5 km']=df_distances['universities within 0.5 km']
df_final['attractions within 0.5 km']=df_distances['attractions within 0.5 km']
df_final['closest subway']=df_distances['closest subway']
df_final['closest attraction']=df_distances['closest attraction']
df_final['closest university']=df_distances['closest university']

df_final.to_csv('C:/Users/jojo/Documents/Uni/Intro to Programming/Group Project/ip_project/Clean Files/CSV/Cleaned+Geo_Data_2311.csv')


######################################
#### Neighbourhood Categorization ####
######################################

#%% Data Import
df = pd.read_csv('C:\\Users\\mariu\\OneDrive\\Dokumente\\NOVA\\Semerster 1\\02_Introduction to Programming\\04_Project\\ip_project\\Clean Files\\CSV\\Cleaned+Geo_Data_2311.csv')

#%%
freq = df.groupby('neighborhood').count()['offer_id']
mean = df.groupby('neighborhood').mean()['offer_price']
cluster = pd.concat([freq, mean], axis=1)
cluster['neighborhood'] = cluster.index
cluster.columns = ['freq', 'offer_price','neighborhood']
cluster.describe()

#%% low price and low frequency neighborhoods
cluster_temp = cluster[cluster.offer_price < 665]
cluster1 = cluster_temp[cluster_temp.freq <32]
cluster1.index

#%% low price and high frequency neighborhoods
cluster_temp = cluster[cluster.offer_price < 665]
cluster2 = cluster_temp[cluster_temp.freq > 32]
cluster2.index

#%% high price and low frequency neighborhoods
cluster_temp = cluster[cluster.offer_price > 665]
cluster3 = cluster_temp[cluster_temp.freq <32]
cluster3.index

#%% high price and high frequency neighborhoods
cluster_temp = cluster[cluster.offer_price > 665]
cluster4 = cluster_temp[cluster_temp.freq >=32]
cluster4.indexdef get_group(x):
    if x in cluster1.index:
        return 'low_price_low_freq'
    elif x in cluster2.index:
        return 'low_price_high_freq'
    elif x in cluster3.index:
        return 'high_price_low_freq'
    else:
        return 'high_price_high_freq'
df['cluster'] = df.neighborhood.apply(get_group)


##########################
#### Data Exploration ####
##########################

#%%Imports
import pandas as pd
import seaborn as sns
import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np

#%% Data Import
df = pd.read_csv('C:\\Users\\mariu\\OneDrive\\Dokumente\\NOVA\\Semerster 1\\02_Introduction to Programming\\04_Project\\ip_project\\Clean Files\\CSV\\Cleaned+Geo_Data_2311.csv')

#%% additional cleaning

df = df.drop(['Unnamed: 0'],axis=1)

#%% 

# Check null values
null_values = df.isnull().sum()

# Getting an initial statistical summary
stats_summary = df.describe()

#%% Variable exploration

#mapping the offers on a map trying to detect favourable neighbourhoods
cmap = sns.cubehelix_palette(dark=.3, light=.8, as_cmap=True)
ax = sns.scatterplot(x="longitude", y="latitude",hue="offer_price", size="offer_price",sizes=(20, 200), data=df)
ax = ax.set(xlim=(-9.26,-9), ylim=(38.69,38.81))

#%% Variable exploration

#mapping the distribution and relation of selected variables  accom. Types: "{'private':1 | 'hostel':2 | 'residence':3,}"
df_pairpl = df[['offer_price','commission_amount','deposit_amount','minimum_no_night','closest university']].copy()
sns.pairplot(df_pairpl, size=2.5);

#%% Neighbourhood influence on prices - are the neighbourhood 

    #high priced, low frequency
    sns.boxplot(x="high_price_low_freq", y="offer_price", data=df)
    
    #%% high priced, high frequency
    sns.boxplot(x="high_price_high_freq", y="offer_price", data=df)
    
    #%% low priced, low frequency
    sns.boxplot(x="low_price_low_freq", y="offer_price", data=df)
    
    #%% low priced, high frequency
    sns.boxplot(x="low_price_high_freq", y="offer_price", data=df)

#%% Bed number and types influence on price
    
sns.boxplot(x="single_beds", y="offer_price", data=df)
sns.boxplot(x="double_beds", y="offer_price", data=df)
sns.boxplot(x="double_bed", y="offer_price", data=df)


#%% influence of housetype on price
with sns.axes_style(style='ticks'):
    g = sns.factorplot("property_type", "offer_price", data=df, kind="box")
    g.set_axis_labels("{'house':1 | 'apartment':2 | 'studio':3,}","offer price");
        
#%% influence of propertytype on price
with sns.axes_style(style='ticks'):
    g = sns.factorplot("rental_type", "offer_price", data=df, kind="box")
    g.set_axis_labels("{'property':1 | 'unit':2 |'subunit':3}","offer price");
    

#%% influence of accomodationtype on price
with sns.axes_style(style='ticks'):
    g = sns.factorplot("accomodation_type", "offer_price", data=df, kind="box")
    g.set_axis_labels("{'private':1 | 'hostel':2 | 'residence':3,}","offer price");

#%% correlations 

#extracting relevant variables
df_corr = df[['offer_price','double_beds','single_beds','closest university','property_type','high_price_high_freq','high_price_low_freq','low_price_high_freq','low_price_low_freq']].copy()

# plotting the correlations
corr = df_corr.corr()
sns.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values)


#%% Possible TO DO
# 0 value distribution
# Selecting variables with common sense that should have an influence on the price


####################
#### Regression ####
####################


import pandas as pd
import seaborn as sns
import matplotlib as plt
import numpy as np




df = pd.read_csv('C:/Users/jojo/Documents/Uni/Intro to Programming/Group Project/ip_project/Clean Files/CSV/Cleaned+Geo_Data_2311.csv')

# Form neighborhood clusters
freq = df.groupby('neighborhood').count()['offer_id']
mean = df.groupby('neighborhood').mean()['offer_price']
cluster = pd.concat([freq, mean], axis=1)
cluster['neighborhood'] = cluster.index
cluster.columns = ['freq', 'offer_price','neighborhood']
cluster.describe()

mean_price=688
mean_freq=34

# low price and low frequency neighborhoods
cluster_temp = cluster[cluster.offer_price < mean_price]
cluster1 = cluster_temp[cluster_temp.freq < mean_freq]
cluster1.index

# low price and high frequency neighborhoods
cluster_temp = cluster[cluster.offer_price < mean_price]
cluster2 = cluster_temp[cluster_temp.freq >= mean_freq]
cluster2.index

# high price and low frequency neighborhoods
cluster_temp = cluster[cluster.offer_price > mean_price]
cluster3 = cluster_temp[cluster_temp.freq < mean_freq]
cluster3.index


# high price and high frequency neighborhoods
cluster_temp = cluster[cluster.offer_price > mean_price]
cluster4 = cluster_temp[cluster_temp.freq >= mean_freq]
cluster4.index


def get_group(x):
    if x in cluster1.index:
        return 'low_price_low_freq'
    elif x in cluster2.index:
        return 'low_price_high_freq'
    elif x in cluster3.index:
        return 'high_price_low_freq'
    else:
        return 'high_price_high_freq'
df['cluster'] = df.neighborhood.apply(get_group)

# show null values
null_values = df.isnull().sum()
null_values

# show 0 values
zeros = (df == 0).sum(axis=0).to_frame()
zeros['NaN percentage']=zeros.values/df.shape[0]
zeros

# Drop columns that either 
# a) depend directly on the offer price (commission_amount, deposit_amount)
# or are redundant (e.g. single beds, double beds, closest uni..)
df.drop(columns = ['commission_amount','deposit_amount','single_beds','double_beds','subways within 0.5 km','closest university','closest attraction'], inplace=True)

# drop non-boolean columns with high amount of 0 values since these don't tell us anything
df.drop(columns = ['exclusive'],inplace=True)

# fill nan booleans with median and convert to bool
for i in ['kitchen_window','pets_allowed','smoking_allowed','overnight_guests_allowed','kitchen_fridge','kitchen_stove','landlord_response_rate','double_bed','bedroom_balcony','kitchen_freezer','kitchen_microwave','kitchen_oven','bedroom_window','cleaning','kitchen_washing-machine']:
    df[i].fillna((df[i].median()), inplace=True)
    df[i] = df[i].astype(bool)


df.dtypes
# Plot correlations
corr = df.corr()
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)


# Calulate a new metric: bathroom_per_person
df['bathrooms_per_person'] =  round(df['number_of_bathrooms']/df['number_of_bedrooms'],2)

df['bathrooms_per_person'].replace([np.inf, -np.inf],np.nan,inplace=True)

# more fancy imputing method??
df['bathrooms_per_person'].fillna((df['bathrooms_per_person'].mean()), inplace=True)

# Check which variables are correlated with the price
corr_matrix = df.corr().abs()
corr_matrix["log_offer_price"].sort_values(ascending=False)


# Take the most important variables into a dataframe
df.isnull().sum()
df_regress=df[['rental_type','bathrooms_per_person','number_of_bedrooms','double_bed','cluster','closest subway','cleaning','internet_included','all_expenses_included','bedroom_window','bedroom_balcony']]
df_regress=df[['rental_type','bathrooms_per_person','number_of_bedrooms','double_bed','cluster']]


# Create dummies for categorical values
n = pd.get_dummies(df['rental_type'],prefix='rental_type')
df_regress = pd.concat([df_regress, n], axis=1)
m = pd.get_dummies(df['cluster'],prefix='neighborhood_type')
df_regress = pd.concat([df_regress, m], axis=1)
#h = pd.get_dummies(df['contract_type'],prefix='contract_type')
#df_regress = pd.concat([df_regress, h], axis=1)
df_regress.drop(columns = ['rental_type','cluster'],inplace=True)



### Multi-variate regression
from sklearn import linear_model
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

#select the variable we are trying to predict
df_y = df[['log_offer_price']].copy()

# Select the regression model
reg = linear_model.LinearRegression()

# Create a training and a testing set
x_train, x_test, y_train, y_test = train_test_split(df_regress,df_y,test_size = 0.2, random_state = 4)

#regression analysis
reg.fit(x_train,y_train)
reg.coef_
reg.intercept_

# Save predicted prices to the dataframe
df['predicted_price_multivariate']=np.exp(reg.predict(df_regress))

# Observe the difference in predicted and actual price
test = df[['predicted_price_multivariate','offer_price']]
y_pred = reg.predict(df_regress)
reg.score(x_test,y_test)



# Random Forest Refressor
from sklearn.ensemble import RandomForestRegressor

forest_reg = RandomForestRegressor(random_state=42)
forest_reg.fit(x_train,y_train)
forest_reg.score(x_test,y_test)

# Save estimated prices to dataframe
df['predicted_price_randomforest']=np.exp(forest_reg.predict(df_regress))
# Observe difference to actual price
test = df[['offer_price','predicted_price_randomforest']]



# Gradient Boosting Regressor
from sklearn import ensemble
from sklearn.ensemble import GradientBoostingRegressor
model = ensemble.GradientBoostingRegressor(n_estimators=800,max_depth=5,min_samples_split=2,learning_rate=0.1,loss='ls')
model.fit(x_train,y_train)
model.score(x_test,y_test)

# Save estimated prices to dataframe
df['predicted_price_gradientboost']=np.exp(model.predict(df_regress))
# Observe difference to actual price
df[['predicted_price_gradientboost','offer_price']]


## XG Boost
import xgboost

#most_relevant_features
best_xgb_model = xgboost.XGBRegressor(colsample_bytree=0.4,
                 gamma=0,                 
                 learning_rate=0.07,
                 max_depth=3,
                 min_child_weight=1.5,
                 n_estimators=10000,                                                                    
                 reg_alpha=0.75,
                 reg_lambda=0.45,
                 subsample=0.6,
                 seed=42)
# Train and test the model
best_xgb_model.fit(x_train,y_train)
best_xgb_model.score(x_test,y_test)

df['predicted_price_gxboost']=np.exp(best_xgb_model.predict(df_regress))


# Comparison between real price and all predicted prices
Results = df[['offer_price','predicted_price_multivariate','predicted_price_randomforest','predicted_price_gradientboost','predicted_price_gxboost']]

