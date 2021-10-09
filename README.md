# Kraken
*Scripts for getting data from the Kraken API and performing analysis*

## Features
* kraken_auth
    [x] Send an authenticated API request to kraken
* kraken_market
    [x] Check the price on a market at a specified time
* kraken_ledger
    [x] Update a ledger
        [] Stop using excel/start using a real db for the ledger
    [x] Check for recent staking transactions
    [] Check Trade History
* Crypto Dashboard
    [] Publish PowerBI dashboard template

## Usage
1. Install requirements
`$ pip install -r requirements.txt`
or
`> python -m pip install requirements.txt`

1. Create a `secrets.py` file in the same directory:
    ```
    api_key = 'yourKrakenApiKey'
    api_sec = 'yourKrakenApiSecret'
    ```
1. Run `kraken_ledger.py` to update the ledger.