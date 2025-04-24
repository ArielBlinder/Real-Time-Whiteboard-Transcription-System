import tkinter as tk
from tkinter import filedialog

def select_images():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    filetypes = [
        ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
        ("All files", "*.*")
    ]

    # Ask user to select one or more image files
    file_paths = filedialog.askopenfilenames(
        title="Select Image(s)",
        filetypes=filetypes
    )

    return list(file_paths)

# Example usage
if __name__ == "__main__":
    selected_images = select_images()
    if selected_images:
        print("Selected files:")
        for img in selected_images:
            print(img)
    else:
        print("No files selected.")
