# Scripts de diagramas

Scripts que generan diagramas con la librería [`diagrams`](https://diagrams.mingrammer.com/)
(mingrammer). No forman parte del sitio publicado: se ejecutan a mano y su salida `.png`
se guarda en `docs/images/`.

## Scripts

| Script | Título del diagrama | Salida |
|---|---|---|
| `ML.py` | ML Taxonomy | `ml_taxonomy.png` |
| `clustering_types.py` | Taxonomy of Clustering Methods | `taxonomy_clustering.png` |
| `clustering_analysis_flow.py` | ML Development On Node | `ml_development_on_node.png` |

## Requisitos

`diagrams` necesita **Graphviz** instalado en el sistema:

```bash
sudo apt install graphviz          # Debian / Ubuntu
pip install diagrams
```

## Regenerar

Los scripts escriben el `.png` en el directorio de trabajo, así que hay que ejecutarlos
desde `docs/images/`:

```bash
cd docs/images
python ../diagrams/clustering_types.py
```

## Estado

- `taxonomy_clustering.png` está en el repositorio y se usa en
  [Unsupervised Learning](../02_UNSUPERVISED_LEARNING/introduccion.md).
- `ml_taxonomy.png` y `ml_development_on_node.png` **no** están en `docs/images/`:
  hay que regenerarlos antes de referenciarlos desde alguna nota.

`ML.py` importa `urllib.request.urlretrieve` pero nunca lo llama: es un import muerto,
se puede eliminar.
