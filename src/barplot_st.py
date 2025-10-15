import plotly.graph_objects as go
import plotly.express as px

def format_tuple_label(tuple_data):
    """Formata a tupla para exibição no gráfico"""
    tec_terms = ", ".join(tuple_data[0]) if tuple_data[0] else "N/A"
    env_terms = ", ".join(tuple_data[1]) if tuple_data[1] else "N/A"
    return f"TEC: {tec_terms} | ENV: {env_terms}"

def plot_term_tuples(result_dict, top_n=15, title="Combinações de Termos"):
    """
    Cria um gráfico de barras horizontais com as tuplas de termos
    
    Args:
        result_dict: Dicionário retornado por find_terms_in_tuples()
        top_n: Número de combinações a exibir (padrão: 15)
        title: Título do gráfico
    """
    
    # Ordenar por contagem (decrescente)
    sorted_items = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    
    # Pegar apenas os top_n
    top_items = sorted_items[:top_n]
    
    # Preparar dados
    labels = [format_tuple_label(item[0]) for item in top_items]
    counts = [item[1] for item in top_items]
    
    # Criar cores vibrantes para cada barra
    colors = px.colors.qualitative.Bold[:len(labels)]
    
    # Criar figura
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=labels,
        x=counts,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(255, 255, 255, 0.6)', width=1)
        ),
        text=counts,
        textposition='outside',
        textfont=dict(size=12, color='#333'),
        hovertemplate='<b>%{y}</b><br>Contagem: %{x}<extra></extra>'
    ))
    
    # Configurar layout
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color='#2c3e50'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Contagem',
            showgrid=True,
            gridcolor='#e0e0e0',
            title_font=dict(size=14)
        ),
        yaxis=dict(
            title='',
            autorange='reversed',  # Maior valor no topo
            title_font=dict(size=14)
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=max(400, len(labels) * 35),  # Altura dinâmica
        margin=dict(l=20, r=100, t=80, b=50),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    
    return fig