import os
from tkinter import *
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def images_to_pdf(image_folder, output_pdf_path):
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    image_files.sort()

    if not image_files:
        return False

    image_list = []
    for img_file in image_files:
        img = Image.open(os.path.join(image_folder, img_file))
        if img.mode == "RGBA":
            img = img.convert("RGB")
        image_list.append(img)

    image_list[0].save(output_pdf_path, save_all=True, append_images=image_list[1:])
    return True


def extract_pages_logic(input_pdf_path, start_page, end_page, output_pdf_path):
    try:
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        if start_page > len(reader.pages) or end_page > len(reader.pages):
            messagebox.showerror(
                "Page Error",
                f"Document has only {len(reader.pages)} pages."
            )
            return False

        for i in range(start_page - 1, end_page):
            writer.add_page(reader.pages[i])

        with open(output_pdf_path, "wb") as output_file:
            writer.write(output_file)

        return True

    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")
        return False


def combine_pdfs(folder_path, output_pdf_path):
    try:
        writer = PdfWriter()
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
        pdf_files.sort()

        if not pdf_files:
            messagebox.showerror("Error", "No PDFs found in the folder.")
            return False

        for pdf_file in pdf_files:
            reader = PdfReader(os.path.join(folder_path, pdf_file))
            for page in reader.pages:
                writer.add_page(page)

        with open(output_pdf_path, "wb") as output_file:
            writer.write(output_file)

        return True

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False


# UI logic for menu actions
def menu_extract_pages():
    input_pdf = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF Files", "*.pdf")])
    if not input_pdf:
        return

    extract_window = Toplevel(root)
    extract_window.title("Extract PDF Pages")
    extract_window.geometry("350x200")

    Label(extract_window, text="Start Page:").pack(pady=5)
    start_entry = Entry(extract_window, width=10)
    start_entry.pack()

    Label(extract_window, text="End Page:").pack(pady=5)
    end_entry = Entry(extract_window, width=10)
    end_entry.pack()

    def process_extraction():
        try:
            start_p = int(start_entry.get())
            end_p = int(end_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")
            return

        output_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Extracted PDF")
        if not output_pdf:
            return

        success = extract_pages_logic(input_pdf, start_p, end_p, output_pdf)
        if success:
            messagebox.showinfo("Success", "Pages extracted successfully.")
            extract_window.destroy()

    Button(extract_window, text="Extract", command=process_extraction).pack(pady=10)


def menu_combine_pdfs():
    folder = filedialog.askdirectory(title="Select Folder Containing PDFs")
    if not folder:
        return

    output_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Combined PDF")
    if not output_pdf:
        return

    # Optional: convert images inside folder into separate PDF
    images_to_pdf(folder, os.path.join(folder, "combined_images.pdf"))

    success = combine_pdfs(folder, output_pdf)
    if success:
        messagebox.showinfo("Success", "PDFs combined successfully.")


def menu_about():
    messagebox.showinfo("About", "PDF Toolkit\nVersion 1.0\nCreated in Python")


# Main Window
root = Tk()
root.title("PDF Toolkit")
root.geometry("500x350")

# Menubar
menubar = Menu(root)

# File Menu
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

# Tools Menu
tools_menu = Menu(menubar, tearoff=0)
tools_menu.add_command(label="Extract Pages from PDF", command=menu_extract_pages)
tools_menu.add_command(label="Combine PDFs in Folder", command=menu_combine_pdfs)
menubar.add_cascade(label="Tools", menu=tools_menu)

# Help Menu
help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=menu_about)
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)

# Intro Label
Label(root, text="PDF Toolkit", font=("Arial", 18, "bold")).pack(pady=40)
Label(root, text="Use the Tools menu to manage PDFs.", font=("Arial", 12)).pack()

root.mainloop()
