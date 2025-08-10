import random
import json

# Dil paketleri
messages = {
    "tr": {
        "menu": "\nMenü:\n1 - Rastgele kelime\n2 - Bilinen harfleri gir\n3 - Olmayan harfleri gir\n4 - Yanlış pozisyondaki harfleri gir\n5 - Eşleşen kelimeleri göster\n0 - Çıkış",
        "select": "Seçiminiz: ",
        "random_word": "👉👉👉 Rastgele kelime:",
        "known_letters_input": "Bilinen harfleri girin (örn: ş,_,r,_,_): ",
        "known_letters_error": "❗ 5 karakter girmelisin.",
        "absent_letters_input": "Olmayan harfleri girin (örn: a,s,t): ",
        "wrong_pos_input": "Yanlış pozisyondaki harfleri girin (örn: a-2,k-3): ",
        "wrong_pos_error": "❗ Geçersiz format:",
        "filtered_words": "🔍 Filtrelenmiş kelimeler:",
        "no_match": "🚫 Eşleşen kelime bulunamadı.",
        "exit": "Çıkılıyor...",
        "invalid_choice": "❗ Geçersiz seçim!"
    },
    "en": {
        "menu": "\nMenu:\n1 - Random word\n2 - Enter known letters\n3 - Enter absent letters\n4 - Enter wrong position letters\n5 - Show matching words\n0 - Exit",
        "select": "Your choice: ",
        "random_word": "👉👉👉 Random word:",
        "known_letters_input": "Enter known letters (e.g. s,_,r,_,_): ",
        "known_letters_error": "❗ You must enter 5 characters.",
        "absent_letters_input": "Enter absent letters (e.g. a,s,t): ",
        "wrong_pos_input": "Enter wrong position letters (e.g. a-2,k-3): ",
        "wrong_pos_error": "❗ Invalid format:",
        "filtered_words": "🔍 Filtered words:",
        "no_match": "🚫 No matching words found.",
        "exit": "Exiting...",
        "invalid_choice": "❗ Invalid choice!"
    }
}

# Dil seçimi
lang = ""
while lang not in ["tr", "en"]:
    lang = input("Dil seçiniz / Select language (tr/en): ").lower()

with open("words.txt", "r", encoding="utf-8") as f:
    kelimeler = json.load(f)

bilinen_harfler = ["_"] * 5
olmayan_harfler = set()
yanlis_pozisyonlar = []  # [(letter, index), ...]

while True:
    
    print(messages[lang]["menu"])
    secim = input(messages[lang]["select"])

    if secim == "1":
        print(messages[lang]["random_word"], random.choice(kelimeler))

    elif secim == "2":
        girdi = input(messages[lang]["known_letters_input"]).lower().split(",")
        if len(girdi) == 5:
            bilinen_harfler = girdi
        else:
            print(messages[lang]["known_letters_error"])

    elif secim == "3":
        girdi = input(messages[lang]["absent_letters_input"]).lower().split(",")
        olmayan_harfler.update(girdi)

    elif secim == "4":
        girdi = input(messages[lang]["wrong_pos_input"]).lower().split(",")
        yanlis_pozisyonlar.clear()
        for item in girdi:
            try:
                harf, pos = item.split("-")
                yanlis_pozisyonlar.append((harf, int(pos)-1))
            except:
                print(messages[lang]["wrong_pos_error"], item)

    elif secim == "5":
        print(messages[lang]["filtered_words"])
        eslesenler = []
        for kelime in kelimeler:
            if len(kelime) != 5:
                continue

            if any(harf in kelime for harf in olmayan_harfler):
                continue

            yanlis_var = False
            for harf, pos in yanlis_pozisyonlar:
                if harf not in kelime:
                    yanlis_var = True
                    break
                if kelime[pos] == harf:
                    yanlis_var = True
                    break
            if yanlis_var:
                continue

            uyuyor = True
            for i in range(5):
                if bilinen_harfler[i] != "_" and kelime[i] != bilinen_harfler[i]:
                    uyuyor = False
                    break

            if uyuyor:
                eslesenler.append(kelime)

        if eslesenler:
            for k in sorted(eslesenler):
                print("✅", k)
        else:
            print(messages[lang]["no_match"])

    elif secim == "0":
        print(messages[lang]["exit"])
        break

    else:
        print(messages[lang]["invalid_choice"])
