import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import urllib.parse

# Configuração da Página
st.set_page_config(page_title="Investigador Histórico - Salinas", layout="wide", page_icon="🔍")

# Título
st.title("🔍 Investigador Digital: Fontes Históricas")
st.markdown("""
Esta ferramenta cruza dados do **Internet Archive** e **Google Books**.
*Versão Web Otimizada - Prof. Sérgio Araújo*
""")

# --- BARRA LATERAL ---
st.sidebar.header("Configurações")
termo = st.sidebar.text_input("Termo de Pesquisa", placeholder="Ex: Salinas da Margarida")
usar_ia = st.sidebar.checkbox("Internet Archive", value=True)
usar_google = st.sidebar.checkbox("Google Books", value=True)
filtrar_mapas = st.sidebar.checkbox("Buscar Mapas/Imagens (IA)", value=False)
botao_buscar = st.sidebar.button("Investigar")

# --- FUNÇÕES AUXILIARES ---

def formatar_abnt(autor, titulo, ano, url, tipo):
    if autor and str(autor).lower() not in ['desconhecido', 'none']:
        partes = str(autor).split()
        if len(partes) > 1:
            autor_fmt = f"{partes[-1].upper()}, {' '.join(partes[:-1])}"
        else:
            autor_fmt = str(autor).upper()
    else:
        autor_fmt = "AUTOR DESCONHECIDO"
    
    data_hoje = datetime.now().strftime("%d %b. %Y")
    return f"{autor_fmt}. {titulo}. {ano if ano else '[s.d.]'}. ({tipo}). Disponível em: <{url}>. Acesso em: {data_hoje}."

def buscar_ia_via_api_direta(termo, buscar_mapas):
    """
    Esta função não usa a biblioteca 'internetarchive', mas sim uma requisição direta
    para evitar bloqueios de IP comuns em servidores de nuvem.
    """
    resultados = []
    
    # Montagem da Query Avançada
    if buscar_mapas:
        q_base = f"({termo}) AND (mediatype:image OR subject:maps OR collection:davidrumsey)"
        tipo_padrao = "MAPA/IMG"
    else:
        q_base = f"({termo}) AND mediatype:texts"
        tipo_padrao = "TEXTO"
        
    # Codifica a query para URL (ex: espaço vira %20)
    q_encoded = urllib.parse.quote(q_base)
    
    # URL da API de Busca Avançada (Advanced Search)
    # Pedimos os campos: identifier, title, date, creator
    url = f"https://archive.org/advancedsearch.php?q={q_encoded}&fl[]=identifier&fl[]=title&fl[]=date&fl[]=creator&rows=25&output=json"
    
    try:
        # User-Agent fingindo ser um navegador para evitar bloqueio
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            docs = dados.get('response', {}).get('docs', [])
            
            for item in docs:
                identificador = item.get('identifier')
                titulo = item.get('title', 'Sem Título')
                ano = item.get('date', '----')[:4]
                autor = item.get('creator', 'Desconhecido')
                
                # Tratamento se autor for lista
                if isinstance(autor, list): autor = autor[0]
                
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
        else:
            st.error(f"O Archive retornou erro: {response.status_code}")
            
    except Exception as e:
        st.error(f"Erro de conexão com Archive: {e}")
        
    return resultados

def buscar_google(termo):
    resultados = []
    # Codifica o termo
    termo_enc = urllib.parse.quote(termo)
    url = f"https://www.googleapis.com/books/v1/volumes?q={termo_enc}&langRestrict=pt&maxResults=15"
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
    with st.spinner('Investigando nos arquivos globais...'):
        lista_final = []
        
        if usar_ia:
            # Usa a nova função direta
            lista_final.extend(buscar_ia_via_api_direta(termo, filtrar_mapas))
        
        if usar_google and not filtrar_mapas:
            lista_final.extend(buscar_google(termo))
        
        # Ordenação segura (trata erros se ano não for número)
        lista_final.sort(key=lambda x: str(x['Ano']))

        if not lista_final:
            st.warning("Nenhum resultado encontrado. Tente termos mais abrangentes (ex: 'Bahia', 'Recôncavo').")
        else:
            st.success(f"{len(lista_final)} documentos encontrados.")
            
            # --- DOWNLOAD TXT ---
            texto_referencias = "REFERÊNCIAS BIBLIOGRÁFICAS - PESQUISA HISTÓRICA\n\n"
            for item in lista_final:
                ref = formatar_abnt(item['Autor'], item['Título'], item['Ano'], item['Link'], item['Tipo'])
                texto_referencias += ref + "\n\n"
            
            st.download_button(
                label="📄 Baixar Lista de Referências (TXT)",
                data=texto_referencias,
                file_name=f"referencias_pesquisa_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
            st.divider()

            # --- VISUALIZAÇÃO ---
            for item in lista_final:
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if item['Imagem']: st.image(item['Imagem'], width=80)
                        else: st.text("📄")
                    with col2:
                        st.subheader(item['Título'])
                        st.write(f"**Ano:** {item['Ano']} | **Autor:** {item['Autor']} | **Fonte:** {item['Acervo']}")
                        st.markdown(f"[🔗 Acessar Documento]({item['Link']})", unsafe_allow_html=True)
                        st.divider()

elif botao_buscar and not termo:
    st.warning("Digite um termo para começar.")
