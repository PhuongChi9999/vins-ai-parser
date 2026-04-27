import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer, StandardScaler
from sklearn.tree import DecisionTreeRegressor

FIGURES_DIR = Path("figures")
FIGURES_DIR.mkdir(exist_ok=True)


def main():
    vins = pd.read_csv("vins_cleaned.csv")

    # Q15
    X = vins.drop(columns=["Prix"])
    y = vins["Prix"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=49
    )

    # Q16-18
    print("Q16-18==================")
    results_lr = evaluate_models(
        [
            ("LR", LinearRegression()),
            ("Normalisation + LR", make_pipeline(Normalizer(), LinearRegression())),
            (
                "Standardisation + LR",
                make_pipeline(StandardScaler(), LinearRegression()),
            ),
        ],
        X_train,
        y_train,
        X_test,
        y_test,
    )
    print(results_lr.to_string(index=False))

    # Q19
    print("Q19==================")
    prix_analyse(y)

    # Q20
    print("Q20==================")
    results_log = compare_lr_scores_log(X_train, X_test, y_train, y_test)
    if results_log["R2"].max() > results_lr["R2"].max():
        print("La transformation logarithmique améliore les performances.")
    else:
        print("La transformation logarithmique n'améliore pas les performances.")

    # Q21
    print("Q21==================")
    best_depth = find_best_depth(X_train, y_train)
    results_dt = evaluate_models(
        [
            ("AD", DecisionTreeRegressor(max_depth=best_depth, random_state=49)),
            (
                "Normalisation + AD",
                make_pipeline(
                    Normalizer(),
                    DecisionTreeRegressor(max_depth=best_depth, random_state=49),
                ),
            ),
            (
                "Standardisation + AD",
                make_pipeline(
                    StandardScaler(),
                    DecisionTreeRegressor(max_depth=best_depth, random_state=49),
                ),
            ),
        ],
        X_train,
        y_train,
        X_test,
        y_test,
    )
    print(results_dt.to_string(index=False))

    # Q22
    print("Q22==================")
    results_knn_4 = evaluate_models(
        [
            ("KNN", KNeighborsRegressor(n_neighbors=4)),
            (
                "Normalisation + KNN",
                make_pipeline(Normalizer(), KNeighborsRegressor(n_neighbors=4)),
            ),
            (
                "Standardisation + KNN",
                make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=4)),
            ),
        ],
        X_train,
        y_train,
        X_test,
        y_test,
    )
    results_knn_5 = evaluate_models(
        [
            ("KNN (k=5)", KNeighborsRegressor(n_neighbors=5)),
            (
                "Normalisation + KNN (k=5)",
                make_pipeline(Normalizer(), KNeighborsRegressor(n_neighbors=5)),
            ),
            (
                "Standardisation + KNN (k=5)",
                make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=5)),
            ),
        ],
        X_train,
        y_train,
        X_test,
        y_test,
        plot=False,
    )
    print("Comparaison k=4 vs k=5 :")
    print(pd.concat([results_knn_4, results_knn_5]).to_string(index=False))
    if results_knn_5["R2"].max() > results_knn_4["R2"].max():
        print("k=5 donne de meilleurs résultats que k=4.")
    else:
        print("k=5 ne donne pas de meilleurs résultats significatifs, on conserve k=4.")

    # Q23
    print("Q23==================")
    print(results_knn_4.to_string(index=False))

    # Q24
    print("Q24==================")
    all_results = pd.concat([results_lr, results_dt, results_knn_4], ignore_index=True)
    results_models = pd.DataFrame(
        {
            "Méthode": ["LR", "AD", "KNN"],
            "R2": [results_lr["R2"].max(), results_dt["R2"].max(), results_knn_4["R2"].max()],
        }
    )
    print(results_models.to_string(index=False))
    M_name = all_results.loc[all_results["R2"].idxmax(), "Méthode"]
    print("M =", M_name)

    # Q25
    pca = apply_pca(X, 5)
    cum_var = variance_cumulee(pca)
    plot_pca(cum_var)

    # Q26
    builders = {
        "LR": lambda: LinearRegression(),
        "Normalisation + LR": lambda: make_pipeline(Normalizer(), LinearRegression()),
        "Standardisation + LR": lambda: make_pipeline(StandardScaler(), LinearRegression()),
        "AD": lambda: DecisionTreeRegressor(max_depth=best_depth, random_state=49),
        "Normalisation + AD": lambda: make_pipeline(Normalizer(), DecisionTreeRegressor(max_depth=best_depth, random_state=49)),
        "Standardisation + AD": lambda: make_pipeline(StandardScaler(), DecisionTreeRegressor(max_depth=best_depth, random_state=49)),
        "KNN": lambda: KNeighborsRegressor(n_neighbors=4),
        "Normalisation + KNN": lambda: make_pipeline(Normalizer(), KNeighborsRegressor(n_neighbors=4)),
        "Standardisation + KNN": lambda: make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=4)),
    }
    M_builder = builders[M_name]
    score_pca = pca_model(X_train, X_test, y_train, y_test, M_builder, M_name, 5)

    # Q27
    corr = correlation_matrix(vins)

    # Q28
    best_correlated_attributes(corr)

    # Q29
    select_best_features(vins, corr, M_name, M_builder)

    # Q30
    print("Q30==================")
    results_rf = evaluate_models(
        [
            (
                "RF",
                RandomForestRegressor(n_estimators=200, max_depth=10, random_state=49),
            ),
            (
                "Normalisation + RF",
                make_pipeline(
                    Normalizer(),
                    RandomForestRegressor(
                        n_estimators=200, max_depth=10, random_state=49
                    ),
                ),
            ),
            (
                "Standardisation + RF",
                make_pipeline(
                    StandardScaler(),
                    RandomForestRegressor(
                        n_estimators=200, max_depth=10, random_state=49
                    ),
                ),
            ),
        ],
        X_train,
        y_train,
        X_test,
        y_test,
        plot=False,
    )
    print(results_rf.to_string(index=False))


def evaluate_models(models, X_train, y_train, X_test, y_test, plot=True):
    rows = []
    for name, model in models:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = r2_score(y_test, y_pred)
        if plot:
            filename = re.sub(r"[^\w]+", "_", name.lower()).strip("_") + ".png"
            plot_predictions(y_test, y_pred, name, filename)
        rows.append({"Méthode": name, "R2": score})

    return pd.DataFrame(rows)


def plot_predictions(
    y_true, y_pred, title, filename, x_label="Prédictions", y_label="Valeurs réelles"
):
    plt.figure(figsize=(8, 6))
    plt.scatter(y_pred, y_true, s=25)

    min_val = min(min(y_pred), min(y_true))
    max_val = max(max(y_pred), max(y_true))

    plt.plot([min_val, max_val], [min_val, max_val], linestyle="--")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / filename)
    plt.close()


# ================================
# Q19
def prix_analyse(y):
    print("Prix minimum : ", y.min())
    print("Prix maximum : ", y.max())

    y_log = np.log(y)

    print("============")
    print("ln(Prix) minimum : ", y_log.min())
    print("ln(Prix) maximum : ", y_log.max())


# ================================
# Q20
def compare_lr_scores_log(X_train, X_test, y_train, y_test):
    y_train_log = np.log(y_train)

    models = [
        ("LR + log(y)", LinearRegression()),
        (
            "Normalisation + LR + log(y)",
            make_pipeline(Normalizer(), LinearRegression()),
        ),
        (
            "Standardisation + LR + log(y)",
            make_pipeline(StandardScaler(), LinearRegression()),
        ),
    ]

    rows = []
    preds = {}
    for name, model in models:
        model.fit(X_train, y_train_log) 
        pred = np.exp(model.predict(X_test))  
        #Dans cette partie, le modèle est entraîné sur log(y), donc il prédit log(prix).
        #Pour obtenir les prix réels, nous appliquons la fonction exponentielle aux prédictions.
        #Cela permet de comparer correctement les résultats avec les valeurs réelles
        score = r2_score(y_test, pred)
        rows.append({"Méthode": name, "R2": score})
        preds[name] = pred

    results = pd.DataFrame(rows)
    print("\nTableau des résultats avec log(y) :")
    print(results.to_string(index=False))
    best = results.loc[results["R2"].idxmax()]
    print(
        f"Meilleure méthode avec log(y) : {best['Méthode']} | Score : {best['R2']:.6f}"
    )
    filename = re.sub(r"[^\w]+", "_", best["Méthode"].lower()).strip("_") + ".png"
    plot_predictions(y_test, preds[best["Méthode"]], best["Méthode"], filename)
    return results


# ================================
# Q21
def find_best_depth(X_train, y_train):
    depths = [3, 4, 5]
    best_depth = None
    best_score = -np.inf

    for d in depths:
        tree = DecisionTreeRegressor(max_depth=d, random_state=49)
        scores = cross_val_score(tree, X_train, y_train, cv=5)
        mean_score = scores.mean()

        if mean_score > best_score:
            best_score = mean_score
            best_depth = d

    print("Meilleur depth =", best_depth)
    return best_depth


# =====================
# Q25
def apply_pca(X, n_components=5):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=n_components)
    pca.fit(X_scaled)

    print("Q25===================")
    print(f"\nVariance expliquée ({n_components} composantes) :")
    print(pca.explained_variance_ratio_)
    print("Somme variance expliquée :", pca.explained_variance_ratio_.sum())

    return pca


def variance_cumulee(pca):
    cum_var = np.cumsum(pca.explained_variance_ratio_)

    print("\nVariance cumulée :")
    print(cum_var)

    return cum_var


def plot_pca(cum_var):
    plt.figure(figsize=(8, 5))
    plt.plot(cum_var)
    plt.xlabel("Nombre de composantes")
    plt.ylabel("Variance cumulée")
    plt.title("PCA - Variance cumulée")
    plt.grid()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "q25_pca_variance.png")
    plt.close()


# Q26
def pca_model(
    X_train, X_test, y_train, y_test, model_builder, model_name, n_components=5
):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    pca = PCA(n_components=n_components)
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_test_pca = pca.transform(X_test_scaled)

    model = model_builder()
    model.fit(X_train_pca, y_train)
    y_pred = model.predict(X_test_pca)
    score = r2_score(y_test, y_pred)

    print("Q26====================")
    print(f"\n{model_name} avec PCA ({n_components} composantes)")
    print("score =", score)

    return score


# Q27
def correlation_matrix(vins):
    print("Q27====================")

    corr_matrix = vins.corr(numeric_only=True)

    print("\nMatrice de corrélation :")
    print(corr_matrix)

    plt.figure(figsize=(10, 8))
    plt.matshow(corr_matrix, fignum=1)
    plt.colorbar()
    plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=90)
    plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "q27_correlation_matrix.png")
    plt.close()

    return corr_matrix


# ===================================
# Q28
def best_correlated_attributes(corr_matrix):
    print("Q28====================")

    corr_prix = corr_matrix["Prix"].drop("Prix")
    best_corr = corr_prix.reindex(corr_prix.abs().sort_values(ascending=False).index)

    print("\nAttributs les plus corrélés au prix :")
    print(best_corr)

    return best_corr


# ===================================
# Q29
def select_best_features(vins, corr_matrix, M_name, model_builder):
    print("Q29====================")

    corr_prix = corr_matrix["Prix"].drop("Prix")
    selected_features = (
        corr_prix.abs().sort_values(ascending=False).head(5).index.tolist()
    )

    print("\nTop 5 attributs les plus corrélés au prix :")
    print(selected_features)

    vins_selected = vins[selected_features + ["Prix"]]

    X1 = vins_selected.drop(columns=["Prix"])
    y1 = vins_selected["Prix"]
    X_train1, X_test1, y_train1, y_test1 = train_test_split(
        X1, y1, test_size=0.25, random_state=49
    )

    model = model_builder()
    model.fit(X_train1, y_train1)
    y_pred1 = model.predict(X_test1)
    score1 = r2_score(y_test1, y_pred1)

    print(f"\nScore avec les 5 meilleurs attributs et méthode {M_name} = {score1}")

    plot_predictions(
        y_test1,
        y_pred1,
        f"{M_name} avec 5 attributs corrélés",
        "q29_top5_features_model.png",
        x_label="Prédictions",
        y_label="Prix réels",
    )

    return vins_selected, score1


if __name__ == "__main__":
    main()
