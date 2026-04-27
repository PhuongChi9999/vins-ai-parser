import pandas as pd

from src.aggregation import aggregate_robert, aggregate_robinson, aggregate_suckling
from src.to_ascii import to_ascii


def main():
    vins = pd.read_csv("vins.csv")
    print("Taille initiale :", vins.shape)
    print("Valeurs manquantes avant nettoyage :")
    print(vins.isna().sum())

    # Clearing missing values in the Appellation column
    vins.dropna(subset=["Appellation"], inplace=True)

    # Cleaning "Prix" from unicode
    vins["Prix"] = vins["Prix"].apply(to_ascii)

    # Fill missing critic scores with the appellation average
    for col, agg in [
        ("Robert", aggregate_robert),
        ("J.Robinson", aggregate_robinson),
        ("J.Suckling", aggregate_suckling),
    ]:
        agg_df = agg(vins)
        vins = pd.merge(vins, agg_df, on="Appellation")
        vins[col] = vins[col + "_x"].fillna(vins[col + "_y"])
        vins = vins.drop(columns=[col + "_x", col + "_y"])

    vins.dropna(subset=["Prix"], inplace=True)

    vins = pd.get_dummies(vins, columns=["Appellation"], prefix="App", dtype=int)
    vins.to_csv("vins_cleaned.csv", index=False)


if __name__ == "__main__":
    main()
