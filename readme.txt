Checkout the wiki for some screenshots: https://github.com/manishbajpai/kludge/wiki

This project allows you to download your account records from TD Ameritrade and visualize them locally. You need to know two things in order to use this project:
- Installing python 3 and pip packages
- Getting an API key from TD Ameritrade
 But beyond that, no programming knowledge is required.

I created this application because 
- I want to be able to see all my accounts in one place.
- I don't want to login to individual websites every time I need to see the status
- I don't want to give my username/passwords to companies like Quicken, Mint etc.
- I want all my credentials and files stored locally on my laptop which is fully encrypted

 Here are the steps to use it.

 One time actions:
 1. Register yourself as a developer with TD Ameritrade. Don't worry, you don't need to do any development work. For this, go to TD Ameritrade developer website (https://developer.tdameritrade.com/) and register yourself.
 2. Download this package and install all the dependencies:
 pip install tda-api atexit datetime json pathlib plotly dash matplotlib pandas
 3. Run tda-generate-token.py to get the necessary tokens

To update the data
1. Make sure you have correct API_KEY and other paths in updater.sh
2. Run ./updater.sh
3. Follow the instructions on the console, i.e. go to http://127.0.0.1:8050/ to see your account information
