# business/statistics.py
# Centraliza toda a matemática pesada do projeto (descritiva, intervalos de confiança e testes de hipótese)
# Todas as funções recebem dados já limpos e retornam dicionários formatados, prontos para a interface visual.

import warnings
from typing import Literal
import numpy as np
import pandas as pd
from scipy import stats

def describe_numeric(df: pd.DataFrame, cols: list[str] | None = None) -> pd.DataFrame:
    # Gera estatísticas completas para colunas numéricas (média, mediana, desvio padrão, quartis, etc.)
    if cols is None:
        cols = df.select_dtypes(include="number").columns.tolist()
        cols = [c for c in cols if not c.endswith("_rank")]

    result = {}
    for col in cols:
        s = df[col].dropna()
        result[col] = {
            "n":           len(s),
            "ausentes":    df[col].isna().sum(),
            "média":       s.mean(),
            "mediana":     s.median(),
            "desvio_pad":  s.std(ddof=1),
            "CV_%":        (s.std(ddof=1) / s.mean() * 100) if s.mean() != 0 else np.nan,
            "mínimo":      s.min(),
            "Q1":          s.quantile(0.25),
            "Q3":          s.quantile(0.75),
            "máximo":      s.max(),
            "amplitude":   s.max() - s.min(),
            "IQR":         s.quantile(0.75) - s.quantile(0.25),
            "assimetria":  s.skew(),
            "curtose":     s.kurt(),
        }
    return pd.DataFrame(result).T.round(4)


def describe_categorical(df: pd.DataFrame, col: str) -> pd.DataFrame:
    # Cria uma tabela de frequência absoluta e relativa para textos (ex: Quantos projetos Ágeis, Tradicionais, etc.)
    counts = df[col].value_counts(dropna=False)
    total = counts.sum()

    result = pd.DataFrame({
        "frequência":      counts,
        "freq_relativa_%": (counts / total * 100).round(2),
    })
    result["freq_acumulada_%"] = result["freq_relativa_%"].cumsum().round(2)
    result.index.name = col
    return result


def frequency_table(df: pd.DataFrame, cols: list[str]) -> dict[str, pd.DataFrame]:
    # Aplica a describe_categorical em várias colunas de uma só vez
    return {col: describe_categorical(df, col) for col in cols}


def outlier_summary(df: pd.DataFrame, cols: list[str] | None = None, method: Literal["iqr", "zscore"] = "iqr", zscore_threshold: float = 3.0) -> pd.DataFrame:
    # Identifica pontos fora da curva usando o método IQR (Boxplot) ou Z-Score
    if cols is None:
        cols = df.select_dtypes(include="number").columns.tolist()
        cols = [c for c in cols if not c.endswith("_rank")]

    rows = []
    for col in cols:
        s = df[col].dropna()
        if method == "iqr":
            q1, q3 = s.quantile(0.25), s.quantile(0.75)
            iqr = q3 - q1
            mask = (s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)
        else:
            z = np.abs(stats.zscore(s))
            mask = z > zscore_threshold

        n_out = mask.sum()
        rows.append({
            "variável":        col,
            "n_outliers":      n_out,
            "outliers_%":      round(n_out / len(s) * 100, 2),
            "limite_inferior": round(s.quantile(0.25) - 1.5 * (s.quantile(0.75) - s.quantile(0.25)), 4) if method == "iqr" else None,
            "limite_superior": round(s.quantile(0.75) + 1.5 * (s.quantile(0.75) - s.quantile(0.25)), 4) if method == "iqr" else None,
        })
    return pd.DataFrame(rows).set_index("variável")


def correlation_matrix(df: pd.DataFrame, cols: list[str] | None = None, method: Literal["pearson", "spearman", "kendall"] = "pearson") -> pd.DataFrame:
    # Cruza todas as variáveis numéricas para ver quem cresce junto com quem (Correlação)
    if cols is None:
        cols = df.select_dtypes(include="number").columns.tolist()
        cols = [c for c in cols if not c.endswith("_rank")]
    return df[cols].corr(method=method).round(4)


def correlation_test(series1: pd.Series, series2: pd.Series, method: Literal["pearson", "spearman"] = "spearman") -> dict:
    # Testa matematicamente se a correlação entre duas variáveis é verdadeira ou se foi pura sorte (P-Valor)
    s1, s2 = series1.dropna(), series2.dropna()
    idx = s1.index.intersection(s2.index)
    s1, s2 = s1[idx], s2[idx]

    if method == "pearson":
        coef, p = stats.pearsonr(s1, s2)
    else:
        coef, p = stats.spearmanr(s1, s2)

    return {
        "método":        method,
        "coeficiente":   round(coef, 4),
        "p_valor":       round(p, 6),
        "significativo": p < 0.05,
        "interpretação": _interpret_correlation(coef),
    }

def _interpret_correlation(r: float) -> str:
    # Traduz o número matemático da correlação para um texto humano no relatório
    abs_r = abs(r)
    direction = "positiva" if r >= 0 else "negativa"
    if abs_r < 0.20:
        strength = "muito fraca"
    elif abs_r < 0.40:
        strength = "fraca"
    elif abs_r < 0.60:
        strength = "moderada"
    elif abs_r < 0.80:
        strength = "forte"
    else:
        strength = "muito forte"
    return f"correlação {direction} {strength} (r = {r:.4f})"


def confidence_interval_mean(series: pd.Series, confidence: float = 0.95) -> dict:
    # Constrói o IC para prever entre quais valores a média verdadeira da SoftTech se encontra
    s = series.dropna()
    n = len(s)
    mean = s.mean()
    se = stats.sem(s) 

    alpha = 1 - confidence
    t_crit = stats.t.ppf(1 - alpha / 2, df=n - 1)
    margin = t_crit * se

    return {
        "variável":        series.name,
        "n":               n,
        "média":           round(mean, 4),
        "erro_padrão":     round(se, 4),
        "margem_erro":     round(margin, 4),
        "ic_inferior":     round(mean - margin, 4),
        "ic_superior":     round(mean + margin, 4),
        "nível_confiança": f"{int(confidence * 100)}%",
    }

def confidence_interval_proportion(series: pd.Series, positive_value, confidence: float = 0.95) -> dict:
    # Constrói o IC focado em porcentagens e chances (ex: IC de % de projetos entregues no prazo)
    s = series.dropna()
    n = len(s)
    k = (s == positive_value).sum()
    p_hat = k / n

    alpha = 1 - confidence
    z = stats.norm.ppf(1 - alpha / 2)
    center = (p_hat + z**2 / (2 * n)) / (1 + z**2 / n)
    margin = (z / (1 + z**2 / n)) * np.sqrt(p_hat * (1 - p_hat) / n + z**2 / (4 * n**2))

    return {
        "variável":        series.name,
        "n":               n,
        "sucessos":        int(k),
        "proporção":       round(p_hat, 4),
        "proporção_%":     round(p_hat * 100, 2),
        "ic_inferior":     round(max(center - margin, 0), 4),
        "ic_superior":     round(min(center + margin, 1), 4),
        "nível_confiança": f"{int(confidence * 100)}%",
    }

def normality_test(series: pd.Series) -> dict:
    # Testa se uma variável tem formato de curva de sino (Normal), o que decide qual teste usar depois
    s = series.dropna()
    n = len(s)

    if n <= 50:
        stat, p = stats.shapiro(s)
        test_name = "Shapiro-Wilk"

    else:
        mu = s.mean()
        sigma = s.std(ddof=1)

        # Trata o erro fatal do SciPy caso todos os números da amostra sejam exatamente iguais
        if sigma == 0:
            return {
                "variável": series.name,
                "n": n,
                "teste": "Kolmogorov-Smirnov",
                "estatística": None,
                "p_valor": None,
                "normal_5%": False,
                "interpretação": "Não foi possível testar normalidade: a amostra possui variância nula.",
            }

        stat, p = stats.kstest(s, stats.norm(loc=mu, scale=sigma).cdf)
        test_name = "Kolmogorov-Smirnov"

    normal = p > 0.05

    return {
        "variável": series.name,
        "n": n,
        "teste": test_name,
        "estatística": round(stat, 4) if stat is not None else None,
        "p_valor": round(p, 6) if p is not None else None,
        "normal_5%": bool(normal),
        "interpretação": (
            "Não rejeita H₀: distribuição compatível com normalidade (p > 0,05)"
            if normal
            else
            "Rejeita H₀: distribuição não é normal (p ≤ 0,05)"
        ),
    }

def ttest_two_groups(df: pd.DataFrame, metric_col: str, group_col: str, group_a: str, group_b: str, alternative: Literal["two-sided", "less", "greater"] = "two-sided", alpha: float = 0.05) -> dict:
    # Teste paramétrico: compara se a média de dois grupos é diferente (ex: Atraso da Equipe Alpha vs Beta)
    a = df.loc[df[group_col] == group_a, metric_col].dropna()
    b = df.loc[df[group_col] == group_b, metric_col].dropna()

    _, p_levene = stats.levene(a, b)
    equal_var = p_levene > 0.05
    stat, p = stats.ttest_ind(a, b, equal_var=equal_var, alternative=alternative)
    rejeita = p <= alpha

    return {
        "métrica":           metric_col,
        "grupo_A":           f"{group_col} = {group_a} (n={len(a)}, μ={a.mean():.4f})",
        "grupo_B":           f"{group_col} = {group_b} (n={len(b)}, μ={b.mean():.4f})",
        "H₀":                f"μ({group_a}) = μ({group_b})",
        "H₁":                f"μ({group_a}) ≠ μ({group_b})" if alternative == "two-sided" else f"μ({group_a}) {'<' if alternative == 'less' else '>'} μ({group_b})",
        "variâncias_iguais": equal_var,
        "correção_Welch":    not equal_var,
        "estatística_t":     round(stat, 4),
        "p_valor":           round(p, 6),
        "alpha":             alpha,
        "rejeita_H₀":        rejeita,
        "decisão":           f"Rejeita H₀ — diferença significativa (p = {p:.4f})" if rejeita else f"Não rejeita H₀ — sem evidência de diferença (p = {p:.4f})",
    }

def mann_whitney_test(df: pd.DataFrame, metric_col: str, group_col: str, group_a: str, group_b: str, alternative: Literal["two-sided", "less", "greater"] = "two-sided", alpha: float = 0.05) -> dict:
    # Teste não-paramétrico: alternativa ao Teste T quando os dados falham no teste de normalidade
    a = df.loc[df[group_col] == group_a, metric_col].dropna()
    b = df.loc[df[group_col] == group_b, metric_col].dropna()

    stat, p = stats.mannwhitneyu(a, b, alternative=alternative)
    rejeita = p <= alpha

    return {
        "métrica":       metric_col,
        "grupo_A":       f"{group_col} = {group_a} (n={len(a)}, mediana={a.median():.4f})",
        "grupo_B":       f"{group_col} = {group_b} (n={len(b)}, mediana={b.median():.4f})",
        "teste":         "Mann-Whitney U",
        "H₀":            "As distribuições são iguais nos dois grupos",
        "H₁":            "As distribuições diferem entre os grupos",
        "estatística_U": round(stat, 4),
        "p_valor":       round(p, 6),
        "alpha":         alpha,
        "rejeita_H₀":    rejeita,
        "decisão":       f"Rejeita H₀ — distribuições diferentes (p = {p:.4f})" if rejeita else f"Não rejeita H₀ — sem diferença significativa (p = {p:.4f})",
    }
    
def kruskal_wallis_test(df: pd.DataFrame, metric_col: str, group_col: str, alpha: float = 0.05) -> dict:
    # Teste de Kruskal-Wallis: compara as medianas de três ou mais grupos (ex: Satisfação por Metodologia)
    groups = [df.loc[df[group_col] == m, metric_col].dropna().values for m in df[group_col].unique()]
    
    # Tratamento de exceção para variância nula em todos os grupos combinados
    all_values = np.concatenate(groups)
    if len(all_values) == 0 or np.std(all_values) == 0:
         return {
             "métrica": metric_col,
             "agrupador": group_col,
             "teste": "Kruskal-Wallis",
             "rejeita_H₀": False,
             "decisão": "Teste abortado: variância nula nos dados."
            }
    
    stat, p = stats.kruskal(*groups)
    rejeita = p <= alpha

    return {
        "métrica":       metric_col,
        "agrupador":     group_col,
        "teste":         "Kruskal-Wallis",
        "H₀":            "As medianas são iguais em todos os grupos",
        "H₁":            "Ao menos um grupo tem mediana diferente",
        "estatística_H": round(stat, 4),
        "p_valor":       round(p, 6),
        "alpha":         alpha,
        "rejeita_H₀":    bool(rejeita),
        "decisão":       f"Rejeita H₀ — diferença significativa (p = {p:.4f})" if rejeita else f"Não rejeita H₀ — sem diferença significativa (p = {p:.4f})",
    }

def chi_square_test(df: pd.DataFrame, col_a: str, col_b: str, alpha: float = 0.05) -> dict:
    # Teste Qui-Quadrado: avalia se duas variáveis de texto (ex: Metodologia e Prazo) dependem uma da outra
    contingency = pd.crosstab(df[col_a], df[col_b])
    chi2, p, dof, expected = stats.chi2_contingency(contingency)

    n = contingency.values.sum()
    k = min(contingency.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * k)) if n * k > 0 else 0.0

    low_expected = (expected < 5).sum()
    if low_expected > 0:
        warnings.warn(f"[chi_square_test] {low_expected} célula(s) com frequência esperada < 5. O teste pode não ser confiável.", stacklevel=2)

    rejeita = p <= alpha
    return {
        "variável_A":           col_a,
        "variável_B":           col_b,
        "tabela_contingencia":  contingency,
        "H₀":                   f"{col_a} e {col_b} são independentes",
        "H₁":                   f"{col_a} e {col_b} são associados",
        "estatística_χ²":       round(chi2, 4),
        "graus_de_liberdade":   dof,
        "p_valor":              round(p, 6),
        "V_de_Cramér":          round(cramers_v, 4),
        "força_associação":     _interpret_cramers_v(cramers_v),
        "alpha":                alpha,
        "rejeita_H₀":           rejeita,
        "células_esperadas_<5": int(low_expected),
        "decisão":              f"Rejeita H₀ — as variáveis são associadas (p = {p:.4f})" if rejeita else f"Não rejeita H₀ — as variáveis são independentes (p = {p:.4f})",
    }

def _interpret_cramers_v(v: float) -> str:
    # Traduz a força de associação do Qui-Quadrado para texto humano
    if v < 0.10:
        return "associação desprezível"
    elif v < 0.20:
        return "associação fraca"
    elif v < 0.40:
        return "associação moderada"
    elif v < 0.60:
        return "associação forte"
    else:
        return "associação muito forte"