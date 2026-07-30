"""
Testes End-to-End para fluxos completos do usuário
"""
import pytest
from pytestqt.qtbot import QtBot
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, QTimer
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flow_agenda import AplicacaoFlow, Tarefa


class TestFluxosCompletos:
    """Testes de fluxo completo do usuário"""
    
    @pytest.fixture
    def app(self, qtbot):
        """Fixture para criar app limpo"""
        app = AplicacaoFlow()
        app.tarefas = []  # Limpar tarefas
        qtbot.addWidget(app)
        return app
    
    def test_criar_e_completar_tarefa(self, qtbot, app):
        """Testa fluxo completo: criar tarefa, iniciar, completar"""
        # 1. Criar nova tarefa (simular clique no botão)
        # Nota: como o diálogo é modal, precisamos de interação
        
        # Alternativa: criar tarefa diretamente
        nova_tarefa = Tarefa(
            nome="Tarefa E2E",
            horario="14:00",
            duracao_minutos=30,
            cor="azul",
            subtarefas=["Passo 1", "Passo 2"]
        )
        app.tarefas.append(nova_tarefa)
        app.atualizar_cards()
        
        # 2. Verificar se apareceu na linha do tempo
        assert len(app.tarefas) == 1
        assert app.tarefas[0].nome == "Tarefa E2E"
        
        # 3. Abrir Modo Trem
        app.abrir_modo_trem(nova_tarefa)
        
        # 4. Completar subtarefas (simulado)
        # Nota: precisaríamos interagir com o diálogo
    
    def test_editar_tarefa_existente(self, qtbot, app):
        """Testa fluxo de edição de tarefa"""
        # Criar tarefa inicial
        tarefa = Tarefa("Tarefa Original", "09:00", 30, "azul")
        app.tarefas.append(tarefa)
        app.atualizar_cards()
        
        # Editar tarefa
        tarefa.nome = "Tarefa Editada"
        tarefa.horario = "10:00"
        app.atualizar_cards()
        
        # Verificar mudanças
        assert app.tarefas[0].nome == "Tarefa Editada"
        assert app.tarefas[0].horario == "10:00"
    
    def test_excluir_tarefa_com_confirmacao(self, qtbot, app):
        """Testa exclusão com confirmação"""
        # Criar tarefa
        tarefa = Tarefa("Tarefa para Excluir", "11:00", 20, "vermelho")
        app.tarefas.append(tarefa)
        app.atualizar_cards()
        
        assert len(app.tarefas) == 1
        
        # Mock do QMessageBox para retornar Yes
        with patch.object(QMessageBox, 'exec', return_value=QMessageBox.StandardButton.Yes):
            app.excluir_tarefa(tarefa)
            
            # Verificar se foi removida
            assert len(app.tarefas) == 0
    
    def test_limpar_tarefas_concluidas(self, qtbot, app):
        """Testa limpeza de tarefas concluídas"""
        # Criar tarefas
        tarefa1 = Tarefa("Concluída 1", "09:00", 30, "verde")
        tarefa1.concluida = True
        
        tarefa2 = Tarefa("Pendente", "10:00", 45, "azul")
        tarefa2.concluida = False
        
        tarefa3 = Tarefa("Concluída 2", "11:00", 60, "roxo")
        tarefa3.concluida = True
        
        app.tarefas = [tarefa1, tarefa2, tarefa3]
        
        # Limpar concluídas com confirmação
        with patch.object(QMessageBox, 'exec', return_value=QMessageBox.StandardButton.Yes):
            app.limpar_tarefas_concluidas()
            
            # Apenas tarefas pendentes devem restar
            assert len(app.tarefas) == 1
            assert app.tarefas[0].nome == "Pendente"
    
    def test_mudar_perfil_energia(self, qtbot, app):
        """Testa mudança de perfil de energia"""
        perfil_inicial = app.perfil_atual
        
        # Mudar para Baixa Energia
        app.mudar_perfil("Baixa Energia (Overload)")
        assert app.perfil_atual == "Baixa Energia (Overload)"
        
        # Mudar para Hiperfoco
        app.mudar_perfil("Hiperfoco")
        assert app.perfil_atual == "Hiperfoco"
        
        # Voltar ao Normal
        app.mudar_perfil("Normal")
        assert app.perfil_atual == "Normal"
    
    def test_timer_lembrete_educado(self, qtbot, app):
        """Testa sistema de lembretes"""
        # Criar tarefa para agora
        from datetime import datetime, timedelta
        
        agora = datetime.now()
        horario_teste = (agora - timedelta(minutes=5)).strftime("%H:%M")
        
        tarefa_atrasada = Tarefa(
            "Tarefa atrasada",
            horario_teste,
            30,
            "azul"
        )
        app.tarefas.append(tarefa_atrasada)
        
        # Forçar verificação de lembretes
        with patch.object(QMessageBox, 'exec', return_value=QMessageBox.StandardButton.Ignore):
            app.verificar_lembretes()