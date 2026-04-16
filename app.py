import customtkinter as ctk
from encryptor import hide_message, reveal_message

# Set the look of the app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Secret Image Vault")
app.geometry("400x300")

def handle_hide():
    # This function links your button to your logic
    msg = entry.get()
    hide_message("test.jpg", msg).save("secret.png")
    label.configure(text="Message Hidden in secret.png!")

label = ctk.CTkLabel(app, text="Image Steganography Tool", font=("Arial", 20))
label.pack(pady=20)

entry = ctk.CTkEntry(app, placeholder_text="Enter secret message...")
entry.pack(pady=10)

btn = ctk.CTkButton(app, text="Hide in Image", command=handle_hide)
btn.pack(pady=10)

app.mainloop()