# -*- coding: utf-8 -*-
"""5IndoBERT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Lo2785XWqJfjkBMwuQGJEAdPN_JMoV3F
"""

!pip install transformers

import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/sentimen/dataset/tweet_labeled_balanced.csv')
df = df[df['label_final'].isin(['positif', 'negatif'])]

# Encode label: positif = 1, negatif = 0
df['label'] = df['label_final'].map({'negatif': 0, 'positif': 1})

"""# 1. SPLIT DATASE 80:20"""

import pandas as pd
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv('/content/drive/MyDrive/sentimen/dataset/tweet_labeled_balanced.csv')

# Label encoding (jika belum)
df['label_id'] = df['label_final'].map({'negatif': 0, 'positif': 1})

# Split data
train_df, test_df = train_test_split(df, test_size=0.2, stratify=df['label_id'], random_state=42)

# Tampilkan ringkasan
print("📄 Kolom yang tersedia:", list(df.columns))
print(f"Total : {len(df)} tweet")
print(f"Train : {len(train_df)} tweet ({(len(train_df)/len(df))*100:.1f}%)")
print(f"Test  : {len(test_df)} tweet ({(len(test_df)/len(df))*100:.1f}%)")

# Tampilkan contoh data
print("\ data TRAIN:")
print(train_df[['stemmed_text', 'label_id']].sample(5, random_state=1))

print("\ data TEST:")
print(test_df[['stemmed_text', 'label_id']].sample(5, random_state=2))

"""# 2. TOKENISASI INDOBERT base P1"""

from transformers import BertTokenizer

# Load tokenizer IndoBERT
tokenizer = BertTokenizer.from_pretrained("indobenchmark/indobert-base-p1")

# Tokenisasi untuk data train dan test
train_encodings = tokenizer(list(train_df['stemmed_text']), truncation=True, padding=True, max_length=128)
test_encodings = tokenizer(list(test_df['stemmed_text']), truncation=True, padding=True, max_length=128)

# Pilih salah satu teks (ambil dari training set)
sample_text = train_df['stemmed_text'].iloc[0]

# Tokenisasi manual untuk diperiksa
encoded = tokenizer(sample_text, truncation=True, padding='max_length', max_length=128, return_tensors='pt')

# Tampilkan isi
tokens = tokenizer.convert_ids_to_tokens(encoded['input_ids'][0])
input_ids = encoded['input_ids'][0].tolist()
attention_mask = encoded['attention_mask'][0].tolist()

# Print hasil tokenisasi
print("📝 Original text:\n", sample_text)
print("\n🔢 Token IDs:\n", input_ids[:20], "...")
print("\n🔤 Tokens:\n", tokens[:20], "...")
print("\n🎯 Attention Mask:\n", attention_mask[:20], "...")
print("\n📏 Total Panjang Input:", len(tokens))

print("Jumlah tweet ditokenisasi (train):", len(train_encodings['input_ids']))
print("Jumlah tweet ditokenisasi (test):", len(test_encodings['input_ids']))

import pandas as pd

# Ambil semua data hasil tokenisasi
tokens_list = [tokenizer.convert_ids_to_tokens(ids) for ids in train_encodings['input_ids']]

# Gabungkan ke DataFrame
tokenized_df = pd.DataFrame({
    'original_text': train_df['stemmed_text'].tolist(),
    'tokens': tokens_list,
    'input_ids': train_encodings['input_ids'],
    'attention_mask': train_encodings['attention_mask']
})

# Tampilkan
tokenized_df.head()

from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("indobenchmark/indobert-base-p1")

train_encodings = tokenizer(
    list(train_df['stemmed_text']),
    truncation=True,
    padding=True,
    max_length=128
)

test_encodings = tokenizer(
    list(test_df['stemmed_text']),
    truncation=True,
    padding=True,
    max_length=128
)

train_encodings['input_ids'][0]
tokenizer.convert_ids_to_tokens(train_encodings['input_ids'][0])

"""# 3. FINE TUNING INDOBERT"""

import torch

# Kelas dataset untuk IndoBERT
class IndoDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Buat dataset training dan test
train_dataset = IndoDataset(train_encodings, train_df['label_id'].tolist())
test_dataset = IndoDataset(test_encodings, test_df['label_id'].tolist())

from transformers import BertForSequenceClassification, Trainer, TrainingArguments
import os
from transformers import logging

# Nonaktifkan wandb
os.environ["WANDB_DISABLED"] = "true"
os.environ["TRANSFORMERS_NO_WANDB"] = "1"
logging.set_verbosity_error()

# Hyperparameter
batch_sizes = [16]
epochs = [3]

results = []

# Loop semua kombinasi
for bs in batch_sizes:
    for ep in epochs:
        print(f"\n🔧 Training IndoBERT Base - Batch: {bs}, Epoch: {ep}")

        # Load ulang model di setiap iterasi agar training tidak nyambung
        model = BertForSequenceClassification.from_pretrained("indobenchmark/indobert-base-p1", num_labels=2)

        # Setup TrainingArguments
        training_args = TrainingArguments(
            output_dir=f'./content/drive/MyDrive/sentimen/indobert_bs{bs}_ep{ep}',
            num_train_epochs=ep,
            per_device_train_batch_size=bs,
            per_device_eval_batch_size=bs,
            learning_rate=2e-5,
            weight_decay=0.01,
            logging_dir=f'./logs/bs{bs}_ep{ep}',
            logging_steps=50,
            save_strategy="epoch",
            report_to="none"
        )

        # Trainer setup
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=test_dataset
        )

        # Training & Evaluasi
        trainer.train()
        eval_result = trainer.evaluate()
        eval_result.update({'batch_size': bs, 'epoch': ep})
        results.append(eval_result)

# Buat DataFrame dari hasil evaluasi
import pandas as pd
df_results = pd.DataFrame(results)
print(df_results)

import torch
from torch.utils.data import DataLoader
from tqdm import tqdm
import numpy as np
from sklearn.metrics import classification_report
import pandas as pd

# Buat DataLoader untuk prediksi batch kecil
dataloader = DataLoader(test_dataset, batch_size=32)
model.eval()

all_logits = []

# Loop prediksi
with torch.no_grad():
    for batch in tqdm(dataloader, desc="Predicting"):
        batch = {k: v.to(model.device) for k, v in batch.items()}
        outputs = model(**batch)
        all_logits.append(outputs.logits.cpu())

# Gabungkan dan prediksi
logits = torch.cat(all_logits, dim=0).numpy()
y_pred = np.argmax(logits, axis=1)
y_true = test_df['label_id'].tolist()

# Mapping label
label_map = {0: "negatif", 1: "positif"}
test_df = test_df.reset_index(drop=True)
test_df['predicted_label'] = y_pred
test_df['actual_sentiment'] = test_df['label_id'].map(label_map)
test_df['predicted_sentiment'] = test_df['predicted_label'].map(label_map)

# Tampilkan hasil prediksi
test_df[['stemmed_text', 'actual_sentiment', 'predicted_sentiment']].head(50)

test_df[['stemmed_text', 'actual_sentiment', 'predicted_sentiment']].to_csv(
    '/content/drive/MyDrive/sentimen/hasil_prediksi_indobert.csv', index=False
)

"""# CONFUSION MATRIX"""

import numpy as np

# Ambil label asli dan hasil prediksi
y_true = test_df['label_id'].tolist()
y_pred = test_df['predicted_label'].tolist()

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report

# Buat confusion matrix
cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Negatif", "Positif"])

# Plot confusion matrix
plt.figure(figsize=(6, 6))
disp.plot(cmap='Blues', values_format='d')
plt.title("Confusion Matrix - IndoBERT")
plt.grid(False)
plt.show()

# Tampilkan classification report
report = classification_report(y_true, y_pred, target_names=["Negatif", "Positif"])
print("Classification Report:\n")
print(report)

import seaborn as sns
sns.countplot(x='predicted_sentiment', data=test_df)
plt.title("Distribusi Prediksi Sentimen oleh IndoBERT")
plt.xlabel("Sentimen")
plt.ylabel("Jumlah")
plt.savefig("/content/drive/MyDrive/sentimen/distribusi_prediksi_sentimen.png")
plt.show()

from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def compute_metrics(p):
    preds = np.argmax(p.predictions, axis=1)
    labels = p.label_ids
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')
    acc = accuracy_score(labels, preds)
    return {
        "eval_accuracy": acc,
        "eval_precision": precision,
        "eval_recall": recall,
        "eval_f1": f1
    }

import pandas as pd

# Ganti path ini sesuai file kamu di Google Drive atau lokal
test_df = pd.read_csv('/content/drive/MyDrive/sentimen/hasil_prediksi_indobert.csv')

y_true = test_df['actual_sentiment']
y_pred = test_df['predicted_sentiment']

from sklearn.metrics import classification_report

report = classification_report(y_true, y_pred, output_dict=True)
df_report = pd.DataFrame(report).transpose()
print(df_report[['precision', 'recall', 'f1-score', 'support']])

df_report.to_csv("evaluasi_kuantitatif.csv")

import matplotlib.pyplot as plt

# Hitung jumlah masing-masing sentimen
sentiment_counts = test_df['predicted_sentiment'].value_counts()

# Pie chart
plt.figure(figsize=(6, 6))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140)
plt.title("Distribusi Sentimen Hasil Prediksi IndoBERT")
plt.axis('equal')
plt.show()

# Tampilkan jumlahnya
print("Jumlah prediksi per sentimen:")
print(sentiment_counts)

sentiment_counts.to_csv("distribusi_sentimen.csv")