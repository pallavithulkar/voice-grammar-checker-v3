import tkinter as tk
from tkinter import messagebox, filedialog
import speech_recognition as sr
from deep_translator import GoogleTranslator
import pyttsx3
import random

engine = pyttsx3.init()
history = []

# Daily word list
daily_words = [
    {"word": "grateful", "sentence": "I am grateful for your help."},
    {"word": "patience", "sentence": "Patience is a virtue."},
    {"word": "ambition", "sentence": "Her ambition is to become a scientist."},
    {"word": "courage", "sentence": "It takes courage to speak the truth."},
    {"word": "achieve", "sentence": "You can achieve anything with effort."}
]

def basic_grammar_fix(text):
    corrections = {
        "i am": "I am", "i'm": "I'm", "my name is": "My name is",
        "i like": "I like", "i want": "I want", "he is": "He is",
        "she is": "She is", "they is": "They are", "we is": "We are",
        "you is": "You are"
    }
    lower_text = text.lower()
    corrected = text
    for wrong, right in corrections.items():
        if wrong in lower_text:
            corrected = corrected.replace(wrong, right)
    return corrected

def listen_and_fix():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            label_status.config(text="Listening...", fg="#0078d7")
            window.update()
            audio = r.listen(source)
            text = r.recognize_google(audio)
            corrected = basic_grammar_fix(text)

            entry_input.delete(0, tk.END)
            entry_input.insert(0, text)

            entry_corrected.delete(0, tk.END)
            entry_corrected.insert(0, corrected)

            label_status.config(text="Correction complete ✅", fg="#28a745")

            history.append(f"You: {text}\nCorrected: {corrected}")
            update_history()
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand your voice.")
            label_status.config(text="Voice not recognized ❌", fg="red")
        except sr.RequestError:
            messagebox.showerror("Error", "Network error.")
            label_status.config(text="Network error ❌", fg="red")

def check_typed_grammar():
    typed_text = entry_input.get()
    corrected = basic_grammar_fix(typed_text)

    entry_corrected.delete(0, tk.END)
    entry_corrected.insert(0, corrected)

    label_status.config(text="Correction complete ✅", fg="#28a745")

    history.append(f"You: {typed_text}\nCorrected: {corrected}")
    update_history()

def update_history():
    text_history.delete("1.0", tk.END)
    for item in history[-5:]:
        text_history.insert(tk.END, item + "\n\n")

def translate_to_hindi():
    eng_text = entry_corrected.get()
    if eng_text.strip() != "":
        translated = GoogleTranslator(source='auto', target='hi').translate(eng_text)
        messagebox.showinfo("Hindi Translation", translated)

def speak_corrected():
    corrected_text = entry_corrected.get()
    if corrected_text.strip():
        engine.say(corrected_text)
        engine.runAndWait()

def save_history_to_file():
    if not history:
        messagebox.showwarning("Warning", "No history to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n\n".join(history))
        messagebox.showinfo("Saved", "History saved successfully.")

# 📚 Spelling Practice Feature
def open_spelling_practice():
    word_data = random.choice(daily_words)
    word = word_data["word"]
    sentence = word_data["sentence"]

    spell_win = tk.Toplevel(window)
    spell_win.title("📚 Daily Spelling Practice")
    spell_win.geometry("450x400")
    spell_win.config(bg="#fffaf0")

    tk.Label(spell_win, text="Word of the Day", font=("Segoe UI", 14, "bold"), bg="#fffaf0").pack(pady=10)
    tk.Label(spell_win, text=word, font=("Segoe UI", 18), fg="green", bg="#fffaf0").pack()

    tk.Label(spell_win, text=sentence, wraplength=400, font=("Segoe UI", 11), bg="#fffaf0").pack(pady=10)

    entry_spell = tk.Entry(spell_win, font=("Segoe UI", 14))
    entry_spell.pack(pady=10)

    def check_spelling():
        user_input = entry_spell.get().strip().lower()
        if user_input == word.lower():
            messagebox.showinfo("✅ Correct!", "You spelled it right!")
        else:
            messagebox.showerror("❌ Oops!", f"Correct spelling: {word}")

    def speak_word():
        engine.say(word)
        engine.runAndWait()

    tk.Button(spell_win, text="Check Spelling", font=("Segoe UI", 11), bg="#17a2b8", fg="white", command=check_spelling).pack(pady=5)
    tk.Button(spell_win, text="🔊 Hear Pronunciation", font=("Segoe UI", 11), bg="#28a745", fg="white", command=speak_word).pack(pady=5)

# 🖼 GUI Setup
window = tk.Tk()
window.title("Voice Grammar Checker v3")
window.geometry("600x620")
window.configure(bg="#f5f7fa")

label_title = tk.Label(window, text="Voice Grammar Checker v3", font=("Segoe UI", 16, "bold"), bg="#f5f7fa", fg="#333")
label_title.pack(pady=10)

entry_input = tk.Entry(window, font=("Segoe UI", 12), width=60)
entry_input.pack(pady=5)
entry_input.insert(0, "You said:")

entry_corrected = tk.Entry(window, font=("Segoe UI", 12), width=60)
entry_corrected.pack(pady=5)
entry_corrected.insert(0, "Corrected:")

btn_listen = tk.Button(window, text="🎤 Start Listening", font=("Segoe UI", 11), bg="#0078d7", fg="white", width=25, command=listen_and_fix)
btn_listen.pack(pady=5)

btn_check = tk.Button(window, text="📝 Check Typed Grammar", font=("Segoe UI", 11), bg="#17a2b8", fg="white", width=25, command=check_typed_grammar)
btn_check.pack(pady=5)

btn_translate = tk.Button(window, text="🌐 Translate to Hindi", font=("Segoe UI", 11), bg="#ffcc00", fg="black", width=25, command=translate_to_hindi)
btn_translate.pack(pady=5)

btn_speak = tk.Button(window, text="📢 Speak Corrected Text", font=("Segoe UI", 11), bg="#28a745", fg="white", width=25, command=speak_corrected)
btn_speak.pack(pady=5)

btn_save = tk.Button(window, text="💾 Save History", font=("Segoe UI", 11), bg="#6c757d", fg="white", width=25, command=save_history_to_file)
btn_save.pack(pady=5)

btn_spell_practice = tk.Button(window, text="📚 Daily Spelling Practice", font=("Segoe UI", 11), bg="#ff69b4", fg="white", width=25, command=open_spelling_practice)
btn_spell_practice.pack(pady=5)

label_history = tk.Label(window, text="📝 History (Last 5):", font=("Segoe UI", 10, "bold"), bg="#f5f7fa", fg="#444")
label_history.pack()

text_history = tk.Text(window, height=8, width=70, font=("Segoe UI", 10))
text_history.pack(pady=5)

btn_exit = tk.Button(window, text="❌ Exit", font=("Segoe UI", 11), bg="#cccccc", fg="black", width=10, command=window.quit)
btn_exit.pack(pady=10)

label_status = tk.Label(window, text="", font=("Segoe UI", 10), bg="#f5f7fa", fg="#666")
label_status.pack(pady=5)

window.mainloop()
