import tkinter as tk
from src.gui.interfaces import KeyBindings
from src.gui.settings.pets import Pets
from src.gui.interfaces import Tab, Frame
from src.common import config

class Settings(Tab):
    def __init__(self, parent, **kwargs):
        # 將分頁標題命名為「系統設定」
        super().__init__(parent, '系統設定', **kwargs)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)

        # 第一欄：放置控制與通用按鍵設定
        self.column1 = Frame(self)
        self.column1.grid(row=0, column=1, sticky=tk.N, padx=10, pady=10)
        
        # 中文化介面標題：Auto Maple 控制
        self.controls = KeyBindings(self.column1, '程式快捷鍵控制', config.listener)
        self.controls.pack(side=tk.TOP, fill='x', expand=True)
        
        # 中文化介面標題：遊戲內按鍵
        self.common_bindings = KeyBindings(self.column1, '遊戲內按鍵設定', config.bot)
        self.common_bindings.pack(side=tk.TOP, fill='x', expand=True, pady=(10, 0))
        
        # 寵物設定區塊
        self.pets = Pets(self.column1)
        self.pets.pack(side=tk.TOP, fill='x', expand=True, pady=(10, 0))

        # 第二欄：顯示特定職業的按鍵
        self.column2 = Frame(self)
        self.column2.grid(row=0, column=2, sticky=tk.N, padx=10, pady=10)
        self.class_bindings = KeyBindings(self.column2, '尚未讀取職業指令', None)
        self.class_bindings.pack(side=tk.TOP, fill='x', expand=True)

    def update_class_bindings(self):
        """當讀取指令後，更新右側的職業按鍵顯示"""
        self.class_bindings.destroy()
        class_name = config.bot.command_book.name.capitalize()
        # 顯示例如「Kanna 專屬按鍵」
        self.class_bindings = KeyBindings(self.column2, f'{class_name} 職業按鍵', config.bot.command_book)
        self.class_bindings.pack(side=tk.TOP, fill='x', expand=True)
