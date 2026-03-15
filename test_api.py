import requests
import time

def test_full_quran_retrieval():
    print("🚀 بدء عملية التحقق من بيانات المصحف كاملًا...")
    
    # روابط النسخة الكاملة (نص وصوت)
    text_api_url = "https://api.alquran.cloud/v1/quran/quran-simple"
    audio_api_url = "https://api.alquran.cloud/v1/quran/ar.husary"
    
    start_time = time.time()
    
    try:
        # 1. سحب النصوص
        print("📥 جاري تحميل النصوص (6236 آية)...")
        text_data = requests.get(text_api_url).json()
        
        # 2. سحب روابط الصوت
        print("📥 جاري تحميل روابط الصوت للشيخ الحصري...")
        audio_data = requests.get(audio_api_url).json()
        
        if text_data['code'] == 200 and audio_data['code'] == 200:
            total_text_ayahs = 0
            total_audio_ayahs = 0
            
            # فحص النصوص
            for surah in text_data['data']['surahs']:
                total_text_ayahs += len(surah['ayahs'])
            
            # فحص الصوتيات
            for surah in audio_data['data']['surahs']:
                total_audio_ayahs += len(surah['ayahs'])
            
            end_time = time.time()
            duration = end_time - start_time
            
            # --- التقرير النهائي ---
            print("\n" + "="*30)
            print("📊 تقرير الفحص النهائي:")
            print(f"✅ إجمالي عدد الآيات (نص): {total_text_ayahs}")
            print(f"✅ إجمالي عدد الآيات (صوت): {total_audio_ayahs}")
            print(f"⏱️ الوقت المستغرق: {duration:.2f} ثانية")
            
            if total_text_ayahs == 6236 and total_audio_ayahs == 6236:
                print("🔥 مبروك! البيانات كاملة ومطابقة للمعيار العالمي (6236 آية).")
            else:
                print("⚠️ هناك اختلاف في عدد الآيات، يرجى مراجعة الـ API.")
            print("="*30)
            
        else:
            print("❌ فشل الاتصال بالـ API.")
            
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    test_full_quran_retrieval()