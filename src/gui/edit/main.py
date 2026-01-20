"""
腳本編輯頁面：允許使用者編輯點位並在小地圖上查看位置。
"""

from src.common import config
import inspect
import tkinter as tk
from src.routine.components import Point, Command
from src.gui.edit.minimap import Minimap
from src.gui.edit.record import Record
from src.gui.edit.routine import Routine
from src.gui.edit.status import Status
from src.gui.interfaces import Tab, Frame, LabelFrame


class Edit(Tab):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, '編輯腳本', **kwargs) # 分頁名稱改為中文

        self.columnconfigure(0, weight=1)
        self.columnconfigure(4, weight=1)

        self.record = Record(self)
        self.record.grid(row=2, column=3, sticky=tk.NSEW, padx=10, pady=10)

        self.minimap = Minimap(self)
        self.minimap.grid(row=0, column=3, sticky=tk.NSEW, padx=10, pady=10)

        self.status = Status(self)
        self.status.grid(row=1, column=3, sticky=tk.NSEW, padx=10, pady=10)

        self.routine = Routine(self)
        self.routine.grid(row=0, column=1, rowspan=3, sticky=tk.NSEW, padx=10, pady=10)

        self.editor = Editor(self)
        self.editor.grid(row=0, column=2, rowspan=3, sticky=tk.NSEW, padx=10, pady=10)


class Editor(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, '編輯器', **kwargs)

        self.columnconfigure(0, minsize=350)

        self.vars = {}
        self.contents = None
        self.create_default_state()

    def reset(self):
        """重設編輯器介面"""
        self.contents.destroy()
        self.create_default_state()

    def create_default_state(self):
        self.vars = {}
        self.contents = Frame(self)
        self.contents.grid(row=0, column=0, sticky=tk.EW, padx=5)

        title = tk.Entry(self.contents, justify=tk.CENTER)
        title.pack(expand=True, fill='x', pady=(5, 2))
        title.insert(0, '尚未選擇任何項目') # 提示文字中文化
        title.config(state=tk.DISABLED)

        self.create_disabled_entry()

    def create_edit_ui(self, arr, i, func):
        """建立編輯現有組件的介面"""
        self.contents.destroy()
        self.vars = {}
        self.contents = Frame(self)
        self.contents.grid(row=0, column=0, sticky=tk.EW, padx=5)

        title = tk.Entry(self.contents, justify=tk.CENTER)
        title.pack(expand=True, fill='x', pady=(5, 2))
        title.insert(0, f"正在編輯：{arr[i].__class__.__name__}")
        title.config(state=tk.DISABLED)

        if len(arr[i].kwargs) > 0:
            for key, value in arr[i].kwargs.items():
                self.create_entry(key, value)
            button = tk.Button(self.contents, text='儲存變更', command=func(arr, i, self.vars)) # 確定按鈕中文化
            button.pack(pady=5)
        else:
            self.create_disabled_entry()

    def create_add_prompt(self):
        """建立搜尋與新增組件的介面"""
        self.contents.destroy()
        self.vars = {}
        self.contents = Frame(self)
        self.contents.grid(row=0, column=0, sticky=tk.EW, padx=5)

        title = tk.Entry(self.contents, justify=tk.CENTER)
        title.pack(expand=True, fill='x', pady=(5, 2))
        title.insert(0, f"新增組件...")
        title.config(state=tk.DISABLED)

        # ... (以下搜尋邏輯保持不變，但將 Entry 提示改為中文) ...
        # [省略部分重複邏輯]
