import base64
import requests
import pandas as pd
import re

# Actual API key and secret
api_key = 'c6iblg41yrl9z9m184sle7ptgdniksqk'
secret = 'nvm2sQp5Txrg'

def get_oauth_token():
    # URL encode the API key and secret
    credentials = f"{api_key}:{secret}"
    
    # Base64 encode the credentials
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    # Set up the request headers
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    
    # Set up the request body
    data = {
        'grant_type': 'client_credentials',
        'scope': 'read'
    }
    
    # Make the POST request to get the token
    response = requests.post('https://api.idealista.com/oauth/token', headers=headers, data=data, verify=False)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response and return the access token
        return response.json().get('access_token')
    else:
        # Print the error and return None
        print(f"Error: {response.status_code} - {response.text}")
        return None

def search_properties(token, page_num):
    # Define the endpoint URL
    url = "https://api.idealista.com/3.5/es/search"

    # Define the search parameters
    params = {
        "country": "es",  # Spain
        "operation": "sale",
        "propertyType": "homes",
        "center": "40.394618,-3.753029",  # Approximate coordinates for Calle los Yebenes, Madrid
        "distance": 10000,  # meters
        "maxItems": 50,
        "numPage": page_num,
        "maxPrice": 150000,
        "minPrice": 90000,
        "sinceDate": "M",  # Last month
        "order": "price",
        "sort": "asc",
        "bedrooms": "2",  # At least 2 bedrooms
        "flat": True,
        "minSize": 50  # At least 50 m²
    }

    # Define the headers, including the authorization token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }

    # Make the API request
    response = requests.post(url, headers=headers, data=params, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse and return the JSON response
        return response.json().get('elementList', [])
    else:
        # Print the error and return an empty list
        print(f"Error: {response.status_code} - {response.text}")
        return []

def filter_properties(properties):
    # Words to filter out properties
    exclude_keywords = ["nuda", "alquilado", "alquilada", "no se puede", "ocupado", "okupado", "subasta", "ilegal"]
    filtered_properties = []

    for property in properties:
        # Check if description contains any exclusion keywords
        if 'description' not in property or any(re.search(keyword, property['description'], re.IGNORECASE) for keyword in exclude_keywords):
            continue

        # Check if the property has at least 3 pictures
        if property['numPhotos'] < 3:
            continue

        if "propertyCode" not in property:
            continue
        
        # Add property to the filtered list
        filtered_properties.append({
            'propertyCode': property['propertyCode'],
            'url': f"=HYPERLINK('{property.get('url', 'N/A')}')",
            'price': property.get('price', 'N/A'),
            'size': property.get('size', 'N/A'),
            'address': property.get('address', 'N/A'),
            'bedrooms': property.get('rooms', 'N/A'),
            'floor': property.get('floor', 'N/A'),
            'description': property.get('description', 'N/A')
        })

    return filtered_properties

def update_database(new_properties, db_file='db.xlsx'):
    try:
        # Load existing database
        df_existing = pd.read_excel(db_file)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty DataFrame
        df_existing = pd.DataFrame(columns=['propertyCode', 'url', 'price', 'size', 'address', 'bedrooms', 'floor'])

    # Convert to DataFrame
    df_new = pd.DataFrame(new_properties)

    # Merge new properties with existing database
    df_updated = pd.concat([df_existing, df_new]).drop_duplicates(subset='propertyCode', keep='first')

    # Save updated database
    df_updated.to_excel(db_file, index=False)