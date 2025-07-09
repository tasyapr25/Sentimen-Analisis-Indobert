# 🗳️ Analisis Sentimen Politik Dinasti di Indonesia pada Twitter
### Pendekatan Hybrid: Lexicon-Based dan Fine-Tuned IndoBERT

Proyek ini merupakan bagian dari Tugas Akhir yang bertujuan untuk melakukan analisis sentimen terhadap opini publik terkait **politik dinasti di Indonesia** yang diambil dari media sosial Twitter. Penelitian ini menggunakan **pendekatan hybrid**, yaitu menggabungkan metode **lexicon-based** dengan model **transformer IndoBERT** yang telah di-*fine-tune* untuk klasifikasi sentimen.

## 📌 Tujuan Penelitian
- Mengidentifikasi sentimen publik terhadap isu politik dinasti di Indonesia.
- Mengklasifikasikan tweet menjadi sentimen **positif**, **negatif**, atau **netral**.
- Menganalisis performa pendekatan hybrid dibandingkan dengan metode individual.

## 🛠️ Teknologi & Tools
- **Python 3.10+**
- **Transformers (HuggingFace)**
- **IndoBERT (IndoBERT Base v1 by IndoNLU)**
- **Sastrawi & IDN Lexicon**
- **Scikit-learn**
- **Pandas, Numpy, Matplotlib, Seaborn**
- **Google Colab**

## 🔍 Metodologi
1. **Data Collection**  
   Scraping tweet menggunakan keyword yang relevan dengan politik dinasti.

2. **Preprocessing**  
   - Case folding  
   - Cleansing & filtering  
   - Tokenization  
   - Stopword removal
   - Stemming

3. **Sentiment Labeling**
   - **Lexicon-Based:** Menggunakan kamus sentimen Bahasa Indonesia

4. **Modeling**
   - **Fine-Tuned IndoBERT:** dilakukan dengan skenario epoch tertentu
   - **Evaluation:** Confusion matrix, akurasi, precision, recall, dan F1-score

5. **Hybrid Classification**
   Kombinasi hasil dari lexicon-based dan model IndoBERT untuk meningkatkan akurasi.

## 📈 Visualisasi Hasil
- Confusion Matrix
- Pie chart distribusi sentimen
- Grafik akurasi dan loss selama pelatihan
- Wordcloud kata dominan per sentimen

## 📚 Referensi
- IndoNLU Benchmark: https://github.com/indobenchmark/indonlu
- KBBI & ID Sentiment Lexicon
- [BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805)

## 🙋‍♀️ Penulis
**Nama:** [Tasya Putri  Ramadhani]  
**Email:** [tasyapr00@gmail.com]

