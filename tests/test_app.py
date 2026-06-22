# src/test_app.py

"""
Teste de integração completo.

Objetivo:
- Validar backend
- Extrair todos os dados usados nos gráficos
- Gerar saída pronta para o relatório
"""

from pprint import pprint

from src.layers.data.loader import load_raw_data
from src.layers.data.cleaner import clean

from src.layers.business.kpi_engine import (
    full_kpi_dashboard,
)

from src.layers.business.statistics import (
    describe_numeric,
    describe_categorical,
    correlation_matrix,
    normality_test,
    confidence_interval_mean,
    confidence_interval_proportion,
)

from src.layers.business.analytics import (
    experience_vs_bugs,
    complexity_vs_delay,
    rework_vs_satisfaction,
    overtime_vs_deadline,
    size_vs_cost,
    methodology_vs_performance,
    team_performance_ranking,
)


def print_title(title):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def print_sub(title):
    print("\n" + "-" * 80)
    print(title)
    print("-" * 80)


def main():

    print_title("SOFTTECH ANALYTICS - RELATORIO DE INTEGRACAO")

    # ==========================================================
    # LOAD + CLEAN
    # ==========================================================

    raw_df = load_raw_data()
    df = clean(raw_df)

    print(f"\nProjetos carregados: {len(df)}")
    print(f"Colunas: {len(df.columns)}")

    # ==========================================================
    # PERFIL DO DATASET
    # ==========================================================

    print_title("1. PERFIL DO DATASET")

    categorias = [
        "metodologia",
        "complexidade",
        "porte_projeto",
        "equipe",
        "entregue_no_prazo",
    ]

    for col in categorias:
        print_sub(col.upper())
        print(describe_categorical(df, col))

    # ==========================================================
    # KPI DASHBOARD
    # ==========================================================

    print_title("2. KPIs")

    dashboard = full_kpi_dashboard(df)

    for bloco, dados in dashboard.items():

        print_sub(bloco.upper())

        for chave, valor in dados.items():
            print(f"{chave}: {valor}")

    # ==========================================================
    # DESCRITIVA
    # ==========================================================

    print_title("3. ESTATISTICA DESCRITIVA")

    numericas = [
        "satisfacao_cliente",
        "atraso_dias",
        "custo_real_mil",
        "retrabalho_horas",
        "horas_extras",
        "experiencia_media_anos",
        "bugs_total",
        "bugs_criticos",
    ]

    print(
        describe_numeric(
            df,
            numericas
        )
    )

    print_sub("MATRIZ DE CORRELACAO")

    print(
        correlation_matrix(
            df,
            [
                "satisfacao_cliente",
                "atraso_dias",
                "retrabalho_horas",
                "horas_extras",
                "custo_real_mil",
                "bugs_total",
            ]
        )
    )

    print_sub("TESTES DE NORMALIDADE")

    for col in numericas:

        resultado = normality_test(df[col])

        print(f"\n{col}")
        pprint(resultado)

    # ==========================================================
    # H1
    # ==========================================================

    print_title("4. HIPOTESE H1")

    h1 = experience_vs_bugs(df)

    pprint(h1)

    # ==========================================================
    # H2
    # ==========================================================

    print_title("5. HIPOTESE H2")

    h2 = complexity_vs_delay(df)

    pprint(h2)

    # ==========================================================
    # H3
    # ==========================================================

    print_title("6. HIPOTESE H3")

    h3 = rework_vs_satisfaction(df)

    pprint(h3)

    # ==========================================================
    # H4
    # ==========================================================

    print_title("7. HIPOTESE H4")

    h4 = overtime_vs_deadline(df)

    pprint(h4)

    # ==========================================================
    # H5
    # ==========================================================

    print_title("8. HIPOTESE H5")

    h5 = size_vs_cost(df)

    pprint(h5)

    # ==========================================================
    # H6
    # ==========================================================

    print_title("9. HIPOTESE H6")

    h6 = methodology_vs_performance(df)

    pprint(h6)

    # ==========================================================
    # RANKING
    # ==========================================================

    print_title("10. RANKING DE EQUIPES")

    ranking = team_performance_ranking(df)

    print(ranking)
    
    # ==========================================================
    # INTERVALOS DE CONFIANÇA
    # ==========================================================

    print_title("11. INTERVALOS DE CONFIANÇA")

    print_sub("SATISFACAO DO CLIENTE")

    pprint(
        confidence_interval_mean(
            df["satisfacao_cliente"]
        )
    )

    print_sub("ATRASO DOS PROJETOS")

    pprint(
        confidence_interval_mean(
            df["atraso_dias"]
        )
    )

    print_sub("ENTREGA NO PRAZO")

    pprint(
        confidence_interval_proportion(
            df["entregue_no_prazo"],
            positive_value="Sim"
        )
    )
    
    print_title("FIM DO TESTE")


if __name__ == "__main__":
    main()