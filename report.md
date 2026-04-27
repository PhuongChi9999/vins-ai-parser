# Rapport synthétique – Projet S6  
## Objectif
L’objectif de ce projet est de prédire le prix d’un vin à partir de plusieurs caractéristiques, notamment :

- les notes des critiques (Robert Parker, J. Robinson, J. Suckling)
- l’appellation

Plusieurs méthodes d’apprentissage supervisé sont testées afin d’identifier celle qui donne les meilleures performances.

## Q15
On commence par séparer les données :
- Variable cible : y = Prix
- Variables explicatives : X = autres colonnes

La variable catégorielle Appellation est transformée en variables numériques via get_dummies().

Ensuite, on divise les données :
    - 75% pour l’entraînement
    - 25% pour le test
    - avec random_state = 49

## Q16
On teste une régression linéaire.
    Résultat : R² ≈ 0.0905
Ce score est faible, ce qui signifie que le modèle explique très peu la variance du prix.
Les variables disponibles ne suffisent donc pas à prédire précisément le prix du vin

## Q17
Sur la figure, les points sont très dispersés autour de la diagonale.
Cela montre que :
    - le modèle capte une tendance globale
    - mais les prédictions restent imprécises

## Q18
On teste deux transformations :
    - Normalisation + LR → 0.0937
    - Standardisation + LR → 0.0905

Conclusion :
    - la normalisation améliore légèrement le modèle
    - l’impact reste très faible
Cela montre que le problème ne vient pas seulement de l’échelle des variables.

## Q19
Prix :
min = 5.21
max = 23000

==>> très grande dispersion

Après transformation logarithmique : valeurs beaucoup plus compactes
==>> en théorie, cela peut aider l’apprentissage

## Q20
Tableau des résultats :
                Méthode        R2
0                    LR  0.090541
1    Normalisation + LR  0.093703
2  Standardisation + LR  0.090541

Meilleure méthode : Normalisation + LR


Avec log(y) :
scores ≈ 0.064

Conclusion : La transformation logarithmique n’améliore pas les performances.
Le score reste faible (≈ 0.094), ce qui indique que les variables disponibles ne capturent qu’une petite partie des facteurs influençant le prix

## Q21 – Arbre de décision
Meilleur depth trouvé : 3

Scores :
score AD = -1.1881618562803853
score Normalisation + AD = -1.3023789801138057
score Standardisation + AD = -1.1881618562803853

Un score négatif signifie que le modèle est moins performant qu’une simple moyenne.
Conclusion : Les arbres de décision ne sont pas adaptés à ce dataset.

## Q22 - KNN :
k = 4
    - KNN ≈ 0.0477 (meilleur)
    - avec pré-traitement → pire
k = 5
    - résultats encore plus faibles

Conclusion :
- k = 4 est meilleur
- augmenter k dégrade les performances
Le pré-traitement n’améliore pas KNN ici, ce qui est surprenant car cette méthode dépend normalement des distances. Cela suggère que le bruit dans les données domine

## Q23 - Meilleur KNN :
Méthode	          R²
KNN	           0.0477
KNN reste moins performant que LR

## Q24 - Comparaison finale

Comparaison finale :
  Méthode        R2
0      LR  0.093703
1      AD -1.188162
2     KNN  0.047712

=> meilleure méthode : M = Normalisation + Régression linéaire

## Q25– PCA
Variance expliquée (5 composantes) ≈ 26% ==>> c’est faible 
L’information est répartie sur de nombreuses variables, donc réduire à 5 dimensions fait perdre trop d’information

## Q26 - PCA + modèle M
Avec PCA :
score ≈ 0.0524
==>> moins bon qu’avant
Conclusion : PCA dégrade les performances

## Q27 - Corrélation
La matrice montre des corrélations globalement faibles.
==>> aucune variable ne permet à elle seule de prédire le prix.

## Q28 - Variables les plus corrélées
Top 5 :
Robert                             0.136747
J.Robinson                         0.120251
J.Suckling                         0.080813
App_Pauillac                       0.076033
App_Haut-Médoc                    -0.058114

==>> les notes des critiques sont les plus importantes

## Q29 – Sélection de features
Avec seulement 5 variables :
Score ≈ 0.0233

=> beaucoup plus faible
Même si ces variables sont les plus corrélées individuellement, elles ne suffisent pas à prédire le prix. Le modèle a besoin de plusieurs variables combinées.

## Q30 - Random Forest
Tableau des résultats RF :
                Méthode        R2
0                    RF -0.507962
1    Normalisation + RF -0.214273
2  Standardisation + RF -0.507913

Random Forest : scores négatifs
Conclusion : Random Forest ne fonctionne pas sur ce dataset.

## Conclusion
Le meilleur modèle est : Normalisation + Régression linéaire
    Score ≈ 0.094 
Cependant, les performances restent faibles.
## Conclusion générale :
Le prix du vin dépend de nombreux facteurs complexes qui ne sont pas présents dans le dataset, comme :
    - le producteur
    - le millésime
    - la rareté

Conclusion finale :
Les notes des critiques ont une influence, mais elles ne suffisent pas à expliquer le prix de manière précise.
