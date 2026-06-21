# business/kpi_engine.py
# Calcula os indicadores-chave de desempenho (KPIs) para a Seção 3.3 do edital.
# Todos os métodos retornam dicionários ou DataFrames prontos para os "cards" e gráficos do Streamlit.

import numpy as np
import pandas as pd

def on_time_rate(df: pd.DataFrame) -> dict:
    # Calcula a taxa de entrega no prazo usando a coluna categórica oficial da empresa
    total = len(df)
    no_prazo = (df["entregue_no_prazo"] == "Sim").sum()
    
    return {
        "total_projetos":   total,
        "no_prazo":         int(no_prazo),
        "com_atraso":       int(total - no_prazo),
        "taxa_%":           round(no_prazo / total * 100, 2),
    }

def cost_overrun_rate(df: pd.DataFrame) -> dict:
    # Calcula a taxa de estouro de custo consumindo as colunas já criadas pelo cleaner.py (evita repetição de código)
    estouro = df["custo_desvio_mil"] > 0
    
    return {
        "total_projetos":   len(df),
        "com_estouro":      int(estouro.sum()),
        "taxa_%":           round(estouro.mean() * 100, 2),
        "desvio_medio_mil": round(df["custo_desvio_mil"].mean(), 2),
        "desvio_medio_%":   round(df["custo_desvio_pct"].mean(), 2),
        "desvio_mediano_%": round(df["custo_desvio_pct"].median(), 2),
    }

def average_delay(df: pd.DataFrame) -> dict:
    # Gera estatísticas detalhadas puramente sobre os dias de calendário (atrasos, antecipações e entregas exatas)
    d = df["atraso_dias"]
    return {
        "media_dias":           round(d.mean(), 2),
        "mediana_dias":         round(d.median(), 2),
        "desvio_pad":           round(d.std(), 2),
        "atraso_maximo":        int(d.max()),
        "antecipacao_maxima":   int(d.min()),
        "projetos_atrasados":   int((d > 0).sum()),
        "projetos_antecipados": int((d < 0).sum()),
        "projetos_exatos":      int((d == 0).sum()),
    }

def bug_summary(df: pd.DataFrame) -> dict:
    # Consolida os indicadores de qualidade de software (quantidade e proporção de defeitos críticos)
    total_bugs = df["bugs_total"].sum()
    total_criticos = df["bugs_criticos"].sum()

    return {
        "total_bugs_dataset":     int(total_bugs),
        "total_criticos_dataset": int(total_criticos),
        "proporcao_criticos_%":   round(total_criticos / total_bugs * 100, 2) if total_bugs > 0 else 0,
        "media_bugs_projeto":     round(df["bugs_total"].mean(), 2),
        "media_criticos_projeto": round(df["bugs_criticos"].mean(), 2),
        "mediana_bugs":           round(df["bugs_total"].median(), 2),
        "max_bugs_projeto":       int(df["bugs_total"].max()),
    }

def rework_summary(df: pd.DataFrame) -> dict:
    # Resume o impacto das horas de retrabalho registradas pelas equipes
    rework = df["retrabalho_horas"]
    return {
        "total_horas_retrabalho": round(rework.sum(), 1),
        "media_por_projeto":      round(rework.mean(), 2),
        "mediana":                round(rework.median(), 2),
        "max":                    round(rework.max(), 2),
        "cv_%":                   round(rework.std() / rework.mean() * 100, 2),
    }

def kpis_by_group(df: pd.DataFrame, group_col: str, metrics: list[str] | None = None) -> pd.DataFrame:
    # Agrupa múltiplas métricas por uma categoria (ex: ver média de atraso e bugs agrupado por "Metodologia")
    if metrics is None:
        metrics = [
            "atraso_dias", "bugs_total", "bugs_criticos", "retrabalho_horas", 
            "satisfacao_cliente", "custo_desvio_pct", "horas_extras", "experiencia_media_anos"
        ]
        metrics = [m for m in metrics if m in df.columns]

    return df.groupby(group_col)[metrics].agg(["mean", "median", "std"]).round(3)

def on_time_by_group(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    # Cruza a taxa de entrega no prazo com alguma categoria (ex: qual Equipe entrega mais no prazo?)
    grouped = df.groupby(group_col)["entregue_no_prazo"].apply(
        lambda s: pd.Series({
            "total":    len(s),
            "no_prazo": (s == "Sim").sum(),
            "taxa_%":   round((s == "Sim").mean() * 100, 2),
        })
    ).unstack()
    return grouped

def satisfaction_by_group(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    # Analisa as notas dadas pelos clientes agrupadas por categoria
    return (
        df.groupby(group_col)["satisfacao_cliente"]
        .agg(["mean", "median", "min", "max", "std", "count"])
        .rename(columns={"mean": "média", "median": "mediana", "min": "mínimo", "max": "máximo", "std": "desvio_pad", "count": "n"})
        .round(3)
    )

def cost_deviation_series(df: pd.DataFrame) -> pd.Series:
    # Retorna diretamente a série de desvio percentual calculada na limpeza para alimentar gráficos como Boxplots
    return df["custo_desvio_pct"]

def bugs_per_developer(df: pd.DataFrame) -> pd.Series:
    # Cria indicador de densidade: divide o total de bugs pelo número de pessoas na equipe
    return (df["bugs_total"] / df["num_desenvolvedores"].replace(0, np.nan)).rename("bugs_por_dev")

def overtime_ratio(df: pd.DataFrame) -> pd.Series:
    # Cria indicador de sobrecarga: divide as horas extras pela quantidade de dias reais do projeto
    return (df["horas_extras"] / df["duracao_real_dias"].replace(0, np.nan)).rename("overtime_ratio")

def full_kpi_dashboard(df: pd.DataFrame) -> dict:
    # Pacote completo que dispara todos os cálculos de KPI de uma vez para popular a tela inicial do sistema
    return {
        "prazo":      on_time_rate(df),
        "custo":      cost_overrun_rate(df),
        "atraso":     average_delay(df),
        "bugs":       bug_summary(df),
        "retrabalho": rework_summary(df),
    }