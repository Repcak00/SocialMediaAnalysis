import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
    tsne_embeddings = TSNE(
        n_components=2, perplexity=15, random_state=42, init="random", learning_rate=200
    )
    true_embeddings = tsne_embeddings.fit_transform(numpy_embeddings)

    print("Dataframe manipulations")
    df_embeddings = pd.DataFrame()
    df_embeddings["genre"] = df_combined["genre"]
    df_embeddings["author"] = df_combined["channel"]
    df_embeddings["x"] = true_embeddings[:, 0]
    df_embeddings["y"] = true_embeddings[:, 1]

    print("Plotting")
    fig, ax = plt.subplots(figsize=(16, 9))
    for genre in genres:
        ax.scatter(
            df_embeddings.loc[df_embeddings["genre"] == genre].x,
            df_embeddings.loc[df_embeddings["genre"] == genre].y,
            label=genre,
            alpha=0.7,
        )

    ax.set_title("2D Embeddings")
    ax.legend()

    print("Saving plot")
    plt.savefig(os.path.join(DATA_DIR, "tsne_2D.png"), bbox_inches="tight")

    plt.show()

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time taken: {total_time} seconds")
