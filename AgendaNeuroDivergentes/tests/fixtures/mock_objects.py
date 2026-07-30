"""
Objetos simulados (mocks) para testes do Flow Agenda
"""
from unittest.mock import Mock, MagicMock
from PyQt6.QtCore import QTimer

def criar_tarefa_mock(**kwargs):
    """Cria uma tarefa simulada com comportamento controlado"""
    tarefa = Mock()
    tarefa.nome = kwargs.get('nome', 'Tarefa Mock')
    tarefa.horario = kwargs.get('horario', '12:00')
    tarefa.duracao_minutos = kwargs.get('duracao', 30)
    tarefa.concluida = kwargs.get('concluida', False)
    tarefa.subtarefas = kwargs.get('subtarefas', [])
    return tarefa

def criar_app_mock():
    """Cria uma instância simulada do aplicativo"""
    app = Mock()
    app.tarefas = []
    app.moedas = 0
    app.perfil_atual = "Normal"
    
    # Simular métodos
    app.salvar_dados = Mock()
    app.atualizar_cards = Mock()
    app.verificar_lembretes = Mock()
    
    return app

def criar_timer_mock():
    """Cria um timer simulado para evitar esperas reais"""
    timer = Mock(spec=QTimer)
    timer.start = Mock()
    timer.stop = Mock()
    timer.timeout = Mock()
    return timer

def criar_qmessagebox_mock(resposta=None):
    """Simula caixa de diálogo com resposta predefinida"""
    mock = Mock()
    mock.exec = Mock(return_value=resposta)
    return mock

class MockCard:
    """Simula um Card de tarefa sem interface gráfica"""
    def __init__(self, tarefa):
        self.tarefa = tarefa
        self.visible = True
    
    def show(self):
        self.visible = True
    
    def hide(self):
        self.visible = False
    
    def click(self):
        """Simula clique no card"""
        return self.tarefa

class MockBancoDados:
    """Simula persistência de dados sem arquivo real"""
    def __init__(self):
        self.dados = {"tarefas": [], "moedas": 0}
    
    def salvar(self, dados):
        self.dados = dados
    
    def carregar(self):
        return self.dados
    
    def limpar(self):
        self.dados = {"tarefas": [], "moedas": 0}