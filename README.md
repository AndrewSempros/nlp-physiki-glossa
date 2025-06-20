# NLP Paraphrasing & Reconstruction

Αυτό το repository περιέχει κώδικα για:
1. **Manual Automaton** (rule-based παραφράσεις)  
2. **Transformer Pipelines** (3 προεκπαιδευμένα μοντέλα παραφράσεων)  
3. **Embeddings Analysis** (ποσοτική ανάλυση ομοιότητας & PCA visualization)

---

## Δομή Φακέλων

```
nlp-paraphrasing/
├── paraphrasing_automaton.py       # Παραδοτέο 1.A: Manual Automaton
├── paraphrasing_pipelines_three.py # Παραδοτέο 1.B–C: Transformer Pipelines
├── embeddings_analysis.py          # Παραδοτέο 2: Cosine & PCA ανάλυση
├── README.md                       # Αυτό το αρχείο
├── .gitignore                      # Αγνοούμενα αρχεία
└── .env                            #.env
```

---

## Εγκατάσταση

```bash
git clone https://github.com/<AndrewSempros>/nlp-paraphrasing.git
cd nlp-paraphrasing
conda create -n nlp-env python=3.10 -y
conda activate nlp-env
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Εκτέλεση

1. **Manual Automaton**  
   ```bash
   python paraphrasing_automaton.py
   ```

2. **Transformer Pipelines**  
   ```bash
   python paraphrasing_pipelines_three.py
   ```

3. **Embeddings Analysis**  
   ```bash
   python embeddings_analysis.py
   ```
---

## Συνεισφορά

1. Fork & clone.  
2. Δημιουργήστε branch (`git checkout -b feature/xyz`).  
3. Commit & push.  
4. Pull request.

---


