# business/analytics.py
# Orquestra os cruzamentos de dados para a Seção 3.4 do edital.
# Todas as funções disparam testes estatísticos ou KPIs para investigar as hipóteses.

import pandas as pd
import numpy as np

from .statistics import (
    correlation_test,
    ttest_two_groups,
    mann_whitney_test,
    chi_square_test,
    kruskal_wallis_test,
)
from .kpi_engine import kpis_by_group, satisfaction_by_group, on_time_by_group

def _group_stats(df: pd.DataFrame, group_col: str, metric_col: str) -> pd.DataFrame:
    # Utilitário: devolve o resumo estatístico de uma coluna específica agrupada por categoria
    return df.groupby(group_col)[metric_col].agg(n="count", média="mean", mediana="median", desvio_pad="std").round(3)


def experience_vs_bugs(df: pd.DataFrame) -> dict:
    # Avalia a correlação entre tempo de carreira dos desenvolvedores e quantidade/gravidade dos defeitos no código
    corr_total = correlation_test(df["experiencia_media_anos"], df["bugs_total"])
    corr_critico = correlation_test(df["experiencia_media_anos"], df["bugs_criticos"])

    # Cria blocos (faixas) de experiência para analisar em Boxplot no Streamlit
    df = df.copy()
    df["faixa_exp"] = pd.cut(df["experiencia_media_anos"], bins=[0, 2, 4, 6, 99], labels=["0–2 anos", "2–4 anos", "4–6 anos", "6+ anos"], right=True)
    por_faixa = _group_stats(df, "faixa_exp", "bugs_total")
    por_faixa["bugs_criticos_media"] = df.groupby("faixa_exp")["bugs_criticos"].mean().round(3)

    return {
        "hipotese":                       "Equipes mais experientes produzem menos defeitos",
        "correlação_exp_x_bugs_total":    corr_total,
        "correlação_exp_x_bugs_críticos": corr_critico,
        "estatísticas_por_faixa_exp":     por_faixa,
    }


def complexity_vs_delay(df: pd.DataFrame) -> dict:
    # Verifica se os projetos de maior dificuldade técnica são os que causam os maiores atrasos
    rank_col = "complexidade_rank" if "complexidade_rank" in df.columns else None

    result = {
        "hipotese":                     "Projetos de maior complexidade apresentam maiores atrasos",
        "atraso_por_complexidade":      _group_stats(df, "complexidade", "atraso_dias"),
        "taxa_atraso_por_complexidade": on_time_by_group(df, "complexidade"),
    }

    # Só roda as correlações e testes estatísticos se o cleaner.py gerou os ranks numéricos corretamente
    if rank_col:
        result["correlação_complexidade_x_atraso"] = correlation_test(df[rank_col].astype(float), df["atraso_dias"])

    if df["complexidade"].isin(["Baixa", "Muito alta"]).any():
        result["teste_baixa_vs_muito_alta"] = mann_whitney_test(df, "atraso_dias", "complexidade", "Baixa", "Muito alta")

    return result


def rework_vs_satisfaction(df: pd.DataFrame) -> dict:
    # Confere se os clientes percebem a qualidade e diminuem a nota quando há muito retrabalho interno da equipe
    corr = correlation_test(df["retrabalho_horas"], df["satisfacao_cliente"])

    # Divide o retrabalho em três caixas exatas (os 33% que menos tiveram, o meio, e os 33% que mais tiveram)
    df = df.copy()
    df["tercil_retrabalho"] = pd.qcut(df["retrabalho_horas"], q=3, labels=["baixo", "médio", "alto"])
    por_tercil = _group_stats(df, "tercil_retrabalho", "satisfacao_cliente")

    return {
        "hipotese":                           "Maior retrabalho está associado a menor satisfação do cliente",
        "correlação_retrabalho_x_satisfacao": corr,
        "satisfacao_por_tercil_retrabalho":   por_tercil,
    }


def overtime_vs_deadline(df: pd.DataFrame) -> dict:
    # Estuda se fazer hora extra ajuda a entregar no prazo ou se é um sintoma de um projeto que já está desandando
    corr = correlation_test(df["horas_extras"], df["atraso_dias"])
    test = mann_whitney_test(df, "horas_extras", "entregue_no_prazo", "Sim", "Não")
    media_ot = df.groupby("entregue_no_prazo")["horas_extras"].agg(n="count", média="mean", mediana="median").round(2)

    return {
        "hipotese":                     "Projetos com mais horas extras têm maior dificuldade de cumprir prazo",
        "correlação_overtime_x_atraso": corr,
        "teste_no_prazo_vs_atrasado":   test,
        "horas_extras_por_prazo":       media_ot,
    }


def size_vs_cost(df: pd.DataFrame) -> dict:
    # Compara se o fato do projeto ser de grande porte é o gatilho para os estouros de orçamento
    custo_por_porte = df.groupby("porte_projeto")["custo_real_mil"].agg(n="count", média="mean", mediana="median", desvio_pad="std", min="min", max="max").round(2)
    
    estouro_por_porte = None
    if "custo_desvio_pct" in df.columns:
        estouro_por_porte = df.groupby("porte_projeto")["custo_desvio_pct"].agg(média="mean", mediana="median").round(2)

    result = {
        "hipotese":               "Projetos de maior porte têm custos reais maiores e mais variáveis",
        "custo_real_por_porte":   custo_por_porte,
        "estouro_pct_por_porte":  estouro_por_porte,
    }

    if "porte_projeto_rank" in df.columns:
        result["correlação_porte_x_custo"] = correlation_test(df["porte_projeto_rank"].astype(float), df["custo_real_mil"])

    return result


def methodology_vs_performance(df: pd.DataFrame) -> dict:
    # Dispara os KPIs e testes para provar matematicamente qual Metodologia (Ágil vs Tradicional vs Híbrida) é a melhor
    kpis = kpis_by_group(df, "metodologia")
    satisfacao = satisfaction_by_group(df, "metodologia")
    on_time = on_time_by_group(df, "metodologia")
    
    # Testa dependência categórica e testa médias entre as 3 metodologias (usando função nativa da camada business)
    chi2_result = chi_square_test(df, "metodologia", "entregue_no_prazo")
    kw_result = kruskal_wallis_test(df, "satisfacao_cliente", "metodologia")

    return {
        "hipotese":                         "A metodologia de desenvolvimento influencia o desempenho dos projetos",
        "kpis_por_metodologia":             kpis,
        "satisfacao_por_metodologia":       satisfacao,
        "on_time_por_metodologia":          on_time,
        "qui_quadrado_metodologia_x_prazo": chi2_result,
        "kruskal_wallis_satisfacao":        kw_result,
    }


def team_performance_ranking(df: pd.DataFrame) -> pd.DataFrame:
    # Ranking composto pelas 4 métricas de negócios mais importantes, já indicando quem precisa de bônus ou cobrança
    g = df.groupby("equipe")

    stats_df = pd.DataFrame({
        "n_projetos":          g["id_projeto"].count(),
        "satisfacao_media":    g["satisfacao_cliente"].mean(),
        "on_time_%":           g["entregue_no_prazo"].apply(lambda s: (s == "Sim").mean() * 100),
        "bugs_criticos_media": g["bugs_criticos"].mean(),
        "atraso_medio":        g["atraso_dias"].mean(),
    }).round(3)

    # Normaliza os números entre 0 e 1 (onde 1 é sempre o cenário perfeito para a empresa) para poder somá-los
    def minmax(s):
        mn, mx = s.min(), s.max()
        return (s - mn) / (mx - mn) if mx != mn else pd.Series(0.5, index=s.index)

    score = (minmax(stats_df["satisfacao_media"]) + minmax(stats_df["on_time_%"]) + (1 - minmax(stats_df["bugs_criticos_media"])) + (1 - minmax(stats_df["atraso_medio"]))) / 4

    stats_df["score_composto"] = score.round(4)
    return stats_df.sort_values("score_composto", ascending=False)