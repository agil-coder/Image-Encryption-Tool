import customtkinter as ctk
from PIL import Image
import encryptor
import os
from tkinter import filedialog # Allows picking files from your computer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Image Vault Pro")
        self.geometry("600x800")
        
        self.selected_path = None # Stores the path of the image you pick

        self.label = ctk.CTkLabel(self, text="Image Steganography", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # 1. BROWSE SECTION
        self.browse_btn = ctk.CTkButton(self, text="Step 1: Select Image", fg_color="gray", command=self.browse_file)
        self.browse_btn.pack(pady=10)
        
        self.path_label = ctk.CTkLabel(self, text="No file selected", font=("Arial", 10))
        self.path_label.pack()

        # 2. DISPLAY SECTION
        self.image_display = ctk.CTkLabel(self, text="")
        self.image_display.pack(pady=10)

        # 3. ACTION SECTION
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter secret message...", width=300)
        self.entry.pack(pady=10)

        self.hide_btn = ctk.CTkButton(self, text="Step 2: Hide & Save", command=self.hide_data)
        self.hide_btn.pack(pady=5)

        self.reveal_btn = ctk.CTkButton(self, text="Step 3: Reveal from Selected", command=self.reveal_data)
        self.reveal_btn.pack(pady=5)

        self.result_label = ctk.CTkLabel(self, text="", text_color="yellow", wraplength=500)
        self.result_label.pack(pady=20)

    def browse_file(self):
        # This opens the Windows/Mac file picker
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.selected_path = file_path
            self.path_label.configure(text=os.path.basename(file_path))
            # Preview the original image
            temp_img = Image.open(file_path)
            self.display_image(temp_img)

    def display_image(self, pil_image):
        ratio = min(400 / pil_image.width, 300 / pil_image.height)
        new_size = (int(pil_image.width * ratio), int(pil_image.height * ratio))
        ctk_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=new_size)
        self.image_display.configure(image=ctk_img, text="")
        self.image_display.image = ctk_img

    def hide_data(self):
        if not self.selected_path:
            self.result_label.configure(text="Error: Select an image first!", text_color="red")
            return
        
        msg = self.entry.get()
        if msg:
            try:
                img = encryptor.hide_message(self.selected_path, msg)
                save_path = filedialog.asksaveasfilename(defaultextension=".png")
                if save_path:
                    img.save(save_path)
                    self.result_label.configure(text=f"Success! Saved to {os.path.basename(save_path)}", text_color="green")
            except Exception as e:
                self.result_label.configure(text=f"Error: {e}", text_color="red")

    def reveal_data(self):
        if not self.selected_path:
            self.result_label.configure(text="Error: Select the encrypted image first!", text_color="red")
            return
            
        try:
            annotated_img, msg = encryptor.reveal_and_annotate(self.selected_path)
            if annotated_img:
                self.display_image(annotated_img)
                self.result_label.configure(text=f"Revealed Message: {msg}", text_color="yellow")
        except Exception as e:
            self.result_label.configure(text=f"Error: {e}", text_color="red")

if __name__ == "__main__":
    app = App()
    app.mainloop()
