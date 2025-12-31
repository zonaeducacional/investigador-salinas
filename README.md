# 🔍 Investigador Digital: Fontes Históricas

> *"A história é a única ciência que goza do privilégio de ser impenetrável ao futuro, mas de iluminar o presente."*

Uma ferramenta de soberania digital desenvolvida para auxiliar historiadores, pesquisadores e estudantes na busca e organização de fontes primárias e secundárias em grandes acervos digitais.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://investigador-salinas-bk643vlec5ndiyspqetkxt.streamlit.app/)

## 📖 Sobre o Projeto

Este aplicativo foi desenvolvido no contexto da pesquisa para o livro sobre a **História de Salinas da Margarida (BA)**. 

Diante da dispersão de documentos históricos na rede, esta ferramenta centraliza a busca em acervos globais, permitindo ao pesquisador encontrar desde mapas cartográficos do século XVII até documentos administrativos da Ditadura Militar (como os da Comissão Geral de Investigações - CGI) que elucidam conflitos políticos locais.

O objetivo é democratizar o acesso à informação histórica, permitindo que alunos e pesquisadores acessem fontes originais sem a mediação de algoritmos comerciais opacos.

## 🚀 Funcionalidades

* **Busca Unificada:** Pesquisa simultânea no *Internet Archive* (EUA) e *Google Books*.
* **Filtro Cartográfico:** Modo específico para localizar mapas antigos (Coleção David Rumsey e outros).
* **Geração de Referências:** Formatação automática de citações no padrão **ABNT** para facilitar a bibliografia.
* **Download de Dados:** Exportação da lista de fontes encontradas em arquivo de texto (.txt).
* **Visualização Direta:** Links diretos para leitura e thumbnails (capas) dos documentos.

## 🛠️ Tecnologias Utilizadas

O projeto foi construído inteiramente em **Python**, utilizando bibliotecas de código aberto:

* **Streamlit:** Para interface web interativa.
* **InternetArchive:** Para acesso à API do maior arquivo digital do mundo.
* **Pandas & Requests:** Para manipulação de dados e requisições HTTP.

## 💻 Como Rodar Localmente (Linux/Zorin OS)

Se você deseja rodar este projeto no seu próprio computador:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/investigador-salinas.git](https://github.com/SEU-USUARIO/investigador-salinas.git)
    cd investigador-salinas
    ```

2.  **Crie um ambiente virtual (Recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    ```bash
    streamlit run app.py
    ```

## 📜 Licença

Este projeto é de código aberto e destinado fins educacionais e de pesquisa. Sinta-se livre para usar, modificar e distribuir.

---
**Desenvolvido por Prof. Sérgio** *Escola Municipal Januário Eleodoro de Lima - Salinas da Margarida/BA*