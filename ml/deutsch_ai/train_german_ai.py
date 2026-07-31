import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import os
from torch.optim.lr_scheduler import ReduceLROnPlateau
from GermanTextDataset import GermanTextDataset


class GermanLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super(GermanLSTM,self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim,num_layers=3,dropout=0.3, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self,x):
        embedded = self.embedding(x)
        output, (hidden, cell) = self.lstm(embedded)
        last_word_output = output[:,-1,:]
        logits = self.fc(last_word_output)
        return logits


def generate_sample(model, dataset, start_text="Ich", max_len=30):
    model.eval()
    with torch.no_grad():
        # Use word_to_int instead of vocab
        tokens = [dataset.word_to_int.get(word, 0) for word in start_text.split()]
        input_tensor = torch.LongTensor(tokens).unsqueeze(0).to(DEVICE)

        results = start_text.split()
        for _ in range(max_len):
            outputs = model(input_tensor)
            #next_token = torch.argmax(outputs, dim=1).item()
            probs = torch.softmax(outputs / 0.8, dim=1)  # 0.8 is the temperature
            next_token = torch.multinomial(probs, 1).item()
            # Use int_to_word instead of inv_vocab
            word = dataset.int_to_word.get(next_token, "<UNK>")

            # --- STOP LOGIC ---
            if word == "." or word == "<EOS>":
                results.append(word)
                break  # Stop the loop early!

            results.append(word)

            # Update input for next word
            new_token = torch.LongTensor([[next_token]]).to(DEVICE)
            input_tensor = torch.cat([input_tensor, new_token], dim=1)

            # Keep the window size consistent with max_len
            if input_tensor.size(1) > dataset.max_len:
                input_tensor = input_tensor[:, 1:]

    model.train()
    clean_results = [w for w in results if w not in ["<PAD>", "<EOS>"]]
    return " ".join(clean_results)


VOCAB_SIZE = 40002  # Based on your vocab script
EMBED_DIM = 128    # Dimensions for word meanings
HIDDEN_DIM = 1024   # Complexity of the AI's memory
BATCH_SIZE = 128
LEARNING_RATE = 0.0001
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if __name__ == "__main__":
    dataset = GermanTextDataset("sentences.txt", "german_vocab.pkl", max_len=12)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True,num_workers=2,pin_memory=False)

    model = GermanLSTM(VOCAB_SIZE, EMBED_DIM, HIDDEN_DIM).to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2)
    print(f"Starting training on {DEVICE}...")
    CHECKPOINT_PATH = "german_model.pth"

    if os.path.exists(CHECKPOINT_PATH):
        print(f"--- Loading Checkpoint: {CHECKPOINT_PATH} ---")

        # Load the saved data
        checkpoint = torch.load(CHECKPOINT_PATH, map_location=DEVICE)

        # If you saved just the model:

        print("Ready for CPU Adaptation!")
        # If you saved the optimizer too (highly recommended for "Hot" starts):
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'],strict=False)
            if 'optimizer_state_dict' in checkpoint:
                optimizer.load_state_dict(checkpoint['optimizer_state_dict'])


        print("Successfully resumed training!")
    else:
        print("No checkpoint found, starting from scratch.")
    # 4. The Training Loop
    model.train()
    for epoch in range(2): # We can do multiple passes over the 8M lines
        running_loss = 0.0
        for batch_idx, (x, y) in enumerate(dataloader):
            x, y = x.to(DEVICE,non_blocking=True), y.to(DEVICE,non_blocking=True)


            # Forward Pass
            outputs = model(x)
            loss = criterion(outputs, y)
            # Clear previous gradients
            optimizer.zero_grad()
            loss.backward()
            # Backward Pass (Learning)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

            running_loss += loss.item()

            # Print progress every 100 batches
            if batch_idx % 10 == 0:
                avg_loss = running_loss / 10 if batch_idx > 0 else loss.item()
                print(f"Epoch [{epoch+1}/5] | Batch {batch_idx} | Loss: {avg_loss:.4f}")
                if batch_idx % 100 == 0 and batch_idx > 0:
                    scheduler.step(avg_loss)
                running_loss = 0.0

            # SAVE periodically so you don't lose progress
            if batch_idx % 100 == 0 and batch_idx > 0:
                checkpoint = { 'model_state_dict': model.state_dict(), 'optimizer_state_dict': optimizer.state_dict()}  # Save the teacher's memory!
                #torch.save(model.state_dict(), f"german_model_step_{batch_idx}.pth")
                torch.save(checkpoint, f"german_model_step_{batch_idx}.pth")
                print("--- Model Checkpoint Saved ---")
                sample = generate_sample(model, dataset, start_text="Ich")
                print(f"--- Checkpoint Saved | Sample: '{sample}' ---")

        epoch_save_path = f"german_model_epoch_{epoch + 1}.pth"
        torch.save(model.state_dict(), epoch_save_path)
        print(f"✅ Epoch {epoch + 1} complete. Model saved as {epoch_save_path}")

    # Final Save
    torch.save(model.state_dict(), "german_model_final.pth")
    print("Training Complete!")
