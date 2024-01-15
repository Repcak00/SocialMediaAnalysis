import os
import time

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.manifold import TSNE

from const import DATA_DIR

if __name__ == "__main__":
    start_time = time.time()

    print("File loading")
    with open(os.path.join(DATA_DIR, "filtered_embeddings_final.npy"), "rb") as f:
        numpy_embeddings = np.load(f)
    df_combined = pd.read_csv(
        os.path.join(DATA_DIR, "filtered_combined_final.csv"), encoding="utf-8"
    )

    authors = df_combined["channel"].unique().tolist()
    genres = df_combined["genre"].unique().tolist()

    print("Calculating embeddings")
    embed = TSNE(
        n_components=3, perplexity=15, random_state=42, init="random", learning_rate=200
    )
    true_embeddings = embed.fit_transform(numpy_embeddings)

    print("Dataframe manipulations")
    df_embeddings = pd.DataFrame()
    df_embeddings["genre"] = df_combined["genre"]
    df_embeddings["author"] = df_combined["channel"]
    df_embeddings["x"] = true_embeddings[:, 0]
    df_embeddings["y"] = true_embeddings[:, 1]
    df_embeddings["z"] = true_embeddings[:, 2]

    print("Plotting")
    fig = px.scatter_3d(
        df_embeddings,
        x="x",
        y="y",
        z="z",
        color="genre",
        opacity=0.7,
        title="3D Embeddings",
    )

    print("Saving plot as HTML")
    fig.write_html(os.path.join(DATA_DIR, "tsne_3D.html"))

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time taken: {total_time} seconds")
