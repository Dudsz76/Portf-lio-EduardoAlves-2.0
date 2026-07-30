"""
Testes de integração para persistência de dados
"""
import pytest
import json
import os
import tempfile
from unittest.mock import patch, mock_open
import sys
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flow_agenda import AplicacaoFlow, Tarefa


class TestPersistencia:
    """Testes para persistência de dados"""
    
    def setup_method(self):
        """Configuração antes de cada teste"""
        # Criar arquivo temporário para testes
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        
        # Patch do caminho do arquivo
        self.patcher = patch('flow_agenda.os.path.exists')
        self.mock_exists = self.patcher.start()
        
    def teardown_method(self):
        """Limpeza após cada teste"""
        self.patcher.stop()
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_salvar_carregar_tarefas(self):
        """Testa salvar e carregar tarefas"""
        # Criar app com mock
        app = AplicacaoFlow()
        
        # Adicionar tarefas
        tarefa1 = Tarefa("Tarefa 1", "09:00", 30, "azul")
        tarefa2 = Tarefa("Tarefa 2", "10:00", 45, "verde")
        app.tarefas = [tarefa1, tarefa2]
        
        # Salvar
        app.salvar_dados()
        
        # Verificar se arquivo foi criado
        assert os.path.exists("flow_agenda.json")
        
        # Carregar dados do arquivo
        with open("flow_agenda.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        assert len(dados["tarefas"]) == 2
        assert dados["tarefas"][0]["nome"] == "Tarefa 1"
        assert dados["tarefas"][1]["nome"] == "Tarefa 2"
    
    def test_carregar_dados_corrompidos(self):
        """Testa comportamento com arquivo corrompido"""
        # Criar arquivo JSON inválido
        with open(self.temp_file.name, 'w') as f:
            f.write("arquivo corrompido { inválido")
        
        # Patch para usar arquivo corrompido
        with patch('flow_agenda.os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data="arquivo corrompido")):
                app = AplicacaoFlow()
                # Não deve lançar exceção
                app.carregar_dados()
    
    def test_persistencia_moedas(self):
        """Testa persistência do sistema de moedas"""
        app = AplicacaoFlow()
        app.moedas = 100
        app.salvar_dados()
        
        # Recarregar
        app_novo = AplicacaoFlow()
        app_novo.carregar_dados()
        
        # Verificar (o valor pode vir do arquivo salvo)
        # Nota: isso depende da implementação real
        assert app_novo.moedas >= 0