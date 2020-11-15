# Hebrew-Register-Classification

This project was originally created as a final project for "Workshop in Hebrew Natural Language Processing" (67680) course from the Hebrew University of Jerusalem.

The goal of this project is to develop a classifier that can distinguish between registers of the written Hebrew based on only one sentence.

## The problem

One way to examine the texts we read is through the [linguistic register](https://en.wikipedia.org/wiki/Register_(sociolinguistics)) used to write the text. For us as humans it is clear and easy usually to understand what type of language is appropriate for academic writing, poetry and literature writing, news stories, chats or different types of social networks. Moreover, when we encounter a use of an inappropriate 'version' of language to the social context, it will seem strange to us, even without knowing how to put our finger on what exactly is bothering us.

Over the years, some works have been done in the field of identifying the register and creating texts according to a desired register, but I do not know any work done on the subject on the Hebrew language.

It is important to note that registers exist in both the spoken language and the written language, but since the spoken language requires additional mediation (and not a simple one at all) so that we can analyze it with a computer, I chose to deal only with the written language.

There are works on the subject that have tried to categorize entire documents by register, but because we (humans) are intuitively able to distinguish the register even on a single sentence, and because sometimes one document uses several different registers, I chose to try classifying each sentence individually.

For more information about Hebrew registers see [משלב](https://he.wikipedia.org/wiki/%D7%9E%D7%A9%D7%9C%D7%91).
In this entry, the writers have specified 4 distinct register, but since the differences and hence the distinction between the last two (לשון מדוברת and לשון תת-תקנית) are not clear enough (at least for me), I decided to classify into only 3 registers:
- Formal, לשון גבוהה / מליצית.
- Standard, לשון תקנית.
- Casual, לשון מדוברת / תת תקנית.

In fact, we will define "formal", the sentences use special, uncommon, or "high" (not well defined) idioms, words, or structures.
"Standard" will be sentences that comply with the language's standard, but don't include anything special.
And as "casual" we will define any sentence that doesn't meet the standard.

You probably have noticed that the differences between these registers are expressed through many aspects of the language.
The aspects I Chose to focus on them are: lexicon, morphology, and syntax.
A few examples of those (in Hebrew):
- Lexicon: הצילו (standard) vs. הושיעו (more formal). ירח (standard) vs. סהר or לבנה (more formal).
- Morphology: אינני (formal) vs. אני לא (standard) vs. אנלא (casual). כאשר הלכתי (formal) vs. כשהלכתי (standard) vs. שהלכתי (casual).
- Syntax: אורי הלך לביתו (standard) vs. הלך אורי לביתו (more formal).

## Data

The data collecting task was challenging, because one corpus tends to follow the same register through its texts. In terms of registers, data from a single source tends to be identical or very close from a integrator. Examples: In a journal or a newspaper there is an editor who makes sure that the texts are written in a certain style and for a certain readership; in Wikipedia there are [guidelines](https://he.wikipedia.org/wiki/%D7%95%D7%99%D7%A7%D7%99%D7%A4%D7%93%D7%99%D7%94:%D7%A2%D7%A7%D7%A8%D7%95%D7%A0%D7%95%D7%AA_%D7%95%D7%A7%D7%95%D7%95%D7%99%D7%9D_%D7%9E%D7%A0%D7%97%D7%99%D7%9D) that each of the writers should follow; In a group WhatsApp conversation participants tend to talk "at the same height". Furthermore in order to prevent biases, it is recommended that each of them will deal with various topics, thus avoiding the classifier perceiving the wrong phenomenon, i.e. to really classify by topics when we want it to classify by register.

In practice, I used sources that by my understanding supposed to cover all the registers:
- [Ben Yehuda Project](https://github.com/projectbenyehuda) - a huge library of public domain Hebrew literary texts (copyrights were expired), most of them are very old. Since these are literary works, especially those written at a time when it was more common to write in "high" language, I assumed that it will be a good source for "high" sentences.
- [Thinks](https://thinkil.co.il/) - A website includes articles in medium-high level in various topics, like philosophy, psychology and physics.
- The [Hebrew Wikipedia](https://he.wikipedia.org/) as it was collected by NITE in 2013. (To get it, browse [here](https://hlp.nite.org.il/WebCorpora.aspx).) Being an encyclopedia, its entries deal with a wide variety of topics, Most of them were written in "medium" register.
- WhatsApp chats -  The popular app allows you to export the chats to text files. Most of the chats are group chats that I got from my family members as they were exported by the application.

For privacy and copyrights reasons, I can't publish the data itself, so I put an example file in each of the folders (except of "thinks" that the script itself download the pages from the website).

## Pipeline

### Data cleaning

For the purpose of cleaning the data, I mainly used regular expressions, which managed in an acceptable way to overcome the various cleaning problems that were found in each of the data sources.

The following are examples of cleaning issues by source:
- Ben Yehuda project - the website's signature, different types of titles, spaces, and separators.
- Thinks - It is a website, requires extracting from HTML pages. I used BeautifulSoup library was for this purpose.
- Hebrew Wikipedia - use of many types of signs, words from different languages, types of parentheses, etc.
- WhatsApp chats - the chats are exported in a very noisy format, including the senders' names, time of sending, "נוסף" and "עזב" comments, attachment of contacts, and many more.

An important note: during the cleaning process I noticed that for very short sentences there usually there is no meaning to the register classification.
This because they are usually in kind of "תודה רבה", "בוקר טוב" and "פרק שלישי".
Therefore, I choose to deal with sentences that have four words or more, which also made the cleaning process it self easier.

### Sampling

After the cleaning, a huge amount of sentences were gotten (about 5 million), and there was a large bias
in favor of the large group that is the Ben Yehuda project. It was necessary to sample more uniformly,
so that the model could learn in a non-biased manner (what is called under-sampling).
This was done in *choose_data.py* file.

### Tagging

For the implementation of supervised learning, of course, tagged data is needed.
Since there were no such data available for my problem, I sat down to tag sentences one by one.
Moreover, this required a convenient and suitable tool for labeling,
and I quickly realized that it the easiest way to get such one to develop it by myself.
This tool was developed using QT for python library, and its code was included in the *tagging_tool* module.

I am not an expert in that field (linguistics), and due to the lack of a precise definition of the distinguishes between the various registers,
it is difficult to say that my work was particularly consistent. This makes the learning more difficult,
and even sets an upper bound on the performance of any theoretical classifier.

Two thousand sentences were totally tagged, and they were divided into 1000 for training and 1000 for test.
This irregular division was made when I still thought I would use semi-supervised methods.
In retrospect, for enabling a better supervised learning, the training set should be much greater than the test,
as common.

### YAP

YAP is an open source morpho-syntactic parser for Hebrew language. It was developed by the [Bar-Ilan University ONLP lab](https://nlp.biu.ac.il/~rtsarfaty/onlp), under the supervision of Prof. Reut Tsarfaty. Currently the best Hebrew parser who is free. The main idea behind it is to apply the morphological and the syntactic analysis at the same time, this for preventing the basic problem of the dependency of morphology and syntax when you come to parse Hebrew texts. YAP documentation and demonstration is available [here](https://nlp.biu.ac.il/~rtsarfaty/onlp/hebrew/), and the code is available [here](https://github.com/OnlpLab/yap)

The models YAP is based on them are very heavy, and therefore it is written in GO, to achieve a better runtime. The access to it is hence more difficult and done by HTTP requests. Amit Skolnik has written a python wrapper to simplify the process, and I used it.

### Feature extraction

It is important to note here that the use of "low" language includes many errors, not only grammatical,
but also spelling and typing errors of many types, which makes the syntactic analysis by automated tools (such as YAP) much difficult.
One approach can try to deal with the problem by trying to fix those errors in one method or another,
but since this is a key feature of this register, I chose to leave the sentences as they are.
The way YAP deals with such issues itself can be a feature of this register, although it increases our dependence on the behavior of YAP,
which reduces our ability to understand and analyze what the features say.

Because of this, and the problems presented in the data chapter, i.e. lack of sufficient variety and a limited amount of tagged examples,
I chose not to use the classic method of word-counting (bag-of-words etc.), but to try to classify using morphological and syntactic features.
For this purpose we need of course to use YAP. Its wrapper written by Amit Shkolnik and recently published in open source was very useful.

Morphological features were represented by strings that concatenate the POS tag with the other morphological features that YAP analyzed
such as gender, number, time, and so on. (Although POS is primarily a syntactic feature, it also describes the word type: noun, verb,
adjective, etc. and therefore had to be included in the morphological features.) I also passed a threshold on the number of repetitions
of a feature over all the training set (including the untagged part) to be included in the features vector, in order to prevent the vector
to be too large (and hence sparse), and allow an effective learning.

Regarding the producing of the syntactic features, on one hand they are by nature very diverse and cause the known problem of sparsity,
even more when it comes to a relatively small amount of data. But on the other hand, there are features that we can guess they have a big
influence on the classifier's ability to succeed, such as the lengths of the arcs (for example, the distance between the subject and the verb).
Finally I chose to use a relatively limited approach, and to include the labels of the arcs and POS tag they connect.
Even after this reducing there were too many features, so I used again a threshold of 100 repetitions of a feature over all the training set
(including its untagged part) to be included in the features vector.

After producing the features, I used a bag-of-words-like method i.e. producing the vectors by counting repetitions of the features,
and normalizing by the length of the sentence.

### Learning

If we treat the problem as a classic supervised classification problem, one can very easily try many classifiers, with the help of the sklearn library and so I did.

The great advantage of such classifiers is the simplicity and ease in which they can be operated, but their disadvantages is their limitations on relatively small amounts of data, and the falling into biases.
There are several ways we can try to overcome these problems, but in the frame of the course I didn't have enough time to try them in a satisfactory way. In the chapter 'Further work' I describe one way I guess it has a change to achieve better results on the same data.

### Evaluation

Because this is a classification problem, there are common ways to evaluate success. Since we do not have a particular preference in terms of the type of errors we prefer, I mainly used f1-score and accuracy.

Apart from the difference in results between different classifiers (in term of the learning methods), I used for the purpose of evaluation different types of features:
- "Dummy" classifier - Always chooses the most common class which is the standard register.
- "Naïve" classifier -  Uses only the rule of thumb of the sentence length, that is, classifies by a single feature of the length of the sentence (in characters).
- Morphological classifier - Classified according to morphological features only.
- Syntactic Classifier - Classified according to syntactic features only.
- Combined Classifier - Concatenates the morphological and syntactic feature vectors.

#### Results

Here are the results:

|                   | f1 (macro) | accuracy | best classifier      |
|-------------------|------------|----------|----------------------|
| **"Dummy"**       | 0.24       | 0.58     | -                    |
| **"Naïve"**       | 0.51       | 0.63     | gaussian naive bayes |
| **Morphological** | 0.58       | 0.64     | decision tree        |
| **Syntactic**     | 0.54       | 0.69     | SVC                  |
| **Combined**      | 0.63       | 0.73     | SGD                  |

We can see that, surprisingly, the "naïve" classifier did a very nice work, and the other classifiers worked very hard (in terms of the number of features) but their success was limited. It is interesting to see that the morphological raised significantly the f1 more compared to the syntactic which improved significantly the accuracy. In any case, the combined one seems to have done a good work given the inconsistency of the tagging.

## Further work

*I'm still working on the rest. Will be completed soon.*

## Running



## Credits

Thanks to Amit Shkolnik for [Yap-Wrapper](https://github.com/amit-shkolnik/YAP-Wrapper) module.
I haven't modified any file in it, so all of the copyrights are under [his license](https://github.com/amit-shkolnik/YAP-Wrapper/blob/master/LICENSE).
