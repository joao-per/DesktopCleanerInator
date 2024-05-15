import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
from PIL import Image
from tkinter import scrolledtext
import webbrowser
from tkinter.ttk import Progressbar
from plyer import notification

class DesktopCleanerInator:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Cleaner")
        self.root.geometry("600x725")
        self.root.configure(bg="#1A1A1D")
        #self.root.iconbitmap("icon.ico")
        self.create_widgets()

    def create_widgets(self):
        self.root.configure(bg="#1A1A1D")

        self.title_label = tk.Label(self.root, text="Desktop Cleaner", font=("Courier", 20, "bold"), bg="#1A1A1D", fg="#66FF66")
        self.title_label.pack(pady=10)

        self.instructions = tk.Label(self.root, text="Select folders for each category (optional):", font=("Courier", 12), bg="#1A1A1D", fg="#CCCCCC")
        self.instructions.pack(pady=5)

        self.categories = ['Images', 'Music', 'Documents', 'Videos', 'Archives', 'Others']
        self.category_paths = {}

        frame = tk.Frame(self.root, bg="#1A1A1D")
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        for idx, category in enumerate(self.categories):
            label = tk.Label(frame, text=f"{category} folder:", font=("Courier", 12), bg="#1A1A1D", fg="#CCCCCC", width=15, anchor='w')
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='w')

            entry = tk.Entry(frame, width=40, font=("Courier", 10), bg="#333333", fg="#CCCCCC", insertbackground="#CCCCCC")
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.category_paths[category] = entry

            button = tk.Button(frame, text="Browse", command=lambda c=category: self.browse_folder(c), font=("Courier", 10), bg="#333333", fg="#66FF66", activebackground="#444444", activeforeground="#FFFFFF")
            button.grid(row=idx, column=2, padx=5, pady=5)

            if category == 'Others':
                opt_label = tk.Label(frame, text="(optional)", font=("Courier", 12), bg="#1A1A1D", fg="#666666")
                opt_label.grid(row=idx, column=3, padx=5, pady=5, sticky='w')

        # Exclusion list
        exclusion_frame = tk.Frame(self.root, bg="#1A1A1D")
        exclusion_frame.pack(fill=tk.X, padx=10, pady=5)

        exclusion_label = tk.Label(exclusion_frame, text="Exclude files:", font=("Courier", 12), bg="#1A1A1D", fg="#CCCCCC", width=15, anchor='w')
        exclusion_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.exclusion_entry = tk.Entry(exclusion_frame, width=40, font=("Courier", 10), bg="#333333", fg="#CCCCCC", insertbackground="#CCCCCC")
        self.exclusion_entry.grid(row=0, column=1, padx=5, pady=5)

        self.add_exclusion_button = tk.Button(exclusion_frame, text="Add", command=self.add_exclusion, font=("Courier", 10), bg="#333333", fg="#66FF66", activebackground="#444444", activeforeground="#FFFFFF")
        self.add_exclusion_button.grid(row=0, column=2, padx=5, pady=5)

        self.exclusion_list = []

        self.preview_button = tk.Button(self.root, text="Preview Files", command=self.preview_files, font=("Courier", 12), bg="#333333", fg="#66FF66", activebackground="#444444", activeforeground="#FFFFFF")
        self.preview_button.pack(pady=10)

        self.preview_text = scrolledtext.ScrolledText(self.root, width=70, height=10, font=("Courier", 10), bg="#1A1A1D", fg="#CCCCCC", insertbackground="#CCCCCC")
        self.preview_text.pack(pady=10)

        self.clean_button = tk.Button(self.root, text="Clean Desktop", command=self.clean_desktop, font=("Courier", 12, "bold"), bg="#333333", fg="#66FF66", activebackground="#444444", activeforeground="#FFFFFF")
        self.clean_button.pack(pady=20)

        # Add progress bar
        self.progress_bar = Progressbar(self.root, orient='horizontal', length=400, mode='determinate', maximum=100)
        self.progress_bar.pack(pady=10)

        self.github_button = tk.Button(self.root, text="Visit My GitHub", command=self.open_github, font=("Courier", 12), bg="#333333", fg="#66FF66", activebackground="#444444", activeforeground="#FFFFFF")
        self.github_button.pack(pady=10)

        self.author_label = tk.Label(self.root, text="Made by João Pereira", font=("Courier", 10), bg="#1A1A1D", fg="#666666")
        self.author_label.pack(pady=10)


    def add_exclusion(self):
        file_to_exclude = self.exclusion_entry.get()
        if file_to_exclude and file_to_exclude not in self.exclusion_list:
            self.exclusion_list.append(file_to_exclude)
            self.exclusion_entry.delete(0, tk.END)

    def browse_folder(self, category):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.category_paths[category].delete(0, tk.END)
            self.category_paths[category].insert(0, folder_selected)

    def preview_files(self):
        desktop_path, files = get_desktop_files()
        categorized_files = categorize_files(files)
        preview_text = "Files to be moved:\n\n"
        for category, files in categorized_files.items():
            preview_text += f"{category}:\n"
            for file in files:
                preview_text += f"  - {file}\n"
            preview_text += "\n"
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, preview_text)

    def notify_user(self, message):
        notification.notify(
            title='Desktop Cleaner Inator',
            message=message,
            app_name='Desktop Cleaner',
            timeout=10
        )

    def clean_desktop(self):
        desktop_path, files = get_desktop_files()
        self.create_backup(desktop_path, files)  # Create backup before cleaning
        categorized_files = categorize_files(files)
        
        total_files = sum(len(files) for files in categorized_files.values())
        if total_files == 0:
            messagebox.showinfo("Success", "Desktop is already clean!")
            self.notify_user("Desktop is already clean!")
            return
        processed_files = 0

        for category, entry in self.category_paths.items():
            folder_path = entry.get()
            if not folder_path:
                folder_path = os.path.join(desktop_path, category)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
            self.move_files(categorized_files.get(category, []), desktop_path, folder_path, category)
            
            # Update progress
            processed_files += len(categorized_files.get(category, []))
            progress = (processed_files / total_files) * 100
            self.progress_bar['value'] = progress
            self.root.update_idletasks()
        
        messagebox.showinfo("Success", "Desktop cleaned up successfully!")
        self.notify_user("Everything is cleaned!")
        self.progress_bar['value'] = 0  # Reset progress bar


    def create_backup(self, desktop_path, files):
        backup_path = os.path.join(desktop_path, "DesktopBackup")
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
        for file in files:
            shutil.copy(os.path.join(desktop_path, file), os.path.join(backup_path, file))

    def move_files(self, files, desktop_path, dest_path, category):
        for file in files:
            src = os.path.join(desktop_path, file)
            if category == 'Images':
                year = self.get_image_year(src)
                year_path = os.path.join(dest_path, year)
                if not os.path.exists(year_path):
                    os.makedirs(year_path)
                dst = os.path.join(year_path, file)
            else:
                dst = os.path.join(dest_path, file)
            shutil.move(src, dst)

    def get_image_year(self, filepath):
        try:
            image = Image.open(filepath)
            exif = image._getexif()
            if exif and 36867 in exif:
                date_str = exif[36867]
                year = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S').year
                return str(year)
        except:
            pass
        return str(datetime.fromtimestamp(os.path.getmtime(filepath)).year)

    def open_github(self):
        webbrowser.open_new("https://github.com/joao-per")

def get_desktop_files():
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    files = [f for f in os.listdir(desktop_path) if os.path.isfile(os.path.join(desktop_path, f))]
    return desktop_path, files

def categorize_files(files):
    categories = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'Music': ['.mp3', '.wav', '.aac', '.flac'],
        'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
        'Videos': ['.mp4', '.mov', '.avi', '.mkv'],
        'Archives': ['.zip', '.rar', '.7z', '.tar']
    }
    categorized_files = {key: [] for key in categories}
    categorized_files['Others'] = []

    for file in files:
        file_extension = os.path.splitext(file)[1].lower()
        found = False
        for category, extensions in categories.items():
            if file_extension in extensions:
                categorized_files[category].append(file)
                found = True
                break
        if not found:
            categorized_files['Others'].append(file)
    
    return categorized_files

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopCleanerInator(root)
    root.mainloop()
