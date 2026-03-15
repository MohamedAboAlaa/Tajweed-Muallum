import json

def check_quran_json_structure(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        issues = []
        total_ayas_checked = 0
        
        for surah_key, surah_data in data.items():
            surah_name = surah_data.get('surah_name', 'Unknown')
            ayat = surah_data.get('ayat', {})
            
            for aya_key, aya_data in ayat.items():
                total_ayas_checked += 1
                words = aya_data.get('words', [])
                
                if not words or len(words) == 0:
                    issues.append({
                        "surah": surah_name,
                        "aya_num": aya_data.get('aya_number'),
                        "text": aya_data.get('text', '')
                    })

        print(f"Checked {total_ayas_checked} ayas")
        
        if issues:
            print(f"Found: {len(issues)} ayas without words:\n")
            print(f"{'Surah':<15} | {'Aya Num: ':<10} | {'Text'}")
            print("-" * 60)
            for iss in issues:
                print(f"{iss['surah']:<15} | {iss['aya_num']:<10} | {iss['text']}")
        else:
            print("All Good!")

    except Exception as e:
        print(f"Error: {e}")

check_quran_json_structure('/home/mohamed-alaa/AboAlaa/Me/Work/Self_Startup/Tajweed-Muallum/quran_timestamps.json')