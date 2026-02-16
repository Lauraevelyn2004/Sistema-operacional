from flask import Flask, jsonify, request
from interface_api import InterfaceAPI
import threading
import webbrowser
import time

app = Flask(__name__)
api = InterfaceAPI()

@app.route('/')
def index():
    """Página principal com HTML embutido"""
    return '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Operacional - Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
        }

        header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }

        h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #666;
            font-size: 1.1em;
        }

        .tabs {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }

        .tab-btn {
            background: #f0f0f0;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .tab-btn.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .tab-btn:hover {
            transform: translateY(-2px);
        }

        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: grid;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }

        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }

        .card-icon {
            font-size: 2em;
            margin-right: 15px;
        }

        .card-title {
            font-size: 1.3em;
            color: #333;
            font-weight: 600;
        }

        .card-content {
            color: #666;
            line-height: 1.8;
        }

        .stat-row {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 8px 0;
        }

        .stat-label {
            font-weight: 500;
            color: #555;
        }

        .stat-value {
            font-weight: 600;
            color: #667eea;
        }

        .progress-bar {
            background: #e0e0e0;
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.85em;
            font-weight: 600;
        }

        .process-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 0.85em;
            max-height: 400px;
            overflow-y: auto;
            display: block;
        }

        .process-table thead {
            position: sticky;
            top: 0;
            background: #667eea;
        }

        .process-table th {
            background: #667eea;
            color: white;
            padding: 12px 8px;
            text-align: left;
            font-weight: 600;
        }

        .process-table td {
            padding: 10px 8px;
            border-bottom: 1px solid #f0f0f0;
        }

        .process-table tbody tr:hover {
            background: #f8f9fa;
        }

        .badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }

        .badge-success {
            background: #d4edda;
            color: #155724;
        }

        .badge-warning {
            background: #fff3cd;
            color: #856404;
        }

        .badge-danger {
            background: #f8d7da;
            color: #721c24;
        }

        .loading {
            text-align: center;
            padding: 20px;
            color: #999;
        }

        .btn {
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s ease;
            font-size: 0.85em;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-danger {
            background: #dc3545;
            color: white;
        }

        .btn-success {
            background: #28a745;
            color: white;
        }

        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        }

        .refresh-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-size: 1em;
            cursor: pointer;
            font-weight: 600;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-top: 10px;
        }

        .refresh-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .section-large {
            grid-column: span 2;
        }

        .section-full {
            grid-column: 1 / -1;
        }

        @media (max-width: 768px) {
            .section-large {
                grid-column: span 1;
            }
            
            h1 {
                font-size: 1.8em;
            }
        }

        .auto-refresh {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-top: 15px;
        }

        .auto-refresh label {
            color: #666;
            font-weight: 500;
        }

        input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }

        .disk-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }

        .disk-name {
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }

        .form-group {
            margin: 15px 0;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #555;
        }

        .form-group input {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
        }

        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }

        .file-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            background: #f8f9fa;
            margin: 8px 0;
            border-radius: 8px;
            transition: background 0.2s ease;
        }

        .file-item:hover {
            background: #e9ecef;
        }

        .file-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .file-icon {
            font-size: 1.5em;
        }

        .alert {
            padding: 12px 20px;
            border-radius: 8px;
            margin: 15px 0;
            font-weight: 500;
        }

        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .alert-danger {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }

        .modal-header {
            font-size: 1.5em;
            font-weight: 600;
            margin-bottom: 20px;
            color: #333;
        }

        .modal-footer {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🖥️ Sistema Operacional</h1>
            <p class="subtitle">Monitor e Gerenciamento de Sistema em Tempo Real</p>
            
            <div class="tabs">
                <button class="tab-btn active" onclick="mudarAba('monitor')">📊 Monitor</button>
                <button class="tab-btn" onclick="mudarAba('processos')">⚙️ Processos</button>
                <button class="tab-btn" onclick="mudarAba('arquivos')">📁 Arquivos</button>
                <button class="tab-btn" onclick="mudarAba('memoria')">🧠 Memória</button>
            </div>
            
            <button class="refresh-btn" onclick="atualizarAbaAtual()">🔄 Atualizar</button>
            <div class="auto-refresh">
                <input type="checkbox" id="autoRefresh" onchange="toggleAutoRefresh()">
                <label for="autoRefresh">Atualização Automática (5s)</label>
            </div>
        </header>

        <!-- ABA MONITOR -->
        <div class="dashboard tab-content active" id="tab-monitor">
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">💻</div>
                    <div class="card-title">CPU</div>
                </div>
                <div class="card-content" id="cpu-info">
                    <div class="loading">Carregando...</div>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <div class="card-icon">🧠</div>
                    <div class="card-title">Memória RAM</div>
                </div>
                <div class="card-content" id="ram-info">
                    <div class="loading">Carregando...</div>
                </div>
            </div>

            <div class="card section-large">
                <div class="card-header">
                    <div class="card-icon">💾</div>
                    <div class="card-title">Discos</div>
                </div>
                <div class="card-content" id="hd-info">
                    <div class="loading">Carregando...</div>
                </div>
            </div>

            <div class="card section-large">
                <div class="card-header">
                    <div class="card-icon">📈</div>
                    <div class="card-title">Top 10 - Uso de CPU</div>
                </div>
                <div class="card-content" id="top-cpu">
                    <div class="loading">Carregando...</div>
                </div>
            </div>

            <div class="card section-large">
                <div class="card-header">
                    <div class="card-icon">📊</div>
                    <div class="card-title">Top 10 - Uso de Memória</div>
                </div>
                <div class="card-content" id="top-memoria">
                    <div class="loading">Carregando...</div>
                </div>
            </div>
        </div>

        <!-- ABA PROCESSOS -->
        <div class="dashboard tab-content" id="tab-processos">
            <div class="card section-full">
                <div class="card-header">
                    <div class="card-icon">⚙️</div>
                    <div class="card-title">Gerenciamento de Processos</div>
                </div>
                <div class="card-content">
                    <div id="processos-alert"></div>
                    <div id="processos-lista">
                        <div class="loading">Carregando...</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ABA ARQUIVOS -->
        <div class="dashboard tab-content" id="tab-arquivos">
            <div class="card section-full">
                <div class="card-header">
                    <div class="card-icon">📁</div>
                    <div class="card-title">Gerenciamento de Arquivos</div>
                </div>
                <div class="card-content">
                    <div id="arquivos-alert"></div>
                    
                    <div class="form-group">
                        <label>Caminho (deixe vazio para diretório atual):</label>
                        <input type="text" id="caminho-dir" placeholder="Ex: C:\\Users\\seu_usuario\\Documents">
                        <button class="btn btn-primary" style="margin-top: 10px;" onclick="listarArquivos()">📂 Listar Arquivos</button>
                    </div>

                    <div style="display: flex; gap: 10px; margin: 20px 0;">
                        <button class="btn btn-success" onclick="abrirModalCriarArquivo()">➕ Criar Arquivo</button>
                        <button class="btn btn-success" onclick="abrirModalCriarDiretorio()">📁 Criar Diretório</button>
                    </div>
                    
                    <div id="arquivos-lista">
                        <div class="loading">Clique em "Listar Arquivos" para visualizar</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ABA MEMÓRIA -->
        <div class="dashboard tab-content" id="tab-memoria">
            <div class="card section-large">
                <div class="card-header">
                    <div class="card-icon">🧠</div>
                    <div class="card-title">Status de Memória</div>
                </div>
                <div class="card-content" id="memoria-status">
                    <div class="loading">Carregando...</div>
                </div>
            </div>

            <div class="card section-large">
                <div class="card-header">
                    <div class="card-icon">💾</div>
                    <div class="card-title">Simular Alocação</div>
                </div>
                <div class="card-content">
                    <div id="memoria-alert"></div>
                    <div class="form-group">
                        <label>Quantidade (MB):</label>
                        <input type="number" id="mb-alocar" value="100" min="1">
                        <button class="btn btn-primary" style="margin-top: 10px;" onclick="alocarMemoria()">💾 Alocar</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL CRIAR ARQUIVO -->
    <div id="modalCriarArquivo" class="modal">
        <div class="modal-content">
            <div class="modal-header">➕ Criar Novo Arquivo</div>
            <div class="form-group">
                <label>Caminho completo do arquivo:</label>
                <input type="text" id="novo-arquivo-caminho" placeholder="Ex: C:\\temp\\teste.txt">
            </div>
            <div class="form-group">
                <label>Conteúdo (opcional):</label>
                <input type="text" id="novo-arquivo-conteudo" placeholder="Digite o conteúdo do arquivo">
            </div>
            <div class="modal-footer">
                <button class="btn btn-primary" onclick="criarArquivo()">✅ Criar</button>
                <button class="btn" onclick="fecharModal('modalCriarArquivo')">❌ Cancelar</button>
            </div>
        </div>
    </div>

    <!-- MODAL CRIAR DIRETÓRIO -->
    <div id="modalCriarDiretorio" class="modal">
        <div class="modal-content">
            <div class="modal-header">📁 Criar Novo Diretório</div>
            <div class="form-group">
                <label>Caminho completo do diretório:</label>
                <input type="text" id="novo-dir-caminho" placeholder="Ex: C:\\temp\\nova_pasta">
            </div>
            <div class="modal-footer">
                <button class="btn btn-primary" onclick="criarDiretorio()">✅ Criar</button>
                <button class="btn" onclick="fecharModal('modalCriarDiretorio')">❌ Cancelar</button>
            </div>
        </div>
    </div>

    <script>
        let autoRefreshInterval = null;
        let abaAtual = 'monitor';

        // Muda de aba
        function mudarAba(aba) {
            // Remove active de todas as abas
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            // Adiciona active na aba selecionada
            event.target.classList.add('active');
            document.getElementById('tab-' + aba).classList.add('active');
            
            abaAtual = aba;
            atualizarAbaAtual();
        }

        // Atualiza aba atual
        function atualizarAbaAtual() {
            if (abaAtual === 'monitor') {
                carregarMonitor();
            } else if (abaAtual === 'processos') {
                carregarListaProcessos();
            } else if (abaAtual === 'memoria') {
                carregarMemoriaStatus();
            }
        }

        // Carrega aba monitor
        function carregarMonitor() {
            carregarCPU();
            carregarRAM();
            carregarDiscos();
            carregarTopCPU();
            carregarTopMemoria();
        }

        // Carrega informações da CPU
        async function carregarCPU() {
            try {
                const response = await fetch('/api/hardware/cpu');
                const data = await response.json();
                
                const html = `
                    <div class="stat-row">
                        <span class="stat-label">Núcleos Físicos:</span>
                        <span class="stat-value">${data.nucleos_fisicos}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Núcleos Lógicos:</span>
                        <span class="stat-value">${data.nucleos_logicos}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Frequência:</span>
                        <span class="stat-value">${data.frequencia_atual} MHz</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${data.uso_percentual}%">
                            ${data.uso_percentual}%
                        </div>
                    </div>
                `;
                
                document.getElementById('cpu-info').innerHTML = html;
            } catch (error) {
                console.error('Erro ao carregar CPU:', error);
            }
        }

        // Carrega informações da RAM
        async function carregarRAM() {
            try {
                const response = await fetch('/api/hardware/ram');
                const data = await response.json();
                
                const status = data.percentual_uso < 60 ? 'success' : (data.percentual_uso < 80 ? 'warning' : 'danger');
                
                const html = `
                    <div class="stat-row">
                        <span class="stat-label">Total:</span>
                        <span class="stat-value">${data.total_gb} GB</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Usado:</span>
                        <span class="stat-value">${data.usado_gb} GB</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Disponível:</span>
                        <span class="stat-value">${data.disponivel_gb} GB</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${data.percentual_uso}%">
                            ${data.percentual_uso}%
                        </div>
                    </div>
                `;
                
                document.getElementById('ram-info').innerHTML = html;
            } catch (error) {
                console.error('Erro ao carregar RAM:', error);
            }
        }

        // Carrega informações dos discos
        async function carregarDiscos() {
            try {
                const response = await fetch('/api/hardware/hd');
                const discos = await response.json();
                
                let html = '';
                discos.forEach(disco => {
                    html += `
                        <div class="disk-item">
                            <div class="disk-name">${disco.dispositivo} - ${disco.ponto_montagem}</div>
                            <div class="stat-row">
                                <span class="stat-label">Total:</span>
                                <span class="stat-value">${disco.total_gb} GB</span>
                            </div>
                            <div class="stat-row">
                                <span class="stat-label">Livre:</span>
                                <span class="stat-value">${disco.livre_gb} GB</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${disco.percentual_uso}%">
                                    ${disco.percentual_uso}%
                                </div>
                            </div>
                        </div>
                    `;
                });
                
                document.getElementById('hd-info').innerHTML = html;
            } catch (error) {
                console.error('Erro ao carregar discos:', error);
            }
        }

        // Carrega top CPU
        async function carregarTopCPU() {
            try {
                const response = await fetch('/api/processos/top_cpu');
                const processos = await response.json();
                
                let html = '<table class="process-table"><thead><tr><th>PID</th><th>Nome</th><th>CPU %</th></tr></thead><tbody>';
                
                processos.forEach(proc => {
                    html += `
                        <tr>
                            <td>${proc.pid}</td>
                            <td>${proc.nome}</td>
                            <td><span class="badge badge-warning">${proc.cpu_percentual}%</span></td>
                        </tr>
                    `;
                });
                
                html += '</tbody></table>';
                document.getElementById('top-cpu').innerHTML = html;
            } catch (error) {
                console.error('Erro:', error);
            }
        }

        // Carrega top memória
        async function carregarTopMemoria() {
            try {
                const response = await fetch('/api/memoria/top');
                const processos = await response.json();
                
                let html = '<table class="process-table"><thead><tr><th>PID</th><th>Nome</th><th>Mem %</th></tr></thead><tbody>';
                
                processos.forEach(proc => {
                    html += `
                        <tr>
                            <td>${proc.pid}</td>
                            <td>${proc.nome}</td>
                            <td><span class="badge badge-danger">${proc.memoria_percentual}%</span></td>
                        </tr>
                    `;
                });
                
                html += '</tbody></table>';
                document.getElementById('top-memoria').innerHTML = html;
            } catch (error) {
                console.error('Erro:', error);
            }
        }

        // Carrega lista completa de processos
        async function carregarListaProcessos() {
            try {
                const response = await fetch('/api/processos/listar');
                const processos = await response.json();
                
                let html = `
                    <p style="margin-bottom: 15px; color: #666;">
                        <strong>Total:</strong> ${processos.length} processos (mostrando primeiros 50)
                    </p>
                    <table class="process-table">
                        <thead>
                            <tr>
                                <th>PID</th>
                                <th>Nome</th>
                                <th>Status</th>
                                <th>CPU %</th>
                                <th>Mem %</th>
                                <th>Ação</th>
                            </tr>
                        </thead>
                        <tbody>
                `;
                
                processos.forEach(proc => {
                    html += `
                        <tr>
                            <td>${proc.pid}</td>
                            <td>${proc.nome}</td>
                            <td><span class="badge badge-success">${proc.status}</span></td>
                            <td>${proc.cpu_percentual}%</td>
                            <td>${proc.memoria_percentual}%</td>
                            <td>
                                <button class="btn btn-danger" onclick="finalizarProcesso(${proc.pid}, '${proc.nome}')">
                                    ❌ Finalizar
                                </button>
                            </td>
                        </tr>
                    `;
                });
                
                html += '</tbody></table>';
                document.getElementById('processos-lista').innerHTML = html;
            } catch (error) {
                console.error('Erro:', error);
            }
        }

        // Finaliza processo
        async function finalizarProcesso(pid, nome) {
            if (!confirm(`Deseja realmente finalizar o processo "${nome}" (PID: ${pid})?`)) {
                return;
            }

            try {
                const response = await fetch(`/api/processos/finalizar/${pid}`, {
                    method: 'POST'
                });
                const result = await response.json();
                
                const alertDiv = document.getElementById('processos-alert');
                if (result.sucesso) {
                    alertDiv.innerHTML = `<div class="alert alert-success">✅ ${result.mensagem}</div>`;
                    setTimeout(() => carregarListaProcessos(), 1000);
                } else {
                    alertDiv.innerHTML = `<div class="alert alert-danger">❌ ${result.mensagem}</div>`;
                }
                
                setTimeout(() => alertDiv.innerHTML = '', 5000);
            } catch (error) {
                console.error('Erro:', error);
            }
        }

        // Lista arquivos
        async function listarArquivos() {
            const caminho = document.getElementById('caminho-dir').value;
            
            try {
                const response = await fetch(`/api/arquivos/listar?caminho=${encodeURIComponent(caminho)}`);
                const data = await response.json();
                
                if (data.erro) {
                    document.getElementById('arquivos-lista').innerHTML = `<div class="alert alert-danger">${data.erro}</div>`;
                    return;
                }
                
                let html = `<p style="margin: 15px 0; color: #666;"><strong>Caminho:</strong> ${data.caminho}</p>`;
                
                data.itens.forEach(item => {
                    const icon = item.tipo === 'diretorio' ? '📁' : '📄';
                    html += `
                        <div class="file-item">
                            <div class="file-info">
                                <span class="file-icon">${icon}</span>
                                <div>
                                    <div style="font-weight: 600;">${item.nome}</div>
                                    <div style="font-size: 0.85em; color: #666;">
                                        ${item.tamanho_legivel} • ${item.modificado}
                                    </div>
                                </div>
                            </div>
                            <button class="btn btn-danger" onclick="deletarArquivo('${data.caminho}/${item.nome}', '${item.nome}')">
                                🗑️ Deletar
                            </button>
                        </div>
                    `;
                });
                
                document.getElementById('arquivos-lista').innerHTML = html;
            } catch (error) {
                console.error('Erro:', error);
            }
        }

        // Criar arquivo
        async function criarArquivo() {
            const caminho = document.getElementById('novo-arquivo-caminho').value;
            const conteudo = document.getElementById('novo-arquivo-conteudo').value;
            
            if (!caminho) {
                alert('Digite o caminho do arquivo!');
                return;
            }
            
            try {
                const response = await fetch('/api/arquivos/criar_arquivo', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({caminho, conteudo})
                });
                const result = await response.json();
                
                const alertDiv = document.getElementById('arquivos-alert');
                if (result.sucesso) {
                    alertDiv.innerHTML = `<div class="alert alert-success">✅ ${result.mensagem}</div>`;
                    fecharModal('modalCriarArquivo');
                    document.getElementById('novo-arquivo-caminho').value = '';
                    document.getElementById('novo-arquivo-conteudo').value = '';
                } else {
                    alertDiv.innerHTML = `<div class="alert alert-danger">❌ ${result.erro}</div>`;
                }
                
                setTimeout(() => alertDiv.innerHTML = '', 5000);
            } catch (error) {
                console.error('Erro:', error);
            }
        }

        // Criar diretório
        async function criarDiretorio() {
            const caminho = document.getElementById('novo-dir-caminho').value;
            
            if (!caminho) {
                alert('Digite o caminho do diretório!');
                return;
            }
            
            try {
                const response = await fetch('/api/arquivos/criar_diretorio', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({caminho})
                });
                const result = await response.json();
                
                const alertDiv = document.getElementById('arquivos-alert');
                if (result.sucesso) {
                    alertDiv.innerHTML = `<div class="alert alert-success">✅ ${result.mensagem}</div>`;
                    fecharModal('modalCriarDiretorio');
                    document.getElementById('novo-dir-caminho').value = '';
                } else {
                    alertDiv.innerHTML = `<div class="alert alert-danger">❌ ${result.erro}</div>`;
                }
                
                setTimeout(() => alertDiv.innerHTML = '', 5000);
            } catch (error) {
                console.error('Erro:', error);
            }
        }

        // Deletar arquivo
        async function deletarArquivo(caminho, nome) {
            if (!confirm(`Deseja realmente deletar "${nome}"?`)) {
                return;
            }
            
            try {
                const response = await fetch('/api/arquivos/deletar', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({caminho})
                });
                const result = await response.json();
                
                const alertDiv = document.getElementById('arquivos-alert');
                if (result.sucesso) {
                    alertDiv.innerHTML = `<div class="alert alert-success">✅ ${result.mensagem}</div>`;
                    listarArquivos();
                } else {
                    alertDiv.innerHTML = `<div class="alert alert-danger">❌ ${result.erro}</div>`;
                }
                
                setTimeout(() => alertDiv.innerHTML = '', 5000);
            } catch (error) {
                console.error('Erro:', error);
            }
        }

        // Carrega status memória
        async function carregarMemoriaStatus() {
            try {
                const response = await fetch('/api/memoria/status');
                const data = await response.json();
                
                const mem = data.memoria_virtual;
                const swap = data.memoria_swap;
                
                const html = `
                    <h3 style="margin-bottom: 15px;">💾 Memória Virtual</h3>
                    <div class="stat-row">
                        <span class="stat-label">Total:</span>
                        <span class="stat-value">${mem.total_gb} GB</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Usado:</span>
                        <span class="stat-value">${mem.usado_gb} GB</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Disponível:</span>
                        <span class="stat-value">${mem.disponivel_gb} GB</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${mem.percentual_uso}%">
                            ${mem.percentual_uso}%
                        </div>
                    </div>
                    
                    <h3 style="margin: 25px 0 15px 0;">💿 Memória Swap</h3>
                    <div class="stat-row">
                        <span class="stat-label">Total:</span>
                        <span class="stat-value">${swap.total_gb} GB</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Usado:</span>
                        <span class="stat-value">${swap.usado_gb} GB</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${swap.percentual_uso}%">
                            ${swap.percentual_uso}%
                        </div>
                    </div>
                `;
                
                document.getElementById('memoria-status').innerHTML = html;
            } catch (error) {
                console.error('Erro:', error);
            }
        }

        // Alocar memória (simulação)
        async function alocarMemoria() {
            const mb = document.getElementById('mb-alocar').value;
            
            try {
                const response = await fetch('/api/memoria/alocar', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({quantidade_mb: parseInt(mb)})
                });
                const result = await response.json();
                
                const alertDiv = document.getElementById('memoria-alert');
                if (result.sucesso) {
                    alertDiv.innerHTML = `<div class="alert alert-success">✅ ${result.mensagem}</div>`;
                    carregarMemoriaStatus();
                } else {
                    alertDiv.innerHTML = `<div class="alert alert-danger">❌ ${result.mensagem}</div>`;
                }
                
                setTimeout(() => alertDiv.innerHTML = '', 5000);
            } catch (error) {
                console.error('Erro:', error);
            }
        }

        // Modals
        function abrirModalCriarArquivo() {
            document.getElementById('modalCriarArquivo').classList.add('active');
        }

        function abrirModalCriarDiretorio() {
            document.getElementById('modalCriarDiretorio').classList.add('active');
        }

        function fecharModal(id) {
            document.getElementById(id).classList.remove('active');
        }

        // Auto refresh
        function toggleAutoRefresh() {
            const checkbox = document.getElementById('autoRefresh');
            
            if (checkbox.checked) {
                autoRefreshInterval = setInterval(atualizarAbaAtual, 5000);
            } else {
                if (autoRefreshInterval) {
                    clearInterval(autoRefreshInterval);
                    autoRefreshInterval = null;
                }
            }
        }

        // Inicialização
        window.onload = () => {
            carregarMonitor();
        };
    </script>
</body>
</html>
    '''

@app.route('/api/sistema/status')
def sistema_status():
    req = {'tipo': 'sistema', 'comando': 'status'}
    return jsonify(api.processar_requisicao(req))

@app.route('/api/hardware/<componente>')
def hardware_info(componente):
    comandos = {
        'cpu': 'cpu',
        'ram': 'ram',
        'hd': 'hd',
        'completo': 'info_completa',
        'cpu_nucleos': 'cpu_nucleos'
    }
    
    if componente in comandos:
        req = {'tipo': 'hardware', 'comando': comandos[componente]}
        return jsonify(api.processar_requisicao(req))
    return jsonify({'erro': 'Componente não encontrado'})

@app.route('/api/memoria/<comando>')
def memoria_info(comando):
    if comando == 'status':
        req = {'tipo': 'memoria', 'comando': 'status'}
    elif comando == 'top':
        req = {'tipo': 'memoria', 'comando': 'top_processos', 'parametros': {'limite': 10}}
    else:
        return jsonify({'erro': 'Comando não encontrado'})
    
    return jsonify(api.processar_requisicao(req))

@app.route('/api/memoria/alocar', methods=['POST'])
def memoria_alocar():
    dados = request.json
    req = {'tipo': 'memoria', 'comando': 'alocar', 'parametros': {'quantidade_mb': dados['quantidade_mb']}}
    return jsonify(api.processar_requisicao(req))

@app.route('/api/processos/<comando>')
def processos_info(comando):
    if comando == 'listar':
        req = {'tipo': 'processo', 'comando': 'listar'}
        processos = api.processar_requisicao(req)
        return jsonify(processos[:50])
    elif comando == 'top_cpu':
        req = {'tipo': 'processo', 'comando': 'top_cpu', 'parametros': {'limite': 10}}
    elif comando == 'contagem':
        req = {'tipo': 'processo', 'comando': 'contagem'}
    else:
        return jsonify({'erro': 'Comando não encontrado'})
    
    return jsonify(api.processar_requisicao(req))

@app.route('/api/processos/finalizar/<int:pid>', methods=['POST'])
def processo_finalizar(pid):
    req = {'tipo': 'processo', 'comando': 'finalizar', 'parametros': {'pid': pid}}
    return jsonify(api.processar_requisicao(req))

@app.route('/api/arquivos/listar')
def arquivos_listar():
    caminho = request.args.get('caminho', None)
    if caminho == '':
        caminho = None
    req = {'tipo': 'arquivo', 'comando': 'listar', 'parametros': {'caminho': caminho}}
    return jsonify(api.processar_requisicao(req))

@app.route('/api/arquivos/criar_arquivo', methods=['POST'])
def arquivos_criar_arquivo():
    dados = request.json
    req = {'tipo': 'arquivo', 'comando': 'criar_arquivo', 'parametros': dados}
    return jsonify(api.processar_requisicao(req))

@app.route('/api/arquivos/criar_diretorio', methods=['POST'])
def arquivos_criar_diretorio():
    dados = request.json
    req = {'tipo': 'arquivo', 'comando': 'criar_diretorio', 'parametros': dados}
    return jsonify(api.processar_requisicao(req))

@app.route('/api/arquivos/deletar', methods=['POST'])
def arquivos_deletar():
    dados = request.json
    req = {'tipo': 'arquivo', 'comando': 'deletar', 'parametros': dados}
    return jsonify(api.processar_requisicao(req))

def abrir_navegador():
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🖥️  SISTEMA OPERACIONAL - INTERFACE WEB COMPLETA")
    print("="*60)
    print("\n🌐 Servidor iniciando em: http://127.0.0.1:5000")
    print(" O navegador abrirá automaticamente...")
    print("\n Funcionalidades disponíveis:")
    print("   • Monitor de hardware em tempo real")
    print("   • Gerenciamento de processos")
    print("   • Gerenciamento de arquivos")
    print("   • Controle de memória")
    print("\nPara encerrar, pressione CTRL+C\n")
    
    threading.Thread(target=abrir_navegador, daemon=True).start()
    
    app.run(debug=False, host='127.0.0.1', port=5000)
