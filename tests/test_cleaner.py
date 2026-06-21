import pandas as pd
import pytest

from pandas.api.types import is_string_dtype

from src.layers.data.cleaner import (
    cast_dtypes,
    standardize_categoricals,
    encode_ordinals,
    validate_ranges,
    derive_columns,
    clean,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "id_projeto": ["1", "2"],
            "ano_conclusao": ["2024", "2025"],
            "num_desenvolvedores": ["5", "8"],
            "duracao_planejada_dias": ["100", "120"],
            "duracao_real_dias": ["110", "125"],
            "atraso_dias": ["10", "5"],
            "mudancas_requisitos": ["3", "4"],
            "bugs_total": ["20", "10"],
            "bugs_criticos": ["2", "1"],
            "experiencia_media_anos": ["3.5", "7.2"],
            "horas_extras": ["12.5", "8.0"],
            "tempo_medio_correcao_horas": ["4.0", "6.0"],
            "retrabalho_horas": ["15.0", "20.0"],
            "custo_estimado_mil": ["100.0", "150.0"],
            "custo_real_mil": ["120.0", "140.0"],
            "satisfacao_cliente": ["8.5", "9.1"],
            "setor_cliente": ["  tecnologia  ", "saúde"],
            "metodologia": ["agil", "tradicional"],
            "equipe": ["  equipe alpha ", "equipe beta"],
            "entregue_no_prazo": ["nao", "sim"],
            "porte_projeto": ["pequeno", "médio"],
            "complexidade": ["baixa", "muito alta"],
        }
    )


def test_cast_dtypes_converte_tipos_corretamente(sample_df):
    df = cast_dtypes(sample_df)

    assert str(df["id_projeto"].dtype) == "Int64"
    assert str(df["ano_conclusao"].dtype) == "Int64"
    assert str(df["num_desenvolvedores"].dtype) == "Int64"
    assert str(df["experiencia_media_anos"].dtype) == "float64"
    assert str(df["custo_real_mil"].dtype) == "float64"
    assert is_string_dtype(df["setor_cliente"])
    assert is_string_dtype(df["porte_projeto"])


def test_standardize_categoricals_padroniza_textos(sample_df):
    df = cast_dtypes(sample_df)
    df = standardize_categoricals(df)

    assert df.loc[0, "setor_cliente"] == "Tecnologia"
    assert df.loc[1, "setor_cliente"] == "Saúde"
    assert df.loc[0, "metodologia"] == "Ágil"
    assert df.loc[1, "metodologia"] == "Tradicional"
    assert df.loc[0, "equipe"] == "Equipe Alpha"
    assert df.loc[1, "equipe"] == "Equipe Beta"
    assert df.loc[0, "entregue_no_prazo"] == "Não"
    assert df.loc[1, "entregue_no_prazo"] == "Sim"
    assert df.loc[0, "porte_projeto"] == "Pequeno"
    assert df.loc[1, "complexidade"] == "Muito alta"


def test_encode_ordinals_cria_colunas_rank_e_categoricas_ordenadas(sample_df):
    df = cast_dtypes(sample_df)
    df = standardize_categoricals(df)
    df = encode_ordinals(df)

    assert "porte_projeto_rank" in df.columns
    assert "complexidade_rank" in df.columns

    assert list(df["porte_projeto_rank"]) == [1, 2]
    assert list(df["complexidade_rank"]) == [1, 4]

    assert str(df["porte_projeto"].dtype) == "category"
    assert str(df["complexidade"].dtype) == "category"
    assert df["porte_projeto"].cat.ordered is True
    assert df["complexidade"].cat.ordered is True


def test_validate_ranges_emite_warning_quando_fora_do_intervalo():
    df = pd.DataFrame(
        {
            "satisfacao_cliente": [8.0, 11.5],
            "num_desenvolvedores": [3, 60],
            "experiencia_media_anos": [2.0, 41.0],
            "duracao_planejada_dias": [100, 0],
            "duracao_real_dias": [120, 2000],
            "bugs_criticos": [0, -1],
            "custo_estimado_mil": [100.0, -5.0],
            "custo_real_mil": [120.0, -10.0],
            "retrabalho_horas": [5.0, -2.0],
            "horas_extras": [3.0, -1.0],
        }
    )

    with pytest.warns(UserWarning):
        validate_ranges(df)


def test_validate_ranges_raise_on_error_lanca_value_error():
    df = pd.DataFrame(
        {
            "satisfacao_cliente": [11.5],
        }
    )

    with pytest.raises(ValueError, match="satisfacao_cliente"):
        validate_ranges(df, raise_on_error=True)


def test_derive_columns_cria_colunas_calculadas(sample_df):
    df = cast_dtypes(sample_df)
    df = standardize_categoricals(df)
    df = encode_ordinals(df)
    df = derive_columns(df)

    assert "custo_desvio_mil" in df.columns
    assert "custo_desvio_pct" in df.columns
    assert "atraso_flag" in df.columns
    assert "proporcao_bugs_criticos" in df.columns
    assert "retrabalho_por_dia" in df.columns

    assert df.loc[0, "custo_desvio_mil"] == 20.0
    assert df.loc[0, "custo_desvio_pct"] == 20.0
    assert bool(df.loc[0, "atraso_flag"]) is True
    assert df.loc[0, "proporcao_bugs_criticos"] == 0.1
    assert df.loc[0, "retrabalho_por_dia"] == 15.0 / 110.0


def test_clean_executa_pipeline_completa(sample_df):
    df = clean(sample_df)

    assert str(df["id_projeto"].dtype) == "Int64"
    assert df.loc[0, "setor_cliente"] == "Tecnologia"
    assert "porte_projeto_rank" in df.columns
    assert "complexidade_rank" in df.columns
    assert "custo_desvio_mil" in df.columns
    assert "custo_desvio_pct" in df.columns
    assert "atraso_flag" in df.columns
    assert "proporcao_bugs_criticos" in df.columns
    assert "retrabalho_por_dia" in df.columns

    assert list(df["porte_projeto_rank"]) == [1, 2]
    assert list(df["complexidade_rank"]) == [1, 4]