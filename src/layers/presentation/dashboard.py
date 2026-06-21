import streamlit as st
from src.layers.data import filter
from src.layers.business import kpi_engine, analytics
import src.layers.presentation.charts as charts

def show_dashboard(df):
    # =============================================================================
    # BARRA LATERAL (FILTROS)
    # =============================================================================
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2082/2082151.png", width=80)
    st.sidebar.title("Filtros Globais")
    st.sidebar.markdown("Os filtros aplicam-se a todas as abas do dashboard.")

    # Extrai os valores únicos para popular os selectboxes
    anos_disponiveis = sorted(df["ano_conclusao"].dropna().unique().tolist())
    metodologias = df["metodologia"].dropna().unique().tolist()
    equipes = df["equipe"].dropna().unique().tolist()
    portes = df["porte_projeto"].dropna().unique().tolist()

    f_ano = st.sidebar.multiselect("Ano de Conclusão", anos_disponiveis, default=anos_disponiveis)
    f_metodologia = st.sidebar.multiselect("Metodologia", metodologias, default=metodologias)
    f_equipe = st.sidebar.multiselect("Equipe", equipes, default=equipes)
    f_porte = st.sidebar.multiselect("Porte do Projeto", portes, default=portes)
    f_apenas_no_prazo = st.sidebar.checkbox("Mostrar apenas entregues no prazo")

    # Aplicar os filtros na base através da camada de dados
    filter_kwargs = {}
    if f_ano: filter_kwargs["year"] = f_ano
    if f_metodologia: filter_kwargs["metodologia"] = f_metodologia
    if f_equipe: filter_kwargs["equipe"] = f_equipe
    if f_porte: filter_kwargs["porte"] = f_porte
    if f_apenas_no_prazo: filter_kwargs["on_time"] = True

    df_filtered = filter.apply_filters(df, **filter_kwargs)

    if df_filtered.empty:
        st.warning("Nenhum projeto encontrado com os filtros atuais.")
        st.stop()

    # =============================================================================
    # ESTRUTURA PRINCIPAL (ABAS)
    # =============================================================================
    st.title("📊 SoftTech Analytics - Desempenho de Projetos")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Visão Geral & KPIs", 
        "🎯 Avaliação Descritiva",
        "🔍 Outliers & Correlações", 
        "🧪 Teste de Hipóteses", 
        "🏆 Ranking de Equipes"
    ])

    # =============================================================================
    # ABA 1: VISÃO GERAL & KPIs (SEÇÃO 3.3)
    # =============================================================================
    with tab1:
        st.markdown("### Indicadores Chave de Desempenho (KPIs)")
        
        # Consome o pacote completo de métricas da camada de negócios
        kpis = kpi_engine.full_kpi_dashboard(df_filtered)
        
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Projetos no Prazo", f"{kpis['prazo']['taxa_%']}%", 
                    f"{kpis['prazo']['no_prazo']} de {kpis['prazo']['total_projetos']} projet.")
                    
        col2.metric("Projetos c/ Estouro de Custo", f"{kpis['custo']['taxa_%']}%",
                    f"Desvio Médio: R$ {kpis['custo']['desvio_medio_mil']}k", delta_color="inverse")
                    
        col3.metric("Atraso Médio", f"{kpis['atraso']['media_dias']} dias",
                    f"Máx: {kpis['atraso']['atraso_maximo']} dias", delta_color="inverse")
                    
        col4.metric("Proporção de Bugs Críticos", f"{kpis['bugs']['proporcao_criticos_%']}%",
                    f"Média p/ projeto: {kpis['bugs']['media_criticos_projeto']}")
                    
        st.divider()
        
        st.markdown("### Panorama Geral do Portfólio")
        c1, c2, c3 = st.columns(3)
        with c1:
            charts.graphCreate_metodologia(df_filtered)
        with c2:
            charts.graphCreate_porte_projeto(df_filtered)
        with c3:
            charts.graphCreate_equipe(df_filtered)

    # =============================================================================
    # ABA 2: AVALIAÇÃO DESCRITIVA (SEÇÃO 3.2)
    # =============================================================================
    with tab2:
        st.markdown("### Distribuição das Variáveis Críticas")
        
        colA, colB = st.columns(2)
        with colA:
            charts.graphCreate_satisfacao_cliente(df_filtered)
            charts.graphCreate_custo_real_mil(df_filtered)
            charts.graphCreate_bugs_total(df_filtered)
        with colB:
            charts.graphCreate_atraso_dias(df_filtered)
            charts.graphCreate_retrabalho_horas(df_filtered)
            charts.graphCreate_complexidade(df_filtered)

    # =============================================================================
    # ABA 3: OUTLIERS E CORRELAÇÕES
    # =============================================================================
    with tab3:
        st.markdown("### Matriz de Correlação Global")
        st.info("Valores próximos de 1 indicam forte correlação positiva. Próximos de -1, forte negativa.")
        charts.graphCreate_heatmap_correlacao(df_filtered)
        
        st.divider()
        st.markdown("### Deteção de Anomalias (Outliers)")
        c1, c2 = st.columns(2)
        with c1:
            charts.graphCreate_boxplot_atraso_dias(df_filtered)
            charts.graphCreate_boxplot_retrabalho_horas(df_filtered)
        with c2:
            charts.graphCreate_boxplot_custo_real_mil(df_filtered)
            charts.graphCreate_boxplot_bugs_total(df_filtered)

    # =============================================================================
    # ABA 4: TESTE DE HIPÓTESES (SEÇÃO 3.4)
    # =============================================================================
    with tab4:
        st.markdown("### Investigação de Hipóteses do Negócio")
        st.write("Análise detalhada cruzando os requisitos do edital (Secção 3.4).")
        
        # Hipótese 1
        with st.expander("H1: Equipes mais experientes produzem menos defeitos?", expanded=False):
            res_h1 = analytics.experience_vs_bugs(df_filtered)
            st.markdown(f"**Resultado Estatístico:** {res_h1['correlação_exp_x_bugs_críticos']['interpretação']} para bugs críticos.")
            
            ca, cb = st.columns(2)
            with ca: charts.graphCreate_scatter_exp_vs_bugs(df_filtered)
            with cb: charts.graphCreate_bar_exp_faixa(df_filtered)

        # Hipótese 2
        with st.expander("H2: Projetos mais complexos apresentam maiores atrasos?", expanded=False):
            res_h2 = analytics.complexity_vs_delay(df_filtered)
            if "teste_baixa_vs_muito_alta" in res_h2:
                st.markdown(f"**Resultado (Mann-Whitney):** {res_h2['teste_baixa_vs_muito_alta']['decisão']}")
                
            ca, cb = st.columns(2)
            with ca: charts.graphCreate_boxplot_atraso_complexidade(df_filtered)
            with cb: charts.graphCreate_bar_taxa_atraso_complexidade(df_filtered)

        # Hipótese 3
        with st.expander("H3: Maior retrabalho impacta a satisfação do cliente?", expanded=False):
            res_h3 = analytics.rework_vs_satisfaction(df_filtered)
            st.markdown(f"**Resultado Estatístico:** {res_h3['correlação_retrabalho_x_satisfacao']['interpretação']}")
            
            ca, cb = st.columns(2)
            with ca: charts.graphCreate_scatter_rework_vs_satisfaction(df_filtered)
            with cb: charts.graphCreate_bar_satisfacao_tercil_rework(df_filtered)

        # Hipótese 4
        with st.expander("H4: Horas extras influenciam o cumprimento de prazos?", expanded=False):
            res_h4 = analytics.overtime_vs_deadline(df_filtered)
            st.markdown(f"**Resultado (Mann-Whitney):** {res_h4['teste_no_prazo_vs_atrasado']['decisão']}")
            
            ca, cb = st.columns(2)
            with ca: charts.graphCreate_boxplot_overtime_vs_deadline(df_filtered)
            with cb: charts.graphCreate_bar_overtime_por_prazo(df_filtered)

        # Hipótese 5
        with st.expander("H5: O porte do projeto influencia diretamente o custo?", expanded=False):
            res_h5 = analytics.size_vs_cost(df_filtered)
            if "correlação_porte_x_custo" in res_h5:
                st.markdown(f"**Resultado Estatístico:** {res_h5['correlação_porte_x_custo']['interpretação']}")
                
            ca, cb = st.columns(2)
            with ca: charts.graphCreate_boxplot_cost_vs_size(df_filtered)
            with cb: charts.graphCreate_bar_cost_por_size(df_filtered)

        # Hipótese 6
        with st.expander("H6: A Metodologia influencia o desempenho geral?", expanded=False):
            res_h6 = analytics.methodology_vs_performance(df_filtered)
            st.markdown(f"**Satisfação (Kruskal-Wallis):** {res_h6['kruskal_wallis_satisfacao']['decisão']}")
            st.markdown(f"**Prazo (Qui-Quadrado):** {res_h6['qui_quadrado_metodologia_x_prazo']['decisão']}")
            
            ca, cb = st.columns(2)
            with ca: charts.graphCreate_bar_ontime_metodologia(df_filtered)
            with cb: charts.graphCreate_bar_satisfacao_metodologia(df_filtered)
            st.markdown("<br>", unsafe_allow_html=True)
            charts.graphCreate_heatmap_kpis_metodologia(df_filtered)

    # =============================================================================
    # ABA 5: RANKING DE EQUIPES
    # =============================================================================
    with tab5:
        st.markdown("### Ranking Global de Desempenho")
        st.write("Score composto que penaliza bugs/atrasos e bonifica satisfação/entrega no prazo.")
        
        # Invoca o cálculo do Ranking
        charts.graphCreate_bar_ranking_equipes(df_filtered)
        
        # Exibe também a tabela pura para os diretores que gostam de ver os números
        st.markdown("#### Detalhamento das Métricas por Equipe")
        df_ranking = analytics.team_performance_ranking(df_filtered)
        st.dataframe(df_ranking.style.background_gradient(cmap='Greens', subset=['score_composto']))