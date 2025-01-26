import pandas as pd

import matplotlib.pyplot as plt

def plot_corr(df):
    fig, axis = plt.subplots(2, 2, figsize=(15, 15), dpi=50)
    columns = ["peak_ccu", "score", "Amount OS", "Supported languages", "Audio languages", "price", "dlc_count"]
    # plt.matshow(df_final.drop("name", axis=1).corr())
    axis[0][0].matshow(df[columns].corr())
    axis[0][0].set_xticks(range(len(columns)), columns, rotation=25)
    axis[0][0].set_yticks(range(len(columns)), columns)
    axis[0][0].set_title("Correlation matrix")

    axis[0][1].matshow(df[columns][df["peak_ccu"]!=0].corr())
    axis[0][1].set_xticks(range(len(columns)), columns, rotation=25)
    axis[0][1].set_yticks(range(len(columns)), columns)
    axis[0][1].set_title("Correlation matrix not 0 peak_ccu")

    axis[1][0].matshow(df[df["INDIE"]==0][columns][df["peak_ccu"]!=0].corr())
    axis[1][0].set_xticks(range(len(columns)), columns, rotation=25)
    axis[1][0].set_yticks(range(len(columns)), columns)
    axis[1][0].set_title("Correlation matrix not INDIE")

    axis[1][1].matshow(df[df["INDIE"]==1][columns][df["peak_ccu"]!=0].corr())
    axis[1][1].set_xticks(range(len(columns)), columns, rotation=25)
    axis[1][1].set_yticks(range(len(columns)), columns)
    axis[1][1].set_title("Correlation matrix not 0 peak_ccu and INDIE")
    # Fix the layout where the tittle of the axis appears inside the plots
    plt.tight_layout()

    # plt.tight_layout()
    plt.show()


def plot_boxplots(df):
    fig, axis = plt.subplots(2, 3, figsize=(15, 15), dpi=80)
    columns = ["peak_ccu", "score", "Amount OS", "Supported languages", "Audio languages", "price"]
    # Separate INDIE and not INDIE games in two columns
    for i, col in enumerate(columns):
        ax = axis[i // 3, i % 3]
        df.boxplot(col, by="INDIE", ax=ax)
        ax.set_title(col)
    plt.tight_layout()
    plt.show()

def plot_hist(df):
    columns = ["peak_ccu", "score"]
    columns_2 = ["INDIE", "RACING"]#, "ACTION", "CASUAL", "ADVENTURE", "SIMULATION", "RPG", "STRATEGY", "SPORTS", "RACING"]
    fig, axis = plt.subplots(len(columns_2), len(columns), figsize=(15, 15), dpi=80)
    # Set different colors for each genre
    bins = 10
    for i, col in enumerate(columns):
        for j, col_2 in enumerate(columns_2):
            ax = axis[j, i]
            # Fill the bar with patterns to differentiate the genres
            df[col][df[col_2] == 1].hist(ax=ax, bins=bins, color="purple", alpha=0.5, density=True, hatch="x", label=f"{col_2} = 1")
            df[col][df[col_2] == 0].hist(ax=ax, bins=bins, color="yellow", alpha=0.5, density=True, hatch="o", label=f"{col_2} = 0")
            ax.set_xlabel(col)
            ax.legend()
    plt.tight_layout()
    plt.show()


df = pd.read_csv("data/df_final.csv", index_col=0)

df_final = df[df["peak_ccu"] != 0]
cap_outliers = 0.90
for col in ["peak_ccu", "score", "Amount OS", "Supported languages", "Audio languages", "price"]:
    quantile = df_final[col].quantile(cap_outliers)
    df_final[col] = df_final[col].apply(lambda x: x if x < quantile else quantile)

plot_hist(df_final)