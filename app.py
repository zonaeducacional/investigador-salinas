import streamlit as st
from internetarchive import search_items
import requests
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Investigador Histórico - Salinas", layout="wide", page_icon="🔍")

# Título e Apresentação
st.title("🔍 Investigador Digital: Fontes Históricas")
st.markdown("""
Esta ferramenta cruza dados do **Internet Archive** e **Google Books** para auxiliar na pesquisa histórica.
*Desenvolvido pelo Prof. Sérgio para o projeto História de Salinas da Margarida.*
""")

# --- BARRA LATERAL (Sidebar) ---
st.sidebar.header("Configurações de Busca")
termo = st.sidebar.text_input("Termo de Pesquisa", placeholder="Ex: Salinas da Margarida")
usar_ia = st.sidebar.checkbox("Internet Archive", value=True)
usar_google = st.sidebar.checkbox("Google Books", value=True)
filtrar_mapas = st.sidebar.checkbox("Buscar Mapas/Imagens (IA)", value=False)
botao_buscar = st.sidebar.button("Investigar")

# --- FUNÇÕES DE BUSCA ---

def buscar_ia(termo, buscar_mapas):
    resultados = []
    # Define a query baseada no filtro de mapas
    if buscar_mapas:
        query = f"({termo}) AND (mediatype:image OR subject:maps OR collection:davidrumsey)"
        tipo_padrao = "MAPA/IMG"
    else:
        query = f"({termo}) AND mediatype:texts"
        tipo_padrao = "TEXTO"

    try:
        search = search_items(query)
        # Limitamos a 20 resultados para web (performance)
        for i, item in enumerate(search):
            if i >= 20: break
            
            titulo = item.get('title', 'Sem título')
            ano = item.get('date', '----')[:4]
            autor = item.get('creator', 'Desconhecido')
            if isinstance(autor, list): autor = autor[0]
            identificador = item.get('identifier', '')
            
            # Link direto para o item
            link = f"https://archive.org/details/{identificador}"
            
            # Tenta achar uma imagem de capa (thumbnail)
            thumb = f"https://archive.org/services/img/{identificador}"

            resultados.append({
                'Acervo': 'Internet Archive',
                'Título': titulo,
                'Ano': ano,
                'Autor': autor,
                'Tipo': tipo_padrao,
                'Link': link,
                'Imagem': thumb
            })
    except Exception as e:
        st.error(f"Erro no Archive: {e}")
    
    return resultados

def buscar_google(termo):
    resultados = []
    url = f"https://www.googleapis.com/books/v1/volumes?q={termo}&langRestrict=pt&maxResults=15"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            if 'items' in dados:
                for item in dados['items']:
                    info = item.get('volumeInfo', {})
                    titulo = info.get('title', 'Sem Título')
                    ano = info.get('publishedDate', '----')[:4]
                    autores = info.get('authors', ['Desconhecido'])
                    link = info.get('infoLink', '')
                    
                    # Imagem de capa do Google
                    imgs = info.get('imageLinks', {})
                    thumb = imgs.get('thumbnail', '')

                    resultados.append({
                        'Acervo': 'Google Books',
                        'Título': titulo,
                        'Ano': ano,
                        'Autor': autores[0],
                        'Tipo': 'LIVRO',
                        'Link': link,
                        'Imagem': thumb
                    })
    except:
        pass
    return resultados

# --- EXIBIÇÃO DOS RESULTADOS ---

if botao_buscar and termo:
    with st.spinner('Vasculhando arquivos históricos...'):
        lista_final = []
        
        if usar_ia:
            lista_final.extend(buscar_ia(termo, filtrar_mapas))
        
        if usar_google and not filtrar_mapas: # Google não é bom pra mapas soltos
            lista_final.extend(buscar_google(termo))
        
        # Ordenar por ano
        lista_final.sort(key=lambda x: x['Ano'])

        if not lista_final:
            st.warning("Nenhum documento encontrado com esses termos.")
        else:
            st.success(f"{len(lista_final)} documentos encontrados.")
            
            # Exibir em Cards (Visual mais moderno)
            for item in lista_final:
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    
                    with col1:
                        if item['Imagem']:
                            st.image(item['Imagem'], width=100)
                        else:
                            st.text("Sem imagem")
                    
                    with col2:
                        st.subheader(item['Título'])
                        st.write(f"**Ano:** {item['Ano']} | **Autor:** {item['Autor']} | **Fonte:** {item['Acervo']}")
                        st.markdown(f"[🔗 Acessar Documento Original]({item['Link']})", unsafe_allow_html=True)
                        st.divider()

elif botao_buscar and not termo:
    st.warning("Por favor, digite um termo para pesquisar.")

# Rodapé
st.markdown("---")
st.caption("Ferramenta criada com Python e Streamlit para apoio à pesquisa histórica.")