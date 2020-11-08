import os
from tqdm import tqdm
from random import randint, sample, shuffle


def reduce_data(ready_base, chosen_base, choosing_num, sents_to_choose_by_subdir):
    if not os.path.isdir(chosen_base):
        os.mkdir(chosen_base)
    os.mkdir(os.path.join(chosen_base, str(choosing_num)))

    for dir in sents_to_choose_by_subdir:
        first = True
        print(dir)
        with open(os.path.join(chosen_base, dir + '.txt'), 'w', encoding='utf8') as outfile:
            filenames = set(os.listdir(os.path.join(ready_base, dir)))
            for i in tqdm(range(sents_to_choose_by_subdir[dir])):
                chosen_file_name = sample(filenames, 1)[0]
                chosen_file_path = os.path.join(ready_base, dir, chosen_file_name)
                with open(chosen_file_path, 'r', encoding='utf8') as file:
                    sents = file.read().split('\n')
                chosen_sent_index = randint(0, len(sents) - 1)
                if not first:
                    outfile.write('\n')
                else:
                    first = False
                outfile.write(sents[chosen_sent_index])
                if len(sents) > 1:
                    with open(chosen_file_path, 'w', encoding='utf8') as file:
                        sents = sents[:chosen_sent_index] + sents[chosen_sent_index + 1:]
                        file.write('\n'.join(sents))
                else:
                    os.remove(chosen_file_path)
                    filenames.remove(chosen_file_name)


def split_test_and_merge_train(chosen_base, choosing_num, num_of_test_samples=1000):
    chosen_dir = os.path.join(chosen_base, str(choosing_num))
    sents = []
    for file_name in os.listdir(chosen_dir):
        with open(os.path.join(chosen_dir, file_name), 'r', encoding='utf8') as file:
            sents += file.read().split('\n')

    shuffle(sents)
    test = sents[:num_of_test_samples]
    train = sents[num_of_test_samples:]

    with open('../data/chosen/merged_' + str(choosing_num) + '.txt', 'w', encoding='utf8') as file:
        file.write('\n'.join(train))
    with open('../data/chosen/test_' + str(choosing_num) + '.txt', 'w', encoding='utf8') as file:
        file.write('\n'.join(test))


if __name__ == '__main__':
    ready_base = '../data/ready'
    chosen_base = '../dat/achosen'
    sents_to_choose_by_subdir = {'ben_yehuda_project': 10000, 'NITE_Wiki_2013': 10000, 'thinks': 10000,
                                 'whatsapp': 20000}
    reduce_data(ready_base, chosen_base, 1, sents_to_choose_by_subdir)
    split_test_and_merge_train(chosen_base, 1)
