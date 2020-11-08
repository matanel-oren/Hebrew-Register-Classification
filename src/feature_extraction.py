from yap_wrapper.yap_api import YapApi
import numpy as np
import pandas as pd
import os
from tqdm import tqdm
import pickle


def get_tagged_sents_from_file(filename):
    with open(filename, encoding='utf8') as file:
        lines = file.read().split('\n')
        return [line.split('\t')[0] for line in lines]


def get_untagged_sents_from_file(filename):
    with open(filename, encoding='utf8') as file:
        return file.read().split('\n')


def produce_yap_data_frames(yap_api, ip, sents):
    total_df = pd.DataFrame({'sent': [], 'dep_tree': []})
    if sents:
        for sent in tqdm(sents):
            _, _, _, dep_tree, _, _ = yap_api.run(sent, ip)
            df = pd.DataFrame(
                {'sent': [sent], 'dep_tree': [dep_tree]})
            total_df = total_df.append(df)
    return total_df


def extract_morphology(dep_tree):
    parsed_list = []
    for pos, empty in zip(dep_tree['pos'], dep_tree['empty']):
        parsed_list.append(str('pos=' + pos + '|morph:' + empty))
    return parsed_list


def extract_syntax(dep_tree):
    parsed_list = []
    for pos, dependency_part, dependency_arc in zip(dep_tree['pos'], dep_tree['dependency_part'],
                                                    dep_tree['dependency_arc']):
        dep_pos = 'ROOT' if dependency_arc == '0' else dep_tree.at[int(dependency_arc) - 1, 'pos']
        if type(dep_pos) is not str:
            dep_pos = dep_pos[-1]
        parsed = 'pos=' + pos + '|dep_pos=' + dep_pos + '|dep_part=' + dependency_part
        parsed_list.append(parsed)
    return parsed_list


def features_hist(features_list):
    hist = {}
    for feature in features_list:
        if feature in hist:
            hist[feature] += 1
        else:
            hist[feature] = 1
    return hist


def create_dict_from_feature_to_vector_inx(features_hist_dict, threshold):
    survived_features = [morph for morph in features_hist_dict if features_hist_dict[morph] >= threshold]
    feature_to_inx = {morph: inx for inx, morph in enumerate(survived_features)}
    feature_to_inx['other'] = len(survived_features)
    return feature_to_inx


def make_features_vector(features_dict, features_list):
    features_vector = np.zeros(len(features_dict))
    for feature in features_list:
        if feature in features_dict:
            features_vector[features_dict[feature]] += 1
        else:
            features_vector[features_dict['other']] += 1
    return features_vector / len(features_list)


def get_or_create_dfs(dfs_pkl_path):
    if not os.path.isdir(dfs_pkl_path) or not \
            {'tagged_train.pkl', 'untagged_train.pkl', 'test.pkl'}.issubset(set(os.listdir(dfs_pkl_path))):
        ip = '127.0.0.1:8000'
        yap_api = YapApi()
        tagged_train_df = produce_yap_data_frames(yap_api, ip,
                                                  get_tagged_sents_from_file('../data/tagged/tagged_train_sents.tsv'))
        untagged_train_df = produce_yap_data_frames(yap_api, ip,
                                                    get_untagged_sents_from_file('../data/chosen/merged_1.txt'))
        test_df = produce_yap_data_frames(yap_api, ip,
                                          get_tagged_sents_from_file('../data/tagged/tagged_test_sents.tsv'))

        if not os.path.isdir(dfs_pkl_path):
            os.mkdir(dfs_pkl_path)

        tagged_train_df.to_pickle(os.path.join(dfs_pkl_path, 'tagged_train.pkl'))
        untagged_train_df.to_pickle(os.path.join(dfs_pkl_path, 'untagged_train.pkl'))
        test_df.to_pickle(os.path.join(dfs_pkl_path, 'test.pkl'))

    else:
        tagged_train_df = pd.read_pickle(os.path.join(dfs_pkl_path, 'tagged_train.pkl'))
        untagged_train_df = pd.read_pickle(os.path.join(dfs_pkl_path, 'untagged_train.pkl'))
        test_df = pd.read_pickle(os.path.join(dfs_pkl_path, 'test.pkl'))

    return tagged_train_df, untagged_train_df, test_df


def morph_features_extraction(dfs_pkl_path):
    tagged_train_df, untagged_train_df, test_df = get_or_create_dfs(dfs_pkl_path)

    tagged_train_sents_morphs = [extract_morphology(dep_tree) for dep_tree in tagged_train_df['dep_tree'].tolist()]
    untagged_train_sents_morphs = [extract_morphology(dep_tree) for dep_tree in untagged_train_df['dep_tree'].tolist()]
    tests_sents_morphs = [extract_morphology(dep_tree) for dep_tree in test_df['dep_tree'].tolist()]

    all_morph_features_train = [morph_feature for sent_morphs in tagged_train_sents_morphs + untagged_train_sents_morphs
                                for morph_feature in sent_morphs]
    morph_features_hist = features_hist(all_morph_features_train)
    morph_to_vector_inx_dict = create_dict_from_feature_to_vector_inx(morph_features_hist, 20)

    pickle.dump(morph_to_vector_inx_dict, open('morph_to_vector_inx_dict.p', 'wb'))

    tagged_train_feature_vectors = np.array([make_features_vector(morph_to_vector_inx_dict, sent_morphs)
                                             for sent_morphs in tagged_train_sents_morphs])
    untagged_train_feature_vectors = np.array([make_features_vector(morph_to_vector_inx_dict, sent_morphs)
                                               for sent_morphs in untagged_train_sents_morphs])
    test_feature_vectors = np.array([make_features_vector(morph_to_vector_inx_dict, sent_morphs)
                                     for sent_morphs in tests_sents_morphs])

    return tagged_train_feature_vectors, untagged_train_feature_vectors, test_feature_vectors


def syntax_feature_extraction(dfs_pkl_path):
    tagged_train_df, untagged_train_df, test_df = get_or_create_dfs(dfs_pkl_path)

    tagged_train_sents_syns = [extract_syntax(dep_tree) for dep_tree in tagged_train_df['dep_tree'].tolist()]
    untagged_train_sents_syns = [extract_syntax(dep_tree) for dep_tree in untagged_train_df['dep_tree'].tolist()]
    tests_sents_syns = [extract_syntax(dep_tree) for dep_tree in test_df['dep_tree'].tolist()]

    all_syn_features_train = [syn_feature for sent_syns in tagged_train_sents_syns + untagged_train_sents_syns
                                for syn_feature in sent_syns]
    syn_features_hist = features_hist(all_syn_features_train)
    syn_to_vector_inx_dict = create_dict_from_feature_to_vector_inx(syn_features_hist, 100)

    pickle.dump(syn_to_vector_inx_dict, open('syn_to_vector_inx_dict.p', 'wb'))

    tagged_train_feature_vectors = np.array([make_features_vector(syn_to_vector_inx_dict, sent_syns)
                                             for sent_syns in tagged_train_sents_syns])
    untagged_train_feature_vectors = np.array([make_features_vector(syn_to_vector_inx_dict, sent_syns)
                                               for sent_syns in untagged_train_sents_syns])
    test_feature_vectors = np.array([make_features_vector(syn_to_vector_inx_dict, sent_syns)
                                     for sent_syns in tests_sents_syns])

    return tagged_train_feature_vectors, untagged_train_feature_vectors, test_feature_vectors


def sentences_length_extraction(dfs_pkl_path):
    tagged_train_df, untagged_train_df, test_df = get_or_create_dfs(dfs_pkl_path)

    tagged_train_sents = tagged_train_df['sent'].tolist()
    test_sents = test_df['sent'].tolist()

    train_lengths = np.array([[len(sent)] for sent in tagged_train_sents])
    test_lengths = np.array([[len(sent)] for sent in test_sents])

    return train_lengths, test_lengths


if __name__ == '__main__':
    pkl_path = '../data/data_frames'

    tagged_train_feature_vectors, untagged_train_feature_vectors, test_feature_vectors = morph_features_extraction(pkl_path)
    if not os.path.isdir('extracted'):
        os.mkdir('extracted')
    np.save('extracted/train_tagged_morph', tagged_train_feature_vectors)
    np.save('extracted/train_untagged_morph', untagged_train_feature_vectors)
    np.save('extracted/test_morph', test_feature_vectors)

    tagged_train_feature_vectors, untagged_train_feature_vectors, test_feature_vectors = syntax_feature_extraction(pkl_path)
    np.save('extracted/train_tagged_syn', tagged_train_feature_vectors)
    np.save('extracted/train_untagged_syn', untagged_train_feature_vectors)
    np.save('extracted/test_syn', test_feature_vectors)

    train_lengths, test_lengths = sentences_length_extraction(pkl_path)
    np.save('extracted/train_lengths', train_lengths)
    np.save('extracted/test_lengths', test_lengths)
