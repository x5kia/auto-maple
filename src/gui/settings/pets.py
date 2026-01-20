import tkinter as tk
from src.gui.interfaces import LabelFrame, Frame
from src.common.interfaces import Configurable

class Pets(LabelFrame):
    def __init__(self, parent, **kwargs):
        # 標題改為「寵物自動餵食」
        super().__init__(parent, '寵物自動餵食', **kwargs)

        self.pet_settings = PetSettings('pets')
        # 從設定檔讀取是否開啟自動餵食與寵物數量
        self.auto_feed = tk.BooleanVar(value=self.pet_settings.get('Auto-feed'))
        self.num_pets = tk.IntVar(value=self.pet_settings.get('Num pets'))

        # 第一列：自動餵食勾選框
        feed_row = Frame(self)
        feed_row.pack(side=tk.TOP, fill='x', expand=True, pady=5, padx=5)
        check = tk.Checkbutton(
            feed_row,
            variable=self.auto_feed,
            text='啟用自動餵食功能',
            command=self._on_change
        )
        check.pack()

        # 第二列：寵物數量選擇
        num_row = Frame(self)
        num_row.pack(side=tk.TOP, fill='x', expand=True, pady=(0, 5), padx=5)
        label = tk.Label(num_row, text='請選擇你有幾隻寵物要餵食：')
        label.pack(side=tk.LEFT, padx=(0, 15))
        
        radio_group = Frame(num_row)
        radio_group.pack(side=tk.LEFT)
        for i in range(1, 4):
            radio = tk.Radiobutton(
                radio_group,
                text=f'{i} 隻',
                variable=self.num_pets,
                value=i,
                command=self._on_change
            )
            radio.pack(side=tk.LEFT, padx=(0, 10))

    def _on_change(self):
        """當玩家在介面上點選時，自動存檔"""
        self.pet_settings.set('Auto-feed', self.auto_feed.get())
        self.pet_settings.set('Num pets', self.num_pets.get())
        self.pet_settings.save_config()

class PetSettings(Configurable):
    # 預設設定：關閉餵食，寵物 1 隻
    DEFAULT_CONFIG = {
        'Auto-feed': False,
        'Num pets': 1
    }

    def get(self, key):
        return self.config[key]

    def set(self, key, value):
        assert key in self.config
        self.config[key] = value
