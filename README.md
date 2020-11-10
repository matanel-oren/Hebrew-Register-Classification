# Hebrew-Register-Classification

This project was originally made as a final project for "Workshop in Hebrew Natural Language Processing" (67680) course from the Hebrew University of Jerusalem.

The goal of this project is to develop a classifier that can distinguish between registers of the written Hebrew based on only one sentence.

## The problem

For more information about registers generally in language see [Register](https://en.wikipedia.org/wiki/Register_(sociolinguistics\)), and about Hebrew registers see: [משלב](https://he.wikipedia.org/wiki/%D7%9E%D7%A9%D7%9C%D7%91).
In the later, the writers have specified 4 distinct register, but since the differences and hence the distinction between the last two are not clear enough (at least for me), I've decided to classify into only 3 registers:
- Formal, לשון גבוהה / מליצית.
- Standard, לשון תקנית.
- Casual, לשון מדוברת / תת תקנית.

In fact, we will define "formal", the sentences use special, uncommon, or "high" (not well defined) idioms, words, or structures. 
"Standard" will be sentences that comply with the language's standard, but don't include anything special.
And as "casual" we will define any sentence that doesn't meet the standard. 

You probably have noticed that the differences between these registers are expressed through many aspects of the language.
The aspects I've Chosen to focus on them are: lexicon, morphology, and syntax.
A few examples of those (in Hebrew):
- Lexicon: הצילו (standard) vs. הושיעו (more formal). ירח (standard) vs. סהר or לבנה (more formal).
- Morphology: אינני (formal) vs. אני לא (standard) vs. אנלא (casual). כאשר הלכתי (formal) vs. כשהלכתי (standard) vs. שהלכתי (casual).
- Syntax: אורי הלך לביתו (standard) vs. הלך אורי לביתו (more formal).

## Data

The data collecting task was challenging, because one corpus tends to follow the same register across its texts. 
For example, in journal or newspaper there is an editor that cares the writing style, in Wikipedia there are [guidelines](https://he.wikipedia.org/wiki/%D7%95%D7%99%D7%A7%D7%99%D7%A4%D7%93%D7%99%D7%94:%D7%A2%D7%A7%D7%A8%D7%95%D7%A0%D7%95%D7%AA_%D7%95%D7%A7%D7%95%D7%95%D7%99%D7%9D_%D7%9E%D7%A0%D7%97%D7%99%D7%9D) that each of the writers should follow.
Therefore, we need several different sources of data, but it is recommended that each of them will deal with various topics, in order to prevent biases.

The sources I was satisfied with them are:
- [Ben Yehuda Project](https://github.com/projectbenyehuda) - a huge library of public domain Hebrew literary texts, most of them are very old.
- [Thinks](https://thinkil.co.il/) - A website includes articles in medium-high level.
- The [Hebrew Wikipedia](https://he.wikipedia.org/) as it was collected by NITE in 2013. (To get it, browse [here](https://hlp.nite.org.il/WebCorpora.aspx))
- Whatsapp chats - group chats that I've gotten from my family members as they exported by the application itself.

For privacy and copyright reasons, I can't publish the data itself, so I put an example file in each of the folders (except of "thinks" that the script itself download the pages from the website).

*I'm still working on the rest. It will be updated soon.* 

## Pipeline

### Data cleaning

### Sampling

### Tagging

### Feature extraction

### Learning

### Evaluation

## Running

## Further work

## Credits