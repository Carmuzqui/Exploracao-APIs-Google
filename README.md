# Validação de APIs geoespaciais para estudos de dimensionamento e alocação de eletropostos

Este repositório consolida a suíte de testes e as provas de conceito (PoCs) para a integração de serviços de mapeamento (Google Maps Platform) e visualização GIS (ArcGIS). Os scripts aqui contidos são responsáveis por validar a extração e o processamento dos dados espaciais necessários para alimentar os modelos matemáticos de otimização e alocação da infraestrutura de recarga.

As coordenadas padrão utilizadas nos scripts de roteamento e matriz de distâncias estão focadas na região de Campinas, permitindo uma validação controlada do ambiente de estudo.

## Requisitos do sistema

* Python 3.9+
* Chave de API da Google Maps Platform (com acesso a Places, Directions, Distance Matrix e Roads)
* Ambiente virtual recomendado (venv ou conda)

## Instalação e configuração

1. Clone o repositório e acesse a raiz do projeto.
2. Instale as dependências listadas no arquivo de configuração:
   pip install -r requirements.txt
3. Crie um arquivo .env na raiz do projeto contendo as credenciais necessárias, como a chave de acesso da Google:
   GOOGLE_MAPS_API_KEY=sua_chave_aqui

## Estrutura de testes e módulos

A arquitetura de testes está dividida em duas frentes metodológicas: processamento em lote via terminal (para validação de algoritmos de rede) e visualização interativa via painéis (para análise espacial qualitativa).

### 1. Testes de backend (execução via terminal com python)
Estes scripts validam o retorno bruto das APIs do Google para cálculos de custo, distância e conectividade topológica.

* `test_directions.py`: valida a extração de rotas simples, tempos de viagem e instruções de navegação passo a passo.
* `test_distance_matrix.py`: executa o cálculo de matrizes de origem-destino (O-D), testando a cobertura radial e calculando taxas de conectividade entre pontos de interesse.
* `test_roads.py`: valida as funções de *Snap to Roads* e identificação de vias próximas, essenciais para ajustar coordenadas de GPS imprecisas à malha viária real.

Como executar:
python test_distance_matrix.py

### 2. Painéis exploratórios e análise espacial (execução via terminal com Streamlit)
Interfaces interativas desenvolvidas para visualização de dados georreferenciados e identificação de padrões de demanda.

* `teste_eletropostos.py`: dashboard principal para mapeamento da infraestrutura existente. Consome a Places API para identificar postos de recarga operacionais dentro de um raio de busca configurável.
* `teste_pois.py`: ferramenta analítica para geração de nós candidatos. Utiliza modelos de gravidade para classificar Polos Geradores de Viagem (POIs) e discretiza o espaço em uma malha (grid) de 200x200m, calculando os centroides de maior potencial atrativo.
* `teste_arcgis.py`: prova de conceito para renderização de elementos urbanos em 3D, validando a integração de modelos cilíndricos (representando os eletropostos) sobre o basemap OpenStreetMap.

Como executar:
streamlit run teste_pois.py
