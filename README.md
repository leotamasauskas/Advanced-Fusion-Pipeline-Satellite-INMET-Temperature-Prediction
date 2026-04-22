# Predição de Temperatura em Belém: Fusão de Dados (Satélite + INMET) e Machine Learning

> **Aviso de Projeto:** Este repositório reflete uma metodologia refinada e paralela implementando modelos tradicionais e avançados de predição de temperatura diária.

Este projeto tem como objetivo prever a temperatura do ar (a 2 metros de altura) em Belém do Pará, utilizando uma arquitetura inovadora de fusão de dados. O pipeline combina dados meteorológicos de medição direta em superfície por estações (INMET) com estimativas de sensoriamento remoto (Satélite), mitigando lacunas de dados físicos e aumentando a capacidade de captação de tendências através de modelos de Machine Learning.

## Fontes de Dados
*   **Target (Variável Alvo):** Medições diárias autênticas da temperatura média vindas das estações do **INMET** (Instituto Nacional de Meteorologia).
*   **Dados Complementares (Satélite):** Histórico de temperatura 2m (`1994 - 2024`) recuperados de datasets de satélite. Fornecem ampla cobertura e continuidade onde dados físicos podem falhar, servindo como "memória climática" de referência.

## Engenharia de Atributos (Feature Engineering)
As variáveis foram enriquecidas para incorporar o comportamento histórico e cíclico da temperatura na área de estudo:
1.  **Memória Térmica e Tendências:** Lags da temperatura (últimos 30 dias), janelas móveis médias (Rolling Means de 7 e 30 dias) e anomalias térmicas de dados de satélite.
2.  **Sazonalidade Cíclica Harmonizada:** Utilização das transformações trigonométricas (Seno e Cosseno) aplicadas sobre o dia do ano, permitindo que os modelos interpretem a ciclicidade regular das estações.

## Modelagem e Abordagem Temporal
Para impedir qualquer "vazamento temporal" (data leakage) na arquitetura, os dados foram particionados estritamente na forma cronológica:
*   **Treino:** Até 2016
*   **Validação:** 2017 a 2020 (usado para calibração e Early Stopping)
*   **Teste:** 2021 em diante (avaliação final de precisão)

### Modelos Utilizados
A arquitetura se estende sobre diferentes paradigmas científicos para comparação sólida:

1.  **Random Forest (Estratégia Fusion vs SatOnly):** Validado que a incorporação de lags físicos (fusion) traz enormes ganhos de performance (*Skill_Score*) contra modelos ingênuos baseados só em satélites.
2.  **Stacking Ensemble:** Meta-modelo agregador via **RidgeCV**, que penaliza ponderações infladas de modelos ruidosos, consolidando o melhor das múltiplas abordagens Random Forest e tradicionais.
3.  **SARIMAX (Modelo Estatístico V2):** Ajustado em janelas deslizantes otimizadas, incorporando dados de satélite e vetores sazonais (`sin/cos`) como variáveis exógenas (não dependentes), provendo robustez a ciclos de anomalias passadas.
4.  **Rede Neural LSTM (Deep Learning V2):** Arquitetura profunda, purificada de *target leakage*, analisando sequências retroativas temporais curtas (TIMESTEPS limitados) puramente como blocos de predição temporal estrita, operando com taxas moderadas de `Dropout` para assegurar o controle de variância sobre valores anômalos.

## Arquivos no Repositório

```text
├── data/                                 # (No histórico/Raiz do dir: Arquivos .csv limpos e mesclados)
├── models.ipynb                          # Notebook central com os modelos, grids de treino e extração de métricas
├── generate_study_map.py                 # (Se aplicável) Pipeline para geração visual da área de estudo
├── metodologia_implementada.txt          # Diário e anotações científicas de experimentação do Pipeline
├── README.md                             # Este guia
└── .gitignore                            # Exclusão do ambiente virtual Python   
```

## Como Usar
1. Clone o repositório.
2. Crie um ambiente virtual com as dependências apropriadas (`numpy`, `pandas`, `tensorflow`, `scikit-learn`, `statsmodels`).
3. Abra o arquvo base `models.ipynb` rodando as células em ordem. A célula "Otimização Pipeline Paralelo" final calculará o *Ranking* métrico oficial dos algoritmos via RMSE e _Sutcliffe Efficiency_.

---
*Criado como passo final da iteração metodológica para documentação de avanço da predição térmica via fusão satélite-superfície.*
