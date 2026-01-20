"""
全域變數模組：儲存多個模組之間共享的變數。
"""

# --- 常數設定 ---
RESOURCES_DIR = 'resources'  # 資源資料夾路徑

# --- 即時狀態變數 ---
player_pos = (0, 0)    # 玩家目前在小地圖上的座標 (x, y)
enabled = False        # 腳本開關狀態：True 代表正在運行，False 代表停止
stage_fright = False   # 「舞台恐懼」狀態：當地圖有其他玩家時，會切換到隨機防測模式
path = []              # 機器人目前計畫行走的移動路徑點清單

# --- 核心物件引用 (由各模組初始化) ---
routine = None         # 目前載入的「腳本」物件
layout = None          # 目前地圖的「地形佈局」資料
bot = None             # 機器人執行邏輯核心
capture = None         # 畫面擷取與影像處理核心
listener = None        # 鍵盤監聽器（處理快捷鍵）
gui = None             # 圖形化介面物件
