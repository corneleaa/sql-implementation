import os
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "customer_segmentation",
    "user": "corneleaa",
    "password": "kornachka123",
}

os.makedirs("diagramos", exist_ok=True)
sns.set_theme(style="whitegrid", palette="Set2")

COLORS = {"A": "#2ecc71", "B": "#3498db", "C": "#e67e22", "D": "#e74c3c"}
LABELS = {"A": "A – Premium", "B": "B – Established", "C": "C – Potential", "D": "D – Budget"}


def load(sql):
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df


def plot_segment_distribution():
    df = load("""
        SELECT segmentation, COUNT(*) AS cnt
        FROM customers WHERE segmentation IS NOT NULL
        GROUP BY segmentation ORDER BY segmentation
    """)
    colors = [COLORS[s] for s in df["segmentation"]]
    labels = [LABELS[s] for s in df["segmentation"]]

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        df["cnt"], labels=labels, colors=colors,
        autopct="%1.1f%%", startangle=140,
        textprops={"fontsize": 11}
    )
    ax.set_title("Klientų pasiskirstymas pagal segmentą", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("diagramos/klientu_pasiskirstymas", dpi=150)
    plt.close()


def plot_age_distribution():
    df = load("""
        SELECT segmentation, age FROM customers
        WHERE segmentation IS NOT NULL AND age IS NOT NULL
    """)
    fig, ax = plt.subplots(figsize=(9, 5))
    for seg in ["A", "B", "C", "D"]:
        subset = df[df["segmentation"] == seg]["age"]
        subset.plot.kde(ax=ax, label=LABELS[seg], color=COLORS[seg], linewidth=2)

    ax.set_title("Amžiaus pasiskirstymas pagal segmentą", fontsize=14, fontweight="bold")
    ax.set_xlabel("Amžius")
    ax.set_ylabel("Tankis")
    ax.legend()
    plt.tight_layout()
    plt.savefig("diagramos/amziaus_pasiskirstymas", dpi=150)
    plt.close()


def plot_spending_score():
    df = load("""
        SELECT segmentation, spending_score, COUNT(*) AS cnt
        FROM customers WHERE segmentation IS NOT NULL
        GROUP BY segmentation, spending_score
    """)
    pivot = df.pivot(index="segmentation", columns="spending_score", values="cnt").fillna(0)
    pivot = pivot[["Žemas", "Vidutinis", "Aukštas"]]

    pivot.plot(kind="bar", figsize=(9, 5), color=["#e74c3c", "#f39c12", "#2ecc71"],
               edgecolor="white")
    plt.title("Išlaidų lygis pagal segmentą", fontsize=14, fontweight="bold")
    plt.xlabel("Segmentas")
    plt.ylabel("Klientų skaičius")
    plt.xticks(rotation=0)
    plt.legend(title="Išlaidų lygis")
    plt.tight_layout()
    plt.savefig("diagramos/isleidziami_pinigai.png", dpi=150)
    plt.close()


def plot_top_professions():
    df = load("""
        SELECT segmentation, profession, COUNT(*) AS cnt
        FROM customers
        WHERE segmentation IS NOT NULL AND profession IS NOT NULL
        GROUP BY segmentation, profession
        ORDER BY segmentation, cnt DESC
    """)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    for i, seg in enumerate(["A", "B", "C", "D"]):
        top = df[df["segmentation"] == seg].head(5)
        axes[i].barh(top["profession"], top["cnt"], color=COLORS[seg])
        axes[i].set_title(f"Segmentas {LABELS[seg]}", fontweight="bold")
        axes[i].invert_yaxis()

    plt.suptitle("Top 5 profesijos pagal segmentą", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("diagramos/profesijos.png", dpi=150)
    plt.close()


def plot_gender_split():
    df = load("""
        SELECT segmentation, gender, COUNT(*) AS cnt
        FROM customers WHERE segmentation IS NOT NULL
        GROUP BY segmentation, gender
    """)
    pivot = df.pivot(index="segmentation", columns="gender", values="cnt").fillna(0)

    pivot.plot(kind="bar", figsize=(8, 5), color=["#e91e63", "#1976d2"], edgecolor="white")
    plt.title("Lyčių pasiskirstymas pagal segmentą", fontsize=14, fontweight="bold")
    plt.xlabel("Segmentas")
    plt.ylabel("Klientų skaičius")
    plt.xticks(rotation=0)
    plt.legend(title="Lytis")
    plt.tight_layout()
    plt.savefig("diagramos/lyciu_pasiskirstymas.png", dpi=150)
    plt.close()


def plot_age_groups():
    df = load("""
        SELECT segmentation,
            CASE
                WHEN age < 25 THEN '18-24'
                WHEN age < 35 THEN '25-34'
                WHEN age < 50 THEN '35-49'
                ELSE '50+'
            END AS age_group,
            COUNT(*) AS cnt
        FROM customers
        WHERE segmentation IS NOT NULL AND age IS NOT NULL
        GROUP BY segmentation, age_group
    """)
    pivot = df.pivot(index="segmentation", columns="age_group", values="cnt").fillna(0)
    pivot = pivot[["18-24", "25-34", "35-49", "50+"]]

    pivot.plot(kind="bar", stacked=True, figsize=(9, 5),
               colormap="tab10", edgecolor="white")
    plt.title("Amžiaus grupės pagal segmentą", fontsize=14, fontweight="bold")
    plt.xlabel("Segmentas")
    plt.ylabel("Klientų skaičius")
    plt.xticks(rotation=0)
    plt.legend(title="Amžiaus grupė", bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.savefig("diagramos/amziaus_grupes", dpi=150)
    plt.close()

if __name__ == "__main__":
    plot_segment_distribution()
    plot_age_distribution()
    plot_spending_score()
    plot_top_professions()
    plot_gender_split()
    plot_age_groups()
