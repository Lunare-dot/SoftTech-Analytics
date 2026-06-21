# =============================================================================
# GUIA DE INTEGRAÇÃO COM A CAMADA BUSINESS
# =============================================================================
#
# Este módulo deve consumir exclusivamente funções das camadas:
#
#   layers.business.kpi_engine
#   layers.business.analytics
#   layers.data.filter
#
# Fluxo recomendado:
#
# 1) Loader
#    load_raw_data()
#
# 2) Cleaner
#    clean()
#
# 3) Filtros opcionais da interface
#    apply_filters()
#    filter_by_year()
#    filter_by_methodology()
#    filter_by_team()
#    filter_by_sector()
#    filter_by_size()
#    filter_by_complexity()
#
# 4) KPIs principais da tela inicial
#
#    full_kpi_dashboard(df)
#
#    Retorna:
#      - prazo
#      - custo
#      - atraso
#      - bugs
#      - retrabalho
#
#    Alternativamente:
#
#      on_time_rate(df)
#      cost_overrun_rate(df)
#      average_delay(df)
#      bug_summary(df)
#      rework_summary(df)
#
#
# =============================================================================
# REQUISITOS DO EDITAL (SEÇÃO 3.3)
# =============================================================================
#
# KPI: Taxa de projetos entregues no prazo
# -> on_time_rate()
#
# KPI: Desvio de custo / estouro de orçamento
# -> cost_overrun_rate()
#
# KPI: Indicadores de atraso
# -> average_delay()
#
# KPI: Indicadores de bugs
# -> bug_summary()
#
# KPI: Indicadores de retrabalho
# -> rework_summary()
#
#
# =============================================================================
# REQUISITOS DO EDITAL (SEÇÃO 3.4)
# =============================================================================
#
# Hipótese 1:
# Equipes mais experientes produzem menos defeitos
#
# -> analytics.experience_vs_bugs()
#
#
# Hipótese 2:
# Projetos mais complexos apresentam maiores atrasos
#
# -> analytics.complexity_vs_delay()
#
#
# Hipótese 3:
# Retrabalho impacta satisfação do cliente
#
# -> analytics.rework_vs_satisfaction()
#
#
# Hipótese 4:
# Horas extras influenciam cumprimento de prazo
#
# -> analytics.overtime_vs_deadline()
#
#
# Hipótese 5:
# Porte influencia custo
#
# -> analytics.size_vs_cost()
#
#
# Hipótese 6:
# Metodologia influencia desempenho
#
# -> analytics.methodology_vs_performance()
#
#
# Ranking de equipes
#
# -> analytics.team_performance_ranking()
#
#
# IMPORTANTE:
#
# Nenhum cálculo estatístico deve ser reimplementado na camada de apresentação.
#
# Dashboard apenas consome resultados prontos retornados pela camada business.
#
# =============================================================================