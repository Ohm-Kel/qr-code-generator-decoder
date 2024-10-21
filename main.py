import os
import qrcode
import cv2
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, font

def convert_to_png(image_path):
    """Convert an unsupported image format (PDF, SVG, etc.) to PNG using Pillow."""
    img = Image.open(image_path)
    # Create a new file path with .png extension
    png_path = os.path.splitext(image_path)[0] + '.png'
    img.save(png_path, 'PNG')
    return png_path

def generate_qr_code(url, folder_path, file_name, color='black', background='white'):
    """Generates a QR code for the given URL and saves it to the specified folder and file."""
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill=color, back_color=background)
    img.save(file_path)

    print(f"QR code generated and saved to {file_path}")

def decode_qr_code(image_path):
    """Decodes a QR code from an image and prints the URL encoded in the QR code."""
    unsupported_formats = ['.pdf', '.eps', '.ai', '.svg', '.heic', '.raw']
    file_extension = os.path.splitext(image_path)[1].lower()

    if file_extension in unsupported_formats:
        print(f"Converting {image_path} to PNG...")
        image_path = convert_to_png(image_path)

    if not os.path.exists(image_path):
        print(f"Error: The file {image_path} does not exist. Please check the path.")
        return None

    img = cv2.imread(image_path)

    if img is None:
        print(f"Error: Failed to load the image at {image_path}. Check the file path and format.")
        return None

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img)

    if points is not None and data:
        print(f"QR Code detected and the URL is: {data}")
        return data
    else:
        print("No QR code found or the image is not a QR code.")
        return None

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator and Decoder")
        self.root.geometry("400x300")
        self.root.configure(bg='#f7f7f7')

        # Set the application font
        self.title_font = font.Font(family='Helvetica', size=16, weight='bold')

        tk.Label(root, text="QR Code Generator and Decoder", font=self.title_font, bg='#f7f7f7').pack(pady=10)

        tk.Label(root, text="Enter URL:", bg='#f7f7f7').pack(pady=(5, 0))
        self.url_entry = tk.Entry(root, width=40)
        self.url_entry.pack(pady=5)

        tk.Label(root, text="QR Code Color:", bg='#f7f7f7').pack(pady=(5, 0))
        self.color_entry = tk.Entry(root, width=20)
        self.color_entry.insert(0, "black")  # Default color
        self.color_entry.pack(pady=5)

        tk.Label(root, text="Background Color:", bg='#f7f7f7').pack(pady=(5, 0))
        self.background_entry = tk.Entry(root, width=20)
        self.background_entry.insert(0, "white")  # Default background
        self.background_entry.pack(pady=5)

        # Use a frame for buttons to allow for better spacing
        button_frame = tk.Frame(root, bg='#f7f7f7')
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Generate QR Code", command=self.generate_qr_code, width=20, bg='#4CAF50', fg='white', activebackground='#45a049').grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Decode QR Code", command=self.decode_qr_code, width=20, bg='#2196F3', fg='white', activebackground='#0b7dda').grid(row=0, column=1, padx=5)

        # Add footer instructions
        tk.Label(root, text="Select colors in English (e.g., red, blue)", bg='#f7f7f7', fg='gray').pack(pady=(10, 0))

    def generate_qr_code(self):
        url = self.url_entry.get()
        folder_path = filedialog.askdirectory(title="Select Folder to Save QR Code")
        if folder_path:
            file_name = "qrcode.png"
            color = self.color_entry.get()
            background = self.background_entry.get()
            generate_qr_code(url, folder_path, file_name, color, background)
            messagebox.showinfo("Success", f"QR code saved to {os.path.join(folder_path, file_name)}")

    def decode_qr_code(self):
        image_path = filedialog.askopenfilename(title="Select QR Code Image")
        if image_path:
            result = decode_qr_code(image_path)
            if result:
                messagebox.showinfo("Decoded URL", f"QR Code URL: {result}")

def main():
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
