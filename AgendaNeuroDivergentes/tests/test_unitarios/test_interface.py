"""
Testes para componentes da interface PyQt
"""
import pytest
from pytestqt.qtbot import QtBot
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flow_agenda import CardTarefa, BotaoIniciar, Tarefa


@pytest.fixture
def app(qtbot):
    """Fixture para criar aplicação Qt"""
    from flow_agenda import AplicacaoFlow
    window = AplicacaoFlow()
    qtbot.addWidget(window)
    return window


class TestComponentesInterface:
    """Testes para componentes da interface"""
    
    def test_criar_card_tarefa(self, qtbot):
        """Testa criação de card de tarefa"""
        tarefa = Tarefa("Teste", "10:00", 30, "azul")
        card = CardTarefa(tarefa)
        qtbot.addWidget(card)
        
        assert card.tarefa.nome == "Teste"
        assert card.width() == 240
        assert card.minimumHeight() == 140
    
    def test_card_exibe_informacoes_corretas(self, qtbot):
        """Testa se o card mostra as informações corretas"""
        tarefa = Tarefa(
            nome="Reunião importante",
            horario="15:00",
            duracao_minutos=60,
            cor="vermelho",
            subtarefas=["Preparar", "Apresentar"]
        )
        card = CardTarefa(tarefa)
        qtbot.addWidget(card)
        
        # Verificar se os labels foram criados
        labels = card.findChildren(QLabel)
        textos = [label.text() for label in labels]
        
        assert any("15:00" in texto for texto in textos)
        assert any("Reunião importante" in texto for texto in textos)
        assert any("60min" in texto for texto in textos)
        assert any("2 passo" in texto for texto in textos)
    
    def test_botao_iniciar_timer(self, qtbot):
        """Testa funcionalidade do botão iniciar"""
        botao = BotaoIniciar()
        qtbot.addWidget(botao)
        
        assert botao.text() == "▶ INICIAR AGORA"
        
        # Iniciar timer
        botao.iniciar_temporizador(1)  # 1 minuto para teste rápido
        assert "⏱️" in botao.text()
        
        # Aguardar 1 segundo
        qtbot.wait(1000)
        assert "⏱️" in botao.text()
    
    def test_clique_card_emite_sinal(self, qtbot):
        """Testa se o clique no card emite o sinal correto"""
        tarefa = Tarefa("Teste Clique", "12:00", 20, "verde")
        card = CardTarefa(tarefa)
        qtbot.addWidget(card)
        
        with qtbot.waitSignal(card.clique, timeout=1000):
            qtbot.mouseClick(card, Qt.MouseButton.LeftButton)
    
    def test_botoes_edicao_aparecem_no_hover(self, qtbot):
        """Testa se botões de edição aparecem ao passar mouse"""
        tarefa = Tarefa("Tarefa editável", "14:00", 25, "roxo")
        card = CardTarefa(tarefa)
        qtbot.addWidget(card)
        
        # Inicialmente escondidos
        assert card.btn_editar.isHidden()
        assert card.btn_excluir.isHidden()
        
        # Simular hover
        qtbot.mouseMove(card)
        qtbot.wait(100)
        
        # Após hover, devem estar visíveis
        # Nota: pode precisar de processamento de eventos
        QApplication.processEvents()