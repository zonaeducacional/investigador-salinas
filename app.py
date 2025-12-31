import streamlit as st
from internetarchive import search_items
import requests
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Investigador Histórico - Salinas", layout="wide", page_icon="🔍")

# Título e Apresentação
st.title("🔍 Investigador Digital: Fontes Históricas")
st.markdown("""
Esta ferramenta cruza dados do **Internet Archive** e **Google Books**.
*Desenvolvido pelo Prof. Sérgio para o projeto História de Salinas da Margarida.*
""")

# --- BARRA LATERAL ---
st.sidebar.header("Configurações de Busca")
termo = st.sidebar.text_input("Termo de Pesquisa", placeholder="Ex: Salinas da Margarida")
usar_ia = st.sidebar.checkbox("Internet Archive", value=True)
usar_google = st.sidebar.checkbox("Google Books", value=True)
filtrar_mapas = st.sidebar.checkbox("Buscar Mapas/Imagens (IA)", value=False)
botao_buscar = st.sidebar.button("Investigar")

# --- FUNÇÕES AUXILIARES ---

def formatar_abnt(autor, titulo, ano, url, tipo):
    # Formatação básica de autor para ABNT (Último nome em maiúsculo)
    if autor and autor.lower() != 'desconhecido':
        partes = autor.split()
        if len(partes) > 1:
            autor_fmt = f"{partes[-1].upper()}, {' '.join(partes[:-1])}"
        else:
            autor_fmt = autor.upper()
    else:
        autor_fmt = "AUTOR DESCONHECIDO"
    
    data_hoje = datetime.now().strftime("%d %b. %Y")
    
    # Monta a string
    return f"{autor_fmt}. {titulo}. {ano if ano != '----' else '[s.d.]'}. ({tipo}). Disponível em: <{url}>. Acesso em: {data_hoje}."

def buscar_ia(termo, buscar_mapas):
    resultados = []
    if buscar_mapas:
        query = f"({termo}) AND (mediatype:image OR subject:maps OR collection:davidrumsey)"
        tipo_padrao = "MAPA/IMG"
    else:
        query = f"({termo}) AND mediatype:texts"
        tipo_padrao = "TEXTO"

    try:
        search = search_items(query)
        for i, item in enumerate(search):
            if i >= 20: break
            
            titulo = item.get('title', 'Sem título')
            ano = item.get('date', '----')[:4]
            autor = item.get('creator', 'Desconhecido')
            if isinstance(autor, list): autor = autor[0]
            identificador = item.get('identifier', '')
            link = f"https://archive.org/details/{identificador}"
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
    except: pass
    return resultados

# --- EXIBIÇÃO ---

if botao_buscar and termo:
    with st.spinner('Vasculhando arquivos históricos...'):
        lista_final = []
        
        if usar_ia: lista_final.extend(buscar_ia(termo, filtrar_mapas))
        if usar_google and not filtrar_mapas: lista_final.extend(buscar_google(termo))
        
        lista_final.sort(key=lambda x: x['Ano'])

        if not lista_final:
            st.warning("Nenhum documento encontrado.")
        else:
            # --- ÁREA DE DOWNLOAD DAS REFERÊNCIAS ---
            st.success(f"{len(lista_final)} documentos encontrados.")
            
            # Gera o texto completo das referências
            texto_referencias = "REFERÊNCIAS BIBLIOGRÁFICAS - PESQUISA SALINAS\n\n"
            for item in lista_final:
                ref = formatar_abnt(item['Autor'], item['Título'], item['Ano'], item['Link'], item['Tipo'])
                texto_referencias += ref + "\n\n"
            
            # Botão de Download
            st.download_button(
                label="📄 Baixar Todas as Referências (TXT)",
                data=texto_referencias,
                file_name=f"referencias_salinas_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
            st.divider()

            # --- LISTAGEM VISUAL ---
            for item in lista_final:
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if item['Imagem']: st.image(item['Imagem'], width=80)
                        else: st.text("Sem img")
                    with col2:
                        st.subheader(item['Título'])
                        st.write(f"**Ano:** {item['Ano']} | **Autor:** {item['Autor']} | **Fonte:** {item['Acervo']}")
                        st.markdown(f"[🔗 Acessar Original]({item['Link']})", unsafe_allow_html=True)
                        st.divider()

elif botao_buscar and not termo:
    st.warning("Por favor, digite um termo para pesquisar.")

st.markdown("---")
st.caption("Ferramenta Historiográfica - Prof. Sérgio")
