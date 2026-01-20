"""
全域變數模組：這就像是程式的「共用筆記本」，記錄了所有模組需要知道的即時資訊。
"""

# --- 基本設定 ---
RESOURCES_DIR = 'resources'  # 資源資料夾的名稱

# --- 遊戲即時狀態 ---
player_pos = (0, 0)    # 玩家目前在畫面上的座標位置
enabled = False        # 開關：True 代表程式正在幫你玩，False 代表停止
stage_fright = False   # 舞台恐懼：當地圖有其他玩家時，會開啟隨機防測模式
path = []              # 機器人計畫要走的移動路線圖

# --- 核心模組引用 (這些會由程式啟動時自動填入) ---
routine = None         # 負責處理你的動作腳本 (.csv)
layout = None          # 負責記錄地圖的地形資料
bot = None             # 負責執行邏輯的主機板
capture = None         # 負責「看」遊戲畫面的眼睛
listener = None        # 負責監聽鍵盤按鍵的耳朵
gui = None             # 你看到的藍色菇菇視窗介面
