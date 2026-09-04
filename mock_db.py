import csv

def get_clientes():
    """Lê a base de dados de clientes a partir de um arquivo CSV."""
    clientes = []
    try:
        # Mudamos de utf-8 para latin-1 para aceitar os acentos gerados pelo Windows/Excel
        with open("clientes.csv", mode="r", encoding="latin-1") as arquivo:
            leitor_csv = csv.DictReader(arquivo, delimiter=',') # Pode adicionar delimiter=';' se o seu CSV usar ponto-e-vírgula
            for linha in leitor_csv:
                clientes.append({
                    "id": linha["id"],
                    "nome": linha["nome"],
                    "cidade": linha["cidade"],
                    "seguro": linha["seguro"],
                    "perfil": linha["perfil"]
                })
    except FileNotFoundError:
        print("❌ Erro: O arquivo 'clientes.csv' não foi encontrado na pasta.")
        
    return clientes