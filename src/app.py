import streamlit as st
from consts import SearchParams
from search_mechanism import find_complete_articles, find_terms_in_tuples
import pandas as pd
import plotly.graph_objects as go
from barplot_st import plot_term_tuples

# Configuração da página
st.set_page_config(
    page_title="Sumário Tecnologias Petrobras",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para melhorar visual
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🛢️ Sumário de Tecnologias Petrobras</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Análise de tecnologias e termos ambientais em artigos científicos</div>', unsafe_allow_html=True)

# Inicializar params
params = SearchParams()

# Inicializar session state para manter dados entre interações
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'tec_terms_processed' not in st.session_state:
    st.session_state.tec_terms_processed = []
if 'env_terms_processed' not in st.session_state:
    st.session_state.env_terms_processed = []

# Formulário de busca
with st.form("search_form"):
    st.subheader("🔍 Parâmetros de Busca")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tec_terms = st.multiselect(
            "Tecnologias",
            params.tec,
            help="Selecione uma ou mais tecnologias para análise"
        )
    
    with col2:
        env_terms = st.multiselect(
            "Termos Ambientais",
            params.environment,
            help="Selecione termos ambientais relacionados"
        )
    
    with col3:
        # Filtro de anos (opcional)
        all_years = [str(year) for year in range(2015, 2027)]
        selected_years = st.multiselect(
            "Filtrar Anos (opcional)",
            all_years,
            help="Deixe vazio para incluir todos os anos"
        )
    
    # Botão centralizado e estilizado
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        submitted = st.form_submit_button("🚀 Buscar", use_container_width=True, type="primary")

# Processar resultados
if submitted:
    if not tec_terms or not env_terms:
        st.error("⚠️ Por favor, selecione ao menos um termo de cada categoria!")
    else:
        with st.spinner("🔄 Processando dados..."):
            # Processar termos
            tec_terms_processed = ["_".join(s.lower().split()) for s in tec_terms]
            env_terms_processed = ["_".join(s.lower().split()) for s in env_terms]
            
            # Armazenar no session state
            st.session_state.tec_terms_processed = tec_terms_processed
            st.session_state.env_terms_processed = env_terms_processed
            st.session_state.selected_years = selected_years
            
            # Buscar artigos
            available_articles = find_complete_articles(tec_terms_processed, env_terms_processed)
            
            # Buscar combinações de termos (com filtro de anos se fornecido)
            if selected_years:
                data = find_terms_in_tuples(tec_terms_processed, env_terms_processed, years=selected_years)
            else:
                data = find_terms_in_tuples(tec_terms_processed, env_terms_processed)
            
            # Armazenar resultados no session state
            st.session_state.search_results = {
                'available_articles': available_articles,
                'data': data
            }

# Exibir resultados se existirem
if st.session_state.search_results is not None:
    available_articles = st.session_state.search_results['available_articles']
    data = st.session_state.search_results['data']
    
    # Verificar se há resultados
    if not available_articles:
        st.warning("🔍 Nenhum artigo encontrado com os termos selecionados.")
    else:
        # Métricas principais
        total_articles = sum(len(v) for v in available_articles.values())
        years_range = f"{min(available_articles.keys())} - {max(available_articles.keys())}"
        avg_per_year = total_articles / len(available_articles)
        
        st.success(f"✅ Análise concluída! {total_articles} artigos encontrados.")
        
        # Cards de métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📚 Total de Artigos", total_articles)
        with col2:
            st.metric("📅 Período", years_range)
        with col3:
            st.metric("📊 Média/Ano", f"{avg_per_year:.1f}")
        with col4:
            st.metric("🔗 Combinações", len(data))
        
        st.markdown("---")
        
        # Tabs para organizar visualizações
        tab1, tab2, tab3 = st.tabs(["📊 Distribuição Temporal", "🎯 Combinações de Termos", "📄 Dados Detalhados"])
        
        with tab1:
            st.subheader("Evolução Temporal dos Artigos")
            
            # Preparar série temporal
            distrib_arround_years = [len(v) for k, v in available_articles.items()]
            series = pd.DataFrame({
                "count": distrib_arround_years[::-1],
                "year": list(available_articles.keys())[::-1]
            })
            
            # Gráfico de linha melhorado
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=series["year"],
                y=series["count"],
                mode='lines+markers',
                line=dict(color='#1f77b4', width=3),
                marker=dict(color='#1f77b4', size=10, line=dict(color='white', width=2)),
                fill='tozeroy',
                fillcolor='rgba(31, 119, 180, 0.1)',
                name='Artigos',
                hovertemplate='<b>Ano:</b> %{x}<br><b>Artigos:</b> %{y}<extra></extra>'
            ))
            
            fig.update_layout(
                title="Distribuição de Artigos por Ano",
                xaxis=dict(
                    title="Ano",
                    showgrid=True,
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    showline=True,
                    linecolor='black',
                    mirror=True
                ),
                yaxis=dict(
                    title="Número de Artigos",
                    showgrid=True,
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    showline=True,
                    linecolor='black',
                    mirror=True
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Estatísticas adicionais
            col1, col2 = st.columns(2)
            with col1:
                max_year = series.loc[series['count'].idxmax(), 'year']
                max_count = series['count'].max()
                st.info(f"🏆 **Ano com mais artigos**: {max_year} ({max_count} artigos)")
            with col2:
                trend = "crescente 📈" if series['count'].iloc[-1] > series['count'].iloc[0] else "decrescente 📉"
                st.info(f"📉 **Tendência**: {trend}")
        
        with tab2:
            st.subheader("Combinações de Termos Mais Frequentes")
            
            if data:
                # Slider para controlar número de combinações (com key única para evitar reset)
                top_n = st.slider(
                    "Número de combinações a exibir:", 
                    5, 
                    min(30, len(data)), 
                    15,
                    key="top_n_slider"
                )
                
                fig_b = plot_term_tuples(data, top_n=top_n, title="Combinações de Termos")
                st.plotly_chart(fig_b, use_container_width=True)
                
                # Tabela resumida
                with st.expander("📋 Ver tabela de combinações"):
                    combo_df = pd.DataFrame([
                        {
                            "TEC": ", ".join(k[0]),
                            "ENV": ", ".join(k[1]),
                            "Contagem": v
                        }
                        for k, v in sorted(data.items(), key=lambda x: x[1], reverse=True)
                    ])
                    st.dataframe(combo_df, use_container_width=True, height=400)
            else:
                st.warning("Nenhuma combinação de termos encontrada.")
        
        with tab3:
            st.subheader("Artigos Encontrados")
            
            # Preparar DataFrame
            df_data = {}
            c = 0
            for year, articles in available_articles.items():
                for article_id, article_data in articles.items():
                    df_data[c] = {
                        "Ano": year,
                        "Título": article_data.get("title", "N/A"),
                        "Abstract": article_data.get("abstract", "N/A")[:200] + "...",
                        "URL": article_data.get("url", "N/A"),
                        "Termos": ", ".join(article_data.get("terms_founded", []))
                    }
                    c += 1
            
            df = pd.DataFrame(df_data).transpose()
            
            # Filtros
            col1, col2 = st.columns([1, 3])
            with col1:
                year_filter = st.multiselect(
                    "Filtrar por ano:",
                    sorted(df['Ano'].unique()),
                    default=sorted(df['Ano'].unique()),
                    key="year_filter_detail"
                )
            with col2:
                search_text = st.text_input("🔎 Buscar no título:", key="search_text_detail")
            
            # Aplicar filtros
            filtered_df = df[df['Ano'].isin(year_filter)]
            if search_text:
                filtered_df = filtered_df[filtered_df['Título'].str.contains(search_text, case=False, na=False)]
            
            st.info(f"Mostrando {len(filtered_df)} de {len(df)} artigos")
            
            # Tabela com configuração de colunas
            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=500,
                column_config={
                    "URL": st.column_config.LinkColumn("URL"),
                    "Título": st.column_config.TextColumn("Título", width="large"),
                    "Abstract": st.column_config.TextColumn("Abstract", width="large"),
                }
            )
            
            # Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "⬇️ Download CSV Completo",
                csv,
                "artigos_petrobras.csv",
                "text/csv",
                key='download-csv'
            )
            
            # JSON completo em expander
            with st.expander("🔍 Ver JSON completo dos resultados"):
                st.json(available_articles)

else:
    # Estado inicial - mostrar instruções
    st.info("👆 **Comece selecionando os termos de busca no formulário acima**")
    
    # Exemplo visual
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🎯 O que você pode fazer:
        - Analisar distribuição temporal de publicações
        - Identificar combinações de termos mais comuns
        - Explorar artigos em detalhes
        - Exportar dados para análise externa
        """)
    with col2:
        st.markdown("""
        ### 📊 Recursos disponíveis:
        - Gráficos interativos com Plotly
        - Filtros e busca em tempo real
        - Download de dados em CSV
        - Visualização de JSONs completos
        """)