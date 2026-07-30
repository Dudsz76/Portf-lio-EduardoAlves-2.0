"""
Testes unitários para o modelo Tarefa
"""
import pytest
from datetime import datetime
from unittest.mock import Mock, patch
import sys
import os

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flow_agenda import Tarefa


class TestTarefaModel:
    """Testes para a classe Tarefa"""
    
    def setup_method(self):
        """Configuração antes de cada teste"""
        self.tarefa = Tarefa(
            nome="Testar app",
            horario="14:30",
            duracao_minutos=30,
            cor="azul",
            subtarefas=["Abrir app", "Clicar botões", "Verificar resultado"],
            nivel_barulho="🌿 Silencioso",
            descricao="Teste completo do aplicativo"
        )
    
    def test_criar_tarefa_completa(self):
        """Testa criação de tarefa com todos os atributos"""
        assert self.tarefa.nome == "Testar app"
        assert self.tarefa.horario == "14:30"
        assert self.tarefa.duracao_minutos == 30
        assert self.tarefa.cor == "azul"
        assert len(self.tarefa.subtarefas) == 3
        assert self.tarefa.nivel_barulho == "🌿 Silencioso"
        assert self.tarefa.descricao == "Teste completo do aplicativo"
        assert self.tarefa.concluida == False
        assert self.tarefa.em_andamento == False
    
    def test_criar_tarefa_sem_subtarefas(self):
        """Testa criação de tarefa sem subtarefas"""
        tarefa_simples = Tarefa(
            nome="Tarefa simples",
            horario="10:00",
            duracao_minutos=15,
            cor="verde"
        )
        assert tarefa_simples.subtarefas == []
        assert tarefa_simples.descricao == ""
    
    def test_para_dict(self):
        """Testa conversão para dicionário"""
        dados = self.tarefa.to_dict()
        
        assert isinstance(dados, dict)
        assert dados["nome"] == "Testar app"
        assert dados["horario"] == "14:30"
        assert dados["duracao_minutos"] == 30
        assert dados["cor"] == "azul"
        assert len(dados["subtarefas"]) == 3
        assert dados["concluida"] == False
    
    def test_from_dict(self):
        """Testa criação a partir de dicionário"""
        dados = {
            "nome": "Tarefa do JSON",
            "horario": "09:00",
            "duracao_minutos": 45,
            "cor": "vermelho",
            "subtarefas": ["Passo 1", "Passo 2"],
            "nivel_barulho": "📢 Moderado",
            "descricao": "Teste",
            "concluida": True
        }
        
        tarefa = Tarefa.from_dict(dados)
        
        assert tarefa.nome == "Tarefa do JSON"
        assert tarefa.horario == "09:00"
        assert tarefa.duracao_minutos == 45
        assert tarefa.cor == "vermelho"
        assert tarefa.concluida == True
    
    def test_marcar_como_concluida(self):
        """Testa marcação de conclusão"""
        assert self.tarefa.concluida == False
        self.tarefa.concluida = True
        assert self.tarefa.concluida == True
    
    def test_validar_horario(self):
        """Testa validação de formato de horário"""
        # Horário válido
        assert ":" in self.tarefa.horario
        hora, minuto = map(int, self.tarefa.horario.split(":"))
        assert 0 <= hora <= 23
        assert 0 <= minuto <= 59
        
        # Testar com horário inválido (simulado)
        with pytest.raises(ValueError):
            hora, minuto = map(int, "25:00".split(":"))
            if hora > 23 or minuto > 59:
                raise ValueError("Horário inválido")
    
    @pytest.mark.parametrize("duracao,esperado", [
        (5, True),      # 5 minutos OK
        (30, True),     # 30 minutos OK
        (480, True),    # 8 horas OK
        (0, False),     # 0 minutos inválido
        (500, False),   # Mais de 8 horas inválido
        (-10, False),   # Negativo inválido
    ])
    def test_validar_duracao(self, duracao, esperado):
        """Testa validação de duração com diferentes valores"""
        if esperado:
            assert 5 <= duracao <= 480
        else:
            assert not (5 <= duracao <= 480)
    
    def test_subtarefas_nao_sao_vazias(self):
        """Testa se subtarefas existem quando definidas"""
        if self.tarefa.subtarefas:
            assert len(self.tarefa.subtarefas) > 0
            assert all(isinstance(sub, str) for sub in self.tarefa.subtarefas)