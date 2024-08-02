import streamlit as st
import app

def dataframeInfo(df):
    st.subheader("Informações do DataFrame")
    st.write("Número de linhas:", df.shape[0])
    st.write("Número de colunas:", df.shape[1])
    st.dataframe(df)
    app.markdown()

def tipoDados(df):
    # Função para exibir o tipo de dados de cada coluna
    st.subheader("Tipos de Dados de cada coluna: ")
    st.write(df.dtypes)
    app.markdown()


def descricao(df):
    # Função para exibir a descrição dos dados
    st.subheader("Descrição Estatística")
    st.write(df.describe())
    app.markdown()

def linechart(df, coluna):
    st.line_chart(df[coluna], height=600)
    app.markdown()

def barchart(df, coluna):
    st.bar_chart(df[coluna], height=600)
    app.markdown()

def areachart(df, coluna):
    st.area_chart(df[coluna], height=600)
    app.markdown()