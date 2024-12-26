

import sqlite3
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from nltk.tokenize import sent_tokenize
import nltk
import requests
from bs4 import BeautifulSoup

# NLTK Türkçe cümle ayrımı için r"C:\\Users\\sedtt\\mulakat_proje\\results\\chcekpoint-393
nltk.download('punkt')

# Eğitilmiş modeli ve tokenizer'ı yükleme
model_dir = r"C:\\Users\\sedtt\\mulakat_proje\\results\\chcekpoint-393"  # Eğitilmiş modelin bulunduğu dizin
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSequenceClassification.from_pretrained(model_dir)

# Veritabanı bağlantısı oluşturma
conn = sqlite3.connect("metin_konulari.db")
cursor = conn.cursor()

# Tablo oluşturma
cursor.execute('''
CREATE TABLE IF NOT EXISTS konular (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    genel_konu TEXT,
    genel_konu_skor REAL,
    cumle TEXT,
    alt_konu TEXT,
    alt_konu_skor REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS bilgiler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    konu TEXT,
    bilgi TEXT
)
''')

def search_info(query):
    """Google'da bilgi arama."""
    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    search_results = []
    for g in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        search_results.append(g.get_text())
    return search_results[:5]  # İlk 5 sonucu döndür

while True:
    # Kullanıcıdan metni alma
    print("Lütfen bir metin girin (veya çıkmak için 'q' yazın):")
    user_input = input()
    if user_input.lower() == 'q':
        break

    # Metni cümlelere böl
    sentences = sent_tokenize(user_input, language="turkish")

    # konu analizi
    inputs = tokenizer(user_input, return_tensors="pt", truncation=True, max_length=512, padding=True)
    outputs = model(**inputs)
    general_topic = outputs.logits.argmax(dim=1).item()
    general_score = outputs.logits.max().item()

    # Alt konuların analizi
    classified_sentences = []
    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, max_length=512, padding=True)
        outputs = model(**inputs)
        top_label = outputs.logits.argmax(dim=1).item()
        top_score = outputs.logits.max().item()
        classified_sentences.append((sentence, top_label, top_score))

    # Verileri veritabanına kaydetme
    cursor.execute('''
    INSERT INTO konular (genel_konu, genel_konu_skor, cumle, alt_konu, alt_konu_skor)
    VALUES (?, ?, NULL, NULL, NULL)
    ''', (general_topic, general_score))

    for sentence, top_label, top_score in classified_sentences:
        cursor.execute('''
        INSERT INTO konular (genel_konu, genel_konu_skor, cumle, alt_konu, alt_konu_skor)
        VALUES (?, ?, ?, ?, ?)
        ''', (general_topic, general_score, sentence, top_label, top_score))

    conn.commit()

    # Konsola çıktı
    print("\nGirilen Metnin Analizi:")
    print(f"Genel Konu: {general_topic} (Skor: {general_score:.2f})\n")
    print("Alt Konular ve Cümleler:")
    for sentence, top_label, top_score in classified_sentences:
        print(f"- Cümle: {sentence}")
        print(f"  Alt Konu: {top_label} (Skor: {top_score:.2f})")

    # Genel konu için bilgi arama
    print("\nGenel Konu ile İlgili Bilgiler:")
    general_info = search_info(str(general_topic))
    for info in general_info:
        print(f"- {info}")
        cursor.execute('INSERT INTO bilgiler (konu, bilgi) VALUES (?, ?)', (str(general_topic), info))

    conn.commit()

print("\nVeriler 'metin_konulari.db' adlı veritabanına kaydedildi.")
conn.close()