import gradio as gr
import os

BASE_DIR = os.path.abspath("Quran_Database")

def get_ayah_data(surah_num, start_ayah, end_ayah):
    surah_folder = ""
    text_output = ""
    audio_files = []
    
    prefix = str(int(surah_num)).zfill(3)
    
    try:
        if not os.path.exists(BASE_DIR):
            return "❌ Folder 'Quran_Database' not found!", []
            
        all_folders = os.listdir(BASE_DIR)
        for folder in all_folders:
            if folder.startswith(prefix):
                surah_folder = folder
                break
        
        if not surah_folder:
            return f"❌ Surah {surah_num} not found", []

        for a_num in range(int(start_ayah), int(end_ayah) + 1):
            ayah_prefix = str(a_num).zfill(3)
            text_path = os.path.join(BASE_DIR, surah_folder, f"{ayah_prefix}.txt")
            audio_path = os.path.join(BASE_DIR, surah_folder, f"{ayah_prefix}.mp3")
            
            if os.path.exists(text_path) and os.path.exists(audio_path):
                with open(text_path, 'r', encoding='utf-8') as f:
                    text_output += f"({a_num}) {f.read()}\n\n"
                audio_files.append(os.path.abspath(audio_path))
            else:
                text_output += f"⚠️ Aya {a_num} missing.\n\n"

        return text_output, audio_files

    except Exception as e:
        return f"Error: {str(e)}", []

with gr.Blocks(title="Local Elhusary Mushaf") as demo:
    gr.Markdown("# 📖 Local Elhusary Mushaf")
    
    with gr.Row():
        surah_in = gr.Number(label="Surah", value=1)
        start_in = gr.Number(label="From", value=1)
        end_in = gr.Number(label="To", value=5)
    
    submit_btn = gr.Button("Show Ayas", variant="primary")
    
    out_text = gr.Textbox(label="Text")
    
    audio_list_state = gr.State([])

    @gr.render(inputs=audio_list_state)
    def render_audios(paths):
        if not paths:
            gr.Markdown("No files to show")
        else:
            for path in paths:
                gr.Audio(value=path, label=f"Aya {os.path.basename(path).split('.')[0]}", type="filepath")

    submit_btn.click(
        fn=get_ayah_data,
        inputs=[surah_in, start_in, end_in],
        outputs=[out_text, audio_list_state]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", allowed_paths=[BASE_DIR])