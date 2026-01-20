import os
import tkinter as tk
from src.common import config, utils
from src.gui.interfaces import MenuBarItem
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno

class File(MenuBarItem):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, '檔案', **kwargs) # 選單大標題

        self.add_command(
            label='新建腳本',
            command=utils.async_callback(self, File._new_routine),
            state=tk.DISABLED
        )
        self.add_command(
            label='儲存腳本', # 儲存你做好的動作
            command=utils.async_callback(self, File._save_routine),
            state=tk.DISABLED
        )
        self.add_separator()
        self.add_command(
            label='讀取指令', # 載入你的職業按鍵
            command=utils.async_callback(self, File._load_commands)
        )
        self.add_command(
            label='載入腳本', # 開啟現有的地圖動作檔
            command=utils.async_callback(self, File._load_routine),
            state=tk.DISABLED
        )

    def enable_routine_state(self):
        """成功載入職業指令後，才能開啟腳本功能"""
        self.entryconfig('新建腳本', state=tk.NORMAL)
        self.entryconfig('儲存腳本', state=tk.NORMAL)
        self.entryconfig('載入腳本', state=tk.NORMAL)

    # ... (其餘功能邏輯如 _new_routine 等)
