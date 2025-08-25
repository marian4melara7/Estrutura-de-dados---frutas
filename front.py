import os
from main import SistemaEstoque

def limpar_tela():
    os.system('clear' if os.name == 'posix' else 'cls')

def menu():
    sistema = SistemaEstoque()

    while True:
        print("""
        Vendas de Frutas
1 - Cadastrar cliente
2 - Listar clientes
3 - Cadastrar produto
4 - Listar produtos
5 - Realizar venda
6 - Ver fila de vendas
7 - Desfazer última operação
8 - Exibir valor total do estoque
9 - Exibir valor total de vendas realizadas
10 - Exibir clientes e valores gastos
11 - Editar produtos
12 - Sair
""")
        try:
            opcao = int(input("Escolha: "))

            if opcao == 1:
                sistema.cadastrar_cliente()
                input("\nPressione Enter para continuar...")
                limpar_tela()
            elif opcao == 2:
                sistema.listar_clientes()
                input("\nPressione Enter para continuar...")
                limpar_tela()
            elif opcao == 3:
                sistema.cadastrar_produto()
                input("\nPressione Enter para continuar...")
                limpar_tela()
            elif opcao == 4:
                sistema.listar_produtos()
                input("\nPressione Enter para continuar...")
                limpar_tela()
            elif opcao == 5:
                sistema.realizar_venda()
                input("\nPressione Enter para continuar...")
                limpar_tela()
            elif opcao == 6:
                sistema.visualizar_vendas()
                input("\nPressione Enter para continuar...")
                limpar_tela()
            elif opcao == 7:
                sistema.desfazer()
                input("\nPressione Enter para continuar...")
                limpar_tela()
            elif opcao == 8:
                sistema.valor_total_estoque()
                input("\nPressione Enter para continuar...")
                limpar_tela()
            elif opcao == 9:
                sistema.valor_total_vendas()
                input("\nPressione Enter para continuar...")
                limpar_tela()
            elif opcao == 10:
                sistema.clientes_totais()
                input("\nPressione Enter para continuar...")
                limpar_tela()
            elif opcao == 11:
                sistema.modificar_produto()
                input("\nPressione Enter para continuar...")
                limpar_tela()
            elif opcao == 12:
                sistema.salvar_estoque()
                print("Saindo do sistema... Até logo!")
                break
            else:
                print("Opção inválida.")
                input("\nPressione Enter para continuar...")
                limpar_tela()
        except Exception as e:
            print("Erro:", e)
            input("\nPressione Enter para continuar...")
            limpar_tela()

if __name__ == "__main__":
    menu()
