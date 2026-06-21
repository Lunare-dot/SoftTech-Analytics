import numpy as np
import pandas as pd
import pytest

from src.layers.business.kpi_engine import (
    on_time_rate,
    cost_overrun_rate,
    average_delay,
    bug_summary,
    rework_summary,
    kpis_by_group,
    on_time_by_group,
    satisfaction_by_group,
    cost_deviation_series,
    bugs_per_developer,
    overtime_ratio,
    full_kpi_dashboard,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "entregue_no_prazo": [
            "Sim",
            "Não",
            "Sim",
            "Sim"
        ],

        "custo_desvio_mil": [
            10,
            -5,
            0,
            20
        ],

        "custo_desvio_pct": [
            5,
            -2,
            0,
            10
        ],

        "atraso_dias": [
            5,
            -2,
            0,
            10
        ],

        "bugs_total": [
            10,
            5,
            0,
            20
        ],

        "bugs_criticos": [
            2,
            1,
            0,
            5
        ],

        "retrabalho_horas": [
            10,
            5,
            0,
            20
        ],

        "metodologia": [
            "Scrum",
            "Kanban",
            "Scrum",
            "Kanban"
        ],

        "satisfacao_cliente": [
            8,
            6,
            9,
            7
        ],

        "horas_extras": [
            10,
            20,
            0,
            30
        ],

        "duracao_real_dias": [
            5,
            10,
            5,
            15
        ],

        "num_desenvolvedores": [
            2,
            1,
            0,
            4
        ],

        "experiencia_media_anos": [
            5,
            3,
            7,
            4
        ]
    })


# ==========================================================
# on_time_rate
# ==========================================================

def test_on_time_rate(sample_df):
    result = on_time_rate(sample_df)

    assert result["total_projetos"] == 4
    assert result["no_prazo"] == 3
    assert result["com_atraso"] == 1
    assert result["taxa_%"] == 75.0


# ==========================================================
# cost_overrun_rate
# ==========================================================

def test_cost_overrun_rate(sample_df):
    result = cost_overrun_rate(sample_df)

    assert result["total_projetos"] == 4
    assert result["com_estouro"] == 2
    assert result["taxa_%"] == 50.0


# ==========================================================
# average_delay
# ==========================================================

def test_average_delay(sample_df):
    result = average_delay(sample_df)

    assert result["atraso_maximo"] == 10
    assert result["antecipacao_maxima"] == -2
    assert result["projetos_atrasados"] == 2
    assert result["projetos_antecipados"] == 1
    assert result["projetos_exatos"] == 1


# ==========================================================
# bug_summary
# ==========================================================

def test_bug_summary(sample_df):
    result = bug_summary(sample_df)

    assert result["total_bugs_dataset"] == 35
    assert result["total_criticos_dataset"] == 8
    assert result["max_bugs_projeto"] == 20


def test_bug_summary_without_bugs():
    df = pd.DataFrame({
        "bugs_total": [0, 0],
        "bugs_criticos": [0, 0]
    })

    result = bug_summary(df)

    assert result["proporcao_criticos_%"] == 0


# ==========================================================
# rework_summary
# ==========================================================

def test_rework_summary(sample_df):
    result = rework_summary(sample_df)

    assert result["total_horas_retrabalho"] == 35
    assert result["max"] == 20


# ==========================================================
# kpis_by_group
# ==========================================================

def test_kpis_by_group_default_metrics(sample_df):
    result = kpis_by_group(
        sample_df,
        "metodologia"
    )

    assert isinstance(result, pd.DataFrame)
    assert "Scrum" in result.index
    assert "Kanban" in result.index


def test_kpis_by_group_custom_metrics(sample_df):
    result = kpis_by_group(
        sample_df,
        "metodologia",
        metrics=["bugs_total"]
    )

    assert ("bugs_total", "mean") in result.columns


# ==========================================================
# on_time_by_group
# ==========================================================

def test_on_time_by_group(sample_df):
    result = on_time_by_group(
        sample_df,
        "metodologia"
    )

    assert result.loc["Scrum", "total"] == 2
    assert result.loc["Scrum", "taxa_%"] == 100.0


# ==========================================================
# satisfaction_by_group
# ==========================================================

def test_satisfaction_by_group(sample_df):
    result = satisfaction_by_group(
        sample_df,
        "metodologia"
    )

    assert "média" in result.columns
    assert result.loc["Scrum", "média"] == 8.5


# ==========================================================
# cost_deviation_series
# ==========================================================

def test_cost_deviation_series(sample_df):
    result = cost_deviation_series(sample_df)

    assert isinstance(result, pd.Series)
    assert result.name == "custo_desvio_pct"


# ==========================================================
# bugs_per_developer
# ==========================================================

def test_bugs_per_developer(sample_df):
    result = bugs_per_developer(sample_df)

    assert result.name == "bugs_por_dev"
    assert result.iloc[0] == 5


def test_bugs_per_developer_handles_zero_devs(sample_df):
    result = bugs_per_developer(sample_df)

    assert np.isnan(result.iloc[2])


# ==========================================================
# overtime_ratio
# ==========================================================

def test_overtime_ratio(sample_df):
    result = overtime_ratio(sample_df)

    assert result.name == "overtime_ratio"
    assert result.iloc[0] == 2


def test_overtime_ratio_handles_zero_duration():
    df = pd.DataFrame({
        "horas_extras": [10],
        "duracao_real_dias": [0]
    })

    result = overtime_ratio(df)

    assert np.isnan(result.iloc[0])


# ==========================================================
# full_kpi_dashboard
# ==========================================================

def test_full_kpi_dashboard(sample_df):
    result = full_kpi_dashboard(sample_df)

    assert isinstance(result, dict)

    assert "prazo" in result
    assert "custo" in result
    assert "atraso" in result
    assert "bugs" in result
    assert "retrabalho" in result

    assert result["prazo"]["taxa_%"] == 75.0