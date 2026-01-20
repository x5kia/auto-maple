import os
import tkinter as tk
from src.common import config, utils
from src.gui.interfaces import MenuBarItem
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno


class File(MenuBarItem):
    def __init__(self, parent, **kwargs):
        # 初始化選單名稱為「檔案」
        super().__init__(parent, '檔案', **kwargs)

        self.add_command(
            label='新建腳本',
            command=utils.async_callback(self, File._new_routine),
            state=tk.DISABLED
        )
        self.add_command(
            label='儲存腳本', # 你建議的名稱
            command=utils.async_callback(self, File._save_routine),
            state=tk.DISABLED
        )
        self.add_separator()
        self.add_command(
            label='讀取指令', # 你建議的名稱
            command=utils.async_callback(self, File._load_commands)
        )
        self.add_command(
            label='載入腳本',
            command=utils.async_callback(self, File._load_routine),
            state=tk.DISABLED
        )

    def enable_routine_state(self):
        """當指令書讀取成功後，啟動儲存與新建腳本的功能"""
        self.entryconfig('新建腳本', state=tk.NORMAL)
        self.entryconfig('儲存腳本', state=tk.NORMAL)
        self.entryconfig('載入腳本', state=tk.NORMAL)

    @staticmethod
    @utils.run_if_disabled('\n[!] 自動程式運行中，無法新建腳本')
    def _new_routine():
        if config.routine.dirty:
            if not askyesno(title='新建腳本',
                            message='目前的腳本還有未儲存的變更，確定要直接新建嗎？',
                            icon='warning'):
                return
        config.routine.clear()

    @staticmethod
    @utils.run_if_disabled('\n[!] 自動程式運行中，無法儲存腳本')
    def _save_routine():
        file_path = asksaveasfilename(initialdir=get_routines_dir(),
                                      title='儲存腳本',
                                      filetypes=[('*.csv', '*.csv')],
                                      defaultextension='*.csv')
        if file_path:
            config.routine.save(file_path)

    @staticmethod
    @utils.run_if_disabled('\n[!] 自動程式運行中，無法載入腳本')
    def _load_routine():
        if config.routine.dirty:
            if not askyesno(title='載入腳本',
                            message='目前的腳本還有未儲存的變更，確定要直接載入新腳本嗎？',
                            icon='warning'):
                return
        file_path = askopenfilename(initialdir=get_routines_dir(),
                                    title='選擇腳本檔案',
                                    filetypes=[('*.csv', '*.csv')])
        if file_path:
            config.routine.load(file_path)

    @staticmethod
    @utils.run_if_disabled('\n[!] 自動程式運行中，無法更換指令書')
    def _load_commands():
        if config.routine.dirty:
            if not askyesno(title='讀取指令',
                            message='讀取新的指令書會捨棄目前的腳本內容，確定要繼續嗎？',
                            icon='warning'):
                return
        # 設定預設讀取路徑在資源夾內的 command_books
        file_path = askopenfilename(initialdir=os.path.join(config.RESOURCES_DIR, 'command_books'),
                                    title='選擇職業指令書',
                                    filetypes=[('*.py', '*.py')])
        if file_path:
            config.bot.load_commands(file_path)


def get_routines_dir():
    """獲取腳本存放資料夾，若不存在則自動建立"""
    target = os.path.join(config.RESOURCES_DIR, 'routines', config.bot.command_book.name)
    if not os.path.exists(target):
        os.makedirs(target)
    return target
