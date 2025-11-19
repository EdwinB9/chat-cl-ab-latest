"""
Componente de estilos CSS para mejorar la UI/UX de la aplicación.
Estilos simplificados y optimizados para Casa Limpia.
"""

import streamlit as st


def obtener_tema():
    """Retorna siempre 'light' ya que solo usamos modo claro."""
    return "light"


def aplicar_estilos_globales():
    """
    Aplica estilos CSS globales simplificados para Casa Limpia.
    Incluye animaciones optimizadas para performance.
    """
    # Paleta de colores institucionales de Casa Limpia
    primary_color = "#00acc1"
    primary_dark = "#00838f"
    primary_light = "#26c6da"
    success_color = "#43a047"
    error_color = "#e53935"
    warning_color = "#fb8c00"
    info_color = "#1e88e5"
    text_primary = "#1a237e"
    text_secondary = "#546e7a"
    text_tertiary = "#78909c"
    bg_primary = "#ffffff"
    bg_secondary = "#f5f9fa"
    bg_tertiary = "#e8f4f8"
    border_color = "#b0bec5"
    border_hover = "#90a4ae"
    shadow_sm = "0 1px 2px 0 rgba(0, 172, 193, 0.1)"
    shadow_md = "0 4px 6px -1px rgba(0, 172, 193, 0.15)"
    shadow_lg = "0 10px 15px -3px rgba(0, 172, 193, 0.2)"
    shadow_xl = "0 20px 25px -5px rgba(0, 172, 193, 0.25)"
    alert_info_bg = "rgba(30, 136, 229, 0.1)"
    alert_success_bg = "rgba(67, 160, 71, 0.1)"
    alert_error_bg = "rgba(229, 57, 53, 0.1)"
    alert_warning_bg = "rgba(251, 140, 0, 0.1)"
    badge_success_bg = "rgba(67, 160, 71, 0.15)"
    badge_error_bg = "rgba(229, 57, 53, 0.15)"
    badge_warning_bg = "rgba(251, 140, 0, 0.15)"
    download_hover = "#388e3c"
    
    # Cargar fuente Montserrat desde Google Fonts con preload para mejor rendimiento
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap&subset=latin,latin-ext" rel="stylesheet">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        """,
        unsafe_allow_html=True
    )
    
    # Aplicar estilos CSS
    css_content = f"""
        <style>
        /* ============================================
           VARIABLES CSS - Casa Limpia
           ============================================ */
        :root {{
            --primary-color: {primary_color};
            --primary-dark: {primary_dark};
            --primary-light: {primary_light};
            --success-color: {success_color};
            --error-color: {error_color};
            --warning-color: {warning_color};
            --info-color: {info_color};
            --text-primary: {text_primary};
            --text-secondary: {text_secondary};
            --text-tertiary: {text_tertiary};
            --bg-primary: {bg_primary};
            --bg-secondary: {bg_secondary};
            --bg-tertiary: {bg_tertiary};
            --border-color: {border_color};
            --border-hover: {border_hover};
            --shadow-sm: {shadow_sm};
            --shadow-md: {shadow_md};
            --shadow-lg: {shadow_lg};
            --shadow-xl: {shadow_xl};
            --radius-sm: 0.375rem;
            --radius-md: 0.5rem;
            --radius-lg: 0.75rem;
            --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* ============================================
           FUENTE - Montserrat con fallback mejorado
           ============================================ */
        * {{
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            font-size: 0.925rem !important;
            line-height: 1.6 !important;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-rendering: optimizeLegibility;
        }}
        
        /* ============================================
           ESTILOS BASE - Fondo y estructura
           ============================================ */
        html, body, .stApp {{
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            font-size: 0.925rem !important;
            line-height: 1.6 !important;
        }}
        
        .main .block-container {{
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
            animation: fadeIn var(--transition-base) ease-out;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: var(--bg-secondary) !important;
        }}
        
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > div {{
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
        }}
        
        /* ============================================
           ANIMACIONES - Casa Limpia (Sutiles y profesionales)
           ============================================ */
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(5px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateX(-5px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        @keyframes slideDown {{
            from {{ opacity: 0; max-height: 0; }}
            to {{ opacity: 1; max-height: 1000px; }}
        }}
        
        /* ============================================
           CLASES DE CONTENEDORES
           ============================================ */
        .input-container {{
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            margin: 1rem 0;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow-sm);
            animation: fadeInUp 0.2s ease-out;
            transition: box-shadow var(--transition-base), transform var(--transition-base) !important;
        }}
        
        .input-container:hover {{
            box-shadow: var(--shadow-md);
        }}
        
        .historial-container {{
            border-radius: var(--radius-lg);
            padding: 1rem;
            margin: 0.5rem 0;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            animation: fadeIn 0.2s ease-out;
            transition: box-shadow var(--transition-base), transform var(--transition-base) !important;
        }}
        
        .historial-container:hover {{
            box-shadow: var(--shadow-sm);
        }}
        
        .info-container {{
            border-radius: var(--radius-md);
            padding: 0.75rem;
            background: var(--bg-secondary);
            color: var(--text-primary);
            animation: scaleIn 0.3s ease-out;
            transition: background-color var(--transition-base) !important;
        }}
        
        .info-container:hover {{
            background-color: var(--bg-tertiary);
        }}
        
        .footer-text {{
            text-align: center;
            padding: 1rem 0;
            color: var(--text-secondary);
            animation: fadeIn 0.5s ease-out 0.2s both;
        }}
        
        /* Contenedores de ayuda */
        .help-container {{
            box-sizing: border-box !important;
            animation: slideDown 0.2s ease-out;
        }}
        
        .help-content-wrapper {{
            color: var(--text-primary) !important;
            line-height: 1.6;
            animation: fadeIn 0.3s ease-out 0.1s both;
        }}
        
        .help-content-wrapper * {{
            color: inherit !important;
            max-width: 100%;
            overflow-wrap: break-word;
            word-wrap: break-word;
        }}
        
        /* ============================================
           TIPOGRAFÍA - Montserrat
           ============================================ */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--text-primary) !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
        }}
        
        h1 {{
            font-weight: 700 !important;
            font-size: 2.25rem !important;
            margin-bottom: 1rem !important;
            animation: fadeInUp 0.5s ease-out;
        }}
        
        h2, h3 {{
            font-weight: 600 !important;
            animation: fadeIn 0.2s ease-out;
        }}
        
        h2 {{
            font-size: 1.65rem !important;
        }}
        
        h3 {{
            font-size: 1.35rem !important;
        }}
        
        h2 {{
            animation-delay: 0.1s;
            animation-fill-mode: both;
        }}
        
        h3 {{
            animation-delay: 0.15s;
            animation-fill-mode: both;
        }}
        
        .stMarkdown {{
            line-height: 1.6 !important;
            color: var(--text-primary) !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            font-size: 0.925rem !important;
        }}
        
        .stMarkdown p {{
            margin-bottom: 1rem !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            font-size: 0.925rem !important;
        }}
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            margin-top: 1.5rem !important;
            margin-bottom: 1rem !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
        }}
        
        /* Textos generales */
        p, span, div, label, li, ul, ol {{
            color: var(--text-primary) !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            font-size: 0.925rem !important;
        }}
        
        [data-testid="stText"],
        [data-testid="stMarkdownContainer"],
        [data-testid="stCaption"],
        [data-testid="stWidgetLabel"],
        .stText,
        .stWidgetLabel {{
            color: var(--text-primary) !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            font-size: 0.925rem !important;
        }}
        
        [data-testid="stCaption"] {{
            color: var(--text-secondary) !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            font-size: 0.9rem !important;
        }}
        
        /* Elementos específicos de Streamlit */
        [data-testid="stHeader"],
        [data-testid="stHeader"] * {{
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            font-size: 1.2rem !important;
        }}
        
        [data-testid="stSubheader"],
        [data-testid="stSubheader"] * {{
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            font-size: 1.1rem !important;
        }}
        
        /* Asegurar que todos los inputs y selects tengan el tamaño correcto */
        input, textarea, select, button {{
            font-size: 0.925rem !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
        }}
        
        /* Corregir problemas de renderizado de caracteres */
        body {{
            font-feature-settings: "kern" 1, "liga" 1;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        /* Ocultar nombres de iconos de Material Icons que aparecen como texto */
        [class*="material-icons"],
        [class*="MaterialIcons"],
        .material-icons,
        .MaterialIcons {{
            font-family: 'Material Icons' !important;
            font-weight: normal;
            font-style: normal;
            font-size: 24px;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
            -webkit-font-feature-settings: 'liga';
            -webkit-font-smoothing: antialiased;
        }}
        
        /* ============================================
           SOLUCIÓN GLOBAL PARA OCULTAR NOMBRES DE ICONOS
           ============================================ */
        
        /* Ocultar texto de iconos Material Icons que aparece como texto plano */
        [data-testid*="keyboard"],
        [data-testid="stIconMaterial"],
        [aria-label*="keyboard"],
        [class*="keyboard"],
        [class*="material-icons"],
        span[class*="material-icons"],
        i[class*="material-icons"],
        .material-icons,
        [data-baseweb*="icon"] span,
        [data-baseweb*="icon"] i,
        span[data-testid="stIconMaterial"] {{
            font-family: 'Material Icons' !important;
            font-size: 0 !important;
            width: 0 !important;
            height: 0 !important;
            overflow: hidden !important;
            visibility: hidden !important;
            display: none !important;
            line-height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            opacity: 0 !important;
        }}
        
        /* Ocultar específicamente el stIconMaterial que contiene nombres de iconos */
        [data-testid="stIconMaterial"]:not(svg),
        [data-testid="stIconMaterial"]:not([class*="svg"]) {{
            display: none !important;
            visibility: hidden !important;
            font-size: 0 !important;
            width: 0 !important;
            height: 0 !important;
            overflow: hidden !important;
            opacity: 0 !important;
        }}
        
        /* Ocultar específicamente en expanders de Streamlit */
        .streamlit-expanderHeader [class*="keyboard"],
        .streamlit-expanderHeader [class*="arrow"],
        .streamlit-expanderHeader [data-testid="stIconMaterial"],
        .streamlit-expanderHeader span:not([class]):not([id]):not([data-testid]),
        [data-testid="stExpander"] [class*="keyboard"],
        [data-testid="stExpander"] [class*="arrow"],
        [data-testid="stExpander"] [data-testid="stIconMaterial"],
        [data-testid="stExpander"] span:not([class]):not([id]):not([data-testid]),
        [data-baseweb="accordion"] [class*="keyboard"],
        [data-baseweb="accordion"] [class*="arrow"],
        summary [data-testid="stIconMaterial"],
        .st-emotion-cache-pxambx [data-testid="stIconMaterial"] {{
            font-size: 0 !important;
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            width: 0 !important;
            overflow: hidden !important;
            opacity: 0 !important;
        }}
        
        /* Ocultar en botones */
        button [class*="keyboard"],
        button [class*="arrow"],
        button span:not([class]):not([id]),
        .stButton [class*="keyboard"],
        .stButton [class*="arrow"],
        .stButton span:not([class]):not([id]),
        [data-baseweb="button"] [class*="keyboard"],
        [data-baseweb="button"] [class*="arrow"] {{
            font-size: 0 !important;
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            width: 0 !important;
        }}
        
        /* Ocultar en dropdowns y selects */
        [data-baseweb="select"] [class*="keyboard"],
        [data-baseweb="select"] [class*="arrow"],
        [data-baseweb="popover"] [class*="keyboard"],
        [data-baseweb="popover"] [class*="arrow"],
        .stSelectbox [class*="keyboard"],
        .stSelectbox [class*="arrow"] {{
            font-size: 0 !important;
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            width: 0 !important;
        }}
        
        /* Estilos para iconos SVG válidos de Streamlit */
        [data-baseweb*="icon"] svg,
        svg[data-testid*="icon"],
        .stIcon svg {{
            display: inline-block !important;
        }}
        
        /* Ocultar spans vacíos o con solo nombres de iconos */
        span:empty {{
            display: none !important;
        }}
        
        /* Asegurar que todos los elementos usen Montserrat, no Material Icons para texto */
        button, 
        .streamlit-expanderHeader,
        [data-testid="stExpander"],
        [data-baseweb="select"],
        [data-baseweb="popover"],
        [data-baseweb="button"] {{
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
        }}
        
        /* Ocultar elementos específicos que contienen nombres de iconos */
        button[aria-label*="keyboard"],
        button[title*="keyboard"],
        div[aria-label*="keyboard"],
        span[aria-label*="keyboard"],
        [aria-label*="keyboard"],
        [title*="keyboard"] {{
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            width: 0 !important;
            overflow: hidden !important;
        }}
        
        /* ============================================
           BOTONES
           ============================================ */
        .stButton > button {{
            border-radius: var(--radius-md) !important;
            font-weight: 500 !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            font-size: 0.925rem !important;
            transition: transform var(--transition-fast), box-shadow var(--transition-fast),
                        background-color var(--transition-base), border-color var(--transition-base) !important;
            box-shadow: var(--shadow-sm) !important;
            will-change: transform, box-shadow;
            backface-visibility: hidden;
            transform: translateZ(0);
            animation: fadeIn 0.15s ease-out;
        }}
        
        .stButton > button:hover {{
            box-shadow: var(--shadow-md) !important;
        }}
        
        .stButton > button:active {{
            transition: transform 0.1s !important;
        }}
        
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%) !important;
            border: none !important;
            color: white !important;
        }}
        
        .stButton > button[kind="secondary"] {{
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
        }}
        
        .stButton > button[kind="secondary"]:hover {{
            background-color: var(--bg-tertiary) !important;
            border-color: var(--border-hover) !important;
        }}
        
        [data-testid="stSidebar"] .stButton > button {{
            width: 100% !important;
        }}
        
        /* ============================================
           INPUTS Y FORMULARIOS
           ============================================ */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {{
            border-radius: var(--radius-md) !important;
            border: 1px solid var(--border-color) !important;
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            font-size: 0.925rem !important;
            transition: border-color var(--transition-fast), box-shadow var(--transition-fast),
                        transform var(--transition-fast) !important;
            animation: fadeIn 0.2s ease-out;
        }}
        
        .stTextInput > div > div > input:hover,
        .stTextArea > div > div > textarea:hover {{
            box-shadow: var(--shadow-sm);
        }}
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 3px rgba(0, 172, 193, 0.15) !important;
            outline: none !important;
        }}
        
        /* ============================================
           SELECTBOX / DROPDOWN
           ============================================ */
        .stSelectbox > div > div {{
            border-radius: var(--radius-md) !important;
            background-color: var(--bg-primary) !important;
            border: 1px solid var(--border-color) !important;
            transition: border-color var(--transition-base), transform var(--transition-fast) !important;
            animation: fadeIn 0.2s ease-out;
        }}
        
        .stSelectbox > div > div:hover {{
            border-color: var(--border-hover) !important;
        }}
        
        .stSelectbox > div > div:focus-within {{
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 3px rgba(0, 172, 193, 0.15) !important;
        }}
        
        .stSelectbox select,
        [data-baseweb="select"] > div {{
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
        }}
        
        [data-baseweb="popover"] {{
            background-color: var(--bg-primary) !important;
            border: 1px solid var(--border-color) !important;
            box-shadow: var(--shadow-lg) !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
        }}
        
        [data-baseweb="popover"] li,
        [data-baseweb="popover"] [role="option"] {{
            transition: background-color var(--transition-fast), transform var(--transition-fast) !important;
            animation: slideIn 0.15s ease-out;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
        }}
        
        [data-baseweb="popover"] li:hover,
        [data-baseweb="popover"] [role="option"]:hover {{
            background-color: var(--bg-secondary) !important;
        }}
        
        [data-baseweb="popover"] li[aria-selected="true"] {{
            background-color: rgba(0, 172, 193, 0.1) !important;
            color: var(--primary-color) !important;
        }}
        
        /* ============================================
           SLIDER
           ============================================ */
        .stSlider {{
            margin: 1rem 0 !important;
        }}
        
        .stSlider > div > div {{
            background-color: var(--bg-secondary) !important;
            border-radius: var(--radius-md) !important;
        }}
        
        .stSlider > div > div > div {{
            background-color: var(--primary-color) !important;
        }}
        
        .stSlider > div > div > div > div {{
            background-color: var(--primary-color) !important;
            border: 2px solid var(--bg-primary) !important;
            box-shadow: 0 2px 4px rgba(0, 172, 193, 0.3) !important;
            transition: transform var(--transition-fast), background-color var(--transition-fast),
                        box-shadow var(--transition-fast) !important;
        }}
        
        .stSlider > div > div > div > div:hover {{
            background-color: var(--primary-dark) !important;
            box-shadow: 0 4px 8px rgba(0, 172, 193, 0.4) !important;
        }}
        
        .stSlider label,
        .stSlider [data-testid="stWidgetLabel"] {{
            color: var(--text-primary) !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
        }}
        
        /* ============================================
           NUMBER INPUT
           ============================================ */
        .stNumberInput > div > div > div {{
            background-color: var(--bg-primary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            transition: border-color var(--transition-fast) !important;
        }}
        
        .stNumberInput > div > div > div:hover {{
            border-color: var(--border-hover) !important;
        }}
        
        .stNumberInput > div > div > div:focus-within {{
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 3px rgba(0, 172, 193, 0.15) !important;
        }}
        
        .stNumberInput input {{
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
            border: none !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
        }}
        
        .stNumberInput button {{
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
            transition: all var(--transition-fast) !important;
        }}
        
        .stNumberInput button:hover {{
            background-color: var(--bg-tertiary) !important;
            border-color: var(--primary-color) !important;
            color: var(--primary-color) !important;
        }}
        
        .stNumberInput button:active {{
        }}
        
        /* ============================================
           FILE UPLOADER
           ============================================ */
        [data-testid="stFileUploader"] {{
            border: 2px dashed var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            padding: 2rem !important;
            background-color: var(--bg-secondary) !important;
            transition: border-color var(--transition-base), background-color var(--transition-base),
                        transform var(--transition-base) !important;
            animation: fadeIn 0.2s ease-out;
        }}
        
        [data-testid="stFileUploader"]:hover {{
            border-color: var(--primary-color) !important;
            background-color: rgba(0, 172, 193, 0.03) !important;
        }}
        
        [data-testid="stFileUploader"] button {{
            background-color: var(--primary-color) !important;
            color: var(--bg-primary) !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            transition: all var(--transition-fast) !important;
        }}
        
        [data-testid="stFileUploader"] button:hover {{
            background-color: var(--primary-dark) !important;
            box-shadow: var(--shadow-md) !important;
        }}
        
        [data-testid="stFileUploader"] button:active {{
        }}
        
        /* ============================================
           ALERTAS Y NOTIFICACIONES
           ============================================ */
        .stAlert {{
            border-radius: var(--radius-md) !important;
            border-left: 4px solid !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            animation: slideIn var(--transition-base) ease-out;
        }}
        
        .stAlert[data-base="info"] {{
            border-left-color: var(--info-color) !important;
            background-color: {alert_info_bg} !important;
        }}
        
        .stAlert[data-base="success"] {{
            border-left-color: var(--success-color) !important;
            background-color: {alert_success_bg} !important;
        }}
        
        .stAlert[data-base="error"] {{
            border-left-color: var(--error-color) !important;
            background-color: {alert_error_bg} !important;
        }}
        
        .stAlert[data-base="warning"] {{
            border-left-color: var(--warning-color) !important;
            background-color: {alert_warning_bg} !important;
        }}
        
        /* ============================================
           EXPANDERS
           ============================================ */
        .streamlit-expanderHeader {{
            background-color: var(--bg-secondary) !important;
            border-radius: var(--radius-md) !important;
            padding: 0.75rem 1rem !important;
            font-weight: 500 !important;
            color: var(--text-primary) !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            transition: background-color var(--transition-base), transform var(--transition-fast) !important;
            animation: fadeIn 0.2s ease-out;
        }}
        
        .streamlit-expanderHeader:hover {{
            background-color: var(--bg-tertiary) !important;
        }}
        
        .streamlit-expanderContent {{
            padding: 1rem !important;
            background-color: var(--bg-primary) !important;
            animation: slideDown 0.3s ease-out;
        }}
        
        /* ============================================
           TABS
           ============================================ */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.5rem !important;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: var(--radius-md) var(--radius-md) 0 0 !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            transition: background-color var(--transition-base), transform var(--transition-fast) !important;
            animation: fadeIn 0.2s ease-out;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
        }}
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            animation: fadeIn 0.2s ease-out;
        }}
        
        /* ============================================
           DOWNLOAD BUTTONS
           ============================================ */
        .stDownloadButton > button {{
            background-color: var(--success-color) !important;
            color: white !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            transition: background-color var(--transition-base), transform var(--transition-fast),
                        box-shadow var(--transition-fast) !important;
            animation: fadeIn 0.15s ease-out;
        }}
        
        .stDownloadButton > button:hover {{
            background-color: {download_hover} !important;
            box-shadow: var(--shadow-md) !important;
        }}
        
        .stDownloadButton > button:active {{
        }}
        
        /* ============================================
           MÉTRICAS
           ============================================ */
        [data-testid="stMetricValue"] {{
            color: var(--primary-color) !important;
            font-weight: 600 !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            animation: fadeIn 0.2s ease-out;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            animation: fadeIn 0.4s ease-out 0.1s both;
        }}
        
        /* ============================================
           SCROLLBAR
           ============================================ */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--bg-secondary);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--border-color);
            border-radius: 4px;
            transition: background-color var(--transition-base) !important;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--text-secondary);
            box-shadow: 0 0 5px rgba(0, 172, 193, 0.3);
        }}
        
        /* ============================================
           DIVIDERS
           ============================================ */
        hr {{
            margin: 2rem 0 !important;
            border: none !important;
            border-top: 1px solid var(--border-color) !important;
            animation: fadeIn 0.2s ease-out;
            transition: border-color var(--transition-base) !important;
        }}
        
        hr:hover {{
            border-top-color: var(--primary-color) !important;
        }}
        
        /* ============================================
           FOOTER Y MENÚ
           ============================================ */
        footer, #MainMenu {{
            visibility: hidden;
        }}
        
        /* ============================================
           TRANSICIONES GLOBALES
           ============================================ */
        * {{
            transition: background-color var(--transition-base),
                        border-color var(--transition-base),
                        color var(--transition-base) !important;
        }}
        
        /* Animaciones escalonadas para elementos que aparecen */
        [data-testid="stElementContainer"]:nth-child(1) {{
            animation: fadeInUp 0.2s ease-out;
        }}
        
        [data-testid="stElementContainer"]:nth-child(2) {{
            animation: fadeInUp 0.5s ease-out;
            animation-fill-mode: both;
        }}
        
        [data-testid="stElementContainer"]:nth-child(3) {{
            animation: fadeInUp 0.6s ease-out;
            animation-fill-mode: both;
        }}
        
        /* Animación para elementos de lista */
        ul li, ol li {{
            animation: slideIn 0.2s ease-out;
            animation-fill-mode: both;
        }}
        
        ul li:nth-child(1), ol li:nth-child(1) {{
            animation-delay: 0.1s;
        }}
        
        ul li:nth-child(2), ol li:nth-child(2) {{
            animation-delay: 0.2s;
        }}
        
        ul li:nth-child(3), ol li:nth-child(3) {{
            animation-delay: 0.3s;
        }}
        
        ul li:nth-child(4), ol li:nth-child(4) {{
            animation-delay: 0.4s;
        }}
        
        ul li:nth-child(5), ol li:nth-child(5) {{
            animation-delay: 0.5s;
        }}
        
        /* Animación para cards y contenedores */
        .result-card {{
            animation: fadeInUp 0.2s ease-out;
            transition: transform var(--transition-base), box-shadow var(--transition-base) !important;
        }}
        
        .result-card:hover {{
            box-shadow: var(--shadow-md);
        }}
        
        /* Animación para sidebar */
        [data-testid="stSidebar"] {{
            animation: slideIn 0.4s ease-out;
        }}
        
        /* Animación para elementos de columna */
        [data-testid="column"] {{
            animation: fadeIn 0.2s ease-out;
        }}
        
        [data-testid="column"]:nth-child(1) {{
            animation-delay: 0.1s;
            animation-fill-mode: both;
        }}
        
        [data-testid="column"]:nth-child(2) {{
            animation-delay: 0.2s;
            animation-fill-mode: both;
        }}
        
        [data-testid="column"]:nth-child(3) {{
            animation-delay: 0.3s;
            animation-fill-mode: both;
        }}
        
        [data-testid="column"]:nth-child(4) {{
            animation-delay: 0.4s;
            animation-fill-mode: both;
        }}
        
        /* Efecto de carga para spinners */
        [data-testid="stSpinner"] {{
            animation: rotate 1s linear infinite;
        }}
        
        /* Animación suave para cambios de estado */
        .stAlert {{
            animation: fadeIn 0.2s ease-out;
        }}
        
        /* Animación para tooltips */
        [data-testid="stTooltip"] {{
            animation: fadeInUp 0.2s ease-out;
        }}
        
        /* Efecto de shimmer para elementos de carga */
        .loading-shimmer {{
            background: linear-gradient(90deg, 
                var(--bg-secondary) 0%, 
                var(--bg-tertiary) 50%, 
                var(--bg-secondary) 100%);
            background-size: 200% 100%;
            animation: fadeIn 0.2s ease-out;
        }}
        
        /* ============================================
           OPTIMIZACIÓN DE RENDIMIENTO
           ============================================ */
        .main .block-container,
        .stButton > button,
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {{
            will-change: transform, opacity;
            backface-visibility: hidden;
        }}
        </style>
        """
    
    st.markdown(css_content, unsafe_allow_html=True)
    
    # Script mejorado y más agresivo para ocultar nombres de iconos en TODOS los lugares
    st.markdown(
        """
        <script>
        (function() {
            const iconNames = [
                'keyboard_double_arrow_right',
                'keyboard_double_arrow_left',
                'keyboard_arrow_right',
                'keyboard_arrow_left',
                'keyboard_double_arrow_up',
                'keyboard_double_arrow_down',
                'keyboard_arrow_up',
                'keyboard_arrow_down',
                'chevron_right',
                'chevron_left',
                'expand_more',
                'expand_less',
                'arrow_forward',
                'arrow_back',
                'arrow_drop_down',
                'arrow_drop_up'
            ];
            
            function hideIconText() {
                // 1. Buscar todos los elementos de texto que contengan nombres de iconos
                const walker = document.createTreeWalker(
                    document.body,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );
                
                let node;
                const nodesToHide = [];
                
                while (node = walker.nextNode()) {
                    const text = node.textContent.trim();
                    if (iconNames.some(name => text === name || text.includes(name))) {
                        nodesToHide.push(node);
                    }
                }
                
                // Ocultar los nodos encontrados
                nodesToHide.forEach(node => {
                    if (node.parentElement) {
                        const parent = node.parentElement;
                        parent.style.display = 'none';
                        parent.style.visibility = 'hidden';
                        parent.style.height = '0';
                        parent.style.width = '0';
                        parent.style.overflow = 'hidden';
                        parent.style.fontSize = '0';
                        parent.style.lineHeight = '0';
                        parent.style.padding = '0';
                        parent.style.margin = '0';
                    }
                });
                
                // 2. Buscar por atributos de clase y data en TODOS los elementos
                const selectors = [
                    '[class*="keyboard"]',
                    '[class*="arrow"]',
                    '[class*="material-icons"]',
                    '[data-testid*="keyboard"]',
                    '[data-testid="stIconMaterial"]',
                    '[aria-label*="keyboard"]',
                    '[title*="keyboard"]',
                    'span:not([class]):not([id]):not([data-testid])',
                    'i:not([class]):not([id]):not([data-testid])'
                ];
                
                selectors.forEach(selector => {
                    try {
                        document.querySelectorAll(selector).forEach(el => {
                            const text = el.textContent.trim();
                            // Ocultar si contiene nombre de icono O si es stIconMaterial
                            if (el.getAttribute('data-testid') === 'stIconMaterial' ||
                                iconNames.some(name => text === name || text.includes(name)) || 
                                el.className.includes('keyboard') || 
                                el.className.includes('arrow')) {
                                el.style.display = 'none';
                                el.style.visibility = 'hidden';
                                el.style.height = '0';
                                el.style.width = '0';
                                el.style.overflow = 'hidden';
                                el.style.fontSize = '0';
                                el.style.opacity = '0';
                                el.style.lineHeight = '0';
                                el.style.padding = '0';
                                el.style.margin = '0';
                            }
                        });
                    } catch(e) {
                        // Ignorar errores de selectores inválidos
                    }
                });
                
                // 4. Buscar específicamente stIconMaterial que contiene texto de iconos
                try {
                    document.querySelectorAll('[data-testid="stIconMaterial"]').forEach(el => {
                        const text = el.textContent.trim();
                        if (iconNames.some(name => text === name || text.includes(name))) {
                            el.style.display = 'none';
                            el.style.visibility = 'hidden';
                            el.style.height = '0';
                            el.style.width = '0';
                            el.style.overflow = 'hidden';
                            el.style.fontSize = '0';
                            el.style.opacity = '0';
                        }
                    });
                } catch(e) {
                    // Ignorar errores
                }
                
                // 3. Buscar específicamente en botones, expanders, dropdowns
                const componentSelectors = [
                    'button span',
                    'button i',
                    '.stButton span',
                    '.stButton i',
                    '.streamlit-expanderHeader span',
                    '.streamlit-expanderHeader i',
                    '.streamlit-expanderHeader [data-testid="stIconMaterial"]',
                    '[data-testid="stExpander"] span',
                    '[data-testid="stExpander"] i',
                    '[data-testid="stExpander"] [data-testid="stIconMaterial"]',
                    'summary [data-testid="stIconMaterial"]',
                    '[data-baseweb="select"] span',
                    '[data-baseweb="select"] i',
                    '[data-baseweb="popover"] span',
                    '[data-baseweb="popover"] i',
                    '[data-baseweb="button"] span',
                    '[data-baseweb="button"] i'
                ];
                
                componentSelectors.forEach(selector => {
                    try {
                        document.querySelectorAll(selector).forEach(el => {
                            const text = el.textContent.trim();
                            if (iconNames.some(name => text === name)) {
                                el.style.display = 'none';
                                el.style.visibility = 'hidden';
                                el.style.height = '0';
                                el.style.width = '0';
                            }
                        });
                    } catch(e) {
                        // Ignorar errores
                    }
                });
            }
            
            // Función para ejecutar inmediatamente y después de delays
            function runHideIconText() {
                hideIconText();
                setTimeout(hideIconText, 50);
                setTimeout(hideIconText, 100);
                setTimeout(hideIconText, 200);
                setTimeout(hideIconText, 300);
                setTimeout(hideIconText, 500);
                setTimeout(hideIconText, 1000);
            }
            
            // Ejecutar cuando el DOM esté listo
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', runHideIconText);
            } else {
                runHideIconText();
            }
            
            // Observar cambios en el DOM para elementos que se agregan dinámicamente
            const observer = new MutationObserver(function(mutations) {
                let shouldRun = false;
                mutations.forEach(function(mutation) {
                    if (mutation.addedNodes.length) {
                        shouldRun = true;
                    }
                });
                if (shouldRun) {
                    setTimeout(hideIconText, 10);
                    setTimeout(hideIconText, 50);
                }
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true,
                characterData: true,
                attributes: true
            });
            
            // También ejecutar periódicamente para asegurar que se oculten
            setInterval(hideIconText, 1500);
            
            // Ejecutar cuando se hace clic (los expanders se abren/cierran)
            document.addEventListener('click', function() {
                setTimeout(hideIconText, 100);
                setTimeout(hideIconText, 300);
            });
        })();
        </script>
        """,
        unsafe_allow_html=True
    )
