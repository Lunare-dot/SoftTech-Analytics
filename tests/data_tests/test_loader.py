# tests/test_loader.py

from pathlib import Path

import pandas as pd
import pytest

from src.layers.data.loader import (
    load_raw_data,
    load_dictionary,
    _SHEET_DATA,
    _SHEET_DICT
)


def test_load_raw_data_returns_dataframe():
    """
    Deve retornar um DataFrame válido ao ler a sheet Dados_Brutos.
    """
    df = load_raw_data()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_load_dictionary_returns_dataframe():
    """
    Deve retornar um DataFrame válido ao ler a sheet Dicionario.
    """
    df = load_dictionary()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_load_raw_data_file_not_found():
    """
    Deve lançar FileNotFoundError quando o arquivo não existir.
    """
    with pytest.raises(FileNotFoundError):
        load_raw_data("arquivo_inexistente.xlsx")


def test_load_dictionary_file_not_found():
    """
    Deve lançar FileNotFoundError quando o arquivo não existir.
    """
    with pytest.raises(FileNotFoundError):
        load_dictionary("arquivo_inexistente.xlsx")


def test_load_raw_data_invalid_sheet(tmp_path):
    """
    Deve lançar ValueError quando a sheet Dados_Brutos não existir.
    """
    fake_file = tmp_path / "teste.xlsx"

    with pd.ExcelWriter(fake_file, engine="openpyxl") as writer:
        pd.DataFrame({"A": [1, 2, 3]}).to_excel(
            writer,
            sheet_name="OutraSheet",
            index=False
        )

    with pytest.raises(ValueError, match=f"{_SHEET_DATA}"):
        load_raw_data(fake_file)


def test_load_dictionary_invalid_sheet(tmp_path):
    """
    Deve lançar ValueError quando a sheet Dicionario não existir.
    """
    fake_file = tmp_path / "teste.xlsx"

    with pd.ExcelWriter(fake_file, engine="openpyxl") as writer:
        pd.DataFrame({"A": [1, 2, 3]}).to_excel(
            writer,
            sheet_name="OutraSheet",
            index=False
        )

    with pytest.raises(ValueError, match=f"{_SHEET_DICT}"):
        load_dictionary(fake_file)


def test_load_raw_data_removes_empty_rows(tmp_path):
    """
    Deve remover linhas completamente vazias.
    """
    fake_file = tmp_path / "teste.xlsx"

    df_original = pd.DataFrame(
        {
            "A": [1, None, 3],
            "B": [10, None, 30]
        }
    )

    with pd.ExcelWriter(fake_file, engine="openpyxl") as writer:
        df_original.to_excel(
            writer,
            sheet_name=_SHEET_DATA,
            index=False
        )

    df = load_raw_data(fake_file)

    assert len(df) == 2
    assert df.isna().all(axis=1).sum() == 0


def test_load_dictionary_removes_empty_rows(tmp_path):
    """
    Deve remover linhas completamente vazias.
    """
    fake_file = tmp_path / "teste.xlsx"

    df_original = pd.DataFrame(
        {
            "A": [1, None, 3],
            "B": [10, None, 30]
        }
    )

    with pd.ExcelWriter(fake_file, engine="openpyxl") as writer:
        df_original.to_excel(
            writer,
            sheet_name=_SHEET_DICT,
            index=False
        )

    df = load_dictionary(fake_file)

    assert len(df) == 2
    assert df.isna().all(axis=1).sum() == 0