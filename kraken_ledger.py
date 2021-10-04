import datetime
from openpyxl import load_workbook
from kraken_auth import kraken_request
from kraken_market import kraken_price

def update_ledger(wb,ws,last_row,kraken_time_u,kraken_time,transaction,amount,asset_index,asset):
    next_row = last_row + 1
    # get asset price at kraken_time
    price = kraken_price(asset_index,kraken_time_u - 3600,60)
    price = price['result'][asset_index][00][4]
    # add new ledger entry
    ws.cell(row = next_row, column = 1).value = kraken_time
    ws.cell(row = next_row, column = 2).value = transaction
    ws.cell(row = next_row, column = 3).value = asset
    ws.cell(row = next_row, column = 4).value = amount
    ws.cell(row = next_row, column = 5).value = price
    wb.save('Crypto Ledger.xlsx')
    print('Updated Ledger:',kraken_time)


def stake_update(resp):
    # Read most recent staking activity
    kraken_time_u = resp['result'][0]['time']
    kraken_time = datetime.datetime.fromtimestamp(kraken_time_u)
    # Read last entry in ledger
    wb = load_workbook(filename = 'Crypto Ledger.xlsx')
    ws = wb.active
    last_row = ws.max_row
    last_time = ws.cell(row = last_row, column = 1).value
    # compare most recent stake entry timestamp to ledger
    if kraken_time > last_time:
        ahead = 1
        while ahead:
            kraken_time_u = resp['result'][ahead]['time']
            kraken_time = datetime.datetime.fromtimestamp(kraken_time_u)
            if kraken_time > last_time:
                ahead = ahead + 1

            else:
                ahead = ahead - 1
                # Set fields
                kraken_time_u = resp['result'][ahead]['time']
                kraken_time = datetime.datetime.fromtimestamp(kraken_time_u)
                transaction = resp['result'][ahead]['type'].upper()
                asset = str(resp['result'][ahead]['asset'])[:-2]
                asset_index = asset+'USD'
                amount = resp['result'][ahead]['amount']

                update_ledger(wb,ws,last_row,kraken_time_u,kraken_time,transaction,amount,asset_index,asset)
                # Update last row and time for next iteration
                last_row = ws.max_row
                last_time = ws.cell(row = last_row, column = 1).value

    else:
        print('No update needed.')

# Construct the request and print the result
resp = kraken_request('/0/private/Staking/Transactions', {
    "nonce": str(int(1000*datetime.datetime.utcnow().timestamp()))
})

stake_update(resp.json())
print(resp.json())
