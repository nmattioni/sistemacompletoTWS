import time
import csv
from ibapi.client import EClient
from ibapi.wrapper import EWrapper

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.account_details = {}

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
        if tag == "NetLiquidation":
            self.account_details[account] = value

def main():
    account_list = ['U10355581', 'U10375548', 'U10393335', 'F10451695'] 

    app = IBapi()
    app.connect('127.0.0.1', 7496, 123)

    print("Conectando...")
    time.sleep(1)

    app.reqAccountSummary(1, "All", "NetLiquidation")
    time.sleep(3)

    app.disconnect()

    with open('netliquidation.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Account", "NetLiquidation"])

        for account in account_list:
            if account in app.account_details:
                writer.writerow([account, app.account_details[account]])
            else:
                writer.writerow([account, "Not Received"])

    print("Dados salvos em netliquidation.csv")

if __name__ == "__main__":
    main()
