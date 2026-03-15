import json
import re

ARABIC_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]')

def is_valid_word(word: str) -> bool:
    clean = re.sub(r'[\u064B-\u065F\u0670\u0640]', '', word)  # شيل تشكيل
    if len(clean) < 2:
        return False
    if not ARABIC_PATTERN.search(clean):
        return False
    return True

with open('quran_timestamps.json', 'r', encoding='utf-8') as f:
    timestamps = json.load(f)

with open('database.json', 'r', encoding='utf-8') as f:
    database = json.load(f)

db_lookup = {}
for surah in database:
    s_num = surah['number']
    db_lookup[s_num] = {}
    for verse in surah['verses']:
        v_num = verse['number']
        db_lookup[s_num][v_num] = verse['text']['ar']

updated  = 0
missing  = 0
filtered = 0

for surah_key, surah in timestamps.items():
    s_num = surah['surah_number']
    for aya_key, aya in surah['ayat'].items():
        a_num = aya['aya_number']

        if s_num in db_lookup and a_num in db_lookup[s_num]:
            aya['text'] = db_lookup[s_num][a_num]
            updated += 1
        else:
            print(f"⚠️  مش موجود: سورة {s_num} آية {a_num}")
            missing += 1

        before = len(aya['words'])
        aya['words'] = [w for w in aya['words'] if is_valid_word(w['word'])]
        filtered += before - len(aya['words'])

with open('quran_timestamps.json', 'w', encoding='utf-8') as f:
    json.dump(timestamps, f, ensure_ascii=False, indent=2)

print(f"✅ Update: {updated:,}")
print(f"✅ Delete: {filtered:,} words")
print(f"⚠️ Not Found: {missing} aya")