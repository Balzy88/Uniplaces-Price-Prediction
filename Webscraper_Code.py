## WEB SCRAPER ###
import requests
import pandas as pd
from pandas.io.json import json_normalize

# Create columns and dataframes for the coming data
url = []
properties =[]
offers = []
units = []
titles = []
metadata = pd.DataFrame()
df = pd.DataFrame()

# Loop over all pages on uniplaces with the specific parameters of Lisbon. 
# Get the json response of the website and save it in a temporary variable
for i in range(1,140):
    resp = requests.get(
        url = 'https://www.uniplaces.com/api/search/offers', 
        params = {
            "city":'PT-lisbon',
            "limit":'24',
            "locale":'en_GB',
            "ne":'38.804935133335775%2C-9.076080322265625',
            "page":i,
            "sw":'38.67880960144873%2C-9.295806884765625',
               
        })
    body = resp.json()
    base_url = 'https://www.uniplaces.com/accommodation/lisbon'
# from the json response, extract the property id, offer id, title of the offer and the rental type
    for t in body['data']:
        properties.append(t['attributes']['property']['id'])
        offers.append(t['id'])
        units.append(t['attributes']['property']['rent_by'])
        titles.append(t['attributes']['accommodation_offer']['title'])
        url.append(t['id'])

# Convert the lists to columns in the pandas dataframe
metadata['offer_id'] = offers      
metadata['units'] = units
metadata['title'] = titles
metadata['offer_id'] = metadata['offer_id'].astype(int)

# Save the result to a CSV
metadata.to_csv('C:/Users/bryan/Documents/Uni/Intro to Programming/Group Project/ip_project/uniplaces_metadata.csv')
       



# GraphQL Introspection query for the uniplaces API 
       
import requests

query = """
 query IntrospectionQuery {
    __schema {
      queryType { name }
      types {
        ...FullType
      }
      directives {
        name
      }
    }
  }

  fragment FullType on __Type {
    name
    fields(includeDeprecated: false) {
      name

    }
    inputFields {
      ...InputValue
    }
  }

  fragment InputValue on __InputValue {
    name
  }

"""

resp = requests.post(
    'https://offer-aggregate-graphql.uniplaces.com/graphql', 
    json= {
        "query": query}
)

body = resp.json()
print(body)


  
# For each URL (individual page): query the listing specifications via a GraphQL query from the uniplaces GraphQL API
len(url)
len(set(url))        

for i in ((set(url))):
    print(i)
    df_kitchen = pd.DataFrame()
    df_bathroom = pd.DataFrame() 
    df_rules = pd.DataFrame() 
    df_bedroom = pd.DataFrame() 
    df_living_room = pd.DataFrame()

    id = i
    query = """
        query($id: ID!) { 
            offerAggregate(id: $id) { 
                accommodation_offer {
                        id
                    contract {
                            type
                            exclusive
                            is_instant_booking
                            commission
                            deposit{
                                pay_to
                                type
                                value{
                                        amount
                                        currency_code}
                    }
                            admin_fee {
                            exact_value
                            value {
                                    amount
                                    currency_code}}
                          fixed_unitary
                          {
                            extra_per_guest
                            {
                                  amount
                                  currency_code}
                          }
                    
                    }
                    reference_price {
                        amount
                        currency_code
                    }
                    requisites {
                        conditions {
                            cancellation_policy
                            minimum_nights
                            max_guests
                        }
                    }
                    costs {
                            bills {
                                    water {
                                            included
                                            }
                                    electricity {
                                            included
                                            }
                                    gas {
                                            included
                                            }
                                    internet {
                                            included
                                            }
                                    }
                            services {
                                    cleaning
                                    {
                                            periodicity
                                            }
                                    }
                    }
                }
                accommodation_provider
                {
                stats{
                        bookings{
                                accepted{
                                        total}
                                requested{
                                        total}
                                rejected{
                                        total}
                                confirmed{
                                        total}}}
                created{
                        at
                                }
                
                
                }
                id
                units_sorted{unit_id
                __typename}
                property_aggregate {
                    property {
                        id
                        landlord_resident {
                                gender
                                age_range
                                occupation
                        }
            
                        floors {
                                units {
                                        id
                                        type_code
                                        features{Code Exists}
                                        subunits{id
                                        type_code
                                        features
                                        {Code
                                        Exists
                                        }}
                        }
                        }
                        rules {
                                code
                                exists
                        }
                        typology {
                            area
                            accommodation_type_code
                            type_code
                            number_of_bedrooms
                            number_of_bathrooms
                        }
                        location {
                                neighborhood_id
                                geo{
                                    latitude
                                    longitude
                                    }
                        address {
                                postal_code
                                
                                }
                        }
                        verification {
                        verified}
                    
                    }
                        neighborhood{id
                        city_code
                        slug
                        }
                }
                
            } 
        }
    """
    
    resp = requests.post(
        'https://offer-aggregate-graphql.uniplaces.com/graphql', 
        json={
            "query": query,
            "variables": {
                "id": id
            }
        }
    )
    json = resp.json()
    json
    
    # Save the json response into a pandas dataframe
    i = pd.DataFrame.from_dict(json_normalize(resp.json()), orient='columns')
    
    
    # Since the json response is not 'clean' and still contains lists of dictionaries, we have to access the lists and assign the variables to dataframe columns
    # bedroom: in cases where the bedroom unit_id matches the firs unit in the units_sorted list: we can assign this bedroom as the bedroom of this listing
    # in other cases, bedroom information is not given or it is unclear which bedroom the listing is referring to
    units = json['data']['offerAggregate']['property_aggregate']['property']['floors'][0]['units']
    for u in units:
        if u['type_code'] == 'bedroom' and u['id']==json['data']['offerAggregate']['units_sorted'][0]['unit_id'] :
            bedroom_dict = u
            break
        else:
            bedroom_dict = {}
    
                
# assign False and then True if it is true for any bathroom
# since there are several bathrooms it is hard to assign other values to it (e.g. windows) We can assume there is a toilet so only additional feature is bathtub
# Each property can have several bathrooms, so we loop through the units that are a bathroom
# Only important characteristic for is the bathtub
    bathroom_dict = {}             
    for u in units:
        if u['type_code'] == 'bathroom':
            bathr=u
            if bathr['features'] is not None:
                for item in bathr['features']:
                    if item['Code'] == 'bathtub' and item['Exists'] == True:
                        bathroom_dict['bathroom_bathtub'] =  True
                                   

        
    for u in units: 
        if u['type_code'] == 'living-room':
            living_room_dict = u
            break
        else:
            living_room_dict= {}
  
            
    for u in units: 
        if u['type_code'] == 'kitchen':
            kitchen_dict = u
            break
        else:
            kitchen_dict= {}
   

    if kitchen_dict: 
        if kitchen_dict['features'] is not None:
            df_kitchen = json_normalize({('kitchen_' + item['Code']):item['Exists'] for item in kitchen_dict['features']})
    
        
    if bedroom_dict:
        
        if bedroom_dict['features'] is not None: 
            df_bedroom = json_normalize({('bedroom_' + item['Code']):item['Exists'] for item in bedroom_dict['features']})
    
        if bedroom_dict['subunits'] is not None:
            bedr = bedroom_dict['subunits']
            list_sb = []
            for u in bedr:
                if u['type_code'] == 'single-bed':
                    list_sb.append(u)
            df_bedroom['single_beds'] = len(list_sb)
            list_db = []
            for u in bedr:
                if u['type_code'] == 'double-bed':
                    list_db.append(u)
            df_bedroom['double_beds'] = len(list_db)
    
            bathr = bedroom_dict['subunits']
            for u in bathr:
                if u['type_code'] == 'bathroom':
                    df_bedroom['private_bathroom'] = True
                    break
            
    if bathroom_dict:
            for item in bathroom_dict:
                df_bathroom = pd.DataFrame([bathroom_dict])
                
                
        
    if living_room_dict: 
        if living_room_dict['features'] is not None:
            df_living_room = json_normalize({('living_room_' + item['Code']):item['Exists'] for item in living_room_dict['features']})

   
    if json['data']['offerAggregate']['property_aggregate']['property']['rules'] is not None:
        rules_dict = json['data']['offerAggregate']['property_aggregate']['property']['rules']
        df_rules = json_normalize({(item['code']):item['exists'] for item in rules_dict})
    else:
        rules_dict = {'pets-allowed':False,'smoking-allowed':False,'overnight-guests-allowed':False}
        df_rules = pd.DataFrame(rules_dict, columns = ['pets-allowed','smoking-allowed','overnight-guests-allowed'], index=[0] )

    df_result = pd.concat([i,df_kitchen, df_bathroom, df_rules, df_bedroom, df_living_room],axis=1)

    df = df.append(df_result, sort=False)
    
    df[['data.offerAggregate.id','single_beds','double_beds']]

# Convert both offer_id's to integers to be able to merge
df['data.offerAggregate.id']=df['data.offerAggregate.id'].astype(int)
metadata['offer_id']=metadata['offer_id'].astype(int)
df = df.merge(metadata,how='left',left_on='data.offerAggregate.id', right_on='offer_id')
  
df.to_csv('C:/Users/bryan/Documents/Uni/Intro to Programming/Group Project/ip_project/Clean Files/Scraped_Data_2311.csv')
