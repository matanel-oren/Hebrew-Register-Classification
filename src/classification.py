import numpy as np
import pickle
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score

TAGS_TO_NUM = {'formal': 1, 'neutral': 0, 'casual': -1}


def extract_tags(filename):
    with open(filename, encoding='utf8') as file:
        lines = file.read().split('\n')
        tags = [line.split('\t')[1] for line in lines]
        return [TAGS_TO_NUM[tag] for tag in tags]


def classification(train_X, train_Y, test_X, test_Y):
    classifiers = [RandomForestClassifier(), SGDClassifier(), KNeighborsClassifier(), GaussianNB(),
                   DecisionTreeClassifier(), SVC()]
    classifiers_names = ['Random Forest', 'SGD', 'K Neighbors', 'Gaussian Naive Bayes', 'Decision Tree', 'SVC']
    for classifier, classifier_name in zip(classifiers, classifiers_names):
        classifier.fit(train_X, train_Y)
        pred = classifier.predict(test_X)
        print(classifier_name, f1_score(test_Y, pred, labels=[1, 0, -1], average='macro'))

    classifier = SGDClassifier().fit(train_X, train_Y)
    pred = classifier.predict(test_X)
    print(classification_report(test_Y, pred, labels=[1, 0, -1], target_names=['high', 'medium', 'low']))
    print(classification_report(test_Y, np.zeros(1000), labels=[1, 0, -1], target_names=['high', 'medium', 'low']))


def classification_by_morphology():
    train_X = np.load('extracted/train_tagged_morph.npy')
    test_X = np.load('extracted/test_morph.npy')

    train_Y = extract_tags('../data/tagged/tagged_train_sents.tsv')
    test_Y = extract_tags('../data/tagged/tagged_test_sents.tsv')

    classification(train_X, train_Y, test_X, test_Y)

def classification_by_syntax():
    train_X = np.load('extracted/train_tagged_syn.npy')
    test_X = np.load('extracted/test_syn.npy')

    train_Y = extract_tags('../data/tagged/tagged_train_sents.tsv')
    test_Y = extract_tags('../data/tagged/tagged_test_sents.tsv')

    classification(train_X, train_Y, test_X, test_Y)


def classification_by_syntax_and_morphology():
    morph_train_X = np.load('extracted/train_tagged_morph.npy')
    morph_test_X = np.load('extracted/test_morph.npy')
    syn_train_X = np.load('extracted/train_tagged_syn.npy')
    syn_test_X = np.load('extracted/test_syn.npy')

    train_X = np.hstack((morph_train_X, syn_train_X))
    test_X = np.hstack((morph_test_X, syn_test_X))

    train_Y = extract_tags('../data/tagged/tagged_train_sents.tsv')
    test_Y = extract_tags('../data/tagged/tagged_test_sents.tsv')

    classification(train_X, train_Y, test_X, test_Y)


def naive_length_classification():
    train_X = np.load('extracted/train_lengths.npy')
    test_X = np.load('extracted/test_lengths.npy')

    train_Y = extract_tags('../data/tagged/tagged_train_sents.tsv')
    test_Y = extract_tags('../data/tagged/tagged_test_sents.tsv')

    classification(train_X, train_Y, test_X, test_Y)


if __name__ == '__main__':
    naive_length_classification()
    classification_by_morphology()
    classification_by_syntax()
    classification_by_syntax_and_morphology()