# 🫁 Projeto Final IoT - Monitoramento de Asma

**Integrantes:** Dmitri José, Kauã Hiro, Felipe Rocha, Welligton Siqueira, Alvaro Sena, Carlos Leonel

## 📖 O que é o projeto?

[cite_start]Este projeto foi desenvolvido como Projeto Final da disciplina de Internet das Coisas e Aplicações[cite: 533, 470]. [cite_start]O foco da solução é a **Saúde Conectada e Assistência**, atuando especificamente na autogestão de doenças pulmonares crônicas (Asma) voltada para pacientes pediátricos[cite: 481]. 

[cite_start]A solução propõe um dispositivo vestível (wearable) de pânico simulado que, ao ser acionado, alerta imediatamente o responsável através de uma interface interativa[cite: 658, 663]. [cite_start]O diferencial da aplicação é exibir um "Plano de Ação Ágil" na tela durante uma emergência, orientando o responsável com passos de primeiros socorros e administração de medicamentos em vez de deixá-lo procurar informações na internet[cite: 670, 671].

### 🛠️ Tecnologias Utilizadas (Stack 100% Python)
* [cite_start]**Hardware Simulado:** Microcontrolador ESP32 no simulador Wokwi (C++)[cite: 482, 485].
* [cite_start]**Comunicação:** MQTT via Broker (Mosquitto para local ou HiveMQ para nuvem)[cite: 486, 645, 648].
* [cite_start]**Back-end:** Python utilizando **FastAPI** e **fastapi-mqtt**[cite: 486, 611].
* [cite_start]**Banco de Dados:** **TimescaleDB** (PostgreSQL otimizado para séries temporais) rodando via Docker na porta limpa 5433[cite: 487, 463].
* [cite_start]**Front-end (Interface):** **Flet**, rodando nativamente em Python para Web/Desktop[cite: 483, 488].

---

## ⚙️ Como Instalar as Dependências

[cite_start]Para gerenciar os pacotes de forma absurdamente mais rápida que o pip padrão, utilizamos o gerenciador **`uv`**[cite: 452, 461].

### Passo 1: Criar o arquivo de requisitos
[cite_start]Na raiz do seu projeto, certifique-se de ter um arquivo chamado `requirements.txt` com as seguintes bibliotecas oficiais[cite: 454, 630]:

```text
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
```
# Criação do ambiente virtual
uv venv

# Ativação (Windows)
.venv\Scripts\activate

# Ativação (Linux/Mac)
source .venv/bin/activate
