<h1 align="center">
  Auto Maple (自動楓之谷)
</h1>

Auto Maple 是一款智慧型 Python AI，專門為 2D 橫向捲軸 MMORPG《楓之谷》（MapleStory）設計。它結合了模擬按鍵輸入、TensorFlow 機器學習、OpenCV 範本匹配以及多項電腦視覺技術。

由社群建立的資源，例如各職業的 **指令書 (Command Books)** 以及各張地圖的 **腳本 (Routines)**，可以在 **[資源儲存庫](https://github.com/tanjeffreyz/auto-maple-resources)** 中找到。

<br>

<h2 align="center">
  小地圖 (Minimap)
</h2>

<table align="center" border="0">
  <tr>
    <td>
Auto Maple 使用 <b>OpenCV 範本匹配</b> 技術來確定小地圖的邊界以及其中的各種元素，從而精準追蹤玩家在遊戲中的位置。如果將 <code>record_layout</code> (紀錄地形) 設定為 <code>True</code>，Auto Maple 會將玩家之前的座標記錄在一個基於 <b>四元樹 (Quadtree)</b> 的地形物件中，並定期儲存至「layouts」目錄。每當載入新腳本時，對應的地形檔案（若存在）也會被自動載入。該地形物件使用 <b>A* 搜尋演算法</b> 來計算玩家到目標位置的最短路徑，這能顯著提高執行腳本的速度與準確性。
    </td>
    <td align="center" width="400px">
      <img align="center" src="https://user-images.githubusercontent.com/69165598/123177212-b16f0700-d439-11eb-8a21-8b414273f1e1.gif"/>
    </td>
  </tr>
</table>

<br>

<h2 align="center">
  技能指令書 (Command Books)
</h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/69165598/123372905-502e5d00-d539-11eb-81c2-46b8bbf929cc.gif" width="100%"/>
  <br>
  <sub>
    上圖展示了 Auto Maple 穩定地執行一套高難度的技能組合。
  </sub>
</p>
  
<table align="center" border="0">
  <tr>
    <td width="100%">
本程式採用模組化設計，只要提供「指令書」，Auto Maple 就能操作遊戲中的任何角色。指令書是一個 Python 檔案，包含多個類別（代表不同的遊戲技能），定義了應按下的按鍵及時機。指令書一旦匯入，其內容會自動編譯成字典，供程式解讀腳本中的命令。指令可以直接存取 Auto Maple 的全域變數，從而根據玩家位置與遊戲狀態改變行為。
    </td>
  </tr>
</table>
  
<br>

<h2 align="center">
  動作腳本 (Routines)
</h2>

<table align="center" border="0">
  <tr>
    <td width="350px">
      <p align="center">
        <img src="https://user-images.githubusercontent.com/69165598/150469699-d8a94ab4-7d70-49c3-8736-a9018996f39a.png"/>
        <br>
        <sub>
          點擊 <a href="https://github.com/tanjeffreyz02/auto-maple/blob/f13d87c98e9344e0a4fa5c6f85ffb7e66860afc0/routines/dcup2.csv">這裡</a> 查看完整腳本範例。
        </sub>
      </p>
    </td>
    <td>
腳本是一個由使用者建立的 CSV 檔案，用來告訴 Auto Maple 在每個地點應如何移動及使用哪些指令。內建的編譯器會解析 CSV 並將其轉換為 <code>Component</code> 物件清單以供執行。若某行包含無效參數，程式會印出錯誤訊息並忽略該行。
<br><br>
以下是常用的腳本組件摘要：
<ul>
  <li>
    <b><code>Point (座標點)</code></b>：儲存其下方的指令，並在角色進入 <code>move_tolerance</code> (移動誤差範圍) 時執行。可選參數包括：
    <ul>
      <li>
        <code>adjust</code>：在執行指令前，精細調整位置至 <code>adjust_tolerance</code> 範圍內。
      </li>
      <li>
        <code>frequency</code>：設定執行頻率。若設為 N，則每隔 N 次循環執行一次。
      </li>
      <li>
        <code>skip</code>：設定是否跳過第一次循環。
      </li>
    </ul>
  </li>
  <li>
    <b><code>Label (標籤)</code></b>：作為參考點，用於組織腳本區塊或建立迴圈。
  </li>
  <li>
    <b><code>Jump (跳轉)</code></b>：從腳本中任何位置跳轉到指定的標籤。
  </li>
  <li>
    <b><code>Setting (設定)</code></b>：動態更新特定設定值。可放置於腳本任何位置以改變行為。
  </li>
</ul>
    </td>
  </tr>
</table>

<br>

<h2 align="center">
  自動解輪 (Runes)
</h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/69165598/123479558-f61fad00-d5b5-11eb-914c-8f002a96dd62.gif" width="100%"/>
</p>

<table align="center" border="0">
  <tr>
    <td width="100%">
Auto Maple 能夠自動破解遊戲中的「輪」箭頭謎題。它首先使用 OpenCV 的顏色過濾與 <b>Canny 邊緣檢測</b> 演算法來分離箭頭並減少背景雜訊。接著，使用預先訓練好的 <b>TensorFlow</b> 模型對影像進行多次推論，直到辨識結果達成一致為止。這使得程式在各種複雜且混亂的遊戲環境中都能極其準確地解開輪謎題。
    </td>
  </tr>
</table>

<br>

<h2 align="center">
  影片示範
</h2>

<p align="center">
  <a href="https://youtu.be/iNj1CWW2--8?si=MA4n6EAHokI9FX8B"><b>點擊下方觀看完整示範影片</b></a>
</p>

<p align="center">
  <a href="https://youtu.be/iNj1CWW2--8?si=MA4n6EAHokI9FX8B">
    <img src="https://user-images.githubusercontent.com/69165598/123308656-c5b61100-d4d8-11eb-99ac-c465665474b5.gif" width="600px"/>
  </a>
</p>

<br>

<h2 align="center">
  環境架設 (新手教學)
</h2>

<ol>
  <li>
    下載並安裝 <a href="https://www.python.org/downloads/">Python 3</a>。
  </li>
  <li>
    下載並安裝最新版本的 <a href="https://developer.nvidia.com/cuda-downloads">CUDA Toolkit</a>。
  </li>
  <li>
    下載並安裝 <a href="https://git-scm.com/download/win">Git</a>。
  </li>
  <li>
    下載並解壓縮最新版本的 <a href="https://github.com/tanjeffreyz02/auto-maple/releases">Auto Maple 釋出檔</a>。
  </li>
  <li>
    下載 <a href="https://drive.google.com/drive/folders/1SPdTNF4KZczoWyWTgfyTBRvLvy7WSGpu?usp=sharing">TensorFlow 模型</a> 並將其解壓後的「models」資料夾放進 Auto Maple 的「assets」目錄中。
  </li>
  <li>
    在 Auto Maple 主目錄下打開命令提示字元並執行：
    <pre><code>python -m pip install -r requirements.txt</code></pre>
  </li>
  <li>
    最後，執行以下指令建立桌面快捷方式：
    <pre><code>python setup.py</code></pre>
    該快捷方式使用絕對路徑，因此您可以將其移動到任何地方。若您搬移了程式主目錄，則需重新執行 <code>setup.py</code>。
  </li>
</ol>
