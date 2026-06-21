"""
data/cleaner.py
===============
Pipeline de limpeza em sequência: 
cast_dtypes -> standardize_categoricals -> encode_ordinals -> validate_ranges -> derive_columns
"""

import warnings
from typing import Final
import pandas as pd

# Define as colunas que devem ser tratadas como números inteiros, sem converter para float
_INT_COLS: Final[list[str]] = [
    "id_projeto", "ano_conclusao", "num_desenvolvedores",
    "duracao_planejada_dias", "duracao_real_dias", "atraso_dias",
    "mudancas_requisitos", "bugs_total", "bugs_criticos",
]

# Define as colunas que devem ser tratadas como números decimais contínuos (float)
_FLOAT_COLS: Final[list[str]] = [
    "experiencia_media_anos", "horas_extras", "tempo_medio_correcao_horas",
    "retrabalho_horas", "custo_estimado_mil", "custo_real_mil", "satisfacao_cliente",
]

# Define as colunas de texto categóricas nominais
_NOMINAL_COLS: Final[list[str]] = [
    "setor_cliente", "metodologia", "equipe", "entregue_no_prazo",
]

# Define o peso de grandeza para as colunas ordinais e ajuda na ordenação futura
_ORDINAL_MAPS: Final[dict[str, dict]] = {
    "porte_projeto": {"Pequeno": 1, "Médio": 2, "Grande": 3},
    "complexidade": {"Baixa": 1, "Média": 2, "Alta": 3, "Muito alta": 4},
}

# Define os limites de valores permitidos para a auditoria de erros (min, max)
_RANGE_CHECKS: Final[dict[str, tuple]] = {
    "satisfacao_cliente":       (0.0, 10.0),
    "num_desenvolvedores":      (1,   50),
    "experiencia_media_anos":   (0.0, 40.0),
    "duracao_planejada_dias":   (1,   1000),
    "duracao_real_dias":        (1,   1000),
    "bugs_criticos":            (0,   None),
    "custo_estimado_mil":       (0.0, None),
    "custo_real_mil":           (0.0, None),
    "retrabalho_horas":         (0.0, None),
    "horas_extras":             (0.0, None),
}

def cast_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    # Retorna uma cópia do dataframe com os tipos de dados convertidos de acordo com o dicionário
    # Utiliza 'Int64' em vez de int clássico pois aceita células vazias sem forçar erro ou virar float
    df = df.copy()

    for col in _INT_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    for col in _FLOAT_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")

    for col in _NOMINAL_COLS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Mantém os valores ordinais como strings cruas temporariamente para tratamento na próxima função
    for col in _ORDINAL_MAPS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df


def standardize_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    # Retorna o dataframe garantindo que strings categóricas tenham a mesma formatação textual
    # Impede, por exemplo, que "Agil" e "ágil" sejam interpretadas como duas coisas diferentes
    df = df.copy()
    all_cat_cols = _NOMINAL_COLS + list(_ORDINAL_MAPS.keys())

    # Dicionário interno para forçar substituições manuais de erros comuns de digitação na base
    _explicit_maps: dict[str, dict[str, str]] = {
        "metodologia": {"agil": "Ágil", "ágil": "Ágil", "tradicional": "Tradicional", "hibrida": "Híbrida", "híbrida": "Híbrida"},
        "porte_projeto": {"pequeno": "Pequeno", "medio": "Médio", "médio": "Médio", "grande": "Grande"},
        "complexidade": {"baixa": "Baixa", "media": "Média", "média": "Média", "alta": "Alta", "muito alta": "Muito alta"},
        "entregue_no_prazo": {"sim": "Sim", "nao": "Não", "não": "Não", "s": "Sim", "n": "Não"},
    }

    for col in all_cat_cols:
        if col not in df.columns:
            continue
        
        df[col] = df[col].str.strip()

        # Varre a coluna e aplica o dicionário de correção interno caso o valor escrito conste lá
        if col in _explicit_maps:
            mapping = _explicit_maps[col]
            df[col] = df[col].apply(lambda v: mapping.get(str(v).lower(), v) if pd.notna(v) else v)

    # Padroniza as colunas de setores e equipes para a primeira letra sempre maiúscula
    for col in ["equipe", "setor_cliente"]:
        if col in df.columns:
            df[col] = df[col].str.title()

    return df


def encode_ordinals(df: pd.DataFrame) -> pd.DataFrame:
    # Cria uma nova coluna "_rank" numérica ao lado de cada coluna categórica ordinal (ex: Baixa vira 1, Alta vira 3)
    # Isso vai nos permitir calcular correlação estatística com essas variáveis sem perder o texto original
    df = df.copy()

    for col, mapping in _ORDINAL_MAPS.items():
        if col not in df.columns:
            continue

        rank_col = f"{col}_rank"
        df[rank_col] = df[col].map(mapping)
        ordered_cats = sorted(mapping, key=mapping.get)
        
        # Avisa o Pandas que aquela coluna de texto não é livre e possui uma hierarquia de peso lógico
        df[col] = pd.Categorical(df[col], categories=ordered_cats, ordered=True)

    return df


def validate_ranges(df: pd.DataFrame, raise_on_error: bool = False) -> pd.DataFrame:
    # Confere se algum número na base de dados viola o limite lógico que determinamos (ex: dias negativos)
    # Se raise_on_error for True, para o programa se achar erro. Do contrário, apenas joga um aviso na tela e segue
    for col, (vmin, vmax) in _RANGE_CHECKS.items():
        if col not in df.columns:
            continue

        series = df[col].dropna()

        # Valida infração no piso
        if vmin is not None:
            violators = series[series < vmin]
            if not violators.empty:
                msg = f"[validate_ranges] '{col}': {len(violators)} valor(es) abaixo do mínimo ({vmin})."
                if raise_on_error:
                    raise ValueError(msg)
                warnings.warn(msg, stacklevel=2)

        # Valida infração no teto
        if vmax is not None:
            violators = series[series > vmax]
            if not violators.empty:
                msg = f"[validate_ranges] '{col}': {len(violators)} valor(es) acima do máximo ({vmax})."
                if raise_on_error:
                    raise ValueError(msg)
                warnings.warn(msg, stacklevel=2)

    return df


def derive_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Cria colunas calculadas úteis para agilizar as métricas que precisaremos construir depois na camada de negócios
    df = df.copy()

    df["custo_desvio_mil"] = df["custo_real_mil"] - df["custo_estimado_mil"]
    df["custo_desvio_pct"] = (df["custo_desvio_mil"] / df["custo_estimado_mil"].replace(0, pd.NA) * 100)
    
    # Retorna uma coluna tipo booleano True ou False
    df["atraso_flag"] = df["atraso_dias"] > 0
    df["proporcao_bugs_criticos"] = df.apply(lambda r: r["bugs_criticos"] / r["bugs_total"] if r["bugs_total"] > 0 else 0.0, axis=1)
    df["retrabalho_por_dia"] = (df["retrabalho_horas"] / df["duracao_real_dias"].replace(0, pd.NA))

    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    # Agrupa e roda sequencialmente todas as transformações de limpeza em um comando único
    df = cast_dtypes(df)
    df = standardize_categoricals(df)
    df = encode_ordinals(df)
    df = validate_ranges(df)
    df = derive_columns(df)
    
    # Caso futuras etapas removam linhas
    # Considerar df.reset_index(drop=True) antes do retorno
    return df