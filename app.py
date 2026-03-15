import gradio as gr
import requests

def get_quran_data(surah_num, start_ayah, end_ayah):
    full_text = ""
    audio_links = []
    
    try:
        # بنلف على الآيات من البداية للنهاية
        for ayah_num in range(start_ayah, end_ayah + 1):
            # 1. طلب النص (simple text)
            text_url = f"https://api.alquran.cloud/v1/ayah/{surah_num}:{ayah_num}/quran-simple"
            text_response = requests.get(text_url).json()
            
            # 2. طلب الصوت (الشيخ الحصري)
            audio_url = f"https://api.alquran.cloud/v1/ayah/{surah_num}:{ayah_num}/ar.husary"
            audio_response = requests.get(audio_url).json()
            
            if text_response['code'] == 200 and audio_response['code'] == 200:
                ayah_text = text_response['data']['text']
                ayah_audio = audio_response['data']['audio']
                
                full_text += f"({ayah_num}) {ayah_text} \n\n"
                audio_links.append(ayah_audio)
            else:
                return "خطأ في بيانات الآية، تأكد من الأرقام.", None
        
        # تجميع روابط الصوت في شكل HTML عشان Gradio يعرضهم كلهم
        audio_html = ""
        for i, link in enumerate(audio_links):
            audio_html += f"<p>آية {start_ayah + i}:</p><audio controls><source src='{link}' type='audio/mpeg'></audio><br>"
            
        return full_text, audio_html

    except Exception as e:
        return f"حدث خطأ: {str(e)}", ""

# --- واجهة Gradio ---
with gr.Blocks(title="مصحف الحصري المرتل") as demo:
    gr.Markdown("# 📖 مستخرج الآيات والملفات الصوتية")
    gr.Markdown("ادخل رقم السورة ونطاق الآيات للحصول على النص وصوت الشيخ الحصري.")
    
    with gr.Row():
        surah_input = gr.Number(label="رقم السورة", value=1)
        start_input = gr.Number(label="من آية", value=1)
        end_input = gr.Number(label="إلى آية", value=5)
    
    btn = gr.Button("استخراج البيانات", variant="primary")
    
    output_text = gr.Textbox(label="النص القرآني", lines=10)
    output_audio = gr.HTML(label="الملفات الصوتية")

    btn.click(
        fn=get_quran_data, 
        inputs=[surah_input, start_input, end_input], 
        outputs=[output_text, output_audio]
    )

if __name__ == "__main__":
    demo.launch()