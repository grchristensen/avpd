#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from os.path import join
import pandas as pd
from pathlib import Path
import pdpipe as pdp
import sys
import numpy as np
from tqdm import tqdm

project_root = Path('..')
sys.path.append(os.path.abspath(project_root))
from notebooks.utils import init_data_dir, extract_author_texts  # noqa

from notebooks import pipes
from notebooks.profiles import EuclideanProfile, NaiveBayesProfile
from notebooks import benchmarking as bench
from notebooks.feature_extractors import HeuristicsExtractor, FunctionWordCounter, POS2GramCounter
from notebooks.thresholders import SimpleAccuracyThresholder, SimpleThresholder

init_data_dir(project_root)

preprocess_path = join(project_root, Path('data/preprocess'))
outputs_path = join(project_root, 'outputs')

train_df = pd.read_hdf(join(preprocess_path, 'bawe_train_sentences.hdf5'))
valid_df = pd.read_hdf(join(preprocess_path, 'bawe_valid_sentences.hdf5'))

train_df = train_df.rename(columns={"sentence": "text"})
valid_df = valid_df.rename(columns={"sentence": "text"})


# In[2]:


# feature_extractors = [(HeuristicsExtractor(), "heuristics_extractor")]
feature_extractors = [(POS2GramCounter(), "pos2gram_counter"), (FunctionWordCounter(), "function_word_counter")]

profiles = [(EuclideanProfile(), "euclidean_distance_profile")]
# profiles = [(NaiveBayesProfile(), "naive_bayes_profile")]

thresholders = [(SimpleThresholder(bench.balanced_accuracies), "balanced_accuracy_thresholder")]


# In[3]:


preprocessed_dfs = []

for feature_extractor, display_name in feature_extractors:
    train_path = join(preprocess_path, f"bawe_train_preprocessed_{display_name}.hdf5")
    valid_path = join(preprocess_path, f"bawe_valid_preprocessed_{display_name}.hdf5")

    preprocessed_train_exists = os.path.exists(train_path)
    preprocessed_valid_exists = os.path.exists(valid_path)

    if not (preprocessed_train_exists and preprocessed_valid_exists):
        print(f"Preprocessing train dataset for {display_name}", flush=True)
        preprocessed_train_df = feature_extractor(train_df, show_loading=True)
        print(f"Preprocessing valid dataset for {display_name}", flush=True)
        preprocessed_valid_df = feature_extractor(valid_df, show_loading=True)

        preprocessed_train_df.to_hdf(train_path, key=f"bawe_train_preprocessed_{display_name}")
        preprocessed_valid_df.to_hdf(valid_path, key=f"bawe_valid_preprocessed_{display_name}")
    else:
        preprocessed_train_df = pd.read_hdf(train_path)
        preprocessed_valid_df = pd.read_hdf(valid_path)

    preprocessed_dfs.append((preprocessed_train_df, preprocessed_valid_df, display_name))


# In[6]:


function_train, function_valid, _ = preprocessed_dfs[1]


# In[47]:


overall_var = function_train.var()

average_author_var = function_train.groupby(level="author").var().mean()


# In[48]:


useful_features = ((overall_var - average_author_var) / overall_var) > 0

actual_words = useful_features[useful_features].index.tolist()


# In[49]:


better_function_train, better_function_valid = function_train[actual_words], function_valid[actual_words]


# In[41]:


def train_threshold(profile, df, thresholder):
    author_set = set(df.index.get_level_values(0))

    print("Training...", flush=True)
    distance_sets = []
    true_flag_sets = []
    for author in tqdm(author_set):
        profile.reset()

        author_texts, rest_df = extract_author_texts(author, df)
        profile.feed(author_texts)
        distances = profile.distances(rest_df)

        true_flags = distances.index.get_level_values(0) != author

        distance_sets.append(distances.to_numpy())
        true_flag_sets.append(true_flags)

    distances = np.concatenate(distance_sets)
    true_flags = np.concatenate(true_flag_sets)

    return thresholder(distances, true_flags)


def test_profile(profile, threshold, df):
    author_set = set(df.index.get_level_values(0))

    print("Testing...", flush=True)
    flag_sets = []
    true_flag_sets = []
    for author in tqdm(author_set):
        profile.reset()

        author_texts, rest_df = extract_author_texts(author, df)
        profile.feed(author_texts)
        distances = profile.distances(rest_df)

        flags = distances > threshold
        true_flags = distances.index.get_level_values(0) != author

        flag_sets.append(flags.to_numpy())
        true_flag_sets.append(true_flags)

    flags = np.concatenate(flag_sets)
    true_flags = np.concatenate(true_flag_sets)

    return [bench.balanced_accuracy(flags, true_flags)]


# In[42]:


threshold = train_threshold(EuclideanProfile(), better_function_train, SimpleThresholder(bench.balanced_accuracies))


# In[45]:


scores = test_profile(EuclideanProfile(), threshold, better_function_valid)


# In[46]:


scores


# In[61]:


better_function_train = function_train[actual_words]

chosen_author_texts = better_function_train.loc[(6212,)]

author_means = function_train[actual_words].groupby(level="author").mean()
other_author_means = author_means.drop(index=6212)


# In[62]:


other_author_means


# In[63]:


chosen_author_means = chosen_author_texts.groupby(level="text_id").mean()
chosen_author_means
np.linalg.norm(chosen_author_means.iloc[0] - chosen_author_means.iloc[1])


# In[64]:


np.mean(np.linalg.norm(chosen_author_means.iloc[0] - other_author_means, axis=1))


# In[4]:


# heuristics_train = preprocessed_dfs[0][0]
# heuristics_test = preprocessed_dfs[0][1]

# scaled_heuristics_train = (heuristics_train - heuristics_train.mean()) / heuristics_train.std()
# scaled_heuristics_test = (heuristics_test - heuristics_test.mean()) / heuristics_test.std()
# preprocessed_dfs.append((scaled_heuristics_train, scaled_heuristics_test, "scaled_heuristics"))

# function_words_train = preprocessed_dfs[0][0]
# function_words_test = preprocessed_dfs[0][1]
# pca_train = function_words_train

# pca_standardized = (pca_train - pca_train.mean()) / pca_train.std()

# pca_cov = pca_standardized.cov()

# pca_eigvals, pca_eigvecs = np.linalg.eig(pca_cov)
# sort_indices = np.flip(np.argsort(pca_eigvals))
# pca_eigvals, pca_eigvecs = pca_eigvals[sort_indices], pca_eigvecs[sort_indices]

# transformation_matrix0 = pca_eigvecs[:, :5]
# transformation_matrix1 = pca_eigvecs[:, :10]
# transformation_matrix2 = pca_eigvecs[:, :15]
# transformation_matrix3 = pca_eigvecs[:, :20]

# pca_function_words_train0 = function_words_train.dot(transformation_matrix0)
# pca_function_words_test0 = function_words_test.dot(transformation_matrix0)
# pca_function_words_train1 = function_words_train.dot(transformation_matrix1)
# pca_function_words_test1 = function_words_test.dot(transformation_matrix1)
# pca_function_words_train2 = function_words_train.dot(transformation_matrix2)
# pca_function_words_test2 = function_words_test.dot(transformation_matrix2)
# pca_function_words_train3 = function_words_train.dot(transformation_matrix3)
# pca_function_words_test3 = function_words_test.dot(transformation_matrix3)

# preprocessed_dfs.append((pca_function_words_train0, pca_function_words_test0, "pca_function_words0"))
# preprocessed_dfs.append((pca_function_words_train1, pca_function_words_test1, "pca_function_words1"))
# preprocessed_dfs.append((pca_function_words_train2, pca_function_words_test2, "pca_function_words2"))
# preprocessed_dfs.append((pca_function_words_train3, pca_function_words_test3, "pca_function_words3"))

# function_words_train = preprocessed_dfs[0][0]
# function_words_test = preprocessed_dfs[0][1]
# pca_train = function_words_train

# pca_standardized = (pca_train - pca_train.mean()) / pca_train.std()

# pca_cov = pca_standardized.cov()

# pca_eigvals, pca_eigvecs = np.linalg.eig(pca_cov)
# sort_indices = np.flip(np.argsort(pca_eigvals))
# pca_eigvals, pca_eigvecs = pca_eigvals[sort_indices], pca_eigvecs[sort_indices]

# transformation_matrix0 = pca_eigvecs[:, :5]
# transformation_matrix1 = pca_eigvecs[:, :10]
# transformation_matrix2 = pca_eigvecs[:, :15]
# transformation_matrix3 = pca_eigvecs[:, :20]

# pca_function_words_train0 = function_words_train.dot(transformation_matrix0)
# pca_function_words_test0 = function_words_test.dot(transformation_matrix0)
# pca_function_words_train1 = function_words_train.dot(transformation_matrix1)
# pca_function_words_test1 = function_words_test.dot(transformation_matrix1)
# pca_function_words_train2 = function_words_train.dot(transformation_matrix2)
# pca_function_words_test2 = function_words_test.dot(transformation_matrix2)
# pca_function_words_train3 = function_words_train.dot(transformation_matrix3)
# pca_function_words_test3 = function_words_test.dot(transformation_matrix3)

# preprocessed_dfs.append((pca_function_words_train0, pca_function_words_test0, "pca_function_words0"))
# preprocessed_dfs.append((pca_function_words_train1, pca_function_words_test1, "pca_function_words1"))
# preprocessed_dfs.append((pca_function_words_train2, pca_function_words_test2, "pca_function_words2"))
# preprocessed_dfs.append((pca_function_words_train3, pca_function_words_test3, "pca_function_words3"))


# In[5]:


def train_threshold(profile, df, thresholder):
    author_set = set(df.index.get_level_values(0))

    print("Training...", flush=True)
    distance_sets = []
    true_flag_sets = []
    for author in tqdm(author_set):
        profile.reset()

        author_texts, rest_df = extract_author_texts(author, df)
        profile.feed(author_texts)
        distances = profile.distances(rest_df)

        true_flags = distances.index.get_level_values(0) != author

        distance_sets.append(distances.to_numpy())
        true_flag_sets.append(true_flags)

    distances = np.concatenate(distance_sets)
    true_flags = np.concatenate(true_flag_sets)

    return thresholder(distances, true_flags)


def test_profile(profile, threshold, df):
    author_set = set(df.index.get_level_values(0))

    print("Testing...", flush=True)
    flag_sets = []
    true_flag_sets = []
    for author in tqdm(author_set):
        profile.reset()

        author_texts, rest_df = extract_author_texts(author, df)
        profile.feed(author_texts)
        distances = profile.distances(rest_df)

        flags = distances > threshold
        true_flags = distances.index.get_level_values(0) != author

        flag_sets.append(flags.to_numpy())
        true_flag_sets.append(true_flags)

    flags = np.concatenate(flag_sets)
    true_flags = np.concatenate(true_flag_sets)

    return [bench.balanced_accuracy(flags, true_flags)]


score_data = []
thresholds = []
model_names = []

for profile, profile_name in profiles:
    for thresholder, thresholder_name in thresholders:
        for preprocessed_train_df, preprocessed_valid_df, extractor_name in preprocessed_dfs:
            threshold = train_threshold(profile, preprocessed_train_df, thresholder)
            thresholds.append(threshold)
            profile.reset()

            scores = test_profile(pr
                                  ofile, threshold, preprocessed_valid_df)
            score_data.append(scores)
            model_names.append(f"{profile_name}-{thresholder_name}-{extractor_name}")


# In[6]:


score_data, model_names


# In[7]:


# test_profile(EuclideanProfile(), thresholds[0], preprocessed_dfs[0][0])


# In[8]:


# sentence_count = len(function_words_train)

# where_true = ((function_words_train.sum() / (sentence_count / 100)) > 1)

# chosen_word_indices = where_true[where_true].index.tolist()


# In[9]:


# with open("../notebooks/resources/original_function_words.txt") as f:
#     words = f.readlines()


# In[10]:


# chosen_words = [words[chosen_index] for chosen_index in chosen_word_indices]


# In[11]:


# with open("../notebooks/resources/filtered_function_words.txt", "w") as f:
#     f.writelines(chosen_words)


# The threshold may be overfitting to individual author texts, not the dataset

# In[12]:


# score_data = np.concatenate([results[None, :] for results in score_data])

# results_df = pd.DataFrame(np.array(score_data), index=model_names, columns=["balanced_accuracy"])

# results_df

