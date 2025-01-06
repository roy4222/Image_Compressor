# 圖片壓縮工具 (Image Compression Tool)

一個簡單易用的圖片批量壓縮工具，具有圖形化界面，可以幫助你輕鬆壓縮大量圖片。

## 快速開始

### 方法一：直接使用（推薦）

1. 到 [Releases](https://github.com/roy4222/Image_Compressor/releases) 頁面
2. 下載最新版本的 `圖片壓縮工具.exe`
3. 雙擊執行即可使用

### 方法二：從源碼運行

如果你是開發者或想要自行編譯，可以：

1. 克隆此專案：
```bash
git clone https://github.com/roy4222/Image_Compressor.git
```

2. 安裝所需套件：
```bash
pip install -r requirements.txt
```

3. 執行程式：
```bash
python image_compressor.py
```

## 功能特點

- 批量處理圖片壓縮
- 可自定義壓縮品質（1-100）
- 支持調整最大寬度，自動等比例縮放
- 多種輸出格式支持（WebP、JPEG、PNG）
- 友善的圖形化界面
- 支持處理透明圖片
- 即時進度顯示

## 使用說明

1. 啟動程式後，你會看到一個簡潔的圖形界面
2. 選擇輸入資料夾（包含要壓縮的圖片）
3. 選擇輸出資料夾（儲存壓縮後的圖片）
4. 調整壓縮設定：
   - 壓縮品質（1-100，預設80）
   - 最大寬度（預設1920像素）
   - 輸出格式（WebP、JPEG、PNG）
5. 點擊「開始壓縮」
6. 等待處理完成

## 系統需求

### 執行檔版本
- Windows 作業系統
- 不需要安裝 Python 或其他依賴

### 源碼版本
- Python 3.6 或以上版本
- 需要的 Python 套件：
  - tkinter (GUI界面)
  - Pillow (圖片處理)
  - tqdm (進度顯示)

## 注意事項

- 建議先備份原始圖片
- 壓縮過程中請勿關閉程式
- 較大的圖片可能需要較長處理時間
- 如果使用執行檔版本，首次運行可能需要較長時間加載
