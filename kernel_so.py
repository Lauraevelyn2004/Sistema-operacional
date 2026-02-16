from hardware import Hardware
from gerenciador_memoria import GerenciadorMemoria
from gerenciador_processos import GerenciadorProcessos
from gerenciador_arquivos import GerenciadorArquivos

class KernelSO:
    """Kernel do Sistema Operacional - Componente central"""
    
    def __init__(self):
        # Inicializa hardware
        self.hardware = Hardware()
        
        # Inicializa gerenciadores
        self.gerenciador_memoria = GerenciadorMemoria()
        self.gerenciador_processos = GerenciadorProcessos()
        self.gerenciador_arquivos = GerenciadorArquivos()
        
        # Vincula gerenciadores ao hardware
        self.gerenciador_memoria.vincular_hardware(self.hardware)
        self.gerenciador_arquivos.hardware_hd = self.hardware.hd
        
        print("[KERNEL] Sistema operacional inicializado com sucesso!")
    
    def obter_status_sistema(self):
        """Retorna status completo do sistema"""
        return {
            'hardware': self.hardware.obter_informacoes_completas(),
            'memoria': self.gerenciador_memoria.obter_status_memoria(),
            'processos': self.gerenciador_processos.obter_contagem_processos()
        }
    
    def executar_comando_memoria(self, comando, **kwargs):
        """Executa comandos relacionados à memória"""
        if comando == 'status':
            return self.gerenciador_memoria.obter_status_memoria()
        elif comando == 'alocar':
            return self.gerenciador_memoria.alocar_memoria(kwargs.get('quantidade_mb', 100))
        elif comando == 'liberar':
            return self.gerenciador_memoria.liberar_memoria()
        elif comando == 'top_processos':
            return self.gerenciador_memoria.obter_processos_por_memoria(kwargs.get('limite', 10))
        else:
            return {'erro': 'Comando de memória desconhecido'}
    
    def executar_comando_processo(self, comando, **kwargs):
        """Executa comandos relacionados a processos"""
        if comando == 'listar':
            return self.gerenciador_processos.listar_processos()
        elif comando == 'info':
            return self.gerenciador_processos.obter_processo_por_pid(kwargs.get('pid'))
        elif comando == 'finalizar':
            return self.gerenciador_processos.finalizar_processo(kwargs.get('pid'))
        elif comando == 'top_cpu':
            return self.gerenciador_processos.obter_top_processos_cpu(kwargs.get('limite', 10))
        elif comando == 'contagem':
            return self.gerenciador_processos.obter_contagem_processos()
        else:
            return {'erro': 'Comando de processo desconhecido'}
    
    def executar_comando_arquivo(self, comando, **kwargs):
        """Executa comandos relacionados a arquivos"""
        if comando == 'listar':
            return self.gerenciador_arquivos.listar_diretorio(kwargs.get('caminho'))
        elif comando == 'info':
            return self.gerenciador_arquivos.obter_info_arquivo(kwargs.get('caminho'))
        elif comando == 'criar_arquivo':
            return self.gerenciador_arquivos.criar_arquivo(kwargs.get('caminho'), kwargs.get('conteudo', ''))
        elif comando == 'criar_diretorio':
            return self.gerenciador_arquivos.criar_diretorio(kwargs.get('caminho'))
        elif comando == 'deletar':
            return self.gerenciador_arquivos.deletar_arquivo(kwargs.get('caminho'))
        elif comando == 'copiar':
            return self.gerenciador_arquivos.copiar_arquivo(kwargs.get('origem'), kwargs.get('destino'))
        elif comando == 'mover':
            return self.gerenciador_arquivos.mover_arquivo(kwargs.get('origem'), kwargs.get('destino'))
        else:
            return {'erro': 'Comando de arquivo desconhecido'}
    
    def shutdown(self):
        """Desliga o sistema operacional"""
        print("[KERNEL] Sistema operacional desligando...")
        return {'mensagem': 'Sistema desligado com sucesso'}
