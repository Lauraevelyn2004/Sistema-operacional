from kernel_so import KernelSO
import json

class InterfaceAPI:
    """Interface de API para comunicação com o Kernel"""
    
    def __init__(self):
        self.kernel = KernelSO()
        print("[API] Interface inicializada e conectada ao Kernel")
    
    def processar_requisicao(self, requisicao):
        """Processa uma requisição e retorna resposta"""
        tipo = requisicao.get('tipo')
        comando = requisicao.get('comando')
        parametros = requisicao.get('parametros', {})
        
        if tipo == 'sistema':
            return self._processar_sistema(comando, parametros)
        elif tipo == 'memoria':
            return self.kernel.executar_comando_memoria(comando, **parametros)
        elif tipo == 'processo':
            return self.kernel.executar_comando_processo(comando, **parametros)
        elif tipo == 'arquivo':
            return self.kernel.executar_comando_arquivo(comando, **parametros)
        elif tipo == 'hardware':
            return self._processar_hardware(comando, parametros)
        else:
            return {'erro': 'Tipo de requisição desconhecido'}
    
    def _processar_sistema(self, comando, parametros):
        """Processa comandos de sistema"""
        if comando == 'status':
            return self.kernel.obter_status_sistema()
        elif comando == 'shutdown':
            return self.kernel.shutdown()
        else:
            return {'erro': 'Comando de sistema desconhecido'}
    
    def _processar_hardware(self, comando, parametros):
        """Processa comandos de hardware"""
        if comando == 'info_completa':
            return self.kernel.hardware.obter_informacoes_completas()
        elif comando == 'cpu':
            return self.kernel.hardware.cpu.obter_info()
        elif comando == 'cpu_nucleos':
            return {'uso_por_nucleo': self.kernel.hardware.cpu.obter_uso_por_nucleo()}
        elif comando == 'ram':
            return self.kernel.hardware.ram.obter_info()
        elif comando == 'hd':
            return self.kernel.hardware.hd.obter_info()
        else:
            return {'erro': 'Comando de hardware desconhecido'}
    
    def formatar_resposta(self, resposta):
        """Formata resposta em JSON legível"""
        return json.dumps(resposta, indent=2, ensure_ascii=False)
