import os
import requests
import concurrent.futures
from tqdm import tqdm

BASE_DIR = "Quran_Database"
AUDIO_EDITION = "ar.husary"
TEXT_EDITION = "quran-simple"

def setup_folders():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

def download_ayah(ayah_info):
    surah_num = str(ayah_info['surah_num']).zfill(3)
    ayah_num = str(ayah_info['ayah_in_surah']).zfill(3)
    surah_name = ayah_info['surah_name']
    
    surah_path = os.path.join(BASE_DIR, f"{surah_num}_{surah_name}")
    if not os.path.exists(surah_path):
        os.makedirs(surah_path, exist_ok=True)
        
    audio_file = os.path.join(surah_path, f"{ayah_num}.mp3")
    text_file = os.path.join(surah_path, f"{ayah_num}.txt")

    if not os.path.exists(audio_file):
        try:
            r = requests.get(ayah_info['audio_url'], stream=True)
            with open(audio_file, 'wb') as f:
                f.write(r.content)
        except:
            pass

    if not os.path.exists(text_file):
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(ayah_info['text'])

def main():
    setup_folders()
    
    print("⏳ Get from API")
    audio_data = requests.get(f"https://api.alquran.cloud/v1/quran/{AUDIO_EDITION}").json()
    text_data = requests.get(f"https://api.alquran.cloud/v1/quran/{TEXT_EDITION}").json()

    all_ayahs = []
    
    for s_idx, surah in enumerate(audio_data['data']['surahs']):
        for a_idx, ayah in enumerate(surah['ayahs']):
            all_ayahs.append({
                'surah_num': surah['number'],
                'surah_name': surah['englishName'],
                'ayah_in_surah': ayah['numberInSurah'],
                'audio_url': ayah['audio'],
                'text': text_data['data']['surahs'][s_idx]['ayahs'][a_idx]['text']
            })

    print(f"✅ Data prepared =  {len(all_ayahs)} aya.")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        list(tqdm(executor.map(download_ayah, all_ayahs), total=len(all_ayahs)))

    print("\n\n✨ Done")

if __name__ == "__main__":
    main()