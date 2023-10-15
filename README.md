## Projeto TableauPoor
O projeto TableauPoor é uma iniciativa que utiliza o PyGWalker em conjunto com o Streamlit para criar uma interface semelhante ao software Tableau. Este projeto não tem a intenção de substituir o Tableau, mas sim de oferecer uma interface personalizada, com a capacidade de expandir as opções de conexão com bancos de dados.

### Objetivo
O objetivo principal do TableauPoor é proporcionar uma experiência semelhante ao Tableau, permitindo uma fácil visualização e análise de dados. A integração com o PyGWalker e o Streamlit oferece flexibilidade e personalização.

### Recursos
Conexões com Bancos de Dados
O TableauPoor suporta várias opções de conexão com bancos de dados, incluindo:

**CSV/XLSX:** Importação de arquivos locais.
**Postgres:** Conexão com bancos de dados Postgres usando SQLAlchemy.
**MySQL:** Conexão com bancos de dados MySQL usando mysql-connector-python.
**SQL Server:** Conexão com bancos de dados SQL Server usando SQLAlchemy.

### Tratamento de Dados
O projeto inclui funcionalidades para tratar dados nulos, oferecendo opções como:

**Mostrar Dados Nulos:** Exibe uma visualização dos valores nulos no conjunto de dados.
**Tratar Dados Nulos:** Permite preencher manualmente os valores. 

### Manipulação de Colunas
O **TableauPoor** facilita a manipulação de colunas, oferecendo opções para:

**Mostrar Colunas Duplicadas:** Identifica e exibe colunas duplicadas no conjunto de dados.
**Duplicar Coluna Específica:** Permite duplicar uma coluna selecionada.
**Excluir Coluna Específica:** Permite excluir uma coluna selecionada.

### Contribuições
Contribuições são bem-vindas para melhorar e expandir o projeto TableauPoor. Sinta-se à vontade para participar!