import random, os
from collections import deque

class Fruta:
    def __init__(self, nome, quantidade, preco):
        self.id = random.randint(1000, 9999)
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __str__(self):
        return f"ID: {self.id} | Fruta: {self.nome} | Quantidade: {self.quantidade}kg | Preço: R${self.preco:.2f}/kg"


class Cliente:
    def __init__(self, nome):
        self.id = random.randint(1000, 9999)
        self.nome = nome
        self.total_gasto = 0

    def __str__(self):
        return f"ID: {self.id} | Nome: {self.nome} | Total Gasto: R${self.total_gasto:.2f}"


class Venda:
    def __init__(self, cliente, fruta, quantidade):
        self.cliente = cliente
        self.fruta = fruta
        self.quantidade = quantidade
        self.valor_total = fruta.preco * quantidade

    def __str__(self):
        return f"Cliente: {self.cliente.nome} | Fruta: {self.fruta.nome} | Quantidade: {self.quantidade}kg | Valor: R${self.valor_total:.2f}"


class SistemaEstoque:
    def __init__(self):
        self.produtos = []
        self.clientes = []       
        self.fila_vendas = deque()  
        self.pilha_operacoes = []   
        self.total_vendas = 0
        self.total_estoque = 0
        self.carregar_estoque()
        
    def salvar_estoque(self):
        try:
            with open("estoque.txt", "w") as file:
                for produto in self.produtos:
                    file.write(f"PRODUTO,{produto.nome},{produto.quantidade},{produto.preco}\n")
                for cliente in self.clientes:
                    file.write(f"CLIENTE,{cliente.nome},{cliente.total_gasto}\n")
                file.write(f"TOTAL_ESTOQUE,{self.valor_total_estoque()}\n")
                file.write(f"TOTAL_VENDAS,{self.total_vendas}\n")
            print("Estoque salvo com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar estoque: {e}")

    def carregar_estoque(self):
        try:
            with open("estoque.txt", "r") as file:
                for line in file:
                    if line.strip():
                        parts = line.strip().split(",")
                        if parts[0] == "PRODUTO" and len(parts) == 4:
                            _, nome, quantidade, preco = parts
                            fruta = Fruta(nome, int(quantidade), float(preco))
                            self.produtos.append(fruta)
                        elif parts[0] == "CLIENTE" and len(parts) == 3:
                            _, nome, total_gasto = parts
                            cliente = Cliente(nome)
                            cliente.total_gasto = float(total_gasto)
                            self.clientes.append(cliente)
                        elif parts[0] == "TOTAL_ESTOQUE" and len(parts) == 2:
                            self.total_estoque = float(parts[1])
                        elif parts[0] == "TOTAL_VENDAS" and len(parts) == 2:
                            self.total_vendas = float(parts[1])
            print("Estoque carregado com sucesso!")
        except FileNotFoundError:
            print("Arquivo de estoque não encontrado. Um novo será criado.")
        except Exception as e:
            print(f"Erro ao carregar estoque: {e}")

    def cadastrar_cliente(self):
        nome = input("Digite o nome do cliente: ")
        cliente = Cliente(nome)
        self.clientes.append(cliente)
        self.pilha_operacoes.append(("cliente", cliente))
        print(f"Cliente cadastrado com sucesso! (ID: {cliente.id})")
        self.salvar_estoque()

    def listar_clientes(self):
        if not self.clientes:
            print("Nenhum cliente cadastrado.")
        else:
            print("     CLIENTES      ")
            for c in self.clientes:
                print(c)

    def cadastrar_produto(self):
        nome = input("Digite o nome da fruta: ")
        quantidade = int(input("Digite a quantidade: "))
        preco = float(input("Digite o preço: "))
        fruta = Fruta(nome, quantidade, preco)
        self.produtos.append(fruta)
        self.pilha_operacoes.append(("fruta", fruta))
        print(f"Fruta cadastrada com sucesso! (ID: {fruta.id})")
        self.salvar_estoque()

    def listar_produtos(self):
        if not self.produtos:
            print("Estoque vazio.")
        else:
            print("   ESTOQUE ATUAL  ")
            for p in self.produtos:
                print(p)

    def realizar_venda(self):
        if not self.produtos or not self.clientes:
            print("É necessário ter clientes e frutas cadastrados para realizar vendas.")
            return

        nome_cliente = input("Digite o nome do cliente: ")
        cliente = next((c for c in self.clientes if c.nome.lower() == nome_cliente.lower()), None)
        if not cliente:
            print("Cliente não encontrado.")
            return

        nome_fruta = input("Digite o nome da fruta: ")
        fruta = next((f for f in self.produtos if f.nome.lower() == nome_fruta.lower()), None)
        if not fruta:
            print("Fruta não encontrada.")
            return

        qtd = int(input("Digite a quantidade (kg): "))
        if qtd > fruta.quantidade:
            print("Quantidade indisponível no estoque!")
            return

        fruta.quantidade -= qtd
        venda = Venda(cliente, fruta, qtd)
        cliente.total_gasto += venda.valor_total
        self.total_vendas += venda.valor_total

        self.fila_vendas.append(venda)
        self.pilha_operacoes.append(("venda", venda))

        print("Venda realizada com sucesso!")
        print(venda)
        self.salvar_estoque()

    def visualizar_vendas(self):
        if not self.fila_vendas:
            print("Nenhuma venda registrada.")
        else:
            print("--- FILA DE VENDAS ---")
            for v in self.fila_vendas:
                print(v)

    def desfazer(self):
        if not self.pilha_operacoes:
            print("Nenhuma operação para desfazer.")
            return

        operacao = self.pilha_operacoes.pop()
        tipo = operacao[0]

        if tipo == "fruta":
            objeto = operacao[1]
            self.produtos.remove(objeto)
            print(f"Cadastro da fruta '{objeto.nome}' Apagado.")
        elif tipo == "cliente":
            objeto = operacao[1]
            self.clientes.remove(objeto)
            print(f"Cadastro do cliente '{objeto.nome}' Apagado.")
        elif tipo == "venda":
            objeto = operacao[1]
            objeto.fruta.quantidade += objeto.quantidade
            objeto.cliente.total_gasto -= objeto.valor_total
            self.total_vendas -= objeto.valor_total
            self.fila_vendas.remove(objeto)
            print(f"Venda da fruta '{objeto.fruta.nome}' Apagada.")
        elif tipo == "modificacao_produto":
            produto, quantidade_original, preco_original = operacao[1], operacao[2], operacao[3]
            produto.quantidade = quantidade_original
            produto.preco = preco_original
            print(f"Modificação do produto '{produto.nome}' desfeita. Valores restaurados.")

    def valor_total_estoque(self):
        total = sum(p.preco * p.quantidade for p in self.produtos)
        print(f"Valor total do estoque: R${total:.2f}")
        return total

    def valor_total_vendas(self):
        print(f"Valor total de vendas realizadas: R${self.total_vendas:.2f}")

    def clientes_totais(self):
        print("     CLIENTES E VALORES GASTOS   ")
        for c in self.clientes:
            print(c)

    def modificar_produto(self):
        if not self.produtos:
            print("Nenhum produto cadastrado para editar.")
            return

        print("Produtos disponíveis:")
        for i, produto in enumerate(self.produtos, 1):
            print(f"{i}. {produto.nome} (ID: {produto.id}) - Estoque: {produto.quantidade}kg - Preço: R${produto.preco:.2f}/kg")

        try:
            escolha = input("\nDigite o nome ou ID do produto que deseja editar: ")
            
            produto = next((p for p in self.produtos if str(p.id) == escolha), None)
            
            if not produto:
                produto = next((p for p in self.produtos if p.nome.lower() == escolha.lower()), None)
            
            if not produto:
                print("Produto não encontrado.")
                return

            print(f"\nProduto selecionado: {produto.nome}")
            print(f"Estoque atual: {produto.quantidade}kg")
            print(f"Preço atual: R${produto.preco:.2f}/kg")

            original_quantidade = produto.quantidade
            original_preco = produto.preco

            nov0_estoque = input("Novo estoque (deixe em branco para manter atual): ")
            if nov0_estoque.strip():
                produto.quantidade = int(nov0_estoque)

            novo_preco = input("Novo preço (deixe em branco para manter atual): ")
            if novo_preco.strip():
                produto.preco = float(novo_preco)

            self.pilha_operacoes.append(("modificacao_produto", produto, original_quantidade, original_preco))

            print(f"Produto modificado com sucesso!")
            print(f"Novo estoque: {produto.quantidade}kg")
            print(f"Novo preço: R${produto.preco:.2f}/kg")
            
            self.salvar_estoque()

        except ValueError:
            print("Valor inválido. Certifique-se de usar números para quantidade e preço.")
        except Exception as e:
            print(f"Erro ao modificar produto: {e}")