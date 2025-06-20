import os
import nltk
import warnings

warnings.filterwarnings("ignore")
from transformers import logging as hf_logging
hf_logging.set_verbosity_error()

os.environ['TOKENIZERS_PARALLELISM'] = 'false'

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

import builtins
_orig_print = builtins.print
builtins.print = lambda *args, **kwargs: None

from transformers import pipeline

t5_pipeline = pipeline(
    "text2text-generation",
    model="Vamsi/T5_Paraphrase_Paws",
    tokenizer="Vamsi/T5_Paraphrase_Paws",
    framework="pt",
    device=0
)

pegasus_pipeline = pipeline(
    "text2text-generation",
    model="tuner007/pegasus_paraphrase",
    tokenizer="tuner007/pegasus_paraphrase",
    framework="pt",
    device=0
)

humarin_pipeline = pipeline(
    "text2text-generation",
    model="humarin/chatgpt_paraphraser_on_T5_base",
    tokenizer="humarin/chatgpt_paraphraser_on_T5_base",
    framework="pt",
    device=0
)

builtins.print = _orig_print

from nltk.tokenize import sent_tokenize
from difflib import SequenceMatcher

common_kwargs = {
    "do_sample": True,
    "top_k": 40,
    "top_p": 0.92,
    "temperature": 0.85,
    "num_return_sequences": 5,
    "max_length": 96
}

texts = {
    "Text1": (
        "Today is our dragon boat festival, in our Chinese culture, to celebrate it with all safe and great in our lives. "
        "Hope you too, to enjoy it as my deepest wishes. Thank your message to show our words to the doctor, as his next contract checking, to all of us. "
        "I got this message to see the approved message. In fact, I have received the message from the professor to show me a couple of days ago. "
        "I am very appreciated the full support of the professor for our Springer proceedings publication."
    ),
    "Text2": (
        "During our final discuss, I told him about the new submission — the one we were waiting since last autumn, "
        "but the updates was confusing as it not included the full feedback from reviewer or maybe editor? "
        "Anyway, I believe the team, although bit delay and less communication at recent days, they really tried best for paper and cooperation. "
        "We should be grateful, I mean all of us, for the acceptance and efforts until the Springer link came finally last week, I think. "
        "Also, kindly remind me please, if the doctor still plan for the acknowledgments section edit before he sends again. "
        "Because I didn’t see that part final yet, or maybe I missed, I apologize if so. Overall, let us make sure all are safe and celebrate the outcome with strong coffee and future targets."
    )
}

def best_candidate(original: str, candidates: list) -> str:
    ratios = [(SequenceMatcher(None, original, cand).ratio(), cand) for cand in candidates]
    return sorted(ratios, key=lambda x: x[0])[0][1]

def reconstruct(text: str, name: str, pipe):
    print(f"\n=== {name} ===")
    sentences = sent_tokenize(text)
    paraphrased = []
    for sent in sentences:
        try:
            input_text = sent
            if name.startswith("T5"):
                input_text = "paraphrase: " + sent
            outputs = pipe(input_text, **common_kwargs)
            candidates = [o['generated_text'].strip().replace('Paraphrase:', '') for o in outputs]
            chosen = best_candidate(sent, candidates)
        except Exception:
            chosen = sent
        paraphrased.append(chosen)
    print(" ".join(paraphrased))

if __name__ == "__main__":
    for label, txt in texts.items():
        reconstruct(txt, f"T5 PAWS Paraphraser ({label})", t5_pipeline)
        reconstruct(txt, f"Pegasus Paraphraser ({label})", pegasus_pipeline)
        reconstruct(txt, f"Humarin ChatGPT Paraphraser ({label})", humarin_pipeline)
