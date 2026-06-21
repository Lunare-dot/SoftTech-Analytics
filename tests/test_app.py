# src/app.py
# Teste de integração do backend da SoftTech Analytics.
# Exercita o fluxo completo:
# loader -> cleaner -> filter -> kpi_engine -> statistics -> analytics

from src.layers.data.loader import load_raw_data
from src.layers.data.cleaner import clean

from src.layers.data.filter import (
    filter_by_methodology,
    filter_by_team,
)

from src.layers.business.kpi_engine import (
    full_kpi_dashboard,
)

from src.layers.business.statistics import (
    describe_numeric,
    correlation_matrix,
    normality_test,
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


def main():
    print("=" * 80)
    print("SOFTTECH ANALYTICS - TESTE DE INTEGRAÇÃO")
    print("=" * 80)

    # ------------------------------------------------------------------
    # LOADER
    # ------------------------------------------------------------------

    print("\n[1] Loader")

    raw_df = load_raw_data()

    print(f"Projetos carregados: {len(raw_df)}")
    print(f"Colunas encontradas: {len(raw_df.columns)}")

    # ------------------------------------------------------------------
    # CLEANER
    # ------------------------------------------------------------------

    print("\n[2] Cleaner")

    df = clean(raw_df)

    print("Pipeline executado com sucesso.")
    print(f"Shape final: {df.shape}")

    # ------------------------------------------------------------------
    # FILTER
    # ------------------------------------------------------------------

    print("\n[3] Filter")

    agil_df = filter_by_methodology(df, "Ágil")
    print(f"Projetos Ágeis: {len(agil_df)}")

    alpha_df = filter_by_team(df, "Alpha")
    print(f"Projetos da equipe Alpha: {len(alpha_df)}")

    # ------------------------------------------------------------------
    # KPI ENGINE
    # ------------------------------------------------------------------

    print("\n[4] KPI Engine")

    dashboard = full_kpi_dashboard(df)

    for bloco, valores in dashboard.items():
        print(f"\n{bloco.upper()}")
        for chave, valor in valores.items():
            print(f"  {chave}: {valor}")

    # ------------------------------------------------------------------
    # STATISTICS
    # ------------------------------------------------------------------

    print("\n[5] Statistics")

    print("\nEstatísticas numéricas:")
    print(
        describe_numeric(
            df,
            [
                "satisfacao_cliente",
                "atraso_dias",
                "custo_real_mil",
            ],
        )
    )

    print("\nMatriz de correlação:")
    print(
        correlation_matrix(
            df,
            [
                "satisfacao_cliente",
                "atraso_dias",
                "retrabalho_horas",
                "custo_real_mil",
            ],
        )
    )

    print("\nTeste de normalidade:")
    print(
        normality_test(
            df["satisfacao_cliente"]
        )
    )

    # ------------------------------------------------------------------
    # ANALYTICS
    # ------------------------------------------------------------------

    print("\n[6] Analytics")

    analytics_results = {
        "experience_vs_bugs": experience_vs_bugs(df),
        "complexity_vs_delay": complexity_vs_delay(df),
        "rework_vs_satisfaction": rework_vs_satisfaction(df),
        "overtime_vs_deadline": overtime_vs_deadline(df),
        "size_vs_cost": size_vs_cost(df),
        "methodology_vs_performance": methodology_vs_performance(df),
    }

    for nome, resultado in analytics_results.items():
        print(f"\n✔ {nome}")
        print(resultado["hipotese"])

    print("\nRanking de equipes:")
    print(team_performance_ranking(df))

    print("\n" + "=" * 80)
    print("BACKEND VALIDADO COM SUCESSO")
    print("=" * 80)


if __name__ == "__main__":
    main()