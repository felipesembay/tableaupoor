import pygwalker as pyg
import streamlit.components.v1 as components
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import mysql.connector

def load_data(file_picker):
    if file_picker is not None:
        return pd.read_csv(file_picker)

def handle_null_values(df):
    st.subheader("Verificar e Tratar Dados Nulos")

    if df is not None and not df.empty:  # Adicione esta verificação
        show_nulls = st.checkbox("Mostrar Dados Nulos")
        if show_nulls:
            st.dataframe(df.isnull().sum())

        treat_nulls = st.checkbox("Tratar Dados Nulos")
        if treat_nulls:
            null_cols = df.columns[df.isnull().any()]
            for col in null_cols:
                fill_value = st.text_input(f"Valor para preencher nulos em '{col}':", "")
                if fill_value.lower() == 'manual':
                    # Preencher manualmente
                    manual_fill = st.text_input(f"Preencher '{col}' manualmente com:")
                    df[col].fillna(manual_fill, inplace=True)
                elif fill_value.lower() in ['media', 'mean']:
                    df[col].fillna(df[col].mean(), inplace=True)
                elif fill_value.lower() in ['mediana', 'median']:
                    df[col].fillna(df[col].median(), inplace=True)
                elif fill_value.lower() in ['moda', 'mode']:
                    df[col].fillna(df[col].mode()[0], inplace=True)

def delete_duplicate_columns(df):
    st.subheader("Excluir ou Duplicar Colunas")

    if df is not None and not df.empty:
        show_duplicates = st.checkbox("Mostrar Colunas Duplicadas")
        if show_duplicates:
            if not df.columns.empty and df.columns.duplicated().any():  # Verifique se existem colunas e se há duplicatas
                duplicated_cols = df.columns[df.columns.duplicated()]
                st.write(duplicated_cols)
            else:
                st.info("Não há colunas duplicadas no DataFrame.")

        duplicate_col = st.checkbox("Duplicar Coluna Específica")
        if duplicate_col:
            col_to_duplicate = st.multiselect("Selecione a coluna para duplicar:", df.columns)
            for col in col_to_duplicate:
                df[col + "_duplicated"] = df[col]

        delete_col = st.checkbox("Excluir Coluna Específica")
        if delete_col:
            if not df.columns.empty:  # Verifique se existem colunas antes de prosseguir
                col_to_delete = st.multiselect("Selecione a coluna para excluir:", df.columns)
                df.drop(col_to_delete, axis=1, inplace=True)
            else:
                st.warning("O DataFrame não possui colunas para excluir.")

def connect_to_postgres(host, user, password, port, database_name, query):
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database_name}")
    return pd.read_sql_query(query, con=engine)


def connect_to_mysql(host, user, password, port, database_name, query):
    connection = mysql.connector.connect(host=host, user=user, passwd=password, port=port, database=database_name)
    df = pd.read_sql(query, connection)
    connection.close()
    return df

def connect_to_sql_server(host, user, password, port, database_name, query):
    engine = create_engine(f"mssql+pymssql://{user}:{password}@{host}:{port}/{database_name}")
    return pd.read_sql_query(query, con=engine)


def main():
    # Adjust the width of the Streamlit page
    st.set_page_config(
        page_title="Tableau Poor",
        layout="wide"
    )

    # Add Title
    st.title("Tableau Poor - o seu software de Dataviz gratuito")

    # Adicione um selectbox para escolher o banco de dados
    database = st.sidebar.selectbox("Selecione o banco de dados:", ["CSV/XLSX", "Postgres", "MySQL", "SQL Server"])
    
    df = None

    if database != "CSV/XLSX":
        host = st.sidebar.text_input("Host:")
        user = st.sidebar.text_input("Usuário:")
        password = st.sidebar.text_input("Senha:", type="password")
        port = st.sidebar.number_input("Port:", step=1)
        database_name = st.sidebar.text_input("Database:")
        query = st.text_area("Query:")
        
        authenticate_button = st.checkbox("Autenticar e Conectar")
        if authenticate_button:
            try:
                if database == "Postgres":
                    df = connect_to_postgres(host, user, password, port, database_name, query)
                elif database == "MySQL":
                    df = connect_to_mysql(host, user, password, port, database_name, query)
                elif database == "SQL Server":
                    df = connect_to_sql_server(host, user, password, port, database_name, query)

                # Exibir dados
                if 'df' in locals():  # Verifique se df já foi criado
                    df = df  # Substituir df existente
                else:
                    st.dataframe(df)
            except Exception as e:
                st.error(f"Erro ao conectar ao banco de dados: {str(e)}")

            finally:
                if 'engine' in locals():
                    engine.dispose()  # Certifique-se de fechar a conexão

    else:
        file_picker = st.file_uploader("Selecione um arquivo", type=["csv", "xlsx"])
        df = load_data(file_picker)

    # Handle null values
    handle_null_values(df)

    # Delete or duplicate columns
    delete_duplicate_columns(df)

    # Generate the HTML using Pygwalker
    pyg_html = pyg.walk(df, return_html=True, hideDataSourceConfig=False)

    # Embed the HTML into the Streamlit app
    components.html(pyg_html, height=1000, scrolling=True)

if __name__ == "__main__":
    main()