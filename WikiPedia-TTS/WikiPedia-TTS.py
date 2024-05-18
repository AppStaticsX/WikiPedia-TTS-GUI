import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import wikipedia as wiki
import pyttsx3 as tts
import os

SMALL_FONT_STYLE = ("Jost", 14, "bold")
DEFAULT_FONT_STYLE = ("Nunito", 18, "bold")
BUTTON_FONT_STYLE = ("Ubuntu Mono", 14, "bold")
ENTRY_FONT_STYLE = ("Ubuntu Mono", 14, "bold")

PURE_DARK = "#000000"
LITE_DARK = "#919191"
MEDIUM_DARK = "#313131"
LABEL_COLOR = "#FFFFFF"

ctk.set_appearance_mode("dark")


class WikiPedia_TTS:
    def __init__(self):
        self.engine = tts.init('sapi5')  # Windows specific text-to-speech engine
        self.voices = self.engine.getProperty('voices')
        
        # Find the system narrator voice
        for voice in self.voices:
            if "Microsoft David Desktop" in voice.name:  # Adjust the voice name according to your system narrator voice
                self.engine.setProperty('voice', voice.id)
                break
            # Adjust voice speed
        self.engine.setProperty('rate', 150)

        self.window = ctk.CTk()
        self.window.geometry("400x532")
        self.window.resizable(False, False)
        self.window.title("AppStaticsX\u2122-WikiPediaTTS")
        self.window.iconbitmap(r'ImageResources\\icon.ico')

        self.window.configure(bg=PURE_DARK)

        self.frame = tk.Frame(self.window, bg=PURE_DARK)
        self.frame.pack(fill="both")
        
        image = Image.open("ImageResources\\top_banner.jpg").resize((384,162)) 
        self.photo = ImageTk.PhotoImage(image)
        self.banner_label = tk.Label(self.frame, image=self.photo, bg=PURE_DARK)
        self.banner_label.pack(fill="x")

        self.lable = ctk.CTkLabel(self.frame, text="Enter What You Need To Know:", font=SMALL_FONT_STYLE, fg_color=PURE_DARK)
        self.lable.pack(pady=3)


        self.entry = ctk.CTkEntry(self.frame, placeholder_text="Type Something...", width=300, font=ENTRY_FONT_STYLE, border_color=LABEL_COLOR)
        self.entry.pack()

        self.search_button = ctk.CTkButton(self.frame,text="SEARCH", font=BUTTON_FONT_STYLE, fg_color=LABEL_COLOR, text_color=PURE_DARK, 
                                           hover_color=LITE_DARK, command=self.search_on_wikipedia)
        self.search_button.pack(pady=10)

        self.result_text = ctk.CTkTextbox(self.frame, height=200, width=350, border_color=LABEL_COLOR, border_width=1, font=ENTRY_FONT_STYLE, )
        self.result_text.pack(pady=5)

        self.save_button = ctk.CTkButton(self.frame, text="SAVE TO FILE", font=BUTTON_FONT_STYLE, fg_color=LABEL_COLOR, text_color=PURE_DARK,
                                         hover_color=LITE_DARK, command=self.save_to_file)
        self.save_button.pack(pady=5)

        self.speak_button = ctk.CTkButton(self.frame, text="SPEAK", font=BUTTON_FONT_STYLE, fg_color=LABEL_COLOR, text_color=PURE_DARK,
                                  hover_color=LITE_DARK, command=self.speak_txt)
        self.speak_button.pack(pady=5)




    def search_on_wikipedia(self):
        query = self.entry.get()
        try:
            results = wiki.summary(query, sentences=150)
            self.result_text.configure(state=tk.NORMAL)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, results)
            self.result_text.configure(state=tk.DISABLED)
        except wiki.exceptions.DisambiguationError as e:
            self.result_text.configure(state=tk.NORMAL)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, "Multiple results found.\nPlease be more specific.")
            self.result_text.configure(state=tk.DISABLED)
        except wiki.exceptions.PageError as e:
            self.result_text.configure(state=tk.NORMAL)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, "No Results found on your Query!")
            self.result_text.configure(state=tk.DISABLED)
    
    def speak_txt(self):
         text = self.result_text.get("1.0", tk.END)
         self.engine.say(text)
         self.engine.runAndWait()
    
    def save_to_file(self):
        query = self.entry.get()
        results = wiki.summary(query,sentences=150 )
        file_path = os.path.join(os.path.expanduser("~"), "Desktop", query + ".txt")
        with open(file_path, 'w') as f:
            f.write(results)



    def run(self):
     self.window.mainloop()


if __name__ == "__main__":
    WikiPediaTTS = WikiPedia_TTS()
    WikiPediaTTS.run()
