# 🖥️ Sistema Operacional Simplificado

Implementação educacional de um Sistema Operacional simplificado em Python, com interface web moderna para monitoramento e gerenciamento de hardware, processos, memória e arquivos em tempo real.

---

## 📌 Sobre o Projeto

Este projeto implementa um **Sistema Operacional simplificado** baseado na arquitetura de **kernel monolítico**, desenvolvido para fins educacionais.

O sistema coleta dados reais do computador e oferece uma interface web interativa para:

- 📊 Monitorar hardware (CPU, RAM, Disco)
- ⚙️ Gerenciar processos em execução
- 📁 Manipular arquivos e diretórios
- 🧠 Controlar uso de memória

---

## 🎓 Objetivo Educacional

Demonstrar na prática conceitos de:

- Arquitetura de Sistemas Operacionais  
- Gerenciamento de recursos (CPU, memória e I/O)  
- Comunicação entre camadas (User Space ↔ Kernel Space)  
- APIs e interfaces de sistema  
- Estrutura modular de um SO  

---

## Arquitetura

O sistema segue uma arquitetura em camadas inspirada em sistemas operacionais modernos:

```text
┌─────────────────────────────────────────────┐
│          Interface Web (HTML/CSS/JS)        │
│              Camada de Aplicação            │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│            Interface API (Flask)            │
│          Camada de Comunicação              │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│               Kernel SO                     │
│          Núcleo do Sistema                  │
└─────────────────────────────────────────────┘
         ↓              ↓              ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Gerenciador  │ │ Gerenciador  │ │ Gerenciador  │
│ de Memória   │ │ de Processos │ │ de Arquivos  │
└──────────────┘ └──────────────┘ └──────────────┘
         ↓              ↓              ↓
┌─────────────────────────────────────────────┐
│              Hardware (CPU, RAM, HD)        │
│          Camada de Hardware                 │
└─────────────────────────────────────────────┘
```

---

## 🧩 Componentes Principais

| Componente       | Descrição |
|------------------|------------|
| Hardware         | Abstração de CPU, RAM e HD (coleta dados reais do sistema) |
| Kernel SO        | Núcleo central que coordena todos os gerenciadores |
| Gerenciadores    | Módulos especializados em memória, processos e arquivos |
| Interface API    | Camada REST que expõe funcionalidades via HTTP |
| Interface Web    | Dashboard interativo para visualização e controle |

---

## Funcionalidades

### 📊 Monitor de Hardware

#### CPU
- Núcleos físicos e lógicos  
- Frequência atual e máxima  
- Uso percentual em tempo real  
- Uso por núcleo individual  

#### Memória RAM
- Total, usada e disponível  
- Percentual de uso  
- Memória Swap  
- Status de saúde  

#### Discos
- Partições detectadas  
- Espaço total, usado e livre  
- Sistema de arquivos  
- Estatísticas de I/O  

---

### ⚙️ Gerenciamento de Processos

- Listar processos em execução (até 50)
- Exibir PID, nome, status, CPU% e memória%
- Finalizar processos com confirmação
- Top 10 processos por uso de CPU
- Top 10 processos por uso de memória
- Contagem total de processos

---

### 📁 Gerenciamento de Arquivos

- Listar conteúdo de diretórios
- Criar arquivos com conteúdo
- Criar diretórios
- Deletar arquivos e pastas
- Visualizar metadados
- Navegação pelo sistema de arquivos

---

### 🧠 Gerenciamento de Memória

- Status detalhado de memória virtual
- Monitoramento de Swap
- Simulação de alocação
- Identificação de processos que mais consomem RAM
- Indicadores visuais de uso

---

### 🔄 Recursos da Interface

- Atualização automática a cada 5 segundos
- Atualização manual
- Sistema de abas
- Alertas visuais
- Design responsivo
- Barras de progresso animadas
- Modais para ações

---

## 🛠️ Tecnologias Utilizadas

### Backend

```python
psutil      # Acesso a informações de sistema
flask       # Framework web para API REST
threading   # Execução paralela
webbrowser  # Abertura automática do navegador
platform    # Informações da plataforma
```

### Frontend

- HTML5  
- CSS3  
- JavaScript (Vanilla)

---

## 📥 Instalação

### Pré-requisitos

- Python 3.8 ou superior  
- pip  
- Navegador moderno  

---

### Passo a Passo

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/sistema-operacional.git
cd sistema-operacional
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Ou manualmente:

```bash
pip install psutil flask
```

Execute o sistema:

```bash
python web_interface.py
```

Acesse no navegador:

```
http://127.0.0.1:5000
```

---

##  Como Usar

### 🌐 Modo Web (Recomendado)

```bash
python web_interface.py
```

Abas disponíveis:

- 📊 Monitor
- ⚙️ Processos
- 📁 Arquivos
- 🧠 Memória

---

### 💻 Modo Terminal

```bash
python main.py
```

Menu interativo com navegação numérica.

---

## 📁 Estrutura do Projeto

```text
sistema-operacional/
│
├── main.py
├── web_interface.py
├── interface_api.py
├── kernel_so.py
│
├── gerenciador_memoria.py
├── gerenciador_processos.py
├── gerenciador_arquivos.py
│
├── hardware.py
│
├── requirements.txt
├── README.md
└── LICENSE

