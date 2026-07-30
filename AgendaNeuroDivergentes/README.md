# 🧠 Flow Agenda - App de Organização para Neurodivergências

O Flow Agenda é um aplicativo desktop desenvolvido em Python com PyQt6, criado especificamente para atender às necessidades de pessoas neurodivergentes. Diferente das agendas tradicionais (que podem ser entediantes, abstratas e facilmente ignoradas), o Flow Agenda foi pensado para respeitar o funcionamento do cérebro neurodivergente.
## 🎯 Objetivo

Oferecer uma ferramenta de organização que:

    Respeite a previsibilidade necessária para pessoas autistas

    Ajude com a cegueira temporal e paralisia de início do TDAH

    Elimine a culpa associada a lembretes agressivos

    Proporcione controle sensorial através de perfis de energia

# ✨ Funcionalidades Principais
## 📅 Linha do Tempo Visual

    Interface horizontal (como stories do Instagram), não uma lista vertical entediante

    Cards coloridos com significados fixos:

        🔵 Azul = Tarefa sozinho (recuperação)

        🟢 Verde = Tarefa prazerosa (interesse especial)

        🟡 Amarelo = Transição (locomoção, arrumar mochila)

        🔴 Vermelho = Obrigação social (consome energia)

        🟣 Roxo = Surpresa (conteúdo flexível)

## 🚂 Modo "Trem" (Transição Segura)

    Divide tarefas em subtarefas detalhadas

    Mostra o que esperar antes de começar (spoiler da atividade)

    Informa: duração, nível de barulho, próximo passo

    Progresso visual com marcação de etapas concluídas

## ▶️ Botão "Iniciar Agora" com Timer de 5 Minutos

    Solução para a paralisia de início do TDAH

    Timer visual com contagem regressiva

    Recompensa imediata ao concluir

    Frase motivacional: "Você começou! Que tal +10 min?"

## 🔔 Lembretes "Sem Culpa"

    Abordagem educada e permissiva

    Opções: "Reagendar", "15 min" (soneca) ou "Ignorar"

    Nunca faz o usuário se sentir cobrado ou culpado

## 🎛️ Perfis de Energia

    Baixa Energia (Overload): Interface suave, sem animações

    Normal: Equilíbrio padrão

    Hiperfoco: Preto e branco, sem distrações, bloqueio de notificações

## ✏️ CRUD Completo de Tarefas

    Criar, editar, excluir e limpar tarefas concluídas

    Interface acessível com campos claros

    Suporte a subtarefas e descrições detalhadas

---

# 🛠️ Tecnologias Utilizadas
Tecnologia	Finalidade
Python 3.10+	Linguagem principal
PyQt6	Interface gráfica desktop
JSON	Persistência local de dados
QTimer	Gerenciamento de temporizadores e lembretes
QPropertyAnimation	Animações suaves (quando perfil permite)

---
## Pré-requisitos
    bash
# 🚀 Como Executar o Projeto
  

    ###  Instalar Python 3.10 ou superior
    ###  Instalar a biblioteca PyQt6
    ###    pip install PyQt6

# Clone o repositório
git clone https://github.com/seu-usuario/flow-agenda.git

# Entre no diretório
cd flow-agenda

# Execute o aplicativo
python flow_agenda.py

---

# Arquivos do Projeto
    flow-agenda/
    ├── flow_agenda.py          # Código principal do aplicativo
    ├── flow_agenda.json        # Arquivo de dados (criado automaticamente)
    └── README.md               # Este arquivo

## 🎨 Design Neuroinclusivo - Por que funciona?
    Necessidade Neurodivergente	Solução no Flow Agenda
    Dificuldade com transição	"Trem" de subtarefas + aviso progressivo
    Ansiedade por imprevistos	Spoiler da atividade (barulho, duração, próximo passo)
    Paralisia de início	Botão "Iniciar agora" com timer de 5 min
    Cegueira temporal	Linha do tempo horizontal (não lista vertical)
    Sobrecarga sensorial	Perfis de energia (dieta de estímulos)
    Pensamento literal	Perguntas diretas (sim/não/reagendar), sem metáforas
📈 Principais Insights do Desenvolvimento

Durante a criação deste aplicativo, aprendi que:

    Ferramentas de produtividade tradicionais frequentemente falham para pessoas neurodivergentes porque assumem um funcionamento cognitivo "padrão"

    A culpa é o maior inimigo da consistência - lembretes agressivos geram evitação, não ação

    Previsibilidade reduz ansiedade - saber o que esperar de uma tarefa (barulho, duração, próximos passos) é tão importante quanto a tarefa em si

    Interface visual horizontal funciona melhor para TDAH do que listas verticais tradicionais

    Controle sensorial (perfis de energia) permite que o usuário regule seu próprio ambiente

🔮 Próximos Passos (Roadmap)

    Sistema completo de moedas e recompensas

    Sincronização com Google Calendar

    Notificações do sistema (tray icon)

    Modo "Body Double" (estudo/ trabalho junto virtual)

    Versão mobile (Kivy ou React Native)

    Exportação de relatórios de conclusão

    Temas personalizáveis por usuário

📬 Contato

Este projeto é parte do meu portfólio profissional de desenvolvimento de software inclusivo. Se você tem interesse em conhecer mais sobre meu trabalho, discutir oportunidades ou contribuir com o projeto, sinta-se à vontade para entrar em contato:
Contato	Link
LinkedIn	Eduardo Alves
E-mail	oliveiradudu76@gmail.com
📌 Notas Importantes

    Os dados das tarefas são salvos localmente no arquivo flow_agenda.json

    O aplicativo é totalmente offline - seus dados não saem do seu computador

    Desenvolvido com foco em acessibilidade e respeito às necessidades neurodivergentes

    Feedbacks e sugestões são sempre bem-vindos! 😊

🤝 Contribuindo

Contribuições são muito bem-vindas! Se você tem ideias para melhorar o Flow Agenda:

    Faça um fork do projeto

    Crie uma branch para sua feature (git checkout -b feature/nova-funcionalidade)

    Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade')

    Push para a branch (git push origin feature/nova-funcionalidade)

    Abra um Pull Request

📄 Licença

Este projeto está sob a licença MIT - sinta-se livre para usar, modificar e distribuir.

Feito com 💜, café ☕ e respeito às neurodiversidades.

"O mundo não foi feito para cérebros diferentes. Mas a tecnologia pode ser."

<!-- Badges de Status -->
[![CI Status](https://github.com/seu-usuario/flow-agenda/actions/workflows/ci.yml/badge.svg)](https://github.com/seu-usuario/flow-agenda/actions/workflows/ci.yml)
[![Security Scan](https://github.com/seu-usuario/flow-agenda/actions/workflows/security-scan.yml/badge.svg)](https://github.com/seu-usuario/flow-agenda/actions/workflows/security-scan.yml)
[![codecov](https://codecov.io/gh/seu-usuario/flow-agenda/branch/main/graph/badge.svg)](https://codecov.io/gh/seu-usuario/flow-agenda)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Tests](https://img.shields.io/badge/tests-pytest-blue.svg)](https://docs.pytest.org/)
[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)](https://codecov.io/)
