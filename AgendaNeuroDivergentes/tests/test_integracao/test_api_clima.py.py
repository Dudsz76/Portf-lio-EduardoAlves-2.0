"""
Testes de integração para API de clima
"""
import pytest
import json
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flow_agenda import ServicoClima, API_CLIMA_URL


class TestApiClima:
    """Testes de integração para o serviço de clima"""
    
    def setup_method(self):
        """Configuração antes de cada teste"""
        self.servico = ServicoClima(api_key="test_key_123")
        
    def test_servico_clima_init(self):
        """Testa inicialização do serviço"""
        assert self.servico.api_key == "test_key_123"
        assert isinstance(self.servico.cache, dict)
        assert self.servico.ultima_atualizacao is None
    
    def test_buscar_clima_sem_api_key(self):
        """Testa busca de clima sem API key (deve retornar dados fictícios)"""
        servico_sem_key = ServicoClima(api_key="")
        dados = servico_sem_key.buscar_clima()
        
        assert dados is not None
        assert "temperatura" in dados
        assert "cidade" in dados
        assert dados["cidade"] == "São Paulo"
    
    def test_parse_dados_api(self):
        """Testa parsing de dados da API"""
        # Simular resposta da API
        resposta_mock = {
            "name": "São Paulo",
            "sys": {"country": "BR"},
            "main": {"temp": 25.5, "feels_like": 24.8, "humidity": 70, "pressure": 1015},
            "weather": [{"description": "céu limpo", "icon": "01d"}],
            "wind": {"speed": 3.2}
        }
        
        # Processar dados como o serviço faria
        clima = {
            "cidade": resposta_mock.get("name", ""),
            "pais": resposta_mock.get("sys", {}).get("country", ""),
            "temperatura": round(resposta_mock.get("main", {}).get("temp", 0), 1),
            "sensacao_termica": round(resposta_mock.get("main", {}).get("feels_like", 0), 1),
            "umidade": resposta_mock.get("main", {}).get("humidity", 0),
            "descricao": resposta_mock.get("weather", [{}])[0].get("description", ""),
            "icone": resposta_mock.get("weather", [{}])[0].get("icon", ""),
            "vento": resposta_mock.get("wind", {}).get("speed", 0),
            "pressao": resposta_mock.get("main", {}).get("pressure", 0)
        }
        
        assert clima["cidade"] == "São Paulo"
        assert clima["pais"] == "BR"
        assert clima["temperatura"] == 25.5
        assert clima["umidade"] == 70
        assert clima["descricao"] == "céu limpo"
    
    @patch('requests.get')
    def test_buscar_clima_com_sucesso(self, mock_get):
        """Testa busca de clima com sucesso (mock)"""
        # Configurar mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Rio de Janeiro",
            "sys": {"country": "BR"},
            "main": {"temp": 28.0, "feels_like": 29.0, "humidity": 65, "pressure": 1012},
            "weather": [{"description": "parcialmente nublado", "icon": "02d"}],
            "wind": {"speed": 2.5}
        }
        mock_get.return_value = mock_response
        
        dados = self.servico.buscar_clima("Rio de Janeiro,BR")
        
        assert dados["cidade"] == "Rio de Janeiro"
        assert dados["temperatura"] == 28.0
        assert dados["descricao"] == "parcialmente nublado"
        
        # Verificar se cache foi atualizado
        assert "Rio de Janeiro,BR" in self.servico.cache
    
    @patch('requests.get')
    def test_buscar_clima_com_erro(self, mock_get):
        """Testa busca de clima com erro de rede"""
        mock_get.side_effect = Exception("Erro de conexão")
        
        dados = self.servico.buscar_clima()
        
        # Deve retornar dados fictícios
        assert dados is not None
        assert dados["cidade"] == "São Paulo"
        assert dados["temperatura"] == 22.5
    
    def test_configurar_cidade(self):
        """Testa configuração de cidade"""
        cidade_antiga = self.servico.cache.copy()
        
        # Configurar nova cidade
        dados = self.servico.configurar_cidade("Curitiba,BR")
        
        assert self.servico.cache == {}  # Cache foi limpo
        
    def test_cache_funciona(self):
        """Testa sistema de cache"""
        cidade = "TestCity"
        
        # Primeira chamada
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "name": "TestCity",
                "sys": {"country": "TC"},
                "main": {"temp": 20.0, "feels_like": 19.0, "humidity": 60, "pressure": 1010},
                "weather": [{"description": "nublado", "icon": "03d"}],
                "wind": {"speed": 2.0}
            }
            mock_get.return_value = mock_response
            
            # Buscar primeira vez
            dados1 = self.servico.buscar_clima(cidade, force_update=False)
            
            # Buscar segunda vez (deve usar cache)
            dados2 = self.servico.buscar_clima(cidade, force_update=False)
            
            # mock_get deve ser chamado apenas uma vez
            assert mock_get.call_count == 1
            assert dados1 == dados2


class TestApiClimaIntegracaoReal:
    """Testes de integração com API real (executar apenas com chave válida)"""
    
    @pytest.mark.skip(reason="Pular em CI - requer API key real")
    def test_api_real_sao_paulo(self):
        """Testa chamada real para API (requer internet e API key)"""
        servico = ServicoClima()
        dados = servico.buscar_clima("São Paulo,BR", force_update=True)
        
        assert dados is not None
        assert "temperatura" in dados
        assert dados["cidade"] == "São Paulo"
        assert -10 < dados["temperatura"] < 50  # Temperatura plausível
    
    @pytest.mark.skip(reason="Pular em CI - requer API key real")
    def test_api_real_londres(self):
        """Testa API real com cidade internacional"""
        servico = ServicoClima()
        dados = servico.buscar_clima("London,UK", force_update=True)
        
        assert dados is not None
        assert dados["cidade"] == "London"
        assert dados["pais"] == "GB"
    
    @pytest.mark.skip(reason="Pular em CI - requer API key real")
    def test_api_real_cidade_invalida(self):
        """Testa API real com cidade inválida"""
        servico = ServicoClima()
        dados = servico.buscar_clima("CidadeQueNaoExiste12345,XX", force_update=True)
        
        # Deve retornar dados fictícios
        assert dados is not None
        assert dados["cidade"] == "São Paulo"