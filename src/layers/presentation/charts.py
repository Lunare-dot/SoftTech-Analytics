import streamlit as st
import plotly.express as px
import pandas as pd

# =============================================================================
# GRÁFICOS DESCRITIVOS (EDITAL 3.2)
# =============================================================================

# Histogramas:

def graphCreate_satisfacao_cliente(data):
    fig = px.histogram(
        data,
        x="satisfacao_cliente",
        title="Histograma de Satisfação do Cliente",
        color_discrete_sequence=["#00CC96"]
    )
    
    # Notas de 0 a 10, agrupadas em blocos de 1 ponto
    fig.update_traces(xbins=dict(
        start=0,
        end=10,
        size=1
    ))
    
    fig.update_layout(
        bargap=0.1,
        xaxis_title="Nota de Satisfação (0 a 10)",
        yaxis_title="Quantidade de Projetos"
    )
    
    st.plotly_chart(fig)

def graphCreate_atraso_dias(data):
    fig = px.histogram(
        data,
        x="atraso_dias",
        title="Histograma de Atrasos em Projetos",
        color_discrete_sequence=["#CC3332"]
    )
    
    # Atrasos agrupados em ciclos de 15 dias (Sprints)
    fig.update_traces(xbins=dict(
        start=-30,
        end=120,
        size=15
    ))
    
    fig.update_layout(
        bargap=0.1,
        xaxis_title="Atraso (em Dias)",
        yaxis_title="Quantidade de Projetos"
    )
    
    st.plotly_chart(fig)

def graphCreate_custo_real_mil(data):
    fig = px.histogram(
        data,
        x="custo_real_mil",
        title="Distribuição do Custo Real dos Projetos",
        color_discrete_sequence=["#2A9D8F"]
    )
    
    # Custos agrupados em "Tiers" de R$ 25.000,00
    fig.update_traces(xbins=dict(
        start=0,
        end=800,
        size=25
    ))
    
    fig.update_layout(
        bargap=0.1,
        xaxis_title="Custo Real (R$ Mil)",
        yaxis_title="Quantidade de Projetos"
    )
    
    st.plotly_chart(fig)

def graphCreate_retrabalho_horas(data):
    fig = px.histogram(
        data,
        x="retrabalho_horas",
        title="Distribuição de Horas de Retrabalho",
        color_discrete_sequence=["#F4A261"]
    )
    
    # Agrupado de 10 em 10 horas (aprox. 1 dia e pouco de trabalho)
    fig.update_traces(xbins=dict(
        start=0,
        end=430,
        size=10
    ))
    
    fig.update_layout(
        bargap=0.1,
        xaxis_title="Retrabalho (em Horas)",
        yaxis_title="Quantidade de Projetos"
    )
    
    st.plotly_chart(fig)

def graphCreate_bugs_total(data):
    fig = px.histogram(
        data,
        x="bugs_total",
        title="Distribuição do Total de Bugs por Projeto",
        color_discrete_sequence=["#5A189A"]
    )
    
    # Agrupado de 5 em 5 bugs
    fig.update_traces(xbins=dict(
        start=0,
        end=90,
        size=5
    ))
    
    fig.update_layout(
        bargap=0.1,
        xaxis_title="Total de Bugs",
        yaxis_title="Quantidade de Projetos"
    )
    
    st.plotly_chart(fig)
    

# Barras:

def graphCreate_metodologia(data):
    # Conta a quantidade de projetos por metodologia
    contagem = data["metodologia"].value_counts().reset_index()
    contagem.columns = ["Metodologia", "Quantidade"]

    fig = px.bar(
        contagem,
        x="Metodologia",
        y="Quantidade",
        title="Quantidade de Projetos por Metodologia",
        color="Metodologia",
        color_discrete_sequence=["#118AB2", "#EF476F", "#FFD166"]
    )

    fig.update_layout(
        bargap=0.2,
        xaxis_title="Metodologia",
        yaxis_title="Quantidade de Projetos",
        showlegend=False
    )

    st.plotly_chart(fig)

def graphCreate_porte_projeto(data):
    contagem = data["porte_projeto"].value_counts().reset_index()
    contagem.columns = ["Porte", "Quantidade"]
    
    fig = px.bar(
        contagem,
        x="Porte",
        y="Quantidade",
        title="Quantidade de Projetos por Porte",
        color="Porte",
        color_discrete_sequence=["#4383EE", "#54FE69", "#FF473F"],
        category_orders={"Porte": ["Pequeno", "Médio", "Grande"]}
    )
    
    fig.update_layout(
        bargap=0.2,
        xaxis_title="Porte do Projeto",
        yaxis_title="Quantidade de Projetos",
        showlegend=False
    )
    
    st.plotly_chart(fig)
    
def graphCreate_complexidade(data):
    contagem = data["complexidade"].value_counts().reset_index()
    contagem.columns = ["Complexidade", "Quantidade"]
    
    fig = px.bar(
        contagem,
        x="Complexidade",
        y="Quantidade",
        title="Quantidade de Projetos por Complexidade",
        color="Complexidade",
        color_discrete_sequence=["#4383EE", "#54FE69", "#FF473F", "#5A189A"],
        category_orders={"Complexidade": ["Baixa", "Média", "Alta", "Muito alta"]}
    )
    
    fig.update_layout(
        bargap=0.2,
        xaxis_title="Complexidade do Projeto",
        yaxis_title="Quantidade de Projetos",
        showlegend=False
    )
    
    st.plotly_chart(fig)

def graphCreate_setor_cliente(data):
    contagem = data["setor_cliente"].value_counts().reset_index()
    contagem.columns = ["Setor", "Quantidade"]
    
    fig = px.bar(
        contagem,
        x="Setor",
        y="Quantidade",
        title="Quantidade de Projetos por Setor do Cliente",
        color="Setor",
        color_discrete_sequence=["#8A0200", "#FF9E3D", "#00398F", "#007A54", "#C2C2FF", "#41BBD9"],
    )
    
    fig.update_layout(
        bargap=0.2,
        xaxis_title="Setores", 
        yaxis_title="Quantidade de Projetos",
        showlegend=False
    )
    
    st.plotly_chart(fig)

def graphCreate_equipe(data):
    contagem = data["equipe"].value_counts().reset_index()
    contagem.columns = ["Equipe", "Quantidade"]
    
    fig = px.bar(
        contagem,
        x="Equipe",
        y="Quantidade",
        title="Quantidade de Projetos por Equipe",
        color="Equipe",
        color_discrete_sequence=["#753578", "#5FC1C3", "#F05D5E", "#1A389A", "#F7B801", "#B22827"],
        category_orders={"Equipe": ["Alpha", "Beta", "Gamma", "Delta", "Sigma", "Omega"]}
    )
    
    fig.update_layout(
        bargap=0.2,
        xaxis_title="Equipes",
        yaxis_title="Quantidade de Projetos",
        showlegend=False
    )
    
    st.plotly_chart(fig)

#
# =============================================================================
# OUTLIERS
# =============================================================================

def graphCreate_boxplot_atraso_dias(data):
    fig = px.box(
        data,
        y='atraso_dias',
        title='Boxplot: Atrasos em Dias',
        color_discrete_sequence=["#CC3332"]
    )
    fig.update_layout(xaxis_title="Dias de Atraso")
    st.plotly_chart(fig)
    
def graphCreate_boxplot_custo_real_mil(data):
    fig = px.box(
        data,
        x="custo_real_mil",
        title="Boxplot: Custo Real",
        color_discrete_sequence=["#2A9D8F"]
    )
    fig.update_layout(xaxis_title="Custo Real (R$ Mil)")
    st.plotly_chart(fig)

def graphCreate_boxplot_retrabalho_horas(data):
    fig = px.box(
        data,
        x='retrabalho_horas',
        title='Boxplot: Horas de Retrabalho',
        color_discrete_sequence=['#F4A261']
    )
    fig.update_layout(xaxis_title='Retrabalho (em Horas)')
    st.plotly_chart(fig)
    
def graphCreate_boxplot_bugs_total(data):
    fig = px.box(
        data,
        x="bugs_total",
        title="Boxplot: Total de Bugs",
        color_discrete_sequence=["#5A189A"]
    )
    fig.update_layout(xaxis_title="Total de Bugs")
    st.plotly_chart(fig)

#
# =============================================================================
# CORRELAÇÕES
# =============================================================================

def graphCreate_heatmap_correlacao(data):
    cols = ["satisfacao_cliente", "atraso_dias", "retrabalho_horas", "custo_real_mil", "bugs_total"]
    cols_presentes = [c for c in cols if c in data.columns]
    
    corr_matrix = data[cols_presentes].corr().round(2)
    
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Matriz de Correlação",
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1
    )
    st.plotly_chart(fig)

# =============================================================================
# HIPÓTESES DO EDITAL (SEÇÃO 3.4)
# =============================================================================

# experience_vs_bugs()
def graphCreate_scatter_exp_vs_bugs(data):
    #
    fig = px.scatter(
        data,
        x='experiencia_media_anos',
        y='bugs_total',
        title='Experiencia da Equipe vs Bugs',
        color_discrete_sequence=["#118AB2"]
    )
    fig.update_layout(
        xaxis_title="Experiência Média (em anos)",
        yaxis_title="Total de Bugs"
    )
    st.plotly_chart(fig)

def graphCreate_bar_exp_faixa(data):
    df_temp = data.copy()
    df_temp["faixa_exp"] = pd.cut(
        df_temp["experiencia_media_anos"], 
        bins=[0, 2, 4, 6, 99], 
        labels=["0–2 anos", "2–4 anos", "4–6 anos", "6+ anos"],
        right=True
    )
    contagem = df_temp.groupby("faixa_exp", observed=True)["bugs_total"].mean().reset_index()
    
    fig = px.bar(
        contagem, 
        x="faixa_exp", 
        y="bugs_total", 
        title="Média de Bugs por Faixa de Experiência", 
        color_discrete_sequence=["#5A189A"]
    )
    fig.update_layout(xaxis_title="Faixa de Experiência", yaxis_title="Média de Bugs")
    st.plotly_chart(fig)
    
# complexity_vs_delay()
def graphCreate_boxplot_atraso_complexidade(data):
    fig = px.box(
        data, 
        x="atraso_dias", 
        y="complexidade", 
        color="complexidade",
        title="Atrasos por Nível de Complexidade",
        category_orders={"complexidade": ["Baixa", "Média", "Alta", "Muito alta"]}
    )
    fig.update_layout(xaxis_title="Dias de Atraso", yaxis_title="Complexidade")
    st.plotly_chart(fig)

def graphCreate_bar_taxa_atraso_complexidade(data):
    df_temp = data.groupby("complexidade", observed=True)["entregue_no_prazo"].apply(
        lambda x: (x == "Não").mean() * 100
    ).reset_index(name="Taxa_Atraso_Pct")
    
    fig = px.bar(
        df_temp, 
        x="complexidade", 
        y="Taxa_Atraso_Pct", 
        title="Taxa de Atraso (%) por Complexidade",
        category_orders={"complexidade": ["Baixa", "Média", "Alta", "Muito alta"]},
        color="complexidade"
    )
    fig.update_layout(xaxis_title="Complexidade", yaxis_title="Projetos Atrasados (%)")
    st.plotly_chart(fig)
    
#rework vs satisfaction
def graphCreate_scatter_rework_vs_satisfaction(data):
    fig = px.scatter(
        data,
        x="retrabalho_horas",
        y="satisfacao_cliente",
        title="Retrabalho vs Satisfação do Cliente",
        color="entregue_no_prazo",
        opacity=0.7
    )
    fig.update_layout(xaxis_title="Horas de Retrabalho", yaxis_title="Nota de Satisfação")
    st.plotly_chart(fig)

def graphCreate_bar_satisfacao_tercil_rework(data):
    df_temp = data.copy()
    # Divide em 3 grupos exatos pelo volume de retrabalho
    df_temp["tercil_retrabalho"] = pd.qcut(df_temp["retrabalho_horas"], q=3, labels=["Baixo", "Médio", "Alto"])
    contagem = df_temp.groupby("tercil_retrabalho", observed=True)["satisfacao_cliente"].mean().reset_index()
    
    fig = px.bar(
        contagem, 
        x="tercil_retrabalho", 
        y="satisfacao_cliente", 
        title="Satisfação Média por Volume de Retrabalho", 
        color_discrete_sequence=["#F4A261"]
    )
    fig.update_layout(xaxis_title="Volume de Retrabalho", yaxis_title="Satisfação Média")
    st.plotly_chart(fig)
    
# overtime vs deadline
def graphCreate_boxplot_overtime_vs_deadline(data):
    fig = px.box(
        data,
        x="horas_extras",
        y="entregue_no_prazo",
        color="entregue_no_prazo",
        title="Distribuição de Horas Extras por Status de Entrega"
    )
    fig.update_layout(xaxis_title="Horas Extras Registradas", yaxis_title="Entregue no Prazo?")
    st.plotly_chart(fig)

def graphCreate_bar_overtime_por_prazo(data):
    df_temp = data.groupby("entregue_no_prazo")["horas_extras"].mean().reset_index()
    fig = px.bar(
        df_temp, 
        x="entregue_no_prazo", 
        y="horas_extras", 
        title="Média de Horas Extras por Status de Entrega", 
        color="entregue_no_prazo"
    )
    fig.update_layout(xaxis_title="Entregue no Prazo?", yaxis_title="Média de Horas Extras")
    st.plotly_chart(fig)

# size vs cost
def graphCreate_boxplot_cost_vs_size(data):
    fig = px.box(
        data, 
        x="custo_real_mil", 
        y="porte_projeto", 
        color="porte_projeto",
        title="Custo Real por Porte do Projeto",
        category_orders={"porte_projeto": ["Pequeno", "Médio", "Grande"]}
    )
    fig.update_layout(xaxis_title="Custo Real (R$ Mil)", yaxis_title="Porte do Projeto")
    st.plotly_chart(fig)

def graphCreate_bar_cost_por_size(data):
    df_temp = data.groupby("porte_projeto", observed=True)["custo_real_mil"].mean().reset_index()
    fig = px.bar(
        df_temp, 
        x="porte_projeto", 
        y="custo_real_mil", 
        title="Custo Real Médio por Porte do Projeto",
        category_orders={"porte_projeto": ["Pequeno", "Médio", "Grande"]},
        color="porte_projeto"
    )
    fig.update_layout(xaxis_title="Porte do Projeto", yaxis_title="Média de Custo Real (R$ Mil)")
    st.plotly_chart(fig)

# methodology_vs_performance()
def graphCreate_bar_satisfacao_metodologia(data):
    df_temp = data.groupby("metodologia")["satisfacao_cliente"].mean().reset_index()
    fig = px.bar(
        df_temp, 
        x="metodologia", 
        y="satisfacao_cliente", 
        title="Satisfação Média por Metodologia", 
        color="metodologia"
    )
    fig.update_layout(xaxis_title="Metodologia", yaxis_title="Satisfação Média (0 a 10)")
    st.plotly_chart(fig)

def graphCreate_bar_ontime_metodologia(data):
    df_temp = data.groupby("metodologia")["entregue_no_prazo"].apply(
        lambda x: (x == "Sim").mean() * 100
    ).reset_index(name="Taxa_No_Prazo_Pct")
    
    fig = px.bar(
        df_temp, 
        x="metodologia", 
        y="Taxa_No_Prazo_Pct", 
        title="Taxa de Entrega no Prazo por Metodologia", 
        color="metodologia"
    )
    fig.update_layout(xaxis_title="Metodologia", yaxis_title="Entregas no Prazo (%)")
    st.plotly_chart(fig)
    
def graphCreate_heatmap_kpis_metodologia(data):
    cols = ["atraso_dias", "bugs_total", "retrabalho_horas", "satisfacao_cliente"]
    if "custo_desvio_pct" in data.columns:
        cols.append("custo_desvio_pct")
    
    df_temp = data.groupby("metodologia")[cols].mean().round(2)
    
    df_norm = (df_temp - df_temp.min()) / (df_temp.max() - df_temp.min() + 0.0001)
    
    fig = px.imshow(
        df_norm,
        aspect="auto",
        title="Mapa de Calor: Média dos KPIs por Metodologia",
        color_continuous_scale="Blues"
    )
    
    fig.update_traces(text=df_temp.values, texttemplate="%{text}")
    
    st.plotly_chart(fig)

# =============================================================================
# RANKING DE EQUIPES
# =============================================================================

def graphCreate_bar_ranking_equipes(data):
    g = data.groupby("equipe")
    stats_df = pd.DataFrame({
        "satisfacao_media":    g["satisfacao_cliente"].mean(),
        "on_time_%":           g["entregue_no_prazo"].apply(lambda s: (s == "Sim").mean() * 100),
        "bugs_criticos_media": g["bugs_criticos"].mean(),
        "atraso_medio":        g["atraso_dias"].mean(),
    })

    def minmax(s):
        mn, mx = s.min(), s.max()
        return (s - mn) / (mx - mn) if mx != mn else pd.Series(0.5, index=s.index)

    # Fórmula: Maior satisfação e maior on_time = bom. Menor bugs e menor atraso = bom (por isso o 1 - x).
    score = (
        minmax(stats_df["satisfacao_media"]) + 
        minmax(stats_df["on_time_%"]) + 
        (1 - minmax(stats_df["bugs_criticos_media"])) + 
        (1 - minmax(stats_df["atraso_medio"]))
    ) / 4

    stats_df["score_composto"] = score.round(3)
    # Ordena ascendente porque o Plotly constrói as barras horizontais de baixo para cima
    stats_df = stats_df.reset_index().sort_values("score_composto", ascending=True)
    
    fig = px.bar(
        stats_df, 
        y="equipe", 
        x="score_composto", 
        orientation="h",
        title="Ranking de Desempenho das Equipes (Score Composto)",
        color="score_composto",
        color_continuous_scale="Viridis",
        text="score_composto"
    )
    
    fig.update_traces(textposition='auto')
    fig.update_layout(xaxis_title="Score de Qualidade (0 a 1)", yaxis_title="Equipas")
    
    st.plotly_chart(fig)