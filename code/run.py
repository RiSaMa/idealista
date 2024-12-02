from utils import get_oauth_token, search_properties, filter_properties, update_database, upload_to_dropbox
from bot import get_bot_token, get_chat_id, send_telegram_message
from tqdm import tqdm
import json

def main():

    #root_path = "/Users/sanchr87/Library/CloudStorage/OneDrive-MedtronicPLC/Documents/idealista/code"
    root_path = "./code"
    since_date = "M" # M: last month, for initial search. W: last week for recurrent searches
    pages_to_search = (1, 1)  # Adjust the range as needed

    '''
    # Get the OAuth token
    token = get_oauth_token()
    
    
    # Search
    all_properties = []
    for page in tqdm(range(pages_to_search[0], pages_to_search[1] + 1)):
        properties = search_properties(token, page, since_date)
        all_properties.extend(properties)

    # DEBUG
    # Saving the list of dictionaries to a JSON file
    with open('./data.json', 'w') as json_file:
        json.dump(all_properties, json_file, indent=4)
    '''

    # Reading the list of dictionaries from the JSON file
    #with open('./code/data.json', 'r') as json_file:
    with open(f'{root_path}/data.json', 'r') as json_file:
        all_properties = json.load(json_file)
    
    # Filter properties
    filtered_properties = filter_properties(all_properties)

    # Update database
    update_database(filtered_properties, db_file=f'{root_path}/db.xlsx')

    # Upload file and get shareable link
    shareable_link = upload_to_dropbox(f'{root_path}/db.xlsx')

    # Summary message
    message = f"Database updated! There are {len(filtered_properties)} new flats. [Link]({shareable_link})"

    # Escape special characters for MarkdownV2
    message = message.replace('-', '\\-').replace('.', '\\.').replace('(', '\\(').replace(')', '\\)')

    # Send Telegram message
    bot_token = get_bot_token()
    chat_id = get_chat_id()
    send_telegram_message(bot_token, chat_id, message)
    

if __name__ == "__main__":
    main()
