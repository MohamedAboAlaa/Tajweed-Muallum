import os
from pathlib import Path

BASE_DIR = "Quran_Database"

fixed   = 0
skipped = 0

surah_dirs = sorted(Path(BASE_DIR).iterdir())

for surah_dir in surah_dirs:
    if not surah_dir.is_dir():
        continue

    surah_num = int(surah_dir.name.split('_')[0])

    if surah_num in (1, 9):
        skipped += 1
        print(f"Ignore => {surah_num} ({surah_dir.name})")
        continue

    txt_file = surah_dir / "001.txt"
    if not txt_file.exists():
        print(f"Not found: {txt_file}")
        continue

    with open(txt_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()

    words = text.split()

    if len(words) <= 4:
        print(f"⚠️  Surah {surah_num}: only {len(words)} words, skipping")
        continue

    new_text = ' '.join(words[4:])

    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(new_text)

    fixed += 1
    print(f"✅ Surah {surah_num:3d}: '{' '.join(words[:4])}' removed → '{new_text[:40]}'")

print(f"\n✅ Fixed: {fixed} surahs")
print(f"⏭️  Skipped: {skipped} surahs (Al-Fatiha + At-Tawba)")