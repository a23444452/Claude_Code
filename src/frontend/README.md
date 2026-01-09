# YOLO 物件偵測前端

現代化的物件偵測 Web 介面，使用 Vanilla JavaScript 與 Canvas API。

## 功能特色

✨ **主要功能**
- 📤 拖曳上傳圖片
- 🎯 即時物件偵測
- 🎨 視覺化偵測結果（邊界框 + 標籤）
- 📊 詳細的偵測統計
- ⚙️ 可調整信心度和 IOU 閾值
- 📱 響應式設計（支援手機、平板）

✨ **技術特色**
- 純 JavaScript（無框架依賴）
- Canvas 繪圖 API
- Fetch API 與後端通訊
- 現代化 CSS（Grid + Flexbox）
- 拖曳上傳支援

## 啟動服務

### 方法 1: 使用啟動腳本
```bash
cd /Users/vincewang/YOLO_Project/src/frontend
./start_frontend.sh
```

### 方法 2: 手動啟動
```bash
cd /Users/vincewang/YOLO_Project/src/frontend
python3 -m http.server 3000
```

啟動後訪問: **http://localhost:3000**

## 使用說明

### 1. 上傳圖片
- **方法一**: 點擊上傳區域選擇圖片
- **方法二**: 拖曳圖片到上傳區域

### 2. 調整參數（選用）
- **信心度閾值 (Confidence)**: 0-1，預設 0.25
  - 越高越嚴格，只顯示高信心度的偵測
- **IOU 閾值**: 0-1，預設 0.45
  - 用於非極大值抑制（NMS），去除重複框

### 3. 開始偵測
- 點擊「開始偵測」按鈕
- 等待處理（通常 1-3 秒）

### 4. 查看結果
- **左側**: 標註後的圖片（含偵測框和標籤）
- **右側**: 偵測物件清單（按信心度排序）
- **底部**: 統計資訊（總數、平均信心度、類別數）

## 前端架構

### 檔案結構
```
src/frontend/
├── index.html          # 主頁面
├── app.js             # 核心邏輯
├── start_frontend.sh  # 啟動腳本
└── README.md          # 說明文件
```

### 核心函數

#### API 通訊
```javascript
// 檢查 API 健康狀態
checkAPIHealth()

// 執行物件偵測
detectObjects()
```

#### 圖片處理
```javascript
// 處理檔案上傳
processFile(file)

// 繪製偵測結果
drawDetections(data)
```

#### 結果顯示
```javascript
// 顯示偵測結果
displayResults(data)

// 顯示偵測列表
displayDetectionsList(detections)

// 更新統計資訊
updateStats(data)
```

## API 整合範例

### 基本請求
```javascript
const formData = new FormData();
formData.append('file', selectedFile);

const response = await fetch(
    `http://localhost:8000/predict?conf_threshold=0.25`,
    {
        method: 'POST',
        body: formData
    }
);

const data = await response.json();
```

### 回應格式
```javascript
{
    "success": true,
    "filename": "test.jpg",
    "image_size": {
        "width": 1280,
        "height": 720
    },
    "detections": [
        {
            "class_id": 0,
            "class_name": "0",
            "confidence": 0.8523,
            "bbox": {
                "x1": 100.5,
                "y1": 200.3,
                "x2": 150.8,
                "y2": 250.1,
                "center_x": 125.65,
                "center_y": 225.2,
                "width": 50.3,
                "height": 49.8
            }
        }
    ],
    "detection_count": 1
}
```

## Canvas 繪圖技巧

### 繪製邊界框
```javascript
// 設定顏色和線寬
ctx.strokeStyle = '#FF6B6B';
ctx.lineWidth = 3;

// 繪製矩形
ctx.strokeRect(x1, y1, width, height);
```

### 繪製標籤
```javascript
// 背景
ctx.fillStyle = '#FF6B6B';
ctx.fillRect(x, y, width, height);

// 文字
ctx.fillStyle = 'white';
ctx.font = 'bold 16px Arial';
ctx.fillText(label, x + 5, y + 18);
```

## 自訂樣式

### 修改類別顏色
在 `app.js` 中修改 `classColors` 物件：
```javascript
const classColors = {
    0: '#FF6B6B',  // 紅色
    1: '#4ECDC4',  // 青色
    2: '#45B7D1',  // 藍色
    // ...
};
```

### 修改主題色
在 `index.html` 的 `<style>` 中修改：
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 瀏覽器相容性

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

需要支援的功能：
- Fetch API
- Canvas API
- FormData
- Drag & Drop API
- CSS Grid & Flexbox

## 效能優化

### 圖片壓縮
```javascript
// 在上傳前壓縮大圖片
if (file.size > 5 * 1024 * 1024) { // 5MB
    // 使用 Canvas 壓縮
    compressImage(file);
}
```

### 快取結果
```javascript
// 儲存最近的偵測結果
const cache = new Map();
cache.set(fileHash, result);
```

## 疑難排解

### 問題 1: 無法連接 API
**錯誤**: "無法連接到 API 服務"
**解決**: 確認後端服務已啟動
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 問題 2: CORS 錯誤
**錯誤**: "CORS policy blocked"
**解決**: 確認後端 CORS 設定正確（已在 main.py 中設定）

### 問題 3: 圖片顯示異常
**錯誤**: 圖片無法顯示或變形
**解決**: 檢查 Canvas 尺寸設定
```javascript
canvas.width = image.width;
canvas.height = image.height;
```

## 進階功能

### 批次偵測
修改 `app.js` 支援多檔案上傳：
```javascript
// 使用 /predict/batch endpoint
const formData = new FormData();
files.forEach(file => {
    formData.append('files', file);
});
```

### 即時攝影機偵測
整合 WebRTC：
```javascript
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        // 定期擷取畫面並偵測
    });
```

### 匯出結果
```javascript
// 下載標註後的圖片
const link = document.createElement('a');
link.download = 'detected.jpg';
link.href = canvas.toDataURL();
link.click();
```

## 部署

### Nginx 配置
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/frontend;
        index index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

### Docker
```dockerfile
FROM nginx:alpine
COPY index.html app.js /usr/share/nginx/html/
EXPOSE 80
```

## 開發計畫

- [ ] 支援批次上傳
- [ ] 即時攝影機偵測
- [ ] 偵測結果匯出（JSON/CSV）
- [ ] 歷史記錄儲存
- [ ] 深色模式
- [ ] 多語言支援
