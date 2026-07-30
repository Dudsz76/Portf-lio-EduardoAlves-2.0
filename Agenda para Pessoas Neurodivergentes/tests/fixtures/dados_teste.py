"""
Dados de teste reutilizáveis para o Flow Agenda
"""
from flow_agenda import Tarefa

# Tarefas de exemplo
TAREFA_VALIDA = {
    "nome": "Reunião importante",
    "horario": "14:30",
    "duracao_minutos": 60,
    "cor": "vermelho",
    "subtarefas": ["Preparar slides", "Apresentar", "Anotar feedback"],
    "nivel_barulho": "📢 Moderado",
    "descricao": "Reunião semanal da equipe"
}

TAREFA_SIMPLES = {
    "nome": "Café da manhã",
    "horario": "08:00",
    "duracao_minutos": 20,
    "cor": "verde"
}

# Lista de tarefas para testes
LISTA_TAREFAS = [
    Tarefa("Acordar", "07:00", 10, "amarelo"),
    Tarefa("Café", "07:30", 30, "verde"),
    Tarefa("Trabalhar", "09:00", 120, "azul"),
]

# JSON simulado para teste de persistência
JSON_VALIDO = {
    "tarefas": [
        {"nome": "Teste 1", "horario": "10:00", "duracao_minutos": 30, "cor": "azul", "concluida": False},
        {"nome": "Teste 2", "horario": "11:00", "duracao_minutos": 45, "cor": "verde", "concluida": True}
    ],
    "moedas": 50
}

JSON_INVALIDO = '{"tarefas": [arquivo corrompido...'

# Cores disponíveis
CORES_TESTE = ["azul", "verde", "amarelo", "vermelho", "roxo"]

# Níveis de barulho
BARULHOS_TESTE = ["🌿 Silencioso", "📢 Moderado", "⚠️ Caótico"]