"""
Testes de performance
"""
import pytest
from flow_agenda import Tarefa


class TestPerformance:
    def test_criar_muitas_tarefas(self, benchmark):
        def criar_tarefas():
            return [Tarefa(f"Tarefa {i}", "12:00", 30, "azul") for i in range(1000)]
        
        resultado = benchmark(criar_tarefas)
        assert len(resultado) == 1000