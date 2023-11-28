from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.execution import ExecutionFilter
import csv
import time

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.executions = []

    def execDetails(self, redId, contract, execution): #reqId
        print(f"Order execution: {execution.acctNumber}, Symbol: {contract.symbol}, {execution.shares} @ {execution.price}")
        self.executions.append([execution.acctNumber, contract.symbol, execution.shares, execution.price, execution.side])

    def save_to_csv(self, filename):
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for execution in self.executions:
                writer.writerow(execution)

def run_loop():
    app.run()

app = IBapi()
app.connect('127.0.0.1', 7496, 123)

# Iniciar a conexão em um loop separado para não bloquear a thread principal
import threading
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(5)  # Aguardar um pouco para a conexão ser estabelecida

# Solicitar detalhes de execução
app.reqExecutions(1,ExecutionFilter())

time.sleep(5)  # Espera (para não forcar o servidor)

# Salvar detalhes da execução no CSV
app.save_to_csv('executions.csv')

app.disconnect()
