# Hebrew-Register-Classification

This project was originally made as a final project for "Workshop in Hebrew Natural Language Processing" (67680) course from the Hebrew University of Jerusalem.

The goal of this project is to develop a classifier that can distinguish between registers of the written Hebrew based on only one sentence.

## The problem

For more information about registers generally in language see [Register](https://en.wikipedia.org/wiki/Register_(sociolinguistics)), and about Hebrew registers see: [משלב](https://he.wikipedia.org/wiki/%D7%9E%D7%A9%D7%9C%D7%91).
In the later, the writers have specified 4 distinct register, but since the differences and hence the distinction between the last two are not clear enough (at least for me), I decided to classify into only 3 registers:
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

The data collecting task was challenging, because one corpus tends to follow the same register across its texts.
For example, in journal or newspaper there is an editor who cares the writing style, in Wikipedia there are [guidelines](https://he.wikipedia.org/wiki/%D7%95%D7%99%D7%A7%D7%99%D7%A4%D7%93%D7%99%D7%94:%D7%A2%D7%A7%D7%A8%D7%95%D7%A0%D7%95%D7%AA_%D7%95%D7%A7%D7%95%D7%95%D7%99%D7%9D_%D7%9E%D7%A0%D7%97%D7%99%D7%9D) that each of the writers should follow.
Therefore, we need several different sources of data, but it is recommended that each of them will deal with various topics, in order to prevent biases.

The sources I was satisfied with them are:
- [Ben Yehuda Project](https://github.com/projectbenyehuda) - a huge library of public domain Hebrew literary texts, most of them are very old.
- [Thinks](https://thinkil.co.il/) - A website includes articles in medium-high level.
- The [Hebrew Wikipedia](https://he.wikipedia.org/) as it was collected by NITE in 2013. (To get it, browse [here](https://hlp.nite.org.il/WebCorpora.aspx))
- WhatsApp chats - group chats that I got from my family members as they exported by the application itself.

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

*Will be completed soon*

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

*I'm still working on the rest. It will be completed soon.*

### Evaluation

## Running

## Further work

## Credits

Thanks to Amit Shkolnik for [Yap-Wrapper](https://github.com/amit-shkolnik/YAP-Wrapper) module.
I haven't modified any file in it, so all of the copyrights are under [his license](https://github.com/amit-shkolnik/YAP-Wrapper/blob/master/LICENSE).
