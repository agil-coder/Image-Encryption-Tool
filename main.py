from encryptor import process_image

def run():
    print("--- Image Encryptor ---")
    path = input("Enter the full name of your image (e.g., photo.jpg): ")
    key = int(input("Enter a secret numerical key (1-255): "))
    
    try:
        result = process_image(path, key)
        result.save("output_image.png")
        print("Success! Look for 'output_image.png' in your folder.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()