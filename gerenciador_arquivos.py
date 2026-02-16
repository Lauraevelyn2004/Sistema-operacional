import os
import shutil
from datetime import datetime

class GerenciadorArquivos:
    """Gerenciador de arquivos do sistema operacional"""
    
    def __init__(self):
        self.diretorio_atual = os.getcwd()
    
    def listar_diretorio(self, caminho=None):
        """Lista conteúdo de um diretório"""
        if caminho is None:
            caminho = self.diretorio_atual
        
        try:
            itens = []
            for item in os.listdir(caminho):
                caminho_completo = os.path.join(caminho, item)
                stat = os.stat(caminho_completo)
                
                itens.append({
                    'nome': item,
                    'tipo': 'diretorio' if os.path.isdir(caminho_completo) else 'arquivo',
                    'tamanho_bytes': stat.st_size,
                    'tamanho_legivel': self._formatar_tamanho(stat.st_size),
                    'modificado': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'permissoes': oct(stat.st_mode)[-3:]
                })
            
            return {
                'caminho': caminho,
                'itens': itens,
                'total_itens': len(itens)
            }
        except PermissionError:
            return {'erro': f'Permissão negada para acessar {caminho}'}
        except FileNotFoundError:
            return {'erro': f'Diretório não encontrado: {caminho}'}
    
    def obter_info_arquivo(self, caminho_arquivo):
        """Obtém informações detalhadas de um arquivo"""
        try:
            if not os.path.exists(caminho_arquivo):
                return {'erro': 'Arquivo não encontrado'}
            
            stat = os.stat(caminho_arquivo)
            
            return {
                'caminho': os.path.abspath(caminho_arquivo),
                'nome': os.path.basename(caminho_arquivo),
                'tamanho_bytes': stat.st_size,
                'tamanho_legivel': self._formatar_tamanho(stat.st_size),
                'criado': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'modificado': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'acessado': datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
                'permissoes': oct(stat.st_mode)[-3:],
                'e_diretorio': os.path.isdir(caminho_arquivo),
                'e_arquivo': os.path.isfile(caminho_arquivo)
            }
        except Exception as e:
            return {'erro': str(e)}
    
    def criar_arquivo(self, caminho, conteudo=''):
        """Cria um novo arquivo"""
        try:
            with open(caminho, 'w') as f:
                f.write(conteudo)
            return {
                'sucesso': True,
                'mensagem': f'Arquivo criado: {caminho}'
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': str(e)
            }
    
    def criar_diretorio(self, caminho):
        """Cria um novo diretório"""
        try:
            os.makedirs(caminho, exist_ok=True)
            return {
                'sucesso': True,
                'mensagem': f'Diretório criado: {caminho}'
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': str(e)
            }
    
    def deletar_arquivo(self, caminho):
        """Deleta um arquivo"""
        try:
            if os.path.isfile(caminho):
                os.remove(caminho)
                return {
                    'sucesso': True,
                    'mensagem': f'Arquivo deletado: {caminho}'
                }
            elif os.path.isdir(caminho):
                shutil.rmtree(caminho)
                return {
                    'sucesso': True,
                    'mensagem': f'Diretório deletado: {caminho}'
                }
            else:
                return {
                    'sucesso': False,
                    'erro': 'Arquivo ou diretório não encontrado'
                }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': str(e)
            }
    
    def copiar_arquivo(self, origem, destino):
        """Copia um arquivo"""
        try:
            shutil.copy2(origem, destino)
            return {
                'sucesso': True,
                'mensagem': f'Arquivo copiado de {origem} para {destino}'
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': str(e)
            }
    
    def mover_arquivo(self, origem, destino):
        """Move um arquivo"""
        try:
            shutil.move(origem, destino)
            return {
                'sucesso': True,
                'mensagem': f'Arquivo movido de {origem} para {destino}'
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': str(e)
            }
    
    def obter_espaco_disco(self):
        """Obtém informações de espaço em disco"""
        return self.hardware_hd.obter_info() if hasattr(self, 'hardware_hd') else {}
    
    @staticmethod
    def _formatar_tamanho(bytes):
        """Formata tamanho em bytes para formato legível"""
        for unidade in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unidade}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"
