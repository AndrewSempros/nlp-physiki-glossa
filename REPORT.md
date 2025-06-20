# Δομημένη Αναφορά

## 1. Εισαγωγή
Η σημασιολογική ανακατασκευή (semantic reconstruction) στο NLP στοχεύει στη διατήρηση του αρχικού νοήματος του κειμένου ενώ βελτιώνει τη σαφήνεια, τη συνοχή και τον τόνο. Εφαρμόζεται σε πλήθος εργασιών όπως αυτόματη μετάφραση, περίληψη (summarization) και διάλογο (dialog systems), όπου η ποιότητα της αναδιατύπωσης επηρεάζει άμεσα την κατανόηση από τον τελικό χρήστη.

## 2. Μεθοδολογία

### Α. Manual Automaton  
- **Περιγραφή**: Χειροκίνητες κανόνες (manual rewrites) για δύο επιλεγμένες προτάσεις.  
- **Στάδια**:  
  1. Tokenization με NLTK.  
  2. Εφαρμογή map original→improved.  
  3. Επιστροφή rewritten πρότασης.  

### Β. Transformer Pipelines  
Χρησιμοποιήθηκαν τρία προ-εκπαιδευμένα μοντέλα:
1. **T5-PAWS**  
2. **Pegasus Paraphrase**  
3. **Humarin ChatGPT-on-T5**  

Διαδικασία:
1. Διαχωρισμός κειμένου σε προτάσεις.  
2. Κάθε πρόταση περνάει από το pipeline με beam search.  
3. Καθαρισμός εξόδου (normalize punctuation, κεφαλαία “I”).  

### C. Embeddings Analysis  
- **Embedding model**: BERT-base-uncased.  
- **Προεπεξεργασία**: αφαίρεση stopwords, keep-alpha tokens.  
- **Υπολογιστικές τεχνικές**:  
  - **Cosine similarity** μεταξύ αρχικού και ανακατασκευασμένου πλήρους κειμένου (sentence-level mean pooling).  
  - **PCA** οπτικοποίηση μετατοπίσεων λέξεων-κλειδιών.

## 3. Πειράματα & Αποτελέσματα

### A. Manual Automaton  
=== Πρόταση 1 ===
Original: Today is our dragon boat festival, in our Chinese culture, to celebrate it with all safe and great in our lives.
Improved: Today marks our Dragon Boat Festival in Chinese culture, celebrating safety and prosperity in our lives.

=== Πρόταση 2 ===
Original: Anyway, I believe the team, although bit delay and less communication at recent days, they really tried best for paper and cooperation.
Improved: I believe our team, despite some delays and reduced communication recently, has done its best on the paper and in our collaboration.



### B. Transformer Pipelines

#### Text 1
- **T5-PAWS Paraphraser**  
  Today is our dragon boat festival, in our Chinese culture, to celebrate it in our lives with all the safe and great. I hope that you will enjoy it too as my deepest wishes. Thank you for your message to show our words to the doctor, as his next contract to check, to all of us. I received this message to see the accepted message. I received the message from the professor to show me a few days ago. I have very appreciated the professor's full support for our Springer proceedings publication.

- **Pegasus Paraphraser**  
  The dragon boat festival is a celebration in our Chinese culture and we should all be happy. I hope you enjoy it as much as I do. Your message was appreciated by the doctor, as his next contract checking. I saw the approved message when I received this message. The professor sent a message to me a few days ago. The professor was very supportive of the Springer proceedings publication.

- **Humarin ChatGPT Paraphraser**  
  Our Chinese culture features a dragon boat festival to celebrate with all that is good in our lives today [...] The professor's complete backing for our Springer proceedings publication is greatly appreciated by me, especially given the professor's unwavering support.

#### Text 2
- **T5-PAWS Paraphraser**  
  During our final discussion I told him about the new submission — the one we were waiting for since last autumn, but the updates were confusing as they did not include the full feedback of the reviewer or maybe the editor? [...] Let us all make sure they are safe and celebrate the result with strong coffee and future targets.

- **Pegasus Paraphraser**  
  I told him about the new submission we were waiting for, but the updates didn't include the full feedback from the reviewer or editor, which was confusing. [...] Let us celebrate the outcome with strong coffee and future targets and make sure all are safe.

- **Humarin ChatGPT Paraphraser**  
  During our last discussion, I shared with him the new submission that we had been waiting for last autumn, but the updated information was unclear as it did not include the complete feedback from the reviewer or editor [...] Let us secure all and rejoice in the success with high coffee and ambitious goals for the future.

### C. Cosine Similarities (Embeddings)

| Text    | Method   | Cosine Sim. |
|---------|----------|------------:|
| **Text 1** | T5-PAWS   | 0.9687     |
|         | Pegasus  | 0.9178     |
|         | Humarin  | 0.9188     |
| **Text 2** | T5-PAWS   | 0.9557     |
|         | Pegasus  | 0.9323     |
|         | Humarin  | 0.9117     |

#### PCA Visualization  
Για κάθε κείμενο, τα keywords πριν (μπλε) και μετά (κόκκινα) εμφανίζουν μετατοπίσεις στον σημασιολογικό χώρο.

## 4. Συζήτηση
- **Επάρκεια embeddings**: Οι τιμές cosine > 0.9 δείχνουν πως οι embedding-based μετρήσεις διατήρησαν σε μεγάλο βαθμό το αρχικό νόημα.  
- **Προκλήσεις**:  
  - *Manual* rewrites απαιτούν χειροκίνητη συντήρηση κανόνων.  
  - *Transformer* μοντέλα υπερισχύουν στην ροή αλλά ενίοτε αλλοιώνουν λεπτομέρειες.  
- **Αυτοματοποίηση**:  
  - Fine-tuning domain-specific data.  
  - Υβριδικά συστήματα grammar- + ML-based.  
- **Διαφορές ποιότητας**:  
  - Pegasus υπερφορούσε (over-summary) σε ορισμένες προτάσεις.  
  - T5-PAWS ισορροπεί λεκτικά vs. Humarin πιο «ελεύθερα» στυλ.

## 5. Συμπέρασμα
Η συνδυαστική χρήση manual κανόνων και transformer-based μοντέλων παρέχει την καλύτερη ισορροπία ανάμεσα σε ακρίβεια και ευχρηστία. Οι embedding-based μετρήσεις cosine & PCA επιβεβαιώνουν τη στενή διατήρηση νοήματος.

## 6. Βιβλιογραφία
1. Youtube
2. Stackoverflow
3. Chatgpt
4. 
