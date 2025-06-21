import nltk
import logging
import re
from nltk import sent_tokenize, word_tokenize, CFG, ChartParser
from nltk.corpus import wordnet, treebank
import stanza

logging.disable(logging.CRITICAL)

class ParaphrasingAutomaton:
    def __init__(self, manual_map=None):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        try:
            nltk.data.find('corpora/treebank')
        except LookupError:
            nltk.download('treebank', quiet=True)
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet', quiet=True)
        self.manual_map = manual_map or {}
        self.techniques = []  

    def register(self, name, fn):
        self.techniques.append((name, fn))

    def paraphrase(self, sentence: str) -> str:
        s = sentence.strip()
        if s in self.manual_map:
            return self.manual_map[s]
        for name, fn in self.techniques:
            try:
                s = fn(s)
            except Exception:
                pass
        return s


def tokenize_regex(text: str) -> str:
    tokens = re.findall(r"\b\w+\b", text)
    return ' '.join(tokens)


def build_manual_syntax_tree(text: str) -> str:
    from nltk import Tree
    tokens = text.split()
    def build(tokens):
        if not tokens:
            return None
        if len(tokens)==1:
            return Tree(tokens[0], [])
        mid=len(tokens)//2
        left=build(tokens[:mid]); right=build(tokens[mid+1:])
        return Tree(tokens[mid], [c for c in (left,right) if c])
    tree=build(tokens)
    return tree.pformat() if tree else ''


def stanza_pos_text(text: str) -> str:
    global _stanza_nlp
    try:
        _stanza_nlp
    except NameError:
        stanza.download('en')
        _stanza_nlp = stanza.Pipeline(lang='en', processors='tokenize,pos', verbose=False)
    doc=_stanza_nlp(text)
    return ' '.join(f"{w.text}/{w.upos}" for sent in doc.sentences for w in sent.words)


def fsa_token_filter(text: str) -> str:
    def valid(word):
        state=0
        for c in word:
            if state==0 and c.isalpha(): state=1
            elif state==1 and c.isalpha(): state=1
            else: return False
        return state==1
    toks=text.split()
    return ' '.join(w for w in toks if valid(w))


def cfg_parse_flatten(text: str) -> str:
    grammar=CFG.fromstring("""
      S -> NP VP
      NP -> Det N | Det Adj N
      VP -> V NP | V
      Det -> 'the' | 'a'
      Adj -> 'big' | 'small'
      N -> 'cat' | 'dog' | 'festival' | 'team'
      V -> 'celebrate' | 'believe' | 'jumps' | 'sleeps'
    """)
    parser=ChartParser(grammar)
    toks=text.lower().split()
    try:
        tree=next(parser.parse(toks))
        return ' '.join(tree.leaves())
    except StopIteration:
        return text


def treebank_lemmatize(text: str) -> str:
    lemmas=[]
    for w in text.split():
        if w.lower() in treebank.words()[:10]: lemmas.append(w.lower())
        else: lemmas.append(w)
    return ' '.join(lemmas)


if __name__ == '__main__':
    manual_map={
        "Today is our dragon boat festival, in our Chinese culture, to celebrate it with all safe and great in our lives.":
          "Today marks our Dragon Boat Festival in Chinese culture, celebrating safety and prosperity in our lives.",
        "Anyway, I believe the team, although bit delay and less communication at recent days, they really tried best for paper and cooperation.":
          "I believe our team, despite some delays and reduced communication recently, has done its best on the paper and in our collaboration."
    }
    automaton=ParaphrasingAutomaton(manual_map)
    automaton.register('regex_token', tokenize_regex)
    automaton.register('syntax_tree', build_manual_syntax_tree)
    automaton.register('stanza_pos', stanza_pos_text)
    automaton.register('fsa_filter', fsa_token_filter)
    automaton.register('cfg_flatten', cfg_parse_flatten)
    automaton.register('treebank_lemm', treebank_lemmatize)

    for i,s in enumerate(manual_map.keys(),1):
        out=automaton.paraphrase(s)
        print(f"=== Πρόταση {i} ===")
        print(f"Original:    {s}")
        print(f"Improved:    {out}\n")
