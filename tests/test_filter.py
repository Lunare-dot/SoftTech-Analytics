import pandas as pd
import pytest

from src.layers.data.filter import (
    filter_by_year,
    filter_by_methodology,
    filter_by_team,
    filter_by_sector,
    filter_by_size,
    filter_by_complexity,
    filter_on_time,
    filter_delayed,
    filter_anticipated,
    filter_by_satisfaction,
    filter_by_team_size,
    filter_by_experience,
    filter_by_cost_overrun,
    filter_high_criticality,
    apply_filters,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "ano_conclusao": [2023, 2024, 2025],
            "metodologia": ["Ágil", "Tradicional", "Híbrida"],
            "equipe": ["Equipe A", "Equipe B", "Equipe C"],
            "setor_cliente": ["Saúde", "Educação", "Finanças"],
            "porte_projeto": ["Pequeno", "Médio", "Grande"],
            "complexidade": ["Baixa", "Média", "Alta"],
            "entregue_no_prazo": ["Sim", "Não", "Sim"],
            "atraso_dias": [0, 10, -5],
            "satisfacao_cliente": [9.0, 6.5, 8.0],
            "num_desenvolvedores": [3, 8, 15],
            "experiencia_media_anos": [2.0, 5.0, 10.0],
            "custo_desvio_pct": [5.0, 25.0, -10.0],
            "bugs_criticos": [1, 7, 12],
        }
    )


def test_filter_by_year(sample_df):
    result = filter_by_year(sample_df, 2024)

    assert len(result) == 1
    assert result.iloc[0]["ano_conclusao"] == 2024


def test_filter_by_year_multiple(sample_df):
    result = filter_by_year(sample_df, [2023, 2025])

    assert len(result) == 2


def test_filter_by_methodology(sample_df):
    result = filter_by_methodology(sample_df, "Ágil")

    assert len(result) == 1
    assert result.iloc[0]["metodologia"] == "Ágil"


def test_filter_by_team(sample_df):
    result = filter_by_team(sample_df, "Equipe B")

    assert len(result) == 1
    assert result.iloc[0]["equipe"] == "Equipe B"


def test_filter_by_sector(sample_df):
    result = filter_by_sector(sample_df, "Saúde")

    assert len(result) == 1


def test_filter_by_size(sample_df):
    result = filter_by_size(sample_df, "Grande")

    assert len(result) == 1


def test_filter_by_complexity(sample_df):
    result = filter_by_complexity(sample_df, "Alta")

    assert len(result) == 1


def test_filter_on_time(sample_df):
    result = filter_on_time(sample_df)

    assert len(result) == 2
    assert (result["entregue_no_prazo"] == "Sim").all()


def test_filter_delayed(sample_df):
    result = filter_delayed(sample_df)

    assert len(result) == 1
    assert result.iloc[0]["entregue_no_prazo"] == "Não"


def test_filter_anticipated(sample_df):
    result = filter_anticipated(sample_df)

    assert len(result) == 1
    assert result.iloc[0]["atraso_dias"] < 0


def test_filter_by_satisfaction(sample_df):
    result = filter_by_satisfaction(sample_df, 8.0, 10.0)

    assert len(result) == 2


def test_filter_by_team_size(sample_df):
    result = filter_by_team_size(sample_df, 5, 20)

    assert len(result) == 2


def test_filter_by_experience(sample_df):
    result = filter_by_experience(sample_df, 4, 12)

    assert len(result) == 2


def test_filter_by_cost_overrun(sample_df):
    result = filter_by_cost_overrun(sample_df, 10)

    assert len(result) == 1
    assert result.iloc[0]["custo_desvio_pct"] == 25.0


def test_filter_by_cost_overrun_missing_column():
    df = pd.DataFrame({"x": [1, 2, 3]})

    with pytest.raises(KeyError):
        filter_by_cost_overrun(df)


def test_filter_high_criticality(sample_df):
    result = filter_high_criticality(sample_df, 5)

    assert len(result) == 2


def test_apply_filters_single(sample_df):
    result = apply_filters(
        sample_df,
        metodologia="Ágil"
    )

    assert len(result) == 1
    assert result.iloc[0]["metodologia"] == "Ágil"


def test_apply_filters_multiple(sample_df):
    result = apply_filters(
        sample_df,
        year=2023,
        metodologia="Ágil",
        on_time=True,
    )

    assert len(result) == 1
    assert result.iloc[0]["ano_conclusao"] == 2023


def test_apply_filters_unknown_filter(sample_df):
    with pytest.raises(ValueError):
        apply_filters(
            sample_df,
            filtro_inexistente="teste"
        )


def test_filters_return_copy(sample_df):
    original = sample_df.copy()

    result = filter_by_year(sample_df, 2024)

    assert sample_df.equals(original)
    assert result is not sample_df


def test_filters_reset_index(sample_df):
    result = filter_by_year(sample_df, 2024)

    assert list(result.index) == [0]