from interface_api import InterfaceAPI
import json

def exibir_menu():
    """Exibe menu principal do sistema"""
    print("\n" + "="*60)
    print("  SISTEMA OPERACIONAL SIMPLIFICADO")
    print("="*60)
    print("\n[1] Status Completo do Sistema")
    print("[2] Informações de Hardware")
    print("[3] Gerenciamento de Memória")
    print("[4] Gerenciamento de Processos")
    print("[5] Gerenciamento de Arquivos")
    print("[0] Sair")
    print("="*60)

def menu_hardware(api):
    """Menu de hardware"""
    print("\n--- HARDWARE ---")
    print("[1] Informações da CPU")
    print("[2] Informações de RAM")
    print("[3] Informações de HD")
    print("[4] Uso da CPU por núcleo")
    print("[5] Todas as informações")
    print("[0] Voltar")
    
    opcao = input("\nEscolha uma opção: ")
    
    if opcao == '1':
        req = {'tipo': 'hardware', 'comando': 'cpu'}
        print(api.formatar_resposta(api.processar_requisicao(req)))
    elif opcao == '2':
        req = {'tipo': 'hardware', 'comando': 'ram'}
        print(api.formatar_resposta(api.processar_requisicao(req)))
    elif opcao == '3':
        req = {'tipo': 'hardware', 'comando': 'hd'}
        print(api.formatar_resposta(api.processar_requisicao(req)))
    elif opcao == '4':
        req = {'tipo': 'hardware', 'comando': 'cpu_nucleos'}
        print(api.formatar_resposta(api.processar_requisicao(req)))
    elif opcao == '5':
        req = {'tipo': 'hardware', 'comando': 'info_completa'}
        print(api.formatar_resposta(api.processar_requisicao(req)))

def menu_memoria(api):
    """Menu de memória"""
    print("\n--- MEMÓRIA ---")
    print("[1] Status da Memória")
    print("[2] Simular Alocação")
    print("[3] Top 10 Processos (uso de memória)")
    print("[0] Voltar")
    
    opcao = input("\nEscolha uma opção: ")
    
    if opcao == '1':
        req = {'tipo': 'memoria', 'comando': 'status'}
        print(api.formatar_resposta(api.processar_requisicao(req)))
    elif opcao == '2':
        mb = int(input("Quantos MB deseja alocar? "))
        req = {'tipo': 'memoria', 'comando': 'alocar', 'parametros': {'quantidade_mb': mb}}
        print(api.formatar_resposta(api.processar_requisicao(req)))
    elif opcao == '3':
        req = {'tipo': 'memoria', 'comando': 'top_processos', 'parametros': {'limite': 10}}
        print(api.formatar_resposta(api.processar_requisicao(req)))

def menu_processos(api):
    """Menu de processos"""
    print("\n--- PROCESSOS ---")
    print("[1] Listar Todos os Processos")
    print("[2] Top 10 Processos (uso de CPU)")
    print("[3] Informações de Processo (por PID)")
    print("[4] Contagem de Processos")
    print("[5] Finalizar Processo")
    print("[0] Voltar")
    
    opcao = input("\nEscolha uma opção: ")
    
    if opcao == '1':
        req = {'tipo': 'processo', 'comando': 'listar'}
        processos = api.processar_requisicao(req)
        print(f"\nTotal de processos: {len(processos)}")
        print("\nPrimeiros 20 processos:")
        print(json.dumps(processos[:20], indent=2, ensure_ascii=False))
    elif opcao == '2':
        req = {'tipo': 'processo', 'comando': 'top_cpu', 'parametros': {'limite': 10}}
        print(api.formatar_resposta(api.processar_requisicao(req)))
    elif opcao == '3':
        pid = int(input("Digite o PID do processo: "))
        req = {'tipo': 'processo', 'comando': 'info', 'parametros': {'pid': pid}}
        print(api.formatar_resposta(api.processar_requisicao(req)))
    elif opcao == '4':
        req = {'tipo': 'processo', 'comando': 'contagem'}
        print(api.formatar_resposta(api.processar_requisicao(req)))
    elif opcao == '5':
        pid = int(input("Digite o PID do processo para finalizar: "))
        confirmacao = input(f"Tem certeza que deseja finalizar o processo {pid}? (s/n): ")
        if confirmacao.lower() == 's':
            req = {'tipo': 'processo', 'comando': 'finalizar', 'parametros': {'pid': pid}}
            print(api.formatar_resposta(api.processar_requisicao(req)))

def menu_arquivos(api):
    """Menu de arquivos"""
    print("\n--- ARQUIVOS ---")
    print("[1] Listar Diretório")
    print("[2] Informações de Arquivo")
    print("[3] Criar Arquivo")
    print("[4] Criar Diretório")
    print("[5] Deletar Arquivo/Diretório")
    print("[0] Voltar")
    
    opcao = input("\nEscolha uma opção: ")
    
    if opcao == '1':
        caminho = input("Digite o caminho (Enter para diretório atual): ")
        req = {'tipo': 'arquivo', 'comando': 'listar', 'parametros': {'caminho': caminho if caminho else None}}
        print(api.formatar_resposta(api.processar_requisicao(req)))
    elif opcao == '2':
        caminho = input("Digite o caminho do arquivo: ")
        req = {'tipo': 'arquivo', 'comando': 'info', 'parametros': {'caminho': caminho}}
        print(api.formatar_resposta(api.processar_requisicao(req)))
    elif opcao == '3':
        caminho = input("Digite o caminho do novo arquivo: ")
        conteudo = input("Digite o conteúdo (Enter para vazio): ")
        req = {'tipo': 'arquivo', 'comando': 'criar_arquivo', 'parametros': {'caminho': caminho, 'conteudo': conteudo}}
        print(api.formatar_resposta(api.processar_requisicao(req)))
    elif opcao == '4':
        caminho = input("Digite o caminho do novo diretório: ")
        req = {'tipo': 'arquivo', 'comando': 'criar_diretorio', 'parametros': {'caminho': caminho}}
        print(api.formatar_resposta(api.processar_requisicao(req)))
    elif opcao == '5':
        caminho = input("Digite o caminho para deletar: ")
        confirmacao = input(f"Tem certeza que deseja deletar {caminho}? (s/n): ")
        if confirmacao.lower() == 's':
            req = {'tipo': 'arquivo', 'comando': 'deletar', 'parametros': {'caminho': caminho}}
            print(api.formatar_resposta(api.processar_requisicao(req)))

def main():
    """Função principal"""
    print("\nInicializando Sistema Operacional...")
    api = InterfaceAPI()
    
    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            req = {'tipo': 'sistema', 'comando': 'status'}
            print(api.formatar_resposta(api.processar_requisicao(req)))
            input("\nPressione Enter para continuar...")
        
        elif opcao == '2':
            menu_hardware(api)
            input("\nPressione Enter para continuar...")
        
        elif opcao == '3':
            menu_memoria(api)
            input("\nPressione Enter para continuar...")
        
        elif opcao == '4':
            menu_processos(api)
            input("\nPressione Enter para continuar...")
        
        elif opcao == '5':
            menu_arquivos(api)
            input("\nPressione Enter para continuar...")
        
        elif opcao == '0':
            req = {'tipo': 'sistema', 'comando': 'shutdown'}
            print(api.formatar_resposta(api.processar_requisicao(req)))
            break
        
        else:
            print("\nOpção inválida!")

if __name__ == "__main__":
    main()
