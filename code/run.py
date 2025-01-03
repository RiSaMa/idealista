from utils import search_properties, filter_properties, update_database
from bot import send_telegram_messages
from gdrive_utils import download_from_google_sheets, upload_to_google_sheets
from tqdm import tqdm

def main():

    since_date = "Y" # W:last week, M: last month, Y: last 2 days (sale and rooms)
    pages_to_search = (1, 3)  # Adjust the range as needed

    gdrive_link = "https://docs.google.com/spreadsheets/d/1R5gFw0DfeP6-26EXVVIaL-u-3fTXsKrpLWCJVJ2yY2A/edit?usp=sharing"

    # Download existing database from Google Sheets
    spreadsheet_id = '1R5gFw0DfeP6-26EXVVIaL-u-3fTXsKrpLWCJVJ2yY2A'
    sheet_name = 'Sheet1'
    df_existing = download_from_google_sheets(spreadsheet_id, sheet_name)
     
    # Search
    new_properties = []
    for page in tqdm(range(pages_to_search[0], pages_to_search[1] + 1)):
        properties = search_properties(page, since_date)
        if len(properties)==0:
            break
        new_properties.extend(properties)
    
    # Filter properties
    filtered_new_properties = filter_properties(new_properties)

    # Update database
    if len(filtered_new_properties):
        df_updated = update_database(filtered_new_properties, df_existing)

        # Upload database to Google Sheets
        upload_to_google_sheets(df_updated, spreadsheet_id, sheet_name)

        number_new_flats = len(df_updated) - len(df_existing)

        # Send Telegram messages (if new flats)
        if number_new_flats>0:
            message = f"Database updated! There are {number_new_flats} new flats ({len(new_properties)-len(filtered_new_properties)} were filtered out). Link {gdrive_link}."
            print(message)
            send_telegram_messages(message)
            return
        
    message = "No new flats."
    send_telegram_messages(message)

if __name__ == "__main__":
    main()
