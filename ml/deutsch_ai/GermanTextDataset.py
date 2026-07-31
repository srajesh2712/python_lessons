import torch
from torch.utils.data import Dataset, DataLoader
import pickle
import re
import mmap
import os

class GermanTextDataset(Dataset):
    def __init__(self, input_file, vocab_path, max_len=5):
        self.max_len = max_len
        self.input_file = input_file

        with open(vocab_path, "rb") as f:
            self.word_to_int = pickle.load(f)

        self.int_to_word = {i: w for w, i in self.word_to_int.items()}
        print("Indexing file (Memory Mapped)...")
        self.line_offsets = []

        # We open the file once to map the offsets
        with open(input_file, "r", encoding='utf-8', errors='ignore') as f:
            offset = 0
            for line in f:
                self.line_offsets.append(offset)
                offset += len(line.encode('utf-8'))

        # We don't open the file handle here; we open it in __getitem__
        # using mmap for thread-safe memory access.
        self.file_size = os.path.getsize(input_file)

    def __len__(self):
        return len(self.line_offsets)

    def __getitem__(self, index):
        # Open the file and map it to memory for this specific read
        # This is extremely fast and avoids "shared handle" errors
        with open(self.input_file, "rb") as f:
            with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mm:
                start = self.line_offsets[index]
                mm.seek(start)
                # Read until newline
                line_bytes = mm.readline()
                line = line_bytes.decode('utf-8', errors='ignore')

        # --- Your Cleaning Logic ---
        text = re.sub(r'[^a-zA-ZäöüÄÖÜß.\s]', '', line)
        text = text.replace(".", " . ")
        words = text.split()

        nums = [self.word_to_int.get(w, 0) for w in words]

        if len(nums) > self.max_len:
            start_idx = torch.randint(0, len(nums) - self.max_len, (1,)).item()
            window = nums[start_idx: start_idx + self.max_len + 1]
        else:
            window = nums + [1] * (self.max_len + 1 - len(nums))

        return torch.tensor(window[:self.max_len]), torch.tensor(window[self.max_len])

# QUICK TEST
#dataset = GermanTextDataset("sentences.txt", "german_vocab.pkl")
#dataloader = DataLoader(dataset, batch_size=64, shuffle=True)
#x_batch, y_batch = next(iter(dataloader))
#print(x_batch.shape) # Should be [64, 5]