import os

import numpy as np
import pandas as pd

from const import DATA_DIR

num_comments_per_genre = 10_000
# genres = ["pop", "metal", "rock", "hip_hop_rap", "classical", "blues"]
genres = ["pop", "metal", "hip_hop_rap", "classical"]

if __name__ == "__main__":
    # data loading
    with open(os.path.join(DATA_DIR, "embeddings_final.npy"), "rb") as f:
        numpy_embeddings = np.load(f)

    df_comments = pd.read_csv(
        os.path.join(DATA_DIR, "combined_final.csv"), encoding="utf-8"
    )

    # initialize empty DataFrames for each genre
    df_pop = pd.DataFrame(columns=df_comments.columns)
    df_metal = pd.DataFrame(columns=df_comments.columns)
    df_rock = pd.DataFrame(columns=df_comments.columns)
    df_hip_hop_rap = pd.DataFrame(columns=df_comments.columns)
    df_classical = pd.DataFrame(columns=df_comments.columns)
    df_blues = pd.DataFrame(columns=df_comments.columns)

    # limit each genre
    for genre in genres:
        df_genre = df_comments[df_comments["genre"] == genre].head(10_000)

        if genre == "pop":
            df_pop = pd.concat([df_pop, df_genre])
        elif genre == "metal":
            df_metal = pd.concat([df_metal, df_genre])
        elif genre == "rock":
            df_rock = pd.concat([df_rock, df_genre])
        elif genre == "hip_hop_rap":
            df_hip_hop_rap = pd.concat([df_hip_hop_rap, df_genre])
        elif genre == "classical":
            df_classical = pd.concat([df_classical, df_genre])
        elif genre == "blues":
            df_blues = pd.concat([df_blues, df_genre])

    # combine genres
    df_combined = pd.concat(
        [df_pop, df_metal, df_rock, df_hip_hop_rap, df_classical, df_blues]
    ).sample(frac=1)

    # limit embeddings
    selected_indices = df_combined.index
    filtered_numpy_embeddings = numpy_embeddings[selected_indices]

    # save results to files
    df_combined.to_csv(
        os.path.join(DATA_DIR, "filtered_combined_final.csv"),
        index=False,
        encoding="utf-8",
    )

    with open(os.path.join(DATA_DIR, "filtered_embeddings_final.npy"), "wb") as file:
        np.save(file, filtered_numpy_embeddings)
