"""
[視覺辨識模組]
這個模組負責載入由 tools/rune_trainer 訓練出來的 Keras 模型，
並對遊戲畫面進行即時推論。

整合重點：
1. 保持與訓練時一致的影像預處理 (灰階 -> 二值化 -> 去噪)。
2. 使用 TensorFlow Keras 介面載入 .h5 模型。
"""

import cv2
import tensorflow as tf
import numpy as np
from src.common import utils
from skimage import morphology  # 需要安裝 scikit-image: pip install scikit-image

#########################
#       常數設定        #
#########################
# 設定模型路徑，這裡對應到 tools/rune_trainer 訓練出的模型
MODEL_PATH = 'assets/models/arrow_model.h5'

# 這是模型訓練時定義的輸入大小 (60x60)
INPUT_SHAPE = (60, 60, 1)

# 對應的類別標籤 (必須與 common.py 中的 CLASSES 一致)
CLASSES = ['down', 'left', 'right', 'up']


#########################
#       核心功能        #
#########################
def load_model():
    """
    載入 .h5 格式的 Keras 模型。
    """
    try:
        print(f"[~] 正在從 {MODEL_PATH} 載入模型...")
        model = tf.keras.models.load_model(MODEL_PATH)
        return model
    except Exception as e:
        print(f"[!] 模型載入失敗，請確認路徑或是否已訓練模型。錯誤: {e}")
        return None


def preprocess_image(image):
    """
    [影像預處理]
    這部分的邏輯必須與 tools/rune_trainer/preprocessing/preprocess.py 完全一致。
    步驟：高斯模糊 -> 轉 HSV -> 灰階化 -> 自適應二值化 -> 去噪。
    """
    # 1. 高斯模糊 (Gaussian Blur)
    img = cv2.GaussianBlur(image, (3, 3), 0)

    # 2. 顏色轉換 (Color Transform) -> HSV
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 3. 自定義灰階轉換 (根據訓練專案的參數)
    # coefficients = (h, s, v)
    coefficients = (0.0445, 0.6568, 0.2987)
    img = cv2.transform(img, np.array(coefficients).reshape((1, 3)))

    # 4. 二值化 (Binarization)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                cv2.THRESH_BINARY, 5, -1)

    # 5. 去噪 (Denoise)
    # 將圖片轉為布林值矩陣進行形態學操作
    processed = img > 0
    
    # 移除小物件 (雜訊)
    processed = morphology.remove_small_objects(processed, min_size=8, connectivity=2)
    # 移除小孔洞
    processed = morphology.remove_small_holes(processed, area_threshold=8, connectivity=2)

    # 轉回 uint8 格式 (0 或 255)
    result_img = np.zeros_like(img, dtype=np.uint8)
    result_img[processed] = 255
    
    return result_img


def run_inference(model, image):
    """
    對單張裁切好的箭頭圖片進行推論。
    """
    # 執行預處理
    processed_img = preprocess_image(image)
    
    # 調整形狀以符合模型輸入 (Batch Size, Width, Height, Channels)
    # reshape(1, 60, 60, 1)
    data = np.reshape(processed_img, (1, ) + INPUT_SHAPE)
    
    # 讓模型預測
    prediction = model.predict(data)
    
    # 取得信心度最高的類別索引
    class_index = np.argmax(prediction)
    confidence = np.max(prediction)
    
    return CLASSES[class_index], confidence


@utils.run_if_enabled
def merge_detection(model, frame):
    """
    [主偵測邏輯]
    掃描畫面，找出輪的箭頭並回傳方向列表。
    
    注意：原本的 detection.py 是用 Canny 邊緣檢測來找箭頭位置。
    如果要完全整合，我們需要先「定位」出箭頭在哪裡，然後裁切下來給模型看。
    這裡我們保留原本的定位邏輯概念，但改用模型來分類。
    """
    
    # 這裡簡化流程：假設我們已經透過某種方式(例如原本的 find_contours) 切割出了四個箭頭的圖片
    # 實務上，你需要結合 capture.py 的定位邏輯將畫面裁切成四個 60x60 的小圖
    # 下面的 code 是一個示意，實際運作需要配合你的截圖座標

      solution = []
    """
    執行兩次推論：一次是原本的直立圖片，一次是旋轉 90 度的圖片。
    只考慮垂直方向的箭頭，並將兩次推論的結果合併。
    (旋轉圖片中的垂直箭頭，其實就是原本圖片的水平箭頭)。
    這樣做通常能提高辨識準確度。
    :param model:   要使用的模型物件。
    :param image:   輸入的圖片。
    :return:        一個包含四個箭頭方向字串的清單。
    """

    label_map = {1: 'up', 2: 'down', 3: 'left', 4: 'right'}
    converter = {'up': 'right', 'down': 'left'}         # 用於轉換「旋轉後的推論結果」
    classes = []
    
    # 前處理 (Preprocessing)
    height, width, channels = image.shape
    # 裁切圖片，只保留可能出現輪的區域 (通常在螢幕中間偏上)
    cropped = image[120:height//2, width//4:3*width//4]
    filtered = filter_color(cropped)
    cannied = canny(filtered)

    # 隔離出輪的區域 (Rune Box)
    height, width, channels = cannied.shape
    boxes = get_boxes(model, cannied)
    if len(boxes) == 4:      # 只有在正確偵測到 4 個箭頭時才繼續
        y_mins = [b[0][0] for b in boxes]
        x_mins = [b[0][1] for b in boxes]
        y_maxes = [b[0][2] for b in boxes]
        x_maxes = [b[0][3] for b in boxes]
        left = int(round(min(x_mins) * width))
        right = int(round(max(x_maxes) * width))
        top = int(round(min(y_mins) * height))
        bottom = int(round(max(y_maxes) * height))
        rune_box = cannied[top:bottom, left:right]

        # 用黑色邊框填充輪的區域，這能有效消除周圍的雜訊
        height, width, channels = rune_box.shape
        pad_height, pad_width = 384, 455
        preprocessed = np.full((pad_height, pad_width, channels), (0, 0, 0), dtype=np.uint8)
        x_offset = (pad_width - width) // 2
        y_offset = (pad_height - height) // 2

        if x_offset > 0 and y_offset > 0:
            preprocessed[y_offset:y_offset+height, x_offset:x_offset+width] = rune_box

        # 對前處理後的圖片執行偵測
        lst = sort_by_confidence(model, preprocessed)
        # 依照 X 座標排序 (從左到右讀取箭頭)
        lst.sort(key=lambda x: x[1][1])
        classes = [label_map[item[2]] for item in lst]

        # 對旋轉後的圖片執行偵測
        rotated = cv2.rotate(preprocessed, cv2.ROTATE_90_COUNTERCLOCKWISE)
        lst = sort_by_confidence(model, rotated)
        # 依照 X 座標排序 (注意：這裡的座標因為旋轉過所以不同)
        lst.sort(key=lambda x: x[1][2], reverse=True)
        # 只取旋轉後辨識為 上(1) 或 下(2) 的結果，並轉換回原本的 右 或 左
        rotated_classes = [converter[label_map[item[2]]]
                           for item in lst
                           if item[2] in [1, 2]]
            
        # 合併兩次偵測的結果
        for i in range(len(classes)):
            # 如果原本辨識為 左 或 右，嘗試用旋轉後的結果替換 (因為模型對垂直箭頭辨識較準)
            if rotated_classes and classes[i] in ['left', 'right']:
                classes[i] = rotated_classes.pop(0)

    return classes
# 假設我們已經知道輪出現的大概區域 (這部分依賴原本的定位算法)
    # 這裡為了示範，我們先回傳空值，等待你將定位邏輯接上
    # 你需要將裁切下來的 'arrow_img' 傳入 run_inference
    
    # 範例邏輯 (虛擬碼):
    # arrows = locate_arrows(frame) # 這是原本專案找圓圈/輪廓的邏輯
    # for arrow_img in arrows:
    #     direction, conf = run_inference(model, arrow_img)
    #     if conf > 0.8:
    #         solution.append(direction)
            
    return solution



# 用來單獨測試偵測模組的腳本
if __name__ == '__main__':
    from src.common import config, utils
    import mss
    config.enabled = True
    monitor = {'top': 0, 'left': 0, 'width': 1366, 'height': 768}
    model = load_model()
    while True:
        with mss.mss() as sct:
            frame = np.array(sct.grab(monitor))
            cv2.imshow('frame', canny(filter_color(frame)))
            arrows = merge_detection(model, frame)
            print(arrows)
            if cv2.waitKey(1) & 0xFF == 27:     # 27 是 Esc 鍵的 ASCII 碼
                break
