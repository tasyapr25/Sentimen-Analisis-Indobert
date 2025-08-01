# -*- coding: utf-8 -*-
"""4mylabelling.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12rYStvbA7OeDNjBcDVOkOgjWgrA9Low4
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
from collections import Counter
import ast

# Load dataset
df = pd.read_csv("/content/drive/MyDrive/sentimen/dataset/preprocessed_tweets.csv")
df['tokens'] = df['tokens'].apply(ast.literal_eval)

# Flatten tokens and get frequency
all_words = [word for tokens in df['tokens'] for word in tokens]
word_freq = Counter(all_words)
top_words = word_freq.most_common(300)

top_words_df = pd.DataFrame(top_words, columns=['word', 'frequency'])

import pandas as pd
import ast

# 1. Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 2. Load data hasil pre-processing
df = pd.read_csv('/content/drive/MyDrive/sentimen/dataset/preprocessed_tweets.csv')
df['stemmed_list'] = df['stemmed_list'].apply(ast.literal_eval)

# Lexicon positif & negatif umum
pos_df = pd.read_csv('/content/drive/MyDrive/sentimen/dataset/positive.csv')
neg_df = pd.read_csv('/content/drive/MyDrive/sentimen/dataset/negative.csv')

# Pastikan kolom 'word' ada di semua dataframe
pos_df.columns = ['word', 'weight'] if 'word' not in pos_df.columns else pos_df.columns
neg_df.columns = ['word', 'weight'] if 'word' not in neg_df.columns else neg_df.columns
# 4. Gabungkan lexicon jadi satu
lexicon_df = pd.concat([pos_df, neg_df], ignore_index=True).drop_duplicates(subset='word')
lexicon = dict(zip(lexicon_df['word'], lexicon_df['weight']))

# 5. Fungsi untuk memberi label otomatis
def label_by_score(tokens):
    score = sum(lexicon.get(word, 0) for word in tokens)
    if score > 0:
        return 'positif'
    elif score < 0:
        return 'negatif'
    else:
        return 'netral'

# 6. Terapkan ke semua data
df['label_final'] = df['stemmed_list'].apply(label_by_score)

# 7. Simpan ke file hasil akhir
output_path = '/content/drive/MyDrive/sentimen/dataset/tweet_labeled_dinasti.csv'
df.to_csv(output_path, index=False)

# 8. Tampilkan distribusi label
print("✅ Pelabelan otomatis selesai. File disimpan di:")
print(output_path)
print("\n📊 Distribusi label:")
print(df['label_final'].value_counts())

import matplotlib.pyplot as plt

# 1. Load dataset hasil pelabelan otomatis
df = pd.read_csv('/content/drive/MyDrive/sentimen/dataset/tweet_labeled_dinasti.csv')

# 2. Hitung distribusi label
label_counts = df['label_final'].value_counts()

# 3. Bar Chart
plt.figure(figsize=(8, 5))
label_counts.plot(kind='bar', color=['tomato', 'gold', 'skyblue'])
plt.title('Distribusi Label Sentimen Politik Dinasti')
plt.xlabel('Label Sentimen')
plt.ylabel('Jumlah Tweet')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 4. Pie Chart
plt.figure(figsize=(6, 6))
plt.pie(label_counts, labels=label_counts.index, autopct='%1.1f%%', startangle=140,
        colors=['tomato', 'gold', 'skyblue'], wedgeprops={'edgecolor': 'white'})
plt.title('Proporsi Sentimen Politik Dinasti')
plt.axis('equal')
plt.tight_layout()
plt.show()

# Tampilkan 10 tweet berlabel NEGATIF
print("🟥 Tweet Negatif:")
display(df[df['label_final'] == 'negatif'][['stemmed_text']].head(10))

# Tampilkan 10 tweet berlabel POSITIF
print("🟩 Tweet Positif:")
display(df[df['label_final'] == 'positif'][['stemmed_text']].head(10))

# Tampilkan 10 tweet berlabel netral
print("🟩 Tweet Netral:")
display(df[df['label_final'] == 'netral'][['stemmed_text']].head(10))

import pandas as pd
from sklearn.utils import resample

df = pd.read_csv('/content/drive/MyDrive/sentimen/dataset/tweet_labeled_dinasti.csv')

# Filter hanya positif dan negatif
df_binary = df[df['label_final'].isin(['positif', 'negatif'])].copy()

# Undersample ke 3500 masing-masing
df_pos = resample(df_binary[df_binary['label_final'] == 'positif'],
                  replace=False, n_samples=3500, random_state=42)
df_neg = resample(df_binary[df_binary['label_final'] == 'negatif'],
                  replace=False, n_samples=3500, random_state=42)

# Gabungkan dan acak
df_balanced = pd.concat([df_pos, df_neg]).sample(frac=1, random_state=42)

# Simpan hasil balanced
output_path = "/content/drive/MyDrive/sentimen/dataset/tweet_labeled_balanced.csv"
df_balanced.to_csv(output_path, index=False)

output_path

# Coba tampilkan isi file jika tersedia
file_path = "/content/drive/MyDrive/sentimen/dataset/tweet_labeled_balanced.cs"

# Jika file berhasil diakses, kita pisahkan data berdasarkan label
try:
    df = pd.read_csv(file_path)
    df_pos = df[df['label_final'] == 'positif']
    df_neg = df[df['label_final'] == 'negatif']

    # Tampilkan kedua DataFrame
    import ace_tools as tools
    tools.display_dataframe_to_user(name="Data Label Positif", dataframe=df_pos)
    tools.display_dataframe_to_user(name="Data Label Negatif", dataframe=df_neg)
except FileNotFoundError:
    "File belum tersedia. Silakan unggah 'tweet_labeled_balanced.csv'."

# Load ulang file dan pisahkan label (karena sebelumnya environment reset)
df = pd.read_csv('/content/drive/MyDrive/sentimen/dataset/tweet_labeled_balanced.csv')
df_pos = df[df['label_final'] == 'positif'].copy()
df_neg = df[df['label_final'] == 'negatif'].copy()

# Gabungkan semua token
from collections import Counter
import matplotlib.pyplot as plt
import ast

tokens_pos = [token for tokens in df_pos['tokens'].apply(ast.literal_eval) for token in tokens]
tokens_neg = [token for tokens in df_neg['tokens'].apply(ast.literal_eval) for token in tokens]

# Hitung 20 kata paling umum
common_pos = Counter(tokens_pos).most_common(20)
common_neg = Counter(tokens_neg).most_common(20)

# Fungsi untuk plot
def plot_word_distribution(word_freq, title):
    words, freqs = zip(*word_freq)
    plt.figure(figsize=(10, 4))
    plt.bar(words, freqs, color='mediumseagreen')
    plt.title(title)
    plt.ylabel("Frekuensi")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Plot untuk masing-masing label
plot_word_distribution(common_pos, "Top 20 Kata Paling Umum (Label Positif)")
plot_word_distribution(common_neg, "Top 20 Kata Paling Umum (Label Negatif)")

import pandas as pd
from IPython.display import display

# Gabungkan dua tabel frekuensi
df_top_pos = pd.DataFrame(common_pos, columns=["Token Positif", "Frekuensi"])
df_top_neg = pd.DataFrame(common_neg, columns=["Token Negatif", "Frekuensi"])

# Gabungkan jadi satu tabel berdampingan
df_combined = pd.concat([df_top_pos, df_top_neg], axis=1)

# Tampilkan di Google Colab
display(df_combined)