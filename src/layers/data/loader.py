# Responsável exclusivamente por ler o arquivo Excel e retornar o DataFrame
# cru da planilha Dados_Brutos e Dicionario, sem qualquer transformação

from pathlib import Path
import pandas as pd

# Caminho padrão para o arquivo bruto
DEFAULT_PATH = Path(__file__).resolve().parent.parent.parent / "docs" / "Dados_Brutos_estatistica_estudo_caso.xlsx"

# Atribuição de variáveis para cada sheet
_SHEET_DATA = "Dados_Brutos"
_SHEET_DICT = "Dicionario"

def load_raw_data(filepath: str | Path = DEFAULT_PATH) -> pd.DataFrame:
    # Lê a sheet Dados_Brutos e retorna um DataFrame sem nenhum tratamento
    # Retorna FileNotFound error se o arquivo não existir no caminho informado
    # Retorna ValueError se a sheet Dados_Brutos não for encontrada no arquivo
    
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    
    try:
        df = pd.read_excel(
            filepath,
            sheet_name=_SHEET_DATA,
            engine="openpyxl",
            header=0
            )
    except Exception as exc:
        raise ValueError(
            f"Não foi possível ler a sheet '{_SHEET_DATA}': '{exc}'"
        ) from exc
        
    return df.dropna(how="all").reset_index(drop=True) 
    # Remove linhas completamente vazias que às vezes o Excel insere no final
    # Retorna a sheet Dados_Brutos como um DataFrame


def load_dictionary(filepath: str | Path = DEFAULT_PATH) -> pd.DataFrame:
    # Lê a sheet Dicionario e retorna um DataFrame sem nenhum tratamento
    # Retorna FileNotFound error se o arquivo não existir no caminho informado
    # Retorna ValueError se a sheet Dicionaro não for encontrada no arquivo
    
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    
    try:
        df = pd.read_excel(
            filepath,
            sheet_name=_SHEET_DICT,
            engine="openpyxl",
            header=0
        )
    except Exception as exc:
        raise ValueError(
            f"Não foi possível ler a sheet '{_SHEET_DICT}': '{exc}'"
        ) from exc
        
    return df.dropna(how="all").reset_index(drop=True) 
    # Remove linhas completamente vazias que às vezes o Excel insere no final
    # Retorna a sheet Dicionario como um DataFrame