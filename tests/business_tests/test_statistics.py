import warnings

import pandas as pd
import pytest

from src.layers.business.statistics import (
    describe_numeric,
    describe_categorical,
    frequency_table,
    outlier_summary,
    correlation_matrix,
    correlation_test,
    confidence_interval_mean,
    confidence_interval_proportion,
    normality_test,
    ttest_two_groups,
    mann_whitney_test,
    chi_square_test,
    _interpret_correlation,
    _interpret_cramers_v,
)


# ==========================================================
# Fixtures
# ==========================================================

@pytest.fixture
def numeric_df():
    return pd.DataFrame({
        "idade": [20, 25, 30, 35, 40],
        "salario": [2000, 2500, 3000, 3500, 4000],
        "idade_rank": [1, 2, 3, 4, 5],
    })


@pytest.fixture
def categorical_df():
    return pd.DataFrame({
        "metodologia": [
            "Scrum",
            "Kanban",
            "Scrum",
            "XP",
            "Scrum",
        ]
    })


# ==========================================================
# describe_numeric
# ==========================================================

def test_describe_numeric_basic_statistics(numeric_df):
    result = describe_numeric(numeric_df)

    assert "idade" in result.index
    assert "salario" in result.index
    assert "idade_rank" not in result.index

    assert result.loc["idade", "n"] == 5
    assert result.loc["idade", "média"] == 30
    assert result.loc["idade", "mediana"] == 30
    assert result.loc["idade", "mínimo"] == 20
    assert result.loc["idade", "máximo"] == 40
    assert result.loc["idade", "amplitude"] == 20


def test_describe_numeric_missing_values():
    df = pd.DataFrame({
        "idade": [20, None, 30, None, 40]
    })

    result = describe_numeric(df)

    assert result.loc["idade", "n"] == 3
    assert result.loc["idade", "ausentes"] == 2
    assert result.loc["idade", "média"] == 30


def test_describe_numeric_selected_columns(numeric_df):
    result = describe_numeric(numeric_df, cols=["salario"])

    assert list(result.index) == ["salario"]


# ==========================================================
# describe_categorical
# ==========================================================

def test_describe_categorical_frequencies(categorical_df):
    result = describe_categorical(categorical_df, "metodologia")

    assert result.loc["Scrum", "frequência"] == 3
    assert result.loc["Kanban", "frequência"] == 1
    assert result.loc["XP", "frequência"] == 1

    assert result["freq_relativa_%"].sum() == pytest.approx(100.0)


# ==========================================================
# frequency_table
# ==========================================================

def test_frequency_table_returns_dictionary(categorical_df):
    result = frequency_table(categorical_df, ["metodologia"])

    assert isinstance(result, dict)
    assert "metodologia" in result
    assert isinstance(result["metodologia"], pd.DataFrame)


# ==========================================================
# outlier_summary
# ==========================================================

def test_outlier_summary_iqr_detects_outlier():
    df = pd.DataFrame({
        "valor": [10, 11, 12, 13, 14, 15, 100]
    })

    result = outlier_summary(df)

    assert result.loc["valor", "n_outliers"] == 1


def test_outlier_summary_zscore_detects_outlier():
    df = pd.DataFrame({
        "valor": [10] * 20 + [1000]
    })

    result = outlier_summary(
        df,
        method="zscore",
        zscore_threshold=2
    )

    assert result.loc["valor", "n_outliers"] == 1


# ==========================================================
# correlation_matrix
# ==========================================================

def test_correlation_matrix_perfect_correlation():
    df = pd.DataFrame({
        "x": [1, 2, 3, 4, 5],
        "y": [2, 4, 6, 8, 10],
    })

    result = correlation_matrix(df)

    assert result.shape == (2, 2)
    assert result.loc["x", "x"] == 1
    assert result.loc["y", "y"] == 1
    assert result.loc["x", "y"] == pytest.approx(1.0)


# ==========================================================
# correlation_test
# ==========================================================

def test_correlation_test_pearson():
    s1 = pd.Series([1, 2, 3, 4, 5])
    s2 = pd.Series([2, 4, 6, 8, 10])

    result = correlation_test(
        s1,
        s2,
        method="pearson"
    )

    assert result["coeficiente"] == pytest.approx(1.0)
    assert result["significativo"]

# ==========================================================
# confidence_interval_mean
# ==========================================================

def test_confidence_interval_mean():
    s = pd.Series(
        [10, 11, 12, 13, 14],
        name="idade"
    )

    result = confidence_interval_mean(s)

    assert result["n"] == 5
    assert result["média"] == 12

    assert result["ic_inferior"] < result["média"]
    assert result["ic_superior"] > result["média"]


# ==========================================================
# confidence_interval_proportion
# ==========================================================

def test_confidence_interval_proportion():
    s = pd.Series(
        ["Sim", "Sim", "Não", "Sim", "Não"],
        name="prazo"
    )

    result = confidence_interval_proportion(
        s,
        positive_value="Sim"
    )

    assert result["sucessos"] == 3
    assert result["proporção"] == pytest.approx(0.6)

    assert 0 <= result["ic_inferior"] <= 1
    assert 0 <= result["ic_superior"] <= 1


# ==========================================================
# normality_test
# ==========================================================

def test_normality_test_uses_shapiro_for_small_samples():
    s = pd.Series(
        [1, 2, 3, 4, 5],
        name="teste"
    )

    result = normality_test(s)

    assert result["teste"] == "Shapiro-Wilk"


def test_normality_test_uses_ks_for_large_samples():
    s = pd.Series(range(100), name="teste")

    result = normality_test(s)

    assert result["teste"] == "Kolmogorov-Smirnov"


# ==========================================================
# ttest_two_groups
# ==========================================================

def test_ttest_two_groups_detects_difference():
    df = pd.DataFrame({
        "grupo": ["A"] * 20 + ["B"] * 20,
        "valor":
            [9, 10, 11, 10, 9,
             11, 10, 9, 10, 11,
             10, 9, 11, 10, 9,
             10, 11, 10, 9, 10] +
            [29, 30, 31, 30, 29,
             31, 30, 29, 30, 31,
             30, 29, 31, 30, 29,
             30, 31, 30, 29, 30]
    })

    result = ttest_two_groups(
        df,
        metric_col="valor",
        group_col="grupo",
        group_a="A",
        group_b="B"
    )

    assert result["rejeita_H₀"]


# ==========================================================
# mann_whitney_test
# ==========================================================

def test_mann_whitney_detects_difference():
    df = pd.DataFrame({
        "grupo": ["A"] * 10 + ["B"] * 10,
        "valor":
            list(range(1, 11)) +
            list(range(100, 110))
    })

    result = mann_whitney_test(
        df,
        metric_col="valor",
        group_col="grupo",
        group_a="A",
        group_b="B"
    )

    assert result["rejeita_H₀"]


# ==========================================================
# chi_square_test
# ==========================================================

def test_chi_square_detects_association():
    df = pd.DataFrame({
        "metodologia":
            ["Scrum"] * 20 +
            ["Kanban"] * 20,
        "prazo":
            ["Sim"] * 18 +
            ["Não"] * 2 +
            ["Sim"] * 5 +
            ["Não"] * 15
    })

    result = chi_square_test(
        df,
        "metodologia",
        "prazo"
    )

    assert result["rejeita_H₀"]


def test_chi_square_emits_warning_for_low_expected_frequency():
    df = pd.DataFrame({
        "A": ["X", "X", "Y"],
        "B": ["1", "2", "2"]
    })

    with pytest.warns(UserWarning):
        chi_square_test(df, "A", "B")


# ==========================================================
# _interpret_correlation
# ==========================================================

@pytest.mark.parametrize(
    ("r", "texto"),
    [
        (0.10, "muito fraca"),
        (0.30, "fraca"),
        (0.50, "moderada"),
        (0.70, "forte"),
        (0.90, "muito forte"),
    ]
)
def test_interpret_correlation(r, texto):
    assert texto in _interpret_correlation(r)


def test_interpret_correlation_negative():
    texto = _interpret_correlation(-0.8)

    assert "negativa" in texto
    assert "muito forte" in texto


# ==========================================================
# _interpret_cramers_v
# ==========================================================

@pytest.mark.parametrize(
    ("v", "esperado"),
    [
        (0.05, "associação desprezível"),
        (0.15, "associação fraca"),
        (0.30, "associação moderada"),
        (0.50, "associação forte"),
        (0.80, "associação muito forte"),
    ]
)
def test_interpret_cramers_v(v, esperado):
    assert _interpret_cramers_v(v) == esperado