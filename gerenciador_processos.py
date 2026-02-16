import psutil
import os
from datetime import datetime

class GerenciadorProcessos:
    """Gerenciador de processos do sistema operacional"""
    
    def __init__(self):
        self.processos_cache = {}
    
    def listar_processos(self):
        """Lista todos os processos em execução"""
        processos = []
        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent', 'create_time']):
            try:
                info = proc.info
                processos.append({
                    'pid': info['pid'],
                    'nome': info['name'],
                    'status': info['status'],
                    'cpu_percentual': round(info['cpu_percent'], 2),
                    'memoria_percentual': round(info['memory_percent'], 2),
                    'tempo_criacao': datetime.fromtimestamp(info['create_time']).strftime('%Y-%m-%d %H:%M:%S')
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return processos
    
    def obter_processo_por_pid(self, pid):
        """Obtém informações detalhadas de um processo pelo PID"""
        try:
            proc = psutil.Process(pid)
            
            # Tenta obter informações que podem falhar
            try:
                usuario = proc.username()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                usuario = 'N/A (Acesso Negado)'
            
            try:
                executavel = proc.exe()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                executavel = 'N/A (Acesso Negado)'
            
            return {
                'pid': proc.pid,
                'nome': proc.name(),
                'status': proc.status(),
                'cpu_percentual': proc.cpu_percent(interval=0.1),
                'memoria_mb': round(proc.memory_info().rss / (1024**2), 2),
                'threads': proc.num_threads(),
                'usuario': usuario,
                'executavel': executavel
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            return {'erro': str(e)}
    
    def criar_processo(self, comando):
        """Simula criação de processo (apenas demonstração)"""
        return {
            'mensagem': 'Criação de processo é uma operação privilegiada',
            'comando_solicitado': comando,
            'status': 'Simulação apenas'
        }
    
    def finalizar_processo(self, pid):
        """Finaliza um processo pelo PID"""
        try:
            proc = psutil.Process(pid)
            nome = proc.name()
            proc.terminate()
            return {
                'sucesso': True,
                'mensagem': f'Processo {nome} (PID: {pid}) foi finalizado'
            }
        except psutil.NoSuchProcess:
            return {
                'sucesso': False,
                'mensagem': f'Processo com PID {pid} não encontrado'
            }
        except psutil.AccessDenied:
            return {
                'sucesso': False,
                'mensagem': f'Acesso negado para finalizar processo PID {pid}'
            }
    
    def obter_contagem_processos(self):
        """Retorna contagem total de processos"""
        # Conta processos do usuário atual de forma segura
        processos_usuario = 0
        usuario_atual = os.getenv('USERNAME') or os.getenv('USER') or 'unknown'
        
        for proc in psutil.process_iter():
            try:
                if proc.username() == usuario_atual or proc.username().endswith(f'\\{usuario_atual}'):
                    processos_usuario += 1
            except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
                # Ignora processos que não podem ser acessados
                continue
        
        return {
            'total_processos': len(psutil.pids()),
            'processos_usuario': processos_usuario,
            'usuario_atual': usuario_atual
        }
    
    def obter_top_processos_cpu(self, limite=10):
        """Lista processos que mais consomem CPU"""
        processos = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                processos.append({
                    'pid': proc.info['pid'],
                    'nome': proc.info['name'],
                    'cpu_percentual': proc.info['cpu_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        processos_ordenados = sorted(processos, key=lambda x: x['cpu_percentual'], reverse=True)
        return processos_ordenados[:limite]
