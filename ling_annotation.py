import spacy

nlp = spacy.load("en_core_web_sm")

with open("data/wiki_us.txt", "r") as file:
    text = file.read()

doc = nlp(text)

print(doc)

print(len(doc))
print(len(text))

for token in text[0:10]:
    print(token)

for token in doc[0:10]:
    print(token)

for token in text.split()[0:10]:
    print(token)

for sentence in doc.sents:
    print(sentence)
print("===")
sentences = list(doc.sents)[0]
print(sentences)

token2 = sentences[2]
print(token2.text)
print(token2.left_edge)
print(token2.right_edge)
print(token2.ent_type_)
print(token2.ent_iob_)
print(token2.lemma_)
print(token2.morph)
print(token2.pos_)
print(token2.dep_)
print(token2.lang_)

text2 = "I am a student at the university."
doc2 = nlp(text2)
for token in doc2:
    print(token.text, token.lemma_, token.pos_, token.dep_)

from spacy import displacy
displacy.render(doc2, style="dep")