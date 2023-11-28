import threading
import time
import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.execution import ExecutionFilter
import ftplib

HOSTNAME = "167.172.0.133"

# Lista de clientes
lista_clientes = [
    'U10355581', 'U10375548', 'U10393335', 'U11071406', 'U11086471', 'U11239176', 'U11424382', 'U11821945', 
    'U12156732', 'U12167071', 'U12192213', 'U12216291', 'U12236925', 'U12277193', 'U12294610', 'U12320396', 
    'U12321651', 'U12351347', 'U12471035', 'U12631300', 'U12666466', 'U12691955', 'U12843298', 'U12997920', 
    'U4031188', 'U5453084', 'U9578694', 'U9624456', 'U9665342'
]

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.executions = []

    def execDetails(self, reqId, contract, execution):
        print(f"Order execution: {execution.acctNumber}, Symbol: {contract.symbol}, {execution.shares} @ {execution.price}")
        self.executions.append([execution.acctNumber, contract.symbol, execution.shares, execution.price, execution.side])

    def calculate_net_positions(self):
        df = pd.DataFrame(self.executions, columns=['codigo_conta', 'ticker', 'quantidade', 'preco', 'tipo_transacao'])
        valores_liquidos = {cliente: 0 for cliente in lista_clientes}

        for index, row in df.iterrows():
            if row['codigo_conta'] in valores_liquidos:
                if row['tipo_transacao'] == "BOT":
                    valores_liquidos[row['codigo_conta']] += row['quantidade'] * row['preco']
                elif row['tipo_transacao'] == "SLD":
                    valores_liquidos[row['codigo_conta']] -= row['quantidade'] * row['preco']

        df_resultado = pd.DataFrame(valores_liquidos.items(), columns=['codigo_conta', 'valor_liquido'])
        df_resultado.to_csv('contratosabertos.csv', index=False)
        print("Os valores líquidos foram salvos em 'contratosabertos.csv'")

def run_loop(app):
    app.run()

# Inicialização do aplicativo IBapi
app = IBapi()
app.connect('127.0.0.1', 7496, 123)

# Iniciar a conexão em um loop separado para não bloquear a thread principal
api_thread = threading.Thread(target=lambda: run_loop(app), daemon=True)
api_thread.start()

# Loop principal
try:
    while True:
        time.sleep(10)  # Intervalo entre requisições

        # Solicitar detalhes de execução e calcular posições líquidas
        app.reqExecutions(1, ExecutionFilter())
        time.sleep(5)  # Espera para processamento
        app.calculate_net_positions()

except KeyboardInterrupt:
    print("Interrompendo o loop...")
    app.disconnect()
