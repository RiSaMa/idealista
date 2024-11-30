from utils import get_oauth_token
from utils import search_properties
from utils import filter_properties
from utils import update_database
from tqdm import tqdm

def main():

    # Get the OAuth token
    token = get_oauth_token()
    if token:
        print("Authentication correct.")
    else:
        print("Authentication failed.")
        return

    # Define the number of pages to search
    pages_to_search = (1,20)

    # Perform the search
    for page in tqdm(range(pages_to_search[0], pages_to_search[1]+1)):
        properties = search_properties(token, page)

        # Filter properties
        properties = filter_properties(properties)

        # Update database
        update_database(properties)
        
       
    print("Database updated successfully.")

if __name__ == "__main__":
    main()