"""
This is GUI module.
"""
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from core.utils import split_txt, join_txt


class App(tk.Frame):
    """
    This is basic App class.
    """

    def __init__(self, root):
        """
        :param root: root object of tk
        """
        super().__init__(root)
        self.root = root
        self.pack()

        menubar = tk.Frame(root)
        menubar.pack()

        # Define menubar
        self.menubar = tk.Menu(menubar)
        self.menubar_file = tk.Menu(self.menubar, tearoff=False)

        # Add submenu
        self.menubar.add_cascade(label="文件", menu=self.menubar_file)

        # File menubar

        self.menubar_file.add_command(label="退出", command=root.quit)

        # Config menubar
        root.config(menu=self.menubar)

        self.placeholder = None

    def open_file(self) -> str:
        """
        Open fle Base function.
        :return: filename
        """
        filename = filedialog.askopenfilename()
        self.placeholder = None

        return filename

    def open_directory(self) -> str:
        """
        Open dir base function.
        :return: dir name
        """
        directory_name = filedialog.askdirectory()
        self.placeholder = None

        return directory_name


class MainApp(App):  # pylint: disable=too-many-ancestors
    """
    This is the class for MainApp
    """

    def __init__(self, master):
        super().__init__(master)

        # Define variables
        self.txt_path = tk.StringVar()
        self.save_path = tk.StringVar()

        file_selector = tk.LabelFrame(master, text="文件路径", padx=5, pady=5)
        file_selector.pack(side="top")

        tk.Label(file_selector, text="TXT文件: ").grid(row=0)
        tk.Label(file_selector, text="文件保存目录： ").grid(row=1)

        entry_1 = tk.Entry(file_selector, textvariable=self.txt_path)
        entry_2 = tk.Entry(file_selector, textvariable=self.save_path)
        entry_1.grid(row=0, column=1, padx=10, pady=5)
        entry_2.grid(row=1, column=1, padx=10, pady=5)

        button_1 = tk.Button(file_selector, text="打开", command=self.__get_txt_path)
        button_2 = tk.Button(file_selector, text="打开", command=self.__get_txt_save_path)
        button_1.grid(row=0, column=2, padx=5, pady=5)
        button_2.grid(row=1, column=2, padx=5, pady=5)

        # Add menubar entry
        self.menubar_file.add_command(label="打开", command=self.__get_txt_path)

        bottom_area = tk.Frame(master, padx=5, pady=5)
        bottom_area.pack(side="bottom")

        button_3 = tk.Button(bottom_area, text="Bui~!", command=self.__main_process)
        button_4 = tk.Button(bottom_area, text="打开dir~")
        button_3.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        button_4.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        output_area = tk.LabelFrame(master, text="输出", padx=5, pady=5)
        output_area.pack(side="bottom")

        scrollbar1 = tk.Scrollbar(output_area)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

        self.log = tk.Text(output_area, yscrollcommand=scrollbar1.set, width=43, height=5)
        self.log.pack()
        scrollbar1.config(command=self.log.yview)

        self.log.insert(tk.INSERT, '[ info ] Programme started! ' + "\n")

    def __get_txt_path(self):
        path = self.open_file()
        self.log.insert(tk.INSERT, f"[ info ] Select TXT file: {str(path)} \n")
        self.txt_path.set(path)

    def __get_txt_save_path(self):
        path = self.open_directory()
        self.log.insert(tk.INSERT, f"[ info ] Select save path: {str(path)} \n")
        self.save_path.set(path)

    def __main_process(self):
        self.log.insert(tk.INSERT, "[ info ] Start to process! \n")

        def all_in_one():
            split_txt(
                input_file=self.txt_path.get(),
                output_path=self.save_path.get(),
                logger=self.log
            )
            join_txt(
                txt_store_path=os.path.join(self.save_path.get(), "temp"),
                final_txt_path=self.save_path.get(),
                logger=self.log
            )
            path = str(os.path.join(self.save_path.get(), "output.txt"))
            self.log.insert(tk.INSERT, f"""[ info ] Success! Stored in: \n {path}""" )

        thread = threading.Thread(
            target=all_in_one,
            name="process1"
        )
        thread.start()
        messagebox.showinfo(
            title="",
            message="任务开始！"
        )
