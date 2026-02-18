from collections import Counter
import re
import pickle

INPUT_FILE ="sentences.txt"
VOCAB_SIZE = 40000
word_counts = Counter()

print("Starting vocabulary scan. This will take a few minutes...")

with open(INPUT_FILE,'r',encoding='utf-8') as f:
    for line_num,line in enumerate(f):
        # Cleaning: Keep A-Z, a-z, and German specials. NO .lower() here!
        text = re.sub(r'[^a-zA-ZäöüÄÖÜß.\s]', '', line)
        text = text.replace('.', ' . ')
        words = text.split()

        word_counts.update(words)
        if line_num % 500000 == 0 and line_num > 0:
            print(f"Read {line_num} lines...")

# Create the Dictionary
most_common = word_counts.most_common(VOCAB_SIZE)
word_to_int = {word: i+2 for i, (word, count) in enumerate(most_common)}
word_to_int["<UNK>"] = 0
word_to_int["<PAD>"] = 1

# Save it
with open("german_vocab.pkl", "wb") as f:
    pickle.dump(word_to_int, f)

print(f"Done! Saved {len(word_to_int)} CASED words to 'german_vocab.pkl'.")