'''
	Mamagiannos Dimitrios - September 2017
	
	Upload a database's back up to Dropbox. Maximum back ups are defined. 
	If this maximum is reached the oldest back up is deleted from Dropbox
	
'''
import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

access_token = ""
dbx = dropbox.Dropbox(access_token)

try:
        dbx.users_get_current_account()
except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an "
            "access token from the app console on the web.")

#Delete oldest back up according to back up policy
MAX_BACK_UPS = 6

if (len(dbx.files_list_folder('').entries) == MAX_BACK_UPS) :
    #Ascending first uploaded
    oldest_backup_path = dbx.files_list_folder('').entries[0].path_display
    print("Delete... "+oldest_backup_path)
    try:
        dbx.files_delete_v2(oldest_backup_path)
    except ApiError as err:
    # This checks for the specific error where a user doesn't have
    # enough Dropbox space quota to upload this file
        if (err.error.is_path() and err.error.get_path().error.is_insufficient_space()):
            sys.exit("ERROR: Cannot back up; insufficient space.")
        elif err.user_message_text:
            print(err.user_message_text)
            sys.exit()
        else:
            print(err)
            sys.exit()

#Upload the newest back up to Dropbox
LOCALFILE = str(sys.argv[1])
BACKUPPATH = "/"+LOCALFILE

with open(LOCALFILE, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()
