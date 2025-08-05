"""
Utilitário para carregar CSS de arquivos externos.
"""

import os
import streamlit as st


def load_css_file(file_path: str) -> str:
    """
    Carrega o conteúdo CSS de um arquivo.
    
    Args:
        file_path: Caminho para o arquivo CSS relativo à raiz do projeto
        
    Returns:
        Conteúdo CSS como string
    """
    try:
        # Diretório raiz do projeto
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        css_path = os.path.join(project_root, file_path)
        
        with open(css_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        st.warning(f"CSS file not found: {file_path}")
        return ""
    except Exception as e:
        st.error(f"Error loading CSS: {e}")
        return ""


def apply_styles():
    """Carrega e aplica todos os estilos da aplicação."""
    css_content = load_css_file("ui/styles.css")
    
    if css_content:
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        # Fallback: aplicar estilos mínimos
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 2rem;
        }
        </style>
        """, unsafe_allow_html=True) 