# 📊 Painel de Impacto: Pandemia & Economia

Projeto de Data Science desenvolvido para a disciplina do **SENAC Pernambuco**, sob orientação do **Prof. Heuryk Wylk**.  

O dashboard integra dados globais de saúde e indicadores socioeconômicos para analisar o impacto da pandemia de COVID-19 em relação ao PIB dos países.

---

# 🚀 Sobre o Projeto

O objetivo principal deste projeto é demonstrar um pipeline completo de **ETL (Extract, Transform, Load)** utilizando Python, APIs REST, banco de dados relacional e visualização interativa de dados.

A aplicação realiza:

- Coleta automática de dados oficiais de COVID-19
- Integração com indicadores econômicos globais
- Processamento e limpeza de dados
- Armazenamento em banco relacional
- Visualização dinâmica através de dashboard interativo

Além da análise técnica, o projeto também aplica boas práticas de visualização e padronização de dados no formato brasileiro (PT-BR).

---

# 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.12 | Linguagem principal |
| Streamlit | Dashboard interativo |
| Plotly Express | Gráficos e visualizações |
| Pandas | Manipulação e análise de dados |
| SQLAlchemy | ORM e integração com banco |
| SQLite | Persistência local dos dados |

---

# ⚙️ Arquitetura ETL

## 1️⃣ Extract (Extração)

Os dados são obtidos através de APIs públicas:

### 🌍 Dados da Pandemia
- API: Disease.sh
- Informações coletadas:
  - Casos confirmados
  - Óbitos
  - Recuperados
  - Casos ativos
  - Histórico temporal

### 💰 Dados Econômicos
- API: World Bank API
- Informação coletada:
  - PIB (GDP) mais recente do país selecionado

---

## 2️⃣ Transform (Transformação)

Durante esta etapa são aplicadas regras de tratamento e análise:

- Limpeza de dados nulos
- Tratamento de séries temporais
- Conversão e padronização de datas
- Formatação numérica no padrão brasileiro
- Cálculo de média móvel de 7 dias

### 📈 Média Móvel

A média móvel é utilizada para reduzir ruídos causados por:
- atrasos de notificação
- subnotificação
- inconsistências diárias

Isso permite uma análise mais fiel das tendências da pandemia.

---

## 3️⃣ Load (Carga)

Os dados processados são armazenados no banco:

```bash
covid_analise.db
```

O uso do SQLite permite:
- carregamento rápido do dashboard
- persistência local
- simplicidade de manutenção
- facilidade de testes

---

# 📊 Visualizações Implementadas

## ✅ KPI Cards

Indicadores rápidos contendo:
- Casos Totais
- Óbitos
- Recuperados
- PIB do país selecionado

---

## 📈 Evolução Temporal

Gráfico de área mostrando:
- evolução dos óbitos
- comportamento das ondas da pandemia
- tendência através da média móvel

---

## 🍩 Proporção de Desfechos

Gráfico Donut exibindo:
- Casos Ativos
- Recuperados
- Óbitos

### 🎨 Escala de cores padronizada:
- Verde → Recuperados
- Vermelho → Óbitos
- Azul/Laranja → Casos ativos

---

# 🗂️ Estrutura do Projeto

```bash
📦 projeto-covid-dashboard
 ┣ 📂 data
 ┣ 📂 database
 ┣ 📂 services
 ┣ 📂 utils
 ┣ 📜 main.py
 ┣ 📜 requirements.txt
 ┣ 📜 covid_analise.db
 ┗ 📜 README.md
```

---

# 🔧 Como Executar o Projeto

## 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
```

---

## 2️⃣ Acesse a pasta

```bash
cd nome-do-repositorio
```

---

## 3️⃣ Crie um ambiente virtual

### Linux / Mac

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 4️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

Ou manualmente:

```bash
pip install requests pandas sqlalchemy streamlit plotly
```

---

## 5️⃣ Execute a aplicação

```bash
streamlit run main.py
```

---

# 📝 Requisitos do Projeto (SENAC)

Este projeto atende aos requisitos solicitados pela disciplina:

- [x] Extração de dados oficiais
- [x] Integração com indicadores econômicos
- [x] Transformação e tratamento de dados
- [x] Cálculo de média móvel
- [x] Visualizações interativas
- [x] Persistência em banco relacional
- [x] Dashboard funcional em Streamlit

---

# 🎯 Objetivos Acadêmicos

Este projeto foi desenvolvido com foco em:

- Engenharia de Dados
- ETL
- Visualização de Dados
- Integração com APIs REST
- Persistência relacional
- Data Science aplicada
- Boas práticas em Python

---

# 👨‍💻 Desenvolvedores

Desenvolvido por:

**Nicolas Tavares**  
SENAC Pernambuco — 2026

---

# 📄 Licença

Projeto acadêmico desenvolvido exclusivamente para fins educacionais.
