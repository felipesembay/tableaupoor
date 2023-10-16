import pygwalker as pyg
import streamlit.components.v1 as components
import pandas as pd
import streamlit as st
import psycopg2
import mysql.connector
import pymssql

google_analytics_code = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-20S9K4G7X6"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-20S9K4G7X6');
</script>
"""

# Use components.html para incorporar o código no seu aplicativo
components.html(google_analytics_code)


def load_data(file_picker):
    if file_picker is not None:
        try:
            # Especifique a codificação (por exemplo, 'ISO-8859-1') ao carregar o arquivo CSV
            df = pd.read_csv(file_picker, encoding='ISO-8859-1')
            return df
        except UnicodeDecodeError:
            st.error("Erro ao abrir o arquivo. Verifique a codificação correta.")
            return None


def handle_null_values(df):
    st.subheader("Verificar e Tratar Dados Nulos")

    if df is not None and not df.empty:
        show_nulls = st.checkbox("Mostrar Dados Nulos")
        if show_nulls:
            st.dataframe(df.isnull().sum())

        treat_nulls = st.checkbox("Tratar Dados Nulos")
        if treat_nulls:
            null_cols = df.columns[df.isnull().any()]
            for col in null_cols:
                fill_value = st.text_input(f"Valor para preencher nulos em '{col}':", "")
                if fill_value.lower() == 'manual':
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
            if not df.columns.empty and df.columns.duplicated().any():
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
            if not df.columns.empty:
                col_to_delete = st.multiselect("Selecione a coluna para excluir:", df.columns)
                df.drop(col_to_delete, axis=1, inplace=True)
            else:
                st.warning("O DataFrame não possui colunas para excluir.")


def connect_to_postgres(host, user, password, port, database_name, query):
    try:
        connection = psycopg2.connect(host=host, user=user, password=password, port=port, database=database_name)
        df = pd.read_sql(query, connection)
        return df
    except psycopg2.Error as e:
        st.error(f"Erro ao conectar ao banco de dados PostgreSQL: {str(e)}")
        return None
    finally:
        if 'connection' in locals() and connection is not None:
            connection.close()


def connect_to_mysql(host, user, password, port, database_name, query):
    try:
        connection = mysql.connector.connect(host=host, user=user, password=password, port=port, database=database_name)
        df = pd.read_sql(query, connection)
        return df
    except mysql.connector.Error as e:
        st.error(f"Erro ao conectar ao banco de dados MySQL: {str(e)}")
        return None
    finally:
        if 'connection' in locals() and connection is not None:
            connection.close()


def connect_to_sql_server(host, user, password, port, database_name, query):
    try:
        connection = pymssql.connect(host=host, user=user, password=password, port=port, database=database_name)
        df = pd.read_sql(query, connection)
        return df
    except pymssql.Error as e:
        st.error(f"Erro ao conectar ao banco de dados SQL Server: {str(e)}")
        return None
    finally:
        if 'connection' in locals() and connection is not None:
            connection.close()


def main():
    st.set_page_config(
        page_title="Tableau Poor",
        layout="wide"
    )

    st.title("Tableau Poor - o seu software de Dataviz gratuito")

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
            if host and user and password and port and database_name and query:
                if database == "Postgres":
                    df = connect_to_postgres(host, user, password, port, database_name, query)
                elif database == "MySQL":
                    df = connect_to_mysql(host, user, password, port, database_name, query)
                elif database == "SQL Server":
                    df = connect_to_sql_server(host, user, password, port, database_name, query)

                if df is not None:
                    st.dataframe(df)
            else:
                st.warning("Preencha todos os campos obrigatórios.")

    else:
        file_picker = st.file_uploader("Selecione um arquivo", type=["csv", "xlsx"])
        df = load_data(file_picker)

    handle_null_values(df)
    delete_duplicate_columns(df)

    pyg_html = pyg.walk(df, return_html=True, hideDataSourceConfig=False)
    components.html(pyg_html, height=1000, scrolling=True)


if __name__ == "__main__":
    main()
