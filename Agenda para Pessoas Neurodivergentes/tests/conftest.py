"""
Fixtures compartilhadas para TODOS os testes do Flow Agenda
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flow_agenda import AplicacaoFlow, Tarefa


@pytest.fixture
def app(qtbot):
    """App disponível para qualquer teste"""
    app = AplicacaoFlow()
    qtbot.addWidget(app)
    return app


@pytest.fixture
def tarefa_padrao():
    """Tarefa padrão reutilizável"""
    return Tarefa("Teste", "14:00", 30, "azul")


@pytest.fixture
def tarefa_com_subtarefas():
    """Tarefa com subtarefas"""
    return Tarefa(
        "Tarefa Complexa", 
        "15:00", 
        60, 
        "vermelho",
        subtarefas=["Passo 1", "Passo 2", "Passo 3"]
    )


# ⬇️ ADICIONE ESTA FIXTURE ⬇️
@pytest.fixture
def qtbot(qtbot):
    """Fixture do pytest-qt para testes de interface"""
    return qtbot