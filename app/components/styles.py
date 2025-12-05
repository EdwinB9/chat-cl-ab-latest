"""
Componente de estilos CSS para la aplicación Casa Limpia.
"""

import streamlit as st


def obtener_tema():
    """Retorna siempre 'light' ya que solo usamos modo claro."""
    return "light"


def aplicar_estilos_globales():
    """Aplica estilos CSS globales para Casa Limpia."""
    # Paleta de colores
    primary_color = "#00acc1"
    primary_dark = "#00838f"
    success_color = "#43a047"
    error_color = "#e53935"
    warning_color = "#fb8c00"
    info_color = "#1e88e5"
    text_primary = "#1a237e"
    text_secondary = "#546e7a"
    bg_primary = "#ffffff"
    bg_secondary = "#f5f9fa"
    bg_tertiary = "#e8f4f8"
    border_color = "#b0bec5"
    border_hover = "#90a4ae"
    shadow_sm = "0 1px 2px 0 rgba(0, 172, 193, 0.1)"
    shadow_md = "0 4px 6px -1px rgba(0, 172, 193, 0.15)"
    shadow_lg = "0 10px 15px -3px rgba(0, 172, 193, 0.2)"
    alert_info_bg = "rgba(30, 136, 229, 0.1)"
    alert_success_bg = "rgba(67, 160, 71, 0.1)"
    alert_error_bg = "rgba(229, 57, 53, 0.1)"
    alert_warning_bg = "rgba(251, 140, 0, 0.1)"
    download_hover = "#388e3c"
    
    # Cargar fuentes
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        """,
        unsafe_allow_html=True
    )
    
    # CSS
    css_content = f"""
    <style>
    :root {{
        --primary-color: {primary_color};
        --primary-dark: {primary_dark};
        --success-color: {success_color};
        --error-color: {error_color};
        --warning-color: {warning_color};
        --info-color: {info_color};
        --text-primary: {text_primary};
        --text-secondary: {text_secondary};
        --bg-primary: {bg_primary};
        --bg-secondary: {bg_secondary};
        --bg-tertiary: {bg_tertiary};
        --border-color: {border_color};
        --border-hover: {border_hover};
        --shadow-sm: {shadow_sm};
        --shadow-md: {shadow_md};
        --shadow-lg: {shadow_lg};
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --transition: 200ms cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    * {{
        font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        font-size: 0.925rem !important;
        line-height: 1.6 !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}
    
    div[data-testid="stCodeBlock"] *,
    div[data-testid="stCodeBlock"] pre,
    div[data-testid="stCodeBlock"] code {{
        font-family: 'Courier New', 'Consolas', 'Monaco', monospace !important;
    }}
    
    html, body, .stApp {{
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }}
    
    .main .block-container {{
        background-color: var(--bg-primary) !important;
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: var(--bg-secondary) !important;
    }}
    
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > div {{
        background-color: var(--bg-secondary) !important;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(5px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .input-container {{
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin: 1rem 0;
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
        transition: box-shadow var(--transition) !important;
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
        transition: box-shadow var(--transition) !important;
    }}
    
    .historial-container:hover {{
        box-shadow: var(--shadow-sm);
    }}
    
    .info-container {{
        border-radius: var(--radius-md);
        padding: 0.75rem;
        background: var(--bg-secondary);
        transition: background-color var(--transition) !important;
    }}
    
    .info-container:hover {{
        background-color: var(--bg-tertiary);
    }}
    
    .help-container {{
        box-sizing: border-box !important;
    }}
    
    .help-content-wrapper {{
        color: var(--text-primary) !important;
        line-height: 1.6;
    }}
    
    .help-content-wrapper * {{
        color: inherit !important;
        max-width: 100%;
        overflow-wrap: break-word;
    }}
    
    .help-content-wrapper div[data-testid="stCodeBlock"] *,
    .help-content-wrapper div[data-testid="stCodeBlock"] pre,
    .help-content-wrapper div[data-testid="stCodeBlock"] code {{
        overflow-wrap: normal !important;
        word-wrap: normal !important;
        white-space: pre !important;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-primary) !important;
    }}
    
    h1 {{
        font-weight: 700 !important;
        font-size: 2.25rem !important;
        margin-bottom: 1rem !important;
    }}
    
    h2 {{
        font-weight: 600 !important;
        font-size: 1.65rem !important;
    }}
    
    h3 {{
        font-weight: 600 !important;
        font-size: 1.35rem !important;
    }}
    
    .stMarkdown {{
        line-height: 1.6 !important;
        color: var(--text-primary) !important;
    }}
    
    .stMarkdown p {{
        margin-bottom: 1rem !important;
    }}
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }}
    
    [data-testid="stCaption"] {{
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
    }}
    
    [data-testid="stHeader"],
    [data-testid="stHeader"] * {{
        font-size: 1.2rem !important;
    }}
    
    [data-testid="stSubheader"],
    [data-testid="stSubheader"] * {{
        font-size: 1.1rem !important;
    }}
    
    [data-testid="stIconMaterial"],
    [class*="keyboard"],
    [class*="arrow"],
    [aria-label*="keyboard"] {{
        display: none !important;
        visibility: hidden !important;
    }}
    
    .stButton > button {{
        border-radius: var(--radius-md) !important;
        font-weight: 500 !important;
        transition: box-shadow var(--transition), background-color var(--transition) !important;
        box-shadow: var(--shadow-sm) !important;
    }}
    
    .stButton > button:hover {{
        box-shadow: var(--shadow-md) !important;
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
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border-color) !important;
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        transition: border-color var(--transition), box-shadow var(--transition) !important;
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
    
    .stSelectbox > div > div {{
        border-radius: var(--radius-md) !important;
        background-color: var(--bg-primary) !important;
        border: 1px solid var(--border-color) !important;
        transition: border-color var(--transition) !important;
    }}
    
    .stSelectbox > div > div:hover {{
        border-color: var(--border-hover) !important;
    }}
    
    .stSelectbox > div > div:focus-within {{
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(0, 172, 193, 0.15) !important;
    }}
    
    [data-baseweb="popover"] {{
        background-color: var(--bg-primary) !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: var(--shadow-lg) !important;
    }}
    
    [data-baseweb="popover"] li,
    [data-baseweb="popover"] [role="option"] {{
        transition: background-color var(--transition) !important;
    }}
    
    [data-baseweb="popover"] li:hover,
    [data-baseweb="popover"] [role="option"]:hover {{
        background-color: var(--bg-secondary) !important;
    }}
    
    [data-baseweb="popover"] li[aria-selected="true"] {{
        background-color: rgba(0, 172, 193, 0.1) !important;
        color: var(--primary-color) !important;
    }}
    
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
        transition: background-color var(--transition), box-shadow var(--transition) !important;
    }}
    
    .stSlider > div > div > div > div:hover {{
        background-color: var(--primary-dark) !important;
        box-shadow: 0 4px 8px rgba(0, 172, 193, 0.4) !important;
    }}
    
    .stNumberInput > div > div > div {{
        background-color: var(--bg-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        transition: border-color var(--transition) !important;
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
    }}
    
    .stNumberInput button {{
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        transition: all var(--transition) !important;
    }}
    
    .stNumberInput button:hover {{
        background-color: var(--bg-tertiary) !important;
        border-color: var(--primary-color) !important;
        color: var(--primary-color) !important;
    }}
    
    [data-testid="stFileUploader"] {{
        border: 2px dashed var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        padding: 2rem !important;
        background-color: var(--bg-secondary) !important;
        transition: border-color var(--transition), background-color var(--transition) !important;
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
        transition: all var(--transition) !important;
    }}
    
    [data-testid="stFileUploader"] button:hover {{
        background-color: var(--primary-dark) !important;
        box-shadow: var(--shadow-md) !important;
    }}
    
    .stAlert {{
        border-radius: var(--radius-md) !important;
        border-left: 4px solid !important;
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
    
    .streamlit-expanderHeader {{
        background-color: var(--bg-secondary) !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem 1rem !important;
        font-weight: 500 !important;
        color: var(--text-primary) !important;
        transition: background-color var(--transition) !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: var(--bg-tertiary) !important;
    }}
    
    .streamlit-expanderContent {{
        padding: 1rem !important;
        background-color: var(--bg-primary) !important;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: var(--radius-md) var(--radius-md) 0 0 !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: background-color var(--transition) !important;
    }}
    
    .stDownloadButton > button {{
        background-color: var(--success-color) !important;
        color: white !important;
        transition: background-color var(--transition), box-shadow var(--transition) !important;
    }}
    
    .stDownloadButton > button:hover {{
        background-color: {download_hover} !important;
        box-shadow: var(--shadow-md) !important;
    }}
    
    [data-testid="stMetricValue"] {{
        color: var(--primary-color) !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }}
    
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
        transition: background-color var(--transition) !important;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--text-secondary);
    }}
    
    hr {{
        margin: 2rem 0 !important;
        border: none !important;
        border-top: 1px solid var(--border-color) !important;
    }}
    
    footer, #MainMenu {{
        visibility: hidden;
    }}
    
    div[data-testid="stCodeBlock"] {{
        background-color: #f8f9fa !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
    }}
    
    div[data-testid="stCodeBlock"] pre {{
        background-color: #f8f9fa !important;
        color: #1a237e !important;
        font-family: 'Courier New', 'Consolas', 'Monaco', monospace !important;
        font-size: 0.875rem !important;
        line-height: 1.6 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow-x: auto !important;
        white-space: pre !important;
    }}
    
    div[data-testid="stCodeBlock"] code {{
        white-space: pre !important;
        display: block !important;
    }}
    
    [data-testid="stExpander"] [data-testid="column"] div[data-testid="stCodeBlock"] {{
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto !important;
    }}
    
    [data-testid="stExpander"] [data-testid="column"] div[data-testid="stCodeBlock"] pre,
    [data-testid="stExpander"] [data-testid="column"] div[data-testid="stCodeBlock"] code {{
        white-space: pre !important;
        display: block !important;
        width: 100% !important;
        overflow-x: auto !important;
    }}
    
    [data-testid="stExpander"] [data-testid="column"] {{
        min-width: 0 !important;
        overflow: visible !important;
        width: 100% !important;
    }}
    </style>
    """
    
    st.markdown(css_content, unsafe_allow_html=True)
    
    # Script para ocultar nombres de iconos
    st.markdown(
        """
        <script>
        (function() {
            const iconNames = [
                'keyboard_double_arrow_right', 'keyboard_double_arrow_left',
                'keyboard_arrow_right', 'keyboard_arrow_left',
                'keyboard_double_arrow_up', 'keyboard_double_arrow_down',
                'keyboard_arrow_up', 'keyboard_arrow_down',
                'chevron_right', 'chevron_left', 'expand_more', 'expand_less',
                'arrow_forward', 'arrow_back', 'arrow_drop_down', 'arrow_drop_up'
            ];
            
            function hideIconText() {
                const walker = document.createTreeWalker(
                    document.body,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );
                
                let node;
                while (node = walker.nextNode()) {
                    const text = node.textContent.trim();
                    if (iconNames.some(name => text === name || text.includes(name))) {
                        if (node.parentElement) {
                            node.parentElement.style.display = 'none';
                        }
                    }
                }
                
                document.querySelectorAll('[data-testid="stIconMaterial"], [class*="keyboard"], [class*="arrow"]').forEach(el => {
                    el.style.display = 'none';
                });
            }
            
            function runHideIconText() {
                hideIconText();
                setTimeout(hideIconText, 100);
                setTimeout(hideIconText, 300);
            }
            
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', runHideIconText);
            } else {
                runHideIconText();
            }
            
            const observer = new MutationObserver(function() {
                setTimeout(hideIconText, 50);
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
            
            document.addEventListener('click', function() {
                setTimeout(hideIconText, 100);
            });
        })();
        </script>
        """,
        unsafe_allow_html=True
    )
