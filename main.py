import requests
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURAÇÃO ---
DB_CONFIG = "sqlite:///covid_analise.db" 

class CovidETL:
    def __init__(self, country_name="brazil", country_code="BRA"):
        self.country_name = country_name
        self.country_code = country_code

    def extract(self):
        covid_url = f"https://disease.sh/v3/covid-19/historical/{self.country_name}?lastdays=all"
        wb_url = f"http://api.worldbank.org/v2/country/{self.country_code}/indicator/NY.GDP.MKTP.CD?format=json"
        
        c_res = requests.get(covid_url).json()
        w_res = requests.get(wb_url).json()
        
        hist = c_res['timeline']
        df_c = pd.DataFrame({
            'Data': list(hist['cases'].keys()),
            'Casos': list(hist['cases'].values()),
            'Mortes': list(hist['deaths'].values()),
            'Recuperados': list(hist['recovered'].values())
        })
        return df_c, pd.DataFrame(w_res[1])

    def transform(self, df_c, df_w):

        df_c['Data'] = pd.to_datetime(df_c['Data'])

        mortes_diarias = df_c['Mortes'].diff()
        mortes_diarias = mortes_diarias.fillna(0)
        mortes_diarias = mortes_diarias.clip(lower=0)
        limite_superior = mortes_diarias.quantile(0.99)

        mortes_diarias = mortes_diarias.mask(
            mortes_diarias > limite_superior
        )

        mortes_diarias = mortes_diarias.ffill()

        media_movel = (
            mortes_diarias
            .rolling(window=7, min_periods=1)
            .mean()
        )

        media_movel = media_movel.clip(lower=0)

        df_c['Media_Movel_Mortes'] = media_movel.round(2)

        df_w_valid = df_w.dropna(subset=['value'])

        pib_valor = (
            df_w_valid
            .sort_values(by='date', ascending=False)
            .iloc[0]['value']
            if not df_w_valid.empty else 0
        )

        df_c['PIB_Referencia'] = pib_valor
        df_c['Pais'] = self.country_name.capitalize()

        return df_c

    def load(self, df):
        engine = create_engine(DB_CONFIG)
        df.to_sql('dashboard_covid', engine, if_exists='replace', index=False)

def formatar_moeda_br(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_inteiro_br(valor):
    return f"{int(valor):,}".replace(",", ".")

def run_dashboard():
    st.set_page_config(page_title="Data Science SENAC - Projeto COVID", layout="wide")
    
    st.markdown("""
        <style>
        .stMetric { 
            background-color: #1f2937; 
            padding: 20px; 
            border-radius: 12px; 
            border-left: 5px solid #3b82f6;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Painel de Impacto: Pandemia & Economia")
    st.divider()

    etl = CovidETL()
    try:
        raw_c, raw_w = etl.extract()
        df = etl.transform(raw_c, raw_w)
        etl.load(df)

        m1, m2, m3 = st.columns(3)
        total_casos = df['Casos'].iloc[-1]
        total_mortes = df['Mortes'].iloc[-1]
        pib_total = df['PIB_Referencia'].iloc[0]

        m1.metric("Total de Casos", formatar_inteiro_br(total_casos))
        m2.metric("Total de Óbitos", formatar_inteiro_br(total_mortes))
        m3.metric("PIB do País (USD)", f"US$ {formatar_moeda_br(pib_total)}")

        st.write("---")

        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader("Evolução Temporal (Média Móvel)")
            fig_line = px.area(df, x='Data', y='Media_Movel_Mortes', color_discrete_sequence=['#ef4444'])
            fig_line.update_layout(template="plotly_dark")
            st.plotly_chart(fig_line, use_container_width=True)

        with col_right:
            st.subheader("Proporção de Desfechos")
            
            # Em vez de iloc[-1], pegamos o maior valor acumulado para evitar erros de data
            total_confirmados = df['Casos'].max()
            mortes_acumuladas = df['Mortes'].max()
            recuperados_acumulados = df['Recuperados'].max() # Aqui ele vai achar os 17M que você viu no banco
            
            # Cálculo de Ativos baseado nos máximos
            ativos = total_confirmados - (mortes_acumuladas + recuperados_acumulados)
            
            # Segurança: Se ainda assim o cálculo de ativos der erro ou negativo
            if ativos < 0: ativos = 0

            labels = ['Ativos/Em Tratamento', 'Óbitos', 'Recuperados']
            values = [ativos, mortes_acumuladas, recuperados_acumulados]
            
            fig_pie = px.pie(
                names=labels, 
                values=values, 
                color_discrete_sequence=['#3b82f6', '#10b981', '#ef4444'],
                hole=0.5
            )
            
            fig_pie.update_layout(
                template="plotly_dark", 
                showlegend=True,
                margin=dict(t=20, b=20, l=0, r=0)
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)

    except Exception as e:
        st.error(f"Erro no pipeline ETL: {e}")

if __name__ == "__main__":
    run_dashboard()