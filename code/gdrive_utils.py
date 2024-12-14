import os
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread

# Set up the Google Sheets API
def get_gspread_client():
    # Path to your service account key file
    SERVICE_ACCOUNT_FILE = '/Users/sanchr87/Library/CloudStorage/OneDrive-MedtronicPLC/Documents/idealista/code/idealista-444711-aec4a5e9d3c1.json'
    #SERVICE_ACCOUNT_FILE = os.getenv('GDRIVE_SERVICE_ACCOUNT')

    # Define the scopes
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # Authenticate using the service account file
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

def create_empty_df():
    df = pd.DataFrame(columns=['propertyCode', 'url', 'price', 'size', 'address', 'bedrooms', 'floor', 'description', 'Interested?', 'Contacted?'])
    print('Empty df created.')
    return df

def download_from_google_sheets(spreadsheet_id, sheet_name):
    client = get_gspread_client()
    try:
        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
        print('Spreadsheet found in GDrive.')

        # Convert the sheet to a DataFrame
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        
        if len(df)==0:
            df = create_empty_df()
            
    except:
        df = create_empty_df()
    return df

def upload_to_google_sheets(df, spreadsheet_id, sheet_name):
    # Use gspread to update the Google Sheet
    client = get_gspread_client()
    sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

    # Clear existing data
    sheet.clear()

    # Update with new data
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
