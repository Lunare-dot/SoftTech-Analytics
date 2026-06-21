import pandas as pd
import pytest

from src.layers.business.analytics import (
    experience_vs_bugs,
    complexity_vs_delay,
    rework_vs_satisfaction,
    overtime_vs_deadline,
    size_vs_cost,
    methodology_vs_performance,
    team_performance_ranking,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "id_projeto": range(1, 13),

        "experiencia_media_anos": [
            1, 2, 2, 3,
            4, 5, 5, 6,
            7, 8, 8, 9
        ],

        "bugs_total": [
            20, 18, 17, 15,
            12, 10, 9, 8,
            6, 5, 4, 3
        ],

        "bugs_criticos": [
            8, 7, 6, 5,
            4, 4, 3, 3,
            2, 1, 1, 0
        ],

        "complexidade": [
            "Baixa", "Baixa", "Baixa",
            "Média", "Média", "Média",
            "Alta", "Alta", "Alta",
            "Muito alta", "Muito alta", "Muito alta"
        ],

        "complexidade_rank": [
            1, 1, 1,
            2, 2, 2,
            3, 3, 3,
            4, 4, 4
        ],

        "atraso_dias": [
            0, 1, 2,
            5, 6, 7,
            10, 11, 12,
            20, 21, 22
        ],

        "entregue_no_prazo": [
            "Sim", "Sim", "Sim",
            "Sim", "Não", "Não",
            "Não", "Não", "Não",
            "Não", "Não", "Não"
        ],

        "retrabalho_horas": [
            5, 6, 7,
            10, 11, 12,
            15, 16, 17,
            20, 21, 22
        ],

        "satisfacao_cliente": [
            10, 10, 9,
            9, 8, 8,
            7, 7, 6,
            5, 5, 4
        ],

        "horas_extras": [
            2, 3, 4,
            5, 6, 7,
            8, 9, 10,
            11, 12, 13
        ],

        "porte_projeto": [
            "Pequeno", "Pequeno", "Pequeno", "Pequeno",
            "Médio", "Médio", "Médio", "Médio",
            "Grande", "Grande", "Grande", "Grande"
        ],

        "porte_projeto_rank": [
            1, 1, 1, 1,
            2, 2, 2, 2,
            3, 3, 3, 3
        ],

        "custo_real_mil": [
            100, 110, 120, 130,
            200, 210, 220, 230,
            300, 320, 340, 360
        ],

        "custo_desvio_pct": [
            0, 5, 10, 15,
            5, 10, 15, 20,
            10, 15, 20, 25
        ],

        "metodologia": [
            "Ágil", "Ágil", "Ágil", "Ágil",
            "Tradicional", "Tradicional", "Tradicional", "Tradicional",
            "Híbrida", "Híbrida", "Híbrida", "Híbrida"
        ],

        "equipe": [
            "Alpha", "Alpha", "Alpha", "Alpha",
            "Beta", "Beta", "Beta", "Beta",
            "Gamma", "Gamma", "Gamma", "Gamma"
        ],

        "num_desenvolvedores": [
            5, 5, 5, 5,
            6, 6, 6, 6,
            7, 7, 7, 7
        ],
    })


def test_experience_vs_bugs(sample_df):
    result = experience_vs_bugs(sample_df)

    assert isinstance(result, dict)
    assert "correlação_exp_x_bugs_total" in result
    assert "correlação_exp_x_bugs_críticos" in result
    assert isinstance(
        result["estatísticas_por_faixa_exp"],
        pd.DataFrame
    )


def test_complexity_vs_delay_with_rank(sample_df):
    result = complexity_vs_delay(sample_df)

    assert "correlação_complexidade_x_atraso" in result
    assert "teste_baixa_vs_muito_alta" in result


def test_complexity_vs_delay_without_rank(sample_df):
    df = sample_df.drop(columns=["complexidade_rank"])

    result = complexity_vs_delay(df)

    assert "correlação_complexidade_x_atraso" not in result


def test_complexity_vs_delay_without_extreme_groups(sample_df):
    df = sample_df[
        sample_df["complexidade"].isin(["Média", "Alta"])
    ].copy()

    result = complexity_vs_delay(df)

    assert "teste_baixa_vs_muito_alta" not in result


def test_rework_vs_satisfaction(sample_df):
    result = rework_vs_satisfaction(sample_df)

    assert isinstance(result, dict)
    assert "correlação_retrabalho_x_satisfacao" in result
    assert isinstance(
        result["satisfacao_por_tercil_retrabalho"],
        pd.DataFrame
    )


def test_overtime_vs_deadline(sample_df):
    result = overtime_vs_deadline(sample_df)

    assert isinstance(result, dict)
    assert "teste_no_prazo_vs_atrasado" in result
    assert isinstance(
        result["horas_extras_por_prazo"],
        pd.DataFrame
    )


def test_size_vs_cost_full(sample_df):
    result = size_vs_cost(sample_df)

    assert "estouro_pct_por_porte" in result
    assert "correlação_porte_x_custo" in result

    assert isinstance(
        result["custo_real_por_porte"],
        pd.DataFrame
    )


def test_size_vs_cost_without_rank(sample_df):
    df = sample_df.drop(columns=["porte_projeto_rank"])

    result = size_vs_cost(df)

    assert "correlação_porte_x_custo" not in result


def test_size_vs_cost_without_deviation(sample_df):
    df = sample_df.drop(columns=["custo_desvio_pct"])

    result = size_vs_cost(df)

    assert result["estouro_pct_por_porte"] is None


def test_methodology_vs_performance(sample_df):
    result = methodology_vs_performance(sample_df)

    assert isinstance(result, dict)

    assert "kpis_por_metodologia" in result
    assert "satisfacao_por_metodologia" in result
    assert "on_time_por_metodologia" in result
    assert "qui_quadrado_metodologia_x_prazo" in result
    assert "kruskal_wallis_satisfacao" in result


def test_team_performance_ranking(sample_df):
    result = team_performance_ranking(sample_df)

    assert isinstance(result, pd.DataFrame)

    assert "score_composto" in result.columns
    assert len(result) == 3
    assert result["score_composto"].is_monotonic_decreasing


def test_team_performance_ranking_equal_scores():
    df = pd.DataFrame({
        "id_projeto": [1, 2, 3],

        "equipe": [
            "Alpha",
            "Beta",
            "Gamma"
        ],

        "satisfacao_cliente": [
            8, 8, 8
        ],

        "entregue_no_prazo": [
            "Sim",
            "Sim",
            "Sim"
        ],

        "bugs_criticos": [
            2, 2, 2
        ],

        "atraso_dias": [
            5, 5, 5
        ]
    })

    result = team_performance_ranking(df)

    assert isinstance(result, pd.DataFrame)

    assert (result["score_composto"] == 0.5).all()