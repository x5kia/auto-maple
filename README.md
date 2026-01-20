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
  <img src="https://user-images
