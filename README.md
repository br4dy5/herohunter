# herohunter
This script will search urlscan.io submissions for webpages that contain common phishing files such as common credential login splash pages. The naming of this script was inspired by the popular O365 splash page named heroillustration.


## Install dependencies
    pip install -r requirements.txt
    
## Usage
    herohunter.py

## Customization
No parameters/arguments are required. However, there are values that are currently hard-coded which can be revised:
* keyword list (Line 8) (ex: domains, hashes, files, etc. see: https://urlscan.io/search/# under 'Help & Examples)
* domain whitelist (Line 11)
