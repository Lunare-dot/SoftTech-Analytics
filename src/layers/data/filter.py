# data/filter.py
# Funções de filtragem que retornam cópias do DataFrame limpo, sem alterar o original.
# Podem receber uma única string ou uma lista de opções para facilitar o uso no Streamlit.

from typing import Union
import pandas as pd

# Tipo auxiliar para indicar que a função aceita tanto um valor único quanto uma lista
_StrOrList = Union[str, list[str]]

def _to_list(value: _StrOrList) -> list:
    # Transforma o input em lista caso seja apenas uma string, facilitando o uso do df.isin()
    return [value] if isinstance(value, str) else list(value)


def filter_by_year(df: pd.DataFrame, year: Union[int, list[int]]) -> pd.DataFrame:
    # Retorna apenas os projetos concluídos no(s) ano(s) informado(s)
    years = [year] if isinstance(year, int) else list(year)
    return df[df["ano_conclusao"].isin(years)].reset_index(drop=True)

def filter_by_methodology(df: pd.DataFrame, metodologia: _StrOrList) -> pd.DataFrame:
    # Filtra os projetos pela metodologia utilizada ("Ágil", "Tradicional", "Híbrida")
    return df[df["metodologia"].isin(_to_list(metodologia))].reset_index(drop=True)

def filter_by_team(df: pd.DataFrame, equipe: _StrOrList) -> pd.DataFrame:
    # Retorna apenas os projetos de uma ou mais equipes específicas
    return df[df["equipe"].isin(_to_list(equipe))].reset_index(drop=True)

def filter_by_sector(df: pd.DataFrame, setor: _StrOrList) -> pd.DataFrame:
    # Filtra pelo setor de atuação do cliente ("Educação", "Saúde", "Finanças", etc.)
    return df[df["setor_cliente"].isin(_to_list(setor))].reset_index(drop=True)

def filter_by_size(df: pd.DataFrame, porte: _StrOrList) -> pd.DataFrame:
    # Retorna os projetos filtrados pelo porte ("Pequeno", "Médio", "Grande")
    return df[df["porte_projeto"].isin(_to_list(porte))].reset_index(drop=True)

def filter_by_complexity(df: pd.DataFrame, complexidade: _StrOrList) -> pd.DataFrame:
    # Filtra de acordo com a complexidade técnica do projeto
    return df[df["complexidade"].isin(_to_list(complexidade))].reset_index(drop=True)


def filter_on_time(df: pd.DataFrame) -> pd.DataFrame:
    # Retorna estritamente os projetos que a empresa marcou como entregues no prazo
    return df[df["entregue_no_prazo"] == "Sim"].reset_index(drop=True)

def filter_delayed(df: pd.DataFrame) -> pd.DataFrame:
    # Retorna estritamente os projetos que a empresa marcou como NÃO entregues no prazo
    return df[df["entregue_no_prazo"] == "Não"].reset_index(drop=True)

def filter_anticipated(df: pd.DataFrame) -> pd.DataFrame:
    # Retorna apenas projetos que terminaram antes do prazo estipulado (dias de atraso negativos)
    return df[df["atraso_dias"] < 0].reset_index(drop=True)


def filter_by_satisfaction(df: pd.DataFrame, min_score: float = 0.0, max_score: float = 10.0) -> pd.DataFrame:
    # Retorna os projetos cuja nota de satisfação está dentro do intervalo estabelecido
    mask = (df["satisfacao_cliente"] >= min_score) & (df["satisfacao_cliente"] <= max_score)
    return df[mask].reset_index(drop=True)

def filter_by_team_size(df: pd.DataFrame, min_devs: int = 1, max_devs: int = 999) -> pd.DataFrame:
    # Filtra pela quantidade de desenvolvedores alocados na equipe
    mask = (df["num_desenvolvedores"] >= min_devs) & (df["num_desenvolvedores"] <= max_devs)
    return df[mask].reset_index(drop=True)

def filter_by_experience(df: pd.DataFrame, min_years: float = 0.0, max_years: float = 999.0) -> pd.DataFrame:
    # Filtra pela experiência média (em anos) da equipe
    mask = (df["experiencia_media_anos"] >= min_years) & (df["experiencia_media_anos"] <= max_years)
    return df[mask].reset_index(drop=True)

def filter_by_cost_overrun(df: pd.DataFrame, min_pct: float = 0.0) -> pd.DataFrame:
    # Retorna projetos que estouraram o orçamento acima de um percentual específico
    # Exige que a coluna 'custo_desvio_pct' já tenha sido gerada no cleaner.py
    if "custo_desvio_pct" not in df.columns:
        raise KeyError("Coluna 'custo_desvio_pct' não encontrada. Rode cleaner.derive_columns() antes.")
    return df[df["custo_desvio_pct"] > min_pct].reset_index(drop=True)

def filter_high_criticality(df: pd.DataFrame, min_critical_bugs: int = 5) -> pd.DataFrame:
    # Filtra projetos que tiveram um número de bugs críticos igual ou maior que o limite informado
    return df[df["bugs_criticos"] >= min_critical_bugs].reset_index(drop=True)


def apply_filters(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    # Função utilitária para o Streamlit: aplica múltiplos filtros de uma só vez passando os argumentos juntos
    _dispatch = {
        "year":         filter_by_year,
        "metodologia":  filter_by_methodology,
        "equipe":       filter_by_team,
        "setor":        filter_by_sector,
        "porte":        filter_by_size,
        "complexidade": filter_by_complexity,
    }

    for key, value in kwargs.items():
        if key == "on_time":
            if value:
                df = filter_on_time(df)
        elif key in _dispatch:
            df = _dispatch[key](df, value)
        else:
            raise ValueError(f"Filtro desconhecido: '{key}'")

    return df