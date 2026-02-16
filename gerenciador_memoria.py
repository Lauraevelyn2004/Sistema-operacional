import psutil

class GerenciadorMemoria:
    """Gerenciador de memória do sistema operacional"""
    
    def __init__(self):
        self.hardware_ram = None
    
    def vincular_hardware(self, hardware):
        """Vincula o gerenciador ao hardware"""
        self.hardware_ram = hardware.ram
    
    def obter_status_memoria(self):
        """Obtém status atual da memória"""
        if not self.hardware_ram:
            return {'erro': 'Hardware não vinculado'}
        
        memoria_info = self.hardware_ram.obter_info()
        swap_info = self.hardware_ram.obter_swap()
        
        return {
            'memoria_virtual': memoria_info,
            'memoria_swap': swap_info,
            'status': 'OK' if memoria_info['percentual_uso'] < 80 else 'CRÍTICO'
        }
    
    def alocar_memoria(self, quantidade_mb):
        """Simula alocação de memória"""
        memoria = psutil.virtual_memory()
        disponivel_mb = memoria.available / (1024**2)
        
        if quantidade_mb > disponivel_mb:
            return {
                'sucesso': False,
                'mensagem': f'Memória insuficiente. Disponível: {disponivel_mb:.2f}MB'
            }
        else:
            return {
                'sucesso': True,
                'mensagem': f'Alocados {quantidade_mb}MB de memória',
                'memoria_restante_mb': disponivel_mb - quantidade_mb
            }
    
    def liberar_memoria(self):
        """Retorna informações sobre memória que pode ser liberada"""
        return {
            'cache_disponivel': 'Simulação de liberação de cache',
            'memoria_liberavel': 'Processos inativos podem ser finalizados'
        }
    
    def obter_processos_por_memoria(self, limite=10):
        """Lista processos que mais consomem memória"""
        processos = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                processos.append({
                    'pid': proc.info['pid'],
                    'nome': proc.info['name'],
                    'memoria_percentual': round(proc.info['memory_percent'], 2)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        processos_ordenados = sorted(processos, key=lambda x: x['memoria_percentual'], reverse=True)
        return processos_ordenados[:limite]
