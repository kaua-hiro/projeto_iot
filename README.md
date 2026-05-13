# 🫁 Projeto Final IoT - Monitoramento de Asma

**Integrantes:** Dmitri José, Kauã Hiro, Felipe Rocha, Welligton Siqueira, Alvaro Sena, Carlos Leonel

## 📖 O que é o projeto?

Este projeto foi desenvolvido como Projeto Final da disciplina de Internet das Coisas e Aplicações. O foco da solução é a **Saúde Conectada e Assistência**, atuando especificamente na autogestão de doenças pulmonares crônicas (Asma) voltada para pacientes pediátricos. 

A solução propõe um dispositivo vestível (wearable) de pânico simulado que, ao ser acionado, alerta imediatamente o responsável através de uma interface interativa. O diferencial da aplicação é exibir um "Plano de Ação Ágil" na tela durante uma emergência, orientando o responsável com passos de primeiros socorros e administração de medicamentos em vez de deixá-lo procurar informações na internet.

### 🛠️ Tecnologias Utilizadas (Stack 100% Python)
* **Hardware Simulado:** Microcontrolador ESP32 no simulador Wokwi (C++).
* **Comunicação:** MQTT via Broker Público (HiveMQ).
* **Back-end:** Python utilizando **FastAPI** e **fastapi-mqtt**.
* **Banco de Dados:** **TimescaleDB** (PostgreSQL otimizado para séries temporais) rodando via Docker na porta limpa 5433.
* **Front-end (Interface):** **Flet**, rodando nativamente em Python para Desktop.

---

## ⚙️ Como Instalar as Dependências

Para gerenciar os pacotes de forma rápida e eficiente, utilizamos o gerenciador **uv**.

### Passo 1: Arquivo de Requisitos
Na raiz do seu projeto, certifique-se de ter um arquivo chamado `requirements.txt` com as seguintes bibliotecas oficiais:

    databases>=0.9.0
    fastapi>=0.136.1
    fastapi-mqtt>=2.0.0
    asyncpg>=0.29.0
    ruff>=0.15.12
    uvicorn>=0.46.0
    flet>=0.85.0
    requests>=2.34.0
    paho-mqtt>=2.1.0
    flet-desktop>=0.85.0

### Passo 2: Configuração do Ambiente

Criação do ambiente virtual:

    uv venv

Ativação (Windows):

    .venv\Scripts\activate

Ativação (Linux/Mac):

    source .venv/bin/activate

Instalação das bibliotecas:

    uv pip install -r requirements.txt

---

## 🚀 Como Executar a Aplicação

A arquitetura do projeto exige que os serviços sejam iniciados em terminais separados. Siga a ordem exata abaixo:

### 1. Iniciar o Banco de Dados (Docker)
Com o Docker Desktop aberto, levante o contêiner do TimescaleDB rodando na raiz do projeto:

    docker-compose up -d

### 2. Iniciar o Cérebro do Sistema (Back-end)
Abra um terminal (certifique-se de que o Python correto está sendo utilizado) e inicie o servidor escutando a nuvem:

    python backendwokwi.py

### 3. Iniciar a Interface de Alerta (Front-end)
Abra um segundo terminal e execute o aplicativo visual. Ele iniciará com o status de "Monitorando" (Coração Verde):

    python frontend.py

### 4. Disparar a Emergência (Teste de Integração)
Para simular o acionamento do botão do ESP32 via nuvem sem depender do Wokwi, abra um terceiro terminal e execute o script de disparo:

    python disparo.py

Assim que o comando for executado, o payload `{"alerta": "ON"}` será enviado ao Broker MQTT e a interface visual mudará instantaneamente para o Plano de Ação Ágil.
