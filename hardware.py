import psutil
import platform

class CPU:
    """Classe para gerenciar informações da CPU"""
    
    @staticmethod
    def obter_info():
        """Retorna informações da CPU"""
        return {
            'nucleos_fisicos': psutil.cpu_count(logical=False),
            'nucleos_logicos': psutil.cpu_count(logical=True),
            'frequencia_atual': psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A',
            'frequencia_max': psutil.cpu_freq().max if psutil.cpu_freq() else 'N/A',
            'uso_percentual': psutil.cpu_percent(interval=1),
            'arquitetura': platform.machine(),
            'processador': platform.processor()
        }
    
    @staticmethod
    def obter_uso_por_nucleo():
        """Retorna uso de CPU por núcleo"""
        return psutil.cpu_percent(interval=1, percpu=True)


class HD:
    """Classe para gerenciar informações do disco rígido"""
    
    @staticmethod
    def obter_info():
        """Retorna informações dos discos"""
        discos = []
        for particao in psutil.disk_partitions():
            try:
                uso = psutil.disk_usage(particao.mountpoint)
                discos.append({
                    'dispositivo': particao.device,
                    'ponto_montagem': particao.mountpoint,
                    'sistema_arquivos': particao.fstype,
                    'total_gb': round(uso.total / (1024**3), 2),
                    'usado_gb': round(uso.used / (1024**3), 2),
                    'livre_gb': round(uso.free / (1024**3), 2),
                    'percentual_uso': uso.percent
                })
            except PermissionError:
                continue
        return discos
    
    @staticmethod
    def obter_io():
        """Retorna estatísticas de I/O do disco"""
        io = psutil.disk_io_counters()
        return {
            'leituras': io.read_count,
            'escritas': io.write_count,
            'bytes_lidos': round(io.read_bytes / (1024**2), 2),
            'bytes_escritos': round(io.write_bytes / (1024**2), 2)
        }


class RAM:
    """Classe para gerenciar informações da memória RAM"""
    
    @staticmethod
    def obter_info():
        """Retorna informações da memória RAM"""
        memoria = psutil.virtual_memory()
        return {
            'total_gb': round(memoria.total / (1024**3), 2),
            'disponivel_gb': round(memoria.available / (1024**3), 2),
            'usado_gb': round(memoria.used / (1024**3), 2),
            'percentual_uso': memoria.percent,
            'livre_gb': round(memoria.free / (1024**3), 2)
        }
    
    @staticmethod
    def obter_swap():
        """Retorna informações da memória swap"""
        swap = psutil.swap_memory()
        return {
            'total_gb': round(swap.total / (1024**3), 2),
            'usado_gb': round(swap.used / (1024**3), 2),
            'livre_gb': round(swap.free / (1024**3), 2),
            'percentual_uso': swap.percent
        }


class Hardware:
    """Classe principal para agregar todos os componentes de hardware"""
    
    def __init__(self):
        self.cpu = CPU()
        self.hd = HD()
        self.ram = RAM()
    
    def obter_informacoes_completas(self):
        """Retorna todas as informações de hardware"""
        return {
            'cpu': self.cpu.obter_info(),
            'discos': self.hd.obter_info(),
            'ram': self.ram.obter_info(),
            'swap': self.ram.obter_swap(),
            'io_disco': self.hd.obter_io()
        }
