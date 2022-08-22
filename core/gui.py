import os
import threading
import functools
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

    def open_file(self) -> str:
        filename = filedialog.askopenfilename()

        return filename

    def open_directory(self) -> str:
        directoryname = filedialog.askdirectory()

        return directoryname


class MainApp(App):
    def __init__(self, master):
        super(MainApp, self).__init__(master)

        # Define variables
        self.txt_path = tk.StringVar()
        self.save_path = tk.StringVar()

        file_selector = tk.LabelFrame(master, text="文件路径", padx=5, pady=5)
        file_selector.pack(side="top")

        tk.Label(file_selector, text="TXT文件: ").grid(row=0)
        tk.Label(file_selector, text="文件保存目录： ").grid(row=1)

        e1 = tk.Entry(file_selector, textvariable=self.txt_path)
        e2 = tk.Entry(file_selector, textvariable=self.save_path)
        e1.grid(row=0, column=1, padx=10, pady=5)
        e2.grid(row=1, column=1, padx=10, pady=5)

        b1 = tk.Button(file_selector, text="打开", command=self.__get_txt_path)
        b2 = tk.Button(file_selector, text="打开", command=self.__get_txt_save_path)
        b1.grid(row=0, column=2, padx=5, pady=5)
        b2.grid(row=1, column=2, padx=5, pady=5)

        # Add menubar entry
        self.menubar_file.add_command(label="打开", command=self.__get_txt_path)

        bottom_area = tk.Frame(master, padx=5, pady=5)
        bottom_area.pack(side="bottom")

        b3 = tk.Button(bottom_area, text="Bui~!", command=self.__main_process)
        b4 = tk.Button(bottom_area, text="打开dir~")
        b3.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        b4.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        # TODO: Add function to open txt save dir

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
        self.log.insert(tk.INSERT, "[ info ] Select TXT file: %s \n" % str(path))
        self.txt_path.set(path)

    def __get_txt_save_path(self):
        path = self.open_directory()
        self.log.insert(tk.INSERT, "[ info ] Select save path: %s \n" % str(path))
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
            self.log.insert(tk.INSERT, "[ info ] Success! Stored in: \n %s" % str(os.path.join(self.save_path.get(), "output.txt")))

        thread = threading.Thread(
            target=all_in_one,
            name="process1"
        )
        thread.start()
        messagebox.showinfo(
            title="",
            message="任务开始！"
        )

