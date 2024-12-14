from utils import get_oauth_token, search_properties, filter_properties, update_database
from bot import get_bot_token, get_chat_id, send_telegram_message
from gdrive_utils import download_from_google_sheets, upload_to_google_sheets
from tqdm import tqdm
import json

def main():

    root_path = "./code"

    since_date = "M" # M: last month, for initial search. W: last week for recurrent searches
    pages_to_search = (1, 1)  # Adjust the range as needed

    gdrive_link = "https://docs.google.com/spreadsheets/d/1R5gFw0DfeP6-26EXVVIaL-u-3fTXsKrpLWCJVJ2yY2A/edit?usp=sharing"

    # Download existing database from Google Sheets
    spreadsheet_id = '1R5gFw0DfeP6-26EXVVIaL-u-3fTXsKrpLWCJVJ2yY2A'
    sheet_name = 'Sheet1'
    df_existing = download_from_google_sheets(spreadsheet_id, sheet_name)
    
    '''
    # Search
    all_properties = []
    for page in tqdm(range(pages_to_search[0], pages_to_search[1] + 1)):
        properties = search_properties(page, since_date)
        all_properties.extend(properties)

    # DEBUG
    # Saving the list of dictionaries to a JSON file
    with open('./data.json', 'w') as json_file:
        json.dump(all_properties, json_file, indent=4)
    '''

    # Reading the list of dictionaries from the JSON file
    with open(f'{root_path}/data.json', 'r') as json_file:  # DEBUG
        all_properties = json.load(json_file)
    
    # Filter properties
    filtered_properties = filter_properties(all_properties)

    # Update database
    df_updated = update_database(filtered_properties, df_existing)

    # Upload database to Google Sheets
    upload_to_google_sheets(df_updated, spreadsheet_id, sheet_name)

    number_new_flats = len(df_updated) - len(df_existing)

    # Summary message
    if number_new_flats>0:
        message = f"Database updated! There are {len(number_new_flats)} new flats. Link {gdrive_link}."
    else:
        message = f"No new flats. Link {gdrive_link}."

    # Send Telegram message
    bot_token = get_bot_token()
    chat_id = get_chat_id()
    send_telegram_message(bot_token, chat_id, message)
    

if __name__ == "__main__":
    main()
