A faire : explorer energy compaction
	Pour quel facteur de perte, le rapport entre la qualité de l’image et le gain de place est-il optimal
14873
14878
14884
Titre : La compression de données appliquées aux images

Motivation :

Il est intéressant de comprendre comment sont compressées les données et plus particulièrement les images afin d’optimiser leur utilisation et leur stockage. Je m'intéresserai tout particulièrement à la compression JPEG utilisant différents algorithmes de compression tel que le codage de Huffman ou le codage arithmétique.


Rattachement au thème de l’année :

La ville est un lieu abondant de données et d’informations. Il est donc important de comprendre comment l’utilisation des données est optimisée au moyen de leur compression.


Bibliographie commentée :

La compression de données est un procédé permettant de réduire la taille et l’espace de stockage occupé par des données tout en gardant un maximum de précision.

La compression JPEG (Joint Photographic Experts Group) est un procédé de compression d’images avec pertes permettant de réduire entre 3 et 25 fois la taille d’un fichier en fonction de qualité finale que l’on veut obtenir. Il est aujourd’hui l’un des formats de compression les plus utilisés pour les images.

L’algorithme de compression JPEG est constitué de plusieurs étapes. Tout d’abord, il faut transformer l’image en une matrice de pixels donnant la représentation RGB de chaque pixel. Il faut ensuite transformer cette matrice en une matrice donnant la luminance et deux informations de chrominance afin de reconstituer les trois couleurs primaires rouge, vert et bleu.

Il faut ensuite appliquer une transformée de Fourier discrète (DCT) à cette image. La DCT possède une excellente propriété de regroupement de l'énergie ce qui permet à ce que l'information soit essentiellement portée par les coefficients basses fréquences. Seul un petit nombre de coefficients seront non nuls, ce qui permet de réduire le nombre de calculs à effectuer par l’ordinateur.

Vient ensuite la quantification. Il s’agit là de l’étape responsable de la dégradation de l’image.
L’utilisateur doit choisir la qualité de la compression, celle-ci ne devra pas dépasser un facteur 25, au-dessus de cela l’image est trop dégradée et le gain en terme d’espace gagné est négligeable. On lit ensuite la matrice en diagonale, des basses aux hautes fréquences, ce qui fait apparaître de grandes séquences de 0.

On doit ensuite coder cette chaîne de caractères. Plusieurs méthodes de codage existent. Je m’intéresse particulièrement à deux d’entre elles : le codage de Huffman et le codage arithmétique. Je vais essayer de comparer ces deux algorithmes.

Après cela, on décode le tout en réalisant les opérations dans l’ordre inverse.


Problématique :

L’étude de différents algorithmes de compression d’images permet de comprendre l’intérêt propre à chacun et comment les améliorer.
On peut se demander comment est implémenté l’algorithme de compression JPEG ?
Laquelle des deux méthodes de codage précédentes est la plus efficace et pourquoi ?
Pour quel facteur de perte, le rapport entre la qualité de l’image et le gain de place est-il optimal ?

Objectifs :

Mes objectifs sont d’implémenter l’algorithme de compression JPEG, et le tester avec les deux méthodes de compression : le codage arithmétique et le codage de Huffman, pour savoir laquelle est la plus efficace et dans quelle situation mais également d’essayer de trouver le facteur de perte optimalisant le rapport entre la qualité de l’image et le gain de place.
