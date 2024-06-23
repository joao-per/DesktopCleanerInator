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
import json

SETTINGS_FILE = "settings.json"

class DesktopCleanerInator:
	
	def __init__(self, root):
		self.root = root
		self.root.title("Desktop Cleaner")
		self.root.geometry("600x900")
		self.root.configure(bg="#1A1A1D")
		self.create_widgets()

	def save_settings(self):
		settings = {category: entry.get() for category, entry in self.category_paths.items()}
		with open(SETTINGS_FILE, "w") as f:
			json.dump(settings, f)

	def load_settings(self):
		if os.path.exists(SETTINGS_FILE):
			with open(SETTINGS_FILE, "r") as f:
				settings = json.load(f)
			for category, path in settings.items():
				if category in self.category_paths:
					self.category_paths[category].insert(0, path)

	def create_widgets(self):
		self.root.configure(bg="#1A1A1D")

		frame = tk.Frame(self.root, bg="#1A1A1D")
		frame.pack(fill=tk.X, padx=10, pady=5)

		self.title_label = tk.Label(frame, text="Desktop Cleaner", font=("Courier", 20, "bold"), bg="#1A1A1D", fg="#66FF66")
		self.title_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

		self.instructions = tk.Label(frame, text="Select folders for each category (optional):", font=("Courier", 12), bg="#1A1A1D", fg="#CCCCCC")
		self.instructions.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

		self.clean_downloads_var = tk.BooleanVar()
		self.clean_downloads_var.set(True)

		self.clean_downloads_check = tk.Checkbutton(frame, text="Clean Downloads folder", variable=self.clean_downloads_var, font=("Courier", 12), bg="#1A1A1D", fg="#CCCCCC", selectcolor="#1A1A1D", activebackground="#1A1A1D", activeforeground="#CCCCCC")
		self.clean_downloads_check.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

		self.categories = ['Images', 'Music', 'Documents', 'Videos', 'Archives', 'Others']
		self.category_paths = {}

		for idx, category in enumerate(self.categories):
			label = tk.Label(frame, text=f"{category} folder:", font=("Courier", 12), bg="#1A1A1D", fg="#CCCCCC", width=15, anchor='w')
			label.grid(row=idx + 3, column=0, padx=5, pady=5, sticky='w')

			entry = tk.Entry(frame, width=40, font=("Courier", 10), bg="#333333", fg="#CCCCCC", insertbackground="#CCCCCC")
			entry.grid(row=idx + 3, column=1, padx=5, pady=5)
			self.category_paths[category] = entry

			button = tk.Button(frame, text="Browse", command=lambda c=category: self.browse_folder(c), font=("Courier", 10), bg="#333333", fg="#66FF66", activebackground="#444444", activeforeground="#FFFFFF")
			button.grid(row=idx + 3, column=2, padx=5, pady=5)

		# Backup option
		self.backup_var = tk.BooleanVar()
		self.backup_var.set(True)

		self.backup_check = tk.Checkbutton(frame, text="Create Backup", variable=self.backup_var, font=("Courier", 12), bg="#1A1A1D", fg="#CCCCCC", selectcolor="#1A1A1D", activebackground="#1A1A1D", activeforeground="#CCCCCC")
		self.backup_check.grid(row=9, column=0, columnspan=3, padx=5, pady=5)

		# Move folders option
		self.move_folders_var = tk.BooleanVar()
		self.move_folders_var.set(True)

		self.move_folders_check = tk.Checkbutton(frame, text="Move Folders to a New Folder", variable=self.move_folders_var, font=("Courier", 12), bg="#1A1A1D", fg="#CCCCCC", selectcolor="#1A1A1D", activebackground="#1A1A1D", activeforeground="#CCCCCC")
		self.move_folders_check.grid(row=10, column=0, columnspan=3, padx=5, pady=5)

		# Exclusion list
		exclusion_frame = tk.Frame(frame, bg="#1A1A1D")

		exclusion_label = tk.Label(exclusion_frame, text="Exclude files:", font=("Courier", 12), bg="#1A1A1D", fg="#CCCCCC", width=15, anchor='w')
		exclusion_label.grid(row=11, column=0, padx=5, pady=5, sticky='w')

		self.exclusion_entry = tk.Entry(exclusion_frame, width=40, font=("Courier", 10), bg="#333333", fg="#CCCCCC", insertbackground="#CCCCCC")
		self.exclusion_entry.grid(row=11, column=1, padx=5, pady=5)

		self.add_exclusion_button = tk.Button(exclusion_frame, text="Add", command=self.add_exclusion, font=("Courier", 10), bg="#333333", fg="#66FF66", activebackground="#444444", activeforeground="#FFFFFF")
		self.add_exclusion_button.grid(row=11, column=2, padx=5, pady=5)

		self.exclusion_list = []

		self.preview_button = tk.Button(frame, text="Preview Files", command=self.preview_files, font=("Courier", 12), bg="#333333", fg="#66FF66", activebackground="#444444", activeforeground="#FFFFFF")
		self.preview_button.grid(row=12, column=0, columnspan=3, padx=5, pady=5)

		self.preview_text = scrolledtext.ScrolledText(frame, width=70, height=10, font=("Courier", 10), bg="#1A1A1D", fg="#CCCCCC", insertbackground="#CCCCCC")
		self.preview_text.grid(row=13, column=0, columnspan=3, padx=5, pady=5)

		self.clean_button = tk.Button(frame, text="Clean Desktop", command=self.clean_desktop, font=("Courier", 12, "bold"), bg="#333333", fg="#66FF66", activebackground="#444444", activeforeground="#FFFFFF")
		self.clean_button.grid(row=14, column=0, columnspan=3, padx=5, pady=5)

		# Add progress bar
		self.progress_bar = Progressbar(frame, orient='horizontal', length=400, mode='determinate', maximum=100)
		self.progress_bar.grid(row=15, column=0, columnspan=3, padx=5, pady=5)

		self.github_button = tk.Button(frame, text="Visit My GitHub", command=self.open_github, font=("Courier", 12), bg="#333333", fg="#66FF66", activebackground="#444444", activeforeground="#FFFFFF")
		self.github_button.grid(row=16, column=0, columnspan=3, padx=5, pady=5)

		self.author_label = tk.Label(frame, text="Made by João Pereira", font=("Courier", 10), bg="#1A1A1D", fg="#666666")
		self.author_label.grid(row=17, column=0, columnspan=3, padx=5, pady=5)

		self.apply_button_styles()

	def apply_button_styles(self):
		style = ttk.Style()
		style.configure("TButton", font=("Courier", 10), padding=5, background="#333333", foreground="#66FF66")
		style.map("TButton", 
			foreground=[('pressed', 'white'), ('active', '#66FF66')],
			background=[('pressed', '!disabled', '#444444'), ('active', '#444444')]
		)

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
		desktop_path, desktop_files = get_desktop_files()
		categorized_files = categorize_files(desktop_files)
		preview_text = "Files to be moved:\n\n"
		for category, files in categorized_files.items():
			preview_text += f"{category}:\n"
			for file in files:
				preview_text += f"  - {file}\n"
			preview_text += "\n"
		
		if self.clean_downloads_var.get():
			home_path = os.path.expanduser('~')
			downloads_path = os.path.join(home_path, 'Downloads')
			downloads_files = [f for f in os.listdir(downloads_path) if os.path.isfile(os.path.join(downloads_path, f))]
			categorized_downloads_files = categorize_files(downloads_files)

			preview_text += "Downloads folder files to be moved:\n\n"
			for category, files in categorized_downloads_files.items():
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
		if self.backup_var.get():
			self.create_backup(desktop_path, files)
		categorized_files = categorize_files(files)

		if self.move_folders_var.get():
			user_folder = os.path.join(desktop_path, os.path.basename(os.path.expanduser('~')))
			if not os.path.exists(user_folder):
				os.makedirs(user_folder)
			self.move_folders(desktop_path, user_folder)

		total_files = sum(len(files) for files in categorized_files.values())
		if total_files == 0:
			messagebox.showinfo("Success", "Desktop is already clean!")
			self.notify_user("Desktop is already clean!")
		else:
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

		if self.clean_downloads_var.get():
			home_path = os.path.expanduser('~')
			downloads_path = os.path.join(home_path, 'Downloads')
			downloads_files = [f for f in os.listdir(downloads_path) if os.path.isfile(os.path.join(downloads_path, f))]
			if self.backup_var.get():
				self.create_backup(downloads_path, downloads_files)
			categorized_downloads_files = categorize_files(downloads_files)

			total_downloads_files = sum(len(files) for files in categorized_downloads_files.values())
			if total_downloads_files > 0:
				for category, entry in self.category_paths.items():
					folder_path = entry.get()
					if not folder_path:
						folder_path = os.path.join(downloads_path, category)
						if not os.path.exists(folder_path):
							os.makedirs(folder_path)
					self.move_files(categorized_downloads_files.get(category, []), downloads_path, folder_path, category)

				messagebox.showinfo("Success", "Downloads folder cleaned up successfully!")
				self.notify_user("Downloads folder is clean!")
			else:
				messagebox.showinfo("Success", "Downloads folder is already clean!")
				self.notify_user("Downloads folder is already clean!")

	def create_backup(self, path, files):
		backup_path = os.path.join(path, "Backup")
		if not os.path.exists(backup_path):
			os.makedirs(backup_path)
		for file in files:
			shutil.copy(os.path.join(path, file), os.path.join(backup_path, file))

	def move_files(self, files, path, dest_path, category):
		for file in files:
			src = os.path.join(path, file)
			if category == 'Images':
				year = self.get_image_year(src)
				year_path = os.path.join(dest_path, year)
				if not os.path.exists(year_path):
					os.makedirs(year_path)
				dst = os.path.join(year_path, file)
			else:
				dst = os.path.join(dest_path, file)
			shutil.move(src, dst)
			self.open_folder(dst)
			
	def move_folders(self, path, user_folder):
		current_dir = os.path.dirname(os.path.abspath(__file__))
		user_folder_name = os.path.basename(user_folder)  # Get the name of the user's folder
		for item in os.listdir(path):
			item_path = os.path.join(path, item)
			if os.path.isdir(item_path) and item_path != current_dir and item != user_folder_name:
				shutil.move(item_path, os.path.join(user_folder, item))

	def open_folder(self, path):
		folder_path = os.path.dirname(path)
		os.startfile(folder_path)

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
	home_path = os.path.expanduser('~')
	desktop_path = os.path.join(home_path, 'Desktop')
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
