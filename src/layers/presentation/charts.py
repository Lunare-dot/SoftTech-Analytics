# =============================================================================
# GUIA DE GRÁFICOS PARA O STREAMLIT
# =============================================================================
#
# Este módulo deve gerar apenas visualizações.
#
# Toda regra de negócio, KPI e estatística já existe na camada business.
#
#
# =============================================================================
# GRÁFICOS DESCRITIVOS (EDITAL 3.2)
# =============================================================================
#
# Fonte:
#
# statistics.describe_numeric()
# statistics.describe_categorical()
# statistics.frequency_table()
#
#
# Histogramas:
#
#   satisfacao_cliente
#   atraso_dias
#   custo_real_mil
#   retrabalho_horas
#   bugs_total
#
#
# Barras:
#
#   metodologia
#   porte_projeto
#   complexidade
#   equipe
#   setor_cliente
#
#
# =============================================================================
# OUTLIERS
# =============================================================================
#
# Fonte:
#
# statistics.outlier_summary()
#
#
# Boxplots:
#
#   atraso_dias
#   custo_real_mil
#   retrabalho_horas
#   bugs_total
#
#
# =============================================================================
# CORRELAÇÕES
# =============================================================================
#
# Fonte:
#
# statistics.correlation_matrix()
#
#
# Heatmap:
#
#   satisfacao_cliente
#   atraso_dias
#   retrabalho_horas
#   custo_real_mil
#   bugs_total
#
#
# =============================================================================
# HIPÓTESES DO EDITAL (SEÇÃO 3.4)
# =============================================================================
#
# experience_vs_bugs()
#
# Gráficos sugeridos:
#
#   Scatter:
#       experiencia_media_anos x bugs_total
#
#   Barras:
#       estatísticas_por_faixa_exp
#
#
# complexity_vs_delay()
#
# Gráficos sugeridos:
#
#   Boxplot:
#       atraso_dias por complexidade
#
#   Barras:
#       taxa_atraso_por_complexidade
#
#
# rework_vs_satisfaction()
#
# Gráficos sugeridos:
#
#   Scatter:
#       retrabalho_horas x satisfacao_cliente
#
#   Barras:
#       satisfacao_por_tercil_retrabalho
#
#
# overtime_vs_deadline()
#
# Gráficos sugeridos:
#
#   Boxplot:
#       horas_extras por entregue_no_prazo
#
#   Barras:
#       horas_extras_por_prazo
#
#
# size_vs_cost()
#
# Gráficos sugeridos:
#
#   Boxplot:
#       custo_real_mil por porte_projeto
#
#   Barras:
#       custo_real_por_porte
#
#
# methodology_vs_performance()
#
# Gráficos sugeridos:
#
#   Barras:
#       satisfacao_por_metodologia
#
#   Barras:
#       on_time_por_metodologia
#
#   Heatmap:
#       kpis_por_metodologia
#
#
# =============================================================================
# RANKING DE EQUIPES
# =============================================================================
#
# Fonte:
#
# analytics.team_performance_ranking()
#
# Gráfico recomendado:
#
#   Barras horizontais:
#       score_composto
#
#
# =============================================================================
# FILTROS DA INTERFACE
# =============================================================================
#
# Antes de gerar qualquer gráfico:
#
#   apply_filters()
#
# ou
#
#   filter_by_year()
#   filter_by_methodology()
#   filter_by_team()
#   filter_by_sector()
#   filter_by_size()
#   filter_by_complexity()
#
# Todos os gráficos devem respeitar os filtros ativos.
#
# =============================================================================