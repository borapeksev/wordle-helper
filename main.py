import random
import json

# Language packages
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

# Language selection
language = ""
while language not in ["tr", "en"]:
    language = input("Dil seçiniz / Select language (tr/en): ").lower()

with open("words.txt", "r", encoding="utf-8") as f:
    words = json.load(f)

known_letters = ["_"] * 5
absent_letters = set()
wrong_positions = []  # [(letter, index), ...]

while True:
    print(messages[language]["menu"])
    choice = input(messages[language]["select"])

    if choice == "1":
        print(messages[language]["random_word"], random.choice(words))

    elif choice == "2":
        entry = input(messages[language]["known_letters_input"]).lower().split(",")
        if len(entry) == 5:
            known_letters = entry
        else:
            print(messages[language]["known_letters_error"])

    elif choice == "3":
        entry = input(messages[language]["absent_letters_input"]).lower().split(",")
        absent_letters.update(entry)

    elif choice == "4":
        entry = input(messages[language]["wrong_pos_input"]).lower().split(",")
        wrong_positions.clear()
        for item in entry:
            try:
                letter, pos = item.split("-")
                wrong_positions.append((letter, int(pos)-1))
            except:
                print(messages[language]["wrong_pos_error"], item)

    elif choice == "5":
        print(messages[language]["filtered_words"])
        matching_words = set()
        for word in words:
            if len(word) != 5:
                continue

            if any(letter in word for letter in absent_letters):
                continue

            wrong_found = False
            for letter, pos in wrong_positions:
                if letter not in word or word[pos] == letter:
                    wrong_found = True
                    break
            if wrong_found:
                continue

            matches_pattern = True
            for i in range(5):
                if known_letters[i] != "_" and word[i] != known_letters[i]:
                    matches_pattern = False
                    break

            if matches_pattern:
                matching_words.add(word)

        if matching_words:
            for w in sorted(matching_words):
                print("✅", w)
        else:
            print(messages[language]["no_match"])

    elif choice == "0":
        print(messages[language]["exit"])
        break

    else:
        print(messages[language]["invalid_choice"])
