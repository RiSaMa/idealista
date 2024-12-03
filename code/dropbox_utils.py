import os
import dropbox
import pandas as pd 

def get_dropbox_client():
    dbx = dropbox.Dropbox(
        os.getenv('DROPBOX_TOKEN')
        #app_key=os.getenv('DROPBOX_KEY'),
        #app_secret=os.getenv('DROPBOX_SECRET'),
        #oauth2_refresh_token=os.getenv('DROPBOX_TOKEN')
    )
    return dbx

def upload_to_dropbox(file_path):
    dbx = get_dropbox_client()
    
    # Define the path where you want to upload the file in Dropbox
    dropbox_folder = '/Idealista'  # Ensure this folder exists in your Dropbox
    dropbox_file_path = f'{dropbox_folder}/{os.path.basename(file_path)}'

    # Upload the file
    with open(file_path, 'rb') as f:
        dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode.overwrite)

    try:
        # Check if a shared link already exists
        shared_links = dbx.sharing_list_shared_links(path=dropbox_file_path, direct_only=True)
        if shared_links.links:
            # Use the existing shared link
            return shared_links.links[0].url
        else:
            # Create a new shared link if none exists
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_file_path)
            return shared_link_metadata.url
    except dropbox.exceptions.ApiError as e:
        print(f"Dropbox API error: {e}")
        return None

def download_from_dropbox(file_path, local_path):
    """Download a file from Dropbox, or create an empty file if it doesn't exist."""
    dbx = get_dropbox_client()
    
    try:
        # Attempt to download the file
        with open(local_path, "wb") as f:
            metadata, res = dbx.files_download(path=file_path)
            f.write(res.content)
        print(f"File {file_path} downloaded successfully.")
    #except dropbox.exceptions.ApiError as e:
    except:
        #print(f"Dropbox API error: {e}")
        #if isinstance(e.error, dropbox.files.DownloadError):
            # If the file does not exist, create an empty DataFrame and save it as Excel
            df_empty = pd.DataFrame(columns=['propertyCode', 'url', 'price', 'size', 'address', 'bedrooms', 'floor', 'description', 'Interested?', 'Contacted?'])
            df_empty.to_excel(local_path, index=False)
            print(f"Created an empty database at {local_path}.")
        #else:
        #    return None
