# flashcards_app.py
import streamlit as st
import sqlite3
import random
from datetime import datetime

# Configuración de la base de datos SQLite
def init_db():
    conn = sqlite3.connect('flashcards.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT NOT NULL,
            respuesta TEXT NOT NULL,
            fecha_creacion TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Funciones CRUD para SQLite
def agregar_tarjeta(pregunta, respuesta):
    conn = sqlite3.connect('flashcards.db')
    c = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO flashcards (pregunta, respuesta, fecha_creacion)
        VALUES (?, ?, ?)
    ''', (pregunta, respuesta, fecha))
    conn.commit()
    conn.close()

def obtener_todas_tarjetas():
    conn = sqlite3.connect('flashcards.db')
    c = conn.cursor()
    c.execute('SELECT * FROM flashcards')
    tarjetas = c.fetchall()
    conn.close()
    return tarjetas

def eliminar_tarjeta(id_tarjeta):
    conn = sqlite3.connect('flashcards.db')
    c = conn.cursor()
    c.execute('DELETE FROM flashcards WHERE id = ?', (id_tarjeta,))
    conn.commit()
    conn.close()

# Inicializar la base de datos
init_db()

# Configuración de la página
st.set_page_config(page_title="Generador de Flashcards", page_icon="🎴", layout="wide")

# Título principal
st.title("🎴 Generador de Flashcards")
st.markdown("---")

# Menú lateral
menu = st.sidebar.selectbox(
    "Menú Principal",
    ["➕ Crear Tarjeta", "📚 Ver Tarjetas", "🎲 Modo Estudio", "🗑️ Gestionar Tarjetas"]
)

# ========== CREAR TARJETA ==========
if menu == "➕ Crear Tarjeta":
    st.header("Crear Nueva Tarjeta")
    
    col1, col2 = st.columns(2)
    
    with col1:
        pregunta = st.text_area("Pregunta / Concepto", height=150, 
                                placeholder="Ejemplo: ¿Qué es la fotosíntesis?")
    
    with col2:
        respuesta = st.text_area("Respuesta / Definición", height=150,
                                 placeholder="Proceso por el cual las plantas convierten luz solar en energía...")
    
    if st.button("💾 Guardar Tarjeta", type="primary"):
        if pregunta and respuesta:
            agregar_tarjeta(pregunta, respuesta)
            st.success("✅ Tarjeta guardada exitosamente!")
            st.balloons()
        else:
            st.error("⚠️ Por favor completa la pregunta y la respuesta")

# ========== VER TARJETAS ==========
elif menu == "📚 Ver Tarjetas":
    st.header("Todas las Tarjetas")
    
    tarjetas = obtener_todas_tarjetas()
    
    if tarjetas:
        st.info(f"📊 Total de tarjetas: {len(tarjetas)}")
        
        for tarjeta in tarjetas:
            id_tarjeta, pregunta, respuesta, fecha = tarjeta
            
            with st.expander(f"🎴 {pregunta[:50]}..." if len(pregunta) > 50 else f"🎴 {pregunta}"):
                st.markdown(f"**Pregunta:** {pregunta}")
                st.markdown(f"**Respuesta:** {respuesta}")
                st.caption(f"Creada: {fecha}")
    else:
        st.warning("No hay tarjetas disponibles. ¡Crea tu primera tarjeta!")

# ========== MODO ESTUDIO ==========
elif menu == "🎲 Modo Estudio":
    st.header("Modo Estudio")
    
    tarjetas = obtener_todas_tarjetas()
    
    if tarjetas:
        if st.button("🔀 Obtener Tarjeta Aleatoria"):
            tarjeta_random = random.choice(tarjetas)
            st.session_state['tarjeta_actual'] = tarjeta_random
            st.session_state['mostrar_respuesta'] = False
        
        if 'tarjeta_actual' in st.session_state:
            tarjeta = st.session_state['tarjeta_actual']
            id_tarjeta, pregunta, respuesta, fecha = tarjeta
            
            st.markdown(f"## {pregunta}")
            
            if st.button("👁️ Mostrar Respuesta"):
                st.session_state['mostrar_respuesta'] = True
            
            if st.session_state.get('mostrar_respuesta', False):
                st.success(f"**Respuesta:** {respuesta}")
    else:
        st.warning("No hay tarjetas para estudiar. ¡Crea algunas primero!")

# ========== GESTIONAR TARJETAS ==========
elif menu == "🗑️ Gestionar Tarjetas":
    st.header("Gestionar Tarjetas")
    
    tarjetas = obtener_todas_tarjetas()
    
    if tarjetas:
        for tarjeta in tarjetas:
            id_tarjeta, pregunta, respuesta, fecha = tarjeta
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"**{pregunta[:80]}...**" if len(pregunta) > 80 else f"**{pregunta}**")
            
            with col2:
                if st.button("🗑️ Eliminar", key=f"delete_{id_tarjeta}"):
                    eliminar_tarjeta(id_tarjeta)
                    st.success("Tarjeta eliminada")
                    st.rerun()
    else:
        st.info("No hay tarjetas para gestionar")

# Footer
st.markdown("---")
st.caption("🎴 Generador de Flashcards con SQLite | Desarrollado con Streamlit")