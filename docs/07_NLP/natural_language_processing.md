# How to detect name patterns

One interesting project is the detection of name patterns in large datasets of titles, here you do not have enough contextual information to get good results about the semantic meaning of each word part of the title, however we can perform some analysis.


To perform clustering on a set of titles, we can follow these classic steps:

1. Preprocess the titles: Convert the titles into numerical representation that can be used as input to a clustering algorithm. One common approach is to use bag of words or [TF-IDF ](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)representation of the titles.

2. Choose a clustering algorithm: There are many clustering algorithms to choose from such as K-Means, Hierarchical clustering, DBSCAN, etc. Choose the one that suits your data and requirements.

3. Train the clustering algorithm: Train the chosen clustering algorithm on the preprocessed titles. You may have to experiment with different parameters of the algorithm to get the best results.

4. Evaluate the clustering results: Evaluate the clustering results using metrics such as silhouette score, adjusted rand index, etc.

5. Interpreting the results: After evaluating the clustering results, you can inspect the titles assigned to each cluster and name the cluster based on the most common keywords or themes that appear in the titles in the cluster.

In order to improve clustering some preprocess should be performed:

- Lowercases the text
- Lemmatizes each token/word
- Removes punctuation symbols
- Removes stop words


```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

list_titles = [
    "La Gran Estafa",
    "Mundo Jurasico",
    "Cielo de medianoche",
    "Próxima",
    "Aniquilación ",
    "Mad Max: Furia en la carretera",
    "Ex Machina",
    "Al filo del mañana",
    "El congreso",
    "Guía del autoestopista galáctico",
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(list_titles)

kmeans = KMeans(n_clusters=3)
kmeans.fit(X)

cluster_labels = kmeans.labels_
for i, title in enumerate(list_titles):
    print("Title:", title, "Cluster:", cluster_labels[i])

```

```bash
Title: La Gran Estafa Cluster: 1
Title: Mundo Jurasico Cluster: 0
Title: Cielo de medianoche Cluster: 0
Title: Próxima Cluster: 0
Title: Aniquilación  Cluster: 0
Title: Mad Max: Furia en la carretera Cluster: 1
Title: Ex Machina Cluster: 0
Title: Al filo del mañana Cluster: 2
Title: El congreso Cluster: 0
Title: Guía del autoestopista galáctico Cluster: 2

```
To measure the similarity of titles while ignoring prefix or suffix numbers, you can use a preprocessing step to remove the numbers before computing the similarity. There are various ways to do this, but one common approach is to split the title on whitespaces and keep only the first and last words of the title.

Example code in python using cosine similarity:


```python
from sklearn.metrics.pairwise import cosine_similarity

list_titles = [
    "Jurassic Park 1",
    "Jurassic Park 2",
    "Jurassic Park 3",
    "Hunger Games 1",
    "Hunger Games 234",
    "Hunger Games_234",
]

def preprocess_title(title):
    words = title.split()
    return words[0] + " " + words[-1]

preprocessed_titles = [preprocess_title(title) for title in list_titles]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(preprocessed_titles)

similarity = cosine_similarity(X)

print("Similarity matrix:")
print(similarity)
```

```bash
Similarity matrix:
[[1.         1.         1.         0.         0.         0.        ]
 [1.         1.         1.         0.         0.         0.        ]
 [1.         1.         1.         0.         0.         0.        ]
 [0.         0.         0.         1.         0.56921261 0.56921261]
 [0.         0.         0.         0.56921261 1.         0.32400299]
 [0.         0.         0.         0.56921261 0.32400299 1.        ]]

```

In this example, the cosine similarity matrix is computed between the preprocessed titles. The cosine similarity measures the similarity between two documents as the cosine of the angle between their vector representations.



To improve the measure of similarity of titles while ignoring prefix or suffix numbers and typos, you can use several techniques:

1. Preprocessing: Similar to what was discussed in the previous answer, you can use a preprocessing step to remove the numbers and normalize the titles. You can also consider converting the titles to lowercase, removing stopwords, and stemming or lemmatizing the words to reduce the impact of typos.

2. Fuzzy matching: You can use fuzzy matching techniques such as the Jaccard similarity or Levenshtein distance to capture similarities between the titles even when they contain typos or misspellings.

3. Word embeddings: Instead of using a bag-of-words representation, you can use word embeddings, such as Word2Vec or FastText, to represent the titles. These embeddings can capture semantic relationships between the words and provide a more sophisticated representation of the titles.

Example code in python using fuzzywuzzy library and Jaccard similarity:

```python
from fuzzywuzzy import fuzz

list_titles = [
    "Jurassic Park 1",
    "Jurassic Park 2",
    "Jurassic Park 3",
    "Hunger Games 1",
    "Hunger Games 234",
    "Hunger Games_234",
]

def preprocess_title(title):
    title = title.lower()
    words = title.split()
    return " ".join(words)

preprocessed_titles = [preprocess_title(title) for title in list_titles]

similarity = []
for i in range(len(preprocessed_titles)):
    row = []
    for j in range(len(preprocessed_titles)):
        row.append(fuzz.token_set_ratio(preprocessed_titles[i], preprocessed_titles[j]))
    similarity.append(row)

print("Similarity matrix:")
print(similarity)
```

```bash
Similarity matrix:
[[100, 93, 93, 28, 19, 19], 
 [93, 100, 93, 21, 26, 26], 
 [93, 93, 100, 21, 26, 26], 
 [41, 34, 34, 100, 92, 80],
 [32, 39, 39, 92, 100, 75], 
 [26, 26, 26, 80, 75, 100]]
```
In this example, the Jaccard similarity is computed between the preprocessed titles. The Jaccard similarity measures the similarity between two sets of words as the ratio of their intersection to their union.


## Adding Lematization

```python
import spacy

list_titles = [
    "Jurassic Park 1",
    "Jurassic Park 2",
    "Jurassic Park 3",
    "Hunger Games 1",
    "Hunger Games 234",
    "Hunger Games_234",
    "Hunger Gamming_234",
]

def preprocess_title(title):
    title = title.lower()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(title)
    lemmatized_title = " ".join([token.lemma_ for token in doc])
    return lemmatized_title

preprocessed_titles = [preprocess_title(title) for title in list_titles]

similarity = []
for i in range(len(preprocessed_titles)):
    row = []
    for j in range(len(preprocessed_titles)):
        row.append(fuzz.token_set_ratio(preprocessed_titles[i], preprocessed_titles[j]))
    similarity.append(row)

print("Similarity matrix:")
print(similarity)


```

```bash
Similarity matrix before add new text case:
[
    [100, 93, 93, 29, 20, 19], 
    [93, 100, 93, 21, 27, 26], 
    [93, 93, 100, 21, 27, 26], 
    [36, 29, 29, 100, 92, 76], 
    [27, 33, 33, 92, 100, 71], 
    [26, 26, 26, 76, 71, 100]
    ]
```

```bash
Similarity matrix with new case:
[
    [100, 93, 93, 29, 20, 19, 18], 
    [93, 100, 93, 21, 27, 26, 24], 
    [93, 93, 100, 21, 27, 26, 24], 
    [36, 29, 29, 100, 92, 76, 65], 
    [27, 33, 33, 92, 100, 71, 61], 
    [26, 26, 26, 76, 71, 100, 82], 
    [24, 24, 24, 65, 61, 82, 100]
    ]
```

## Now lets improve preprocessing

In this example, the special punctuation, underscores, and numbers are removed using regular expressions as part of the preprocessing step. The lemmatized titles are then computed using the spaCy library and the Jaccard similarity is computed between the preprocessed titles.

```python
import re
import spacy

list_titles = [
    "Jurassic Park 1",
    "Jurassic Park 2",
    "Jurassic Park 3",
    "Hunger Games 1",
    "Hunger Games 234",
    "Hunger Games_234",
]

def preprocess_title(title):
    title = title.lower() # convert to lower case
    title = re.sub(r'[^\w\s]', '', title) # remove punctuation
    title = re.sub(r'\d+', '', title) # remove numbers
    title = re.sub(r'_+', '', title) # remove underscores
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(title)
    lemmatized_title = " ".join([token.lemma_ for token in doc])
    return lemmatized_title

preprocessed_titles = [preprocess_title(title) for title in list_titles]

similarity = []
for i in range(len(preprocessed_titles)):
    row = []
    for j in range(len(preprocessed_titles)):
        row.append(fuzz.token_set_ratio(preprocessed_titles[i], preprocessed_titles[j]))
    similarity.append(row)

print("Similarity matrix:")
print(similarity)


```

```bash
Similarity matrix:
[
    [100, 100, 100, 17, 17, 17, 15], 
    [100, 100, 100, 17, 17, 17, 15], 
    [100, 100, 100, 17, 17, 17, 15], 
    [25, 25, 25, 100, 100, 100, 80], 
    [25, 25, 25, 100, 100, 100, 80], 
    [25, 25, 25, 100, 100, 100, 80], 
    [30, 30, 30, 80, 80, 80, 100]
    ]
```



## Stop words

Using the previous code on:

```python
list_titles = [
    "Jurassic Park 1",
    "Jurassic Park 2",
    "Jurassic Park 3",
    "Jurassic and Park 4",
    "Hunger Games 1",
    "Hunger Games 234",
    "Hunger Games_234",
    "Hunger Game_234",
    "The Hunger Games 2",
]
```
we will got the next matrix of similarity:

```bash
Similarity matrix:
[[100, 100, 100, 100, 17, 17, 17, 15, 21], 
[100, 100, 100, 100, 17, 17, 17, 15, 21], 
[100, 100, 100, 100, 17, 17, 17, 15, 21], 
[100, 100, 100, 100, 21, 21, 21, 32, 19], 
[25, 25, 25, 29, 100, 100, 100, 80, 100], 
[25, 25, 25, 29, 100, 100, 100, 80, 100], 
[25, 25, 25, 29, 100, 100, 100, 80, 100], 
[30, 30, 30, 26, 80, 80, 80, 100, 69], 
[21, 21, 21, 31, 100, 100, 100, 69, 100]]
```

here our current preprocessed titles are:

```python
print(preprocessed_titles)
['jurassic park',
 'jurassic park',
 'jurassic park',
 'jurassic and park',
 'hunger game',
 'hunger game',
 'hunger game',
 'hunger game',
 'the hunger game']
```


```python
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

list_titles = [
    "Jurassic Park 1",
    "Jurassic Park 2",
    "Jurassic Park 3",
    "Jurassic and Park 4",
    "Hunger Games 1",
    "Hunger Games 234",
    "Hunger Games_234",
    "Hunger Game_234",
    "The Hunger Games 2",
]

def preprocess_title(title):
    title = title.lower()
    title = re.sub(r'[^\w\s]', '', title) # remove punctuation
    title = re.sub(r'\d+', '', title) # remove numbers
    title = re.sub(r'_+', '', title) # remove underscores
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(title)
    lemmatized_title = " ".join([token.lemma_ for token in doc if not token.is_stop])
    return lemmatized_title

preprocessed_titles = [preprocess_title(title) for title in list_titles]

similarity = []
for i in range(len(preprocessed_titles)):
    row = []
    for j in range(len(preprocessed_titles)):
        row.append(fuzz.token_set_ratio(preprocessed_titles[i], preprocessed_titles[j]))
    similarity.append(row)

print("Similarity matrix:")
print(similarity)
```
```bash

Similarity matrix:
[[100, 100, 100, 100, 17, 17, 17, 17, 17], 
[100, 100, 100, 100, 17, 17, 17, 17, 17], 
[100, 100, 100, 100, 17, 17, 17, 17, 17], 
[100, 100, 100, 100, 17, 17, 17, 17, 17], 
[25, 25, 25, 25, 100, 100, 100, 100, 100], 
[25, 25, 25, 25, 100, 100, 100, 100, 100], 
[25, 25, 25, 25, 100, 100, 100, 100, 100], 
[25, 25, 25, 25, 100, 100, 100, 100, 100], 
[25, 25, 25, 25, 100, 100, 100, 100, 100]]
]
```

In this example, the stop words are filtered out as part of the preprocessing step by checking if each token is a stop word using the is_stop property in spaCy. The lemmatized titles are then computed using the spaCy library and the Jaccard similarity is computed between the preprocessed titles.


This preprocess make the large change due:

```python
print(preprocessed_titles)
['jurassic park',
 'jurassic park',
 'jurassic park',
 'hunger game',
 'hunger game',
 'hunger game',
 'hunger game']
```

# Levenshtein Metric

```python
def levenshtein_similarity(s1, s2):
    m = len(s1)
    n = len(s2)

    dp = [[0 for j in range(n+1)] for i in range(m+1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

    return 1 - dp[m][n] / max(m, n)

```
La función toma dos cadenas de texto como entrada (s1 y s2) y devuelve un valor flotante que representa la similaridad entre las dos cadenas. La similaridad se calcula utilizando el algoritmo de Levenshtein, que determina el número mínimo de operaciones (inserción, eliminación o sustitución) necesarias para convertir una cadena en otra. Luego, la función devuelve una medida normalizada de la distancia de Levenshtein, que está comprendida entre 0 y 1, donde 1 indica que las dos cadenas son idénticas y 0 indica que son completamente diferentes.

```python
import unittest


class TestLevenshtein(unittest.TestCase):
    def test_levenshtein(self):
        # Test 1: distance of Levenshtein of two equal strings should be 0
        self.assertEqual(levenshtein_similarity("hello", "hello"), 0)

        # Test 2: distance of Levenshtein of two different strings should larger than 0
        self.assertGreater(levenshtein_similarity("hello", "world"), 0)

        # Test 3: distance of Levenshtein if two strings with different length 
        self.assertEqual(levenshtein_similarity("hello", "hi"), 2)

if __name__ == '__main__':
    unittest.main()

```
```python
import unittest

def jaccard_similarity(list1, list2):
    # Implementación de la similaridad de Jaccard
    ...

class TestJaccardSimilarity(unittest.TestCase):
    def test_jaccard_similarity(self):
        # Prueba 1: dos listas iguales deberían tener una similaridad de Jaccard de 1
        self.assertEqual(jaccard_similarity([1, 2, 3], [1, 2, 3]), 1)

        # Prueba 2: dos listas diferentes deberían tener una similaridad de Jaccard menor que 1
        self.assertLess(jaccard_similarity([1, 2, 3], [3, 4, 5]), 1)

        # Prueba 3: dos listas vacías deberían tener una similaridad de Jaccard de 0
        self.assertEqual(jaccard_similarity([], []), 0)

if __name__ == '__main__':
    unittest.main()

```
# Subsequence Metric


```python
def lcs_similarity(s1, s2):
    m = len(s1)
    n = len(s2)

    dp = [[0 for j in range(n+1)] for i in range(m+1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n] / max(m, n)

```

La función toma dos cadenas de texto como entrada (s1 y s2) y devuelve un valor flotante que representa la similaridad basada en subsecuencia entre las dos cadenas. La similaridad se calcula utilizando la longitud de la LCS y se normaliza dividiendo por la longitud máxima de cualquiera de las dos cadenas. La función devuelve un valor comprendido entre 0 y 1, donde 1 indica que las dos cadenas son idénticas y 0 indica que son completamente diferentes.



# Matcher

```python
import spacy

nlp = spacy.load("es_core_news_sm")
matcher = spacy.matcher.Matcher(nlp.vocab)

pattern = [{"POS": "PRON"}, {"IS_DIGIT": True}]
matcher.add("PRON_NUM", None, pattern)

doc = nlp("My name_15")
matches = matcher(doc)

for match_id, start, end in matches:
    matched_span = doc[start:end]
    print("Encontrado un pronombre seguido de un número:", matched_span.text)

```

En este ejemplo, primero se carga el modelo es_core_news_sm de spaCy y se crea un objeto Matcher con el vocabulario del modelo. Luego, se agrega un patrón al matcher que describa un pronombre seguido de un número. Finalmente, se crea un documento de spaCy a partir de la cadena de caracteres que deseas analizar y se utiliza el matcher para buscar coincidencias con el patrón en el documento.


## Clustering

Un enfoque común para el clustering de títulos de libros es convertir cada título en un vector de características que capture su significado semántico, y luego agrupar los títulos en clusters basados en la similitud de sus vectores.

Aquí hay un ejemplo de código que muestra cómo crear un algoritmo de clustering de títulos de libros usando spaCy:

```python

import spacy
import numpy as np
from sklearn.cluster import KMeans

nlp = spacy.load("en_core_web_sm")

# Lista de títulos de libros
titles = ["La Gran Estafa",
    "Mundo Jurasico",
    "Cielo de medianoche",
    "Próxima",
    "Aniquilación ",
    "Mad Max: Furia en la carretera",
    "Ex Machina",
    "Al filo del mañana",
    "El congreso",
    "Guía del autoestopista galáctico",]

# Crea una matriz de embeddings para cada título
X = np.zeros((len(titles), nlp.vocab.vectors_length))
for i, title in enumerate(titles):
    doc = nlp(title)
    X[i, :] = doc.vector

# Aplica clustering KMeans
kmeans = KMeans(n_clusters=2)
kmeans.fit(X)

# Imprime los resultados
for title, label in zip(titles, kmeans.labels_):
    print("Título:", title, "Cluster:", label)
```


En este ejemplo, primero se carga el modelo en_core_web_sm de spaCy y luego se crea una lista de títulos de libros. Luego, se crea una matriz de embeddings para cada título usando el vector del documento creado a partir del título con spaCy. Finalmente, se aplica clustering KMeans a la matriz de embeddings y se imprimen los resultados, mostrando el título y el número de cluster al que pertenece.

Cabe destacar que los resultados pueden variar en función del modelo de spaCy utilizado y la precisión de las embeddings que se hayan entrenado. También es posible que debas ajustar otros parámetros, como el número de clusters, para obtener resultados óptimos.




# Scala

```scala
import org.apache.spark.ml.clustering.KMeans
import org.apache.spark.ml.linalg.Vectors
import org.apache.spark.sql.SparkSession

val spark = SparkSession.builder().appName("BookTitleClustering").getOrCreate()

// Lista de títulos de libros
val titles = Seq("La Gran Estafa",
    "Mundo Jurasico",
    "Cielo de medianoche",
    "Próxima",
    "Aniquilación ",
    "Mad Max: Furia en la carretera",
    "Ex Machina",
    "Al filo del mañana",
    "El congreso",
    "Guía del autoestopista galáctico",)

// Crea una matriz de embeddings para cada título (suponiendo que ya tienes los embeddings previamente calculados)
val titleEmbeddings = titles.map { title =>
  Vectors.dense(...) // Reemplaza con los embeddings correspondientes para cada título
}

val df = spark.createDataFrame(titleEmbeddings.zipWithIndex.map { case (vec, index) => (index, vec) }).toDF("id", "features")

// Aplica clustering KMeans
val kmeans = new KMeans().setK(2).setSeed(1L)
val model = kmeans.fit(df)

// Obtiene los resultados
val predictions = model.transform(df).select("id", "prediction")

// Imprime los resultados
titles.zipWithIndex.foreach { case (title, index) =>
  val cluster = predictions.filter($"id" === index).head().getInt(1)
  println(s"Title: $title Cluster: $cluster")
}

spark.stop()

```



```python 
import spacy

# Cargar el modelo de lenguaje de spacy
nlp = spacy.load("es_core_news_sm")

# Crear un objeto Matcher
matcher = spacy.matcher.Matcher(nlp.vocab)

# Definir un patrón que coincida con los nombres
pattern = [{"POS": "PROPN"}]

# Agregar el patrón al matcher
matcher.add("NOMBRE_PATTERN", None, pattern)

# Procesar un título de libro
doc = nlp("El gran libro de la vida")

# Buscar coincidencias con el matcher
matches = matcher(doc)

# Imprimir los nombres encontrados
for match_id, start, end in matches:
    span = doc[start:end]
    print("Nombre encontrado:", span.text)

# Salida: Nombre encontrado: El, Nombre encontrado: gran, Nombre encontrado: la, Nombre encontrado: la

```


```python
import chardet

# Cadena de caracteres a analizar
text = b"Esta es una cadena de caracteres con un encoding desconocido"

# Detectar el encoding de la cadena de caracteres
result = chardet.detect(text)

# Imprimir el encoding detectado
print("Encoding detectado:", result["encoding"])

# Salida: Encoding detectado: utf-8

```

```python
import chardet

# Cadena de caracteres a separar
text = b"Esta es una cadena de caracteres con un encoding desconocido"

# Detectar el encoding de la cadena de caracteres
result = chardet.detect(text)

# Decodificar la cadena de caracteres a Unicode
decoded_text = text.decode(result["encoding"])

# Imprimir la cadena decodificada
print("Cadena decodificada:", decoded_text)

# Salida: Cadena decodificada: Esta es una cadena de caracteres con un encoding desconocido
```