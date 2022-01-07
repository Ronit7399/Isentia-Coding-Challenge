import requests
from bs4 import BeautifulSoup
import difflib
import time
from datetime import datetime

# target URL
url = "https://7news.com.au/"
# act like a browser
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

OldVersion = ""
InitialRun = True
while True:

    # download the page
    response = requests.get(url, headers=headers)
    # parse the downloaded homepage
    soup = BeautifulSoup(response.text, "lxml")

    for script in soup(["script", "style"]):script.extract() 
    soup = soup.get_text()
    # compare the old version with the text
    if OldVersion != soup:
        # Initial Run
        if InitialRun == True:
            OldVersion = soup
            InitialRun = False
            print ("Start scanning "+url+ ""+ str(datetime.now()))
        else:
            print ("Alert! Changes detected at: "+ str(datetime.now()))
            O_Page = OldVersion.splitlines()
            N_Page = soup.splitlines()
            # compare versions and highlight changes using difflib
            diff = difflib.context_diff(O_Page,N_Page,n=10)
            out_text = "\n".join([ll.rstrip() for ll in '\n'.join(diff).splitlines() if ll.strip()])
            print (out_text)
            O_Page = N_Page
            print ('\n'.join(diff))
            OldVersion = soup
    else:
        print( "No Changes "+ str(datetime.now()))
    time.sleep(10)
    continue