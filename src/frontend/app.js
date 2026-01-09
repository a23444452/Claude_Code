// YOLO Detection Frontend Application
// API 端點配置
const API_BASE_URL = 'http://localhost:8000';

// 全域變數
let selectedFile = null;
let currentImage = null;

// DOM 元素
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const detectBtn = document.getElementById('detectBtn');
const clearBtn = document.getElementById('clearBtn');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const errorMsg = document.getElementById('errorMsg');
const resultCanvas = document.getElementById('resultCanvas');
const detectionsList = document.getElementById('detectionsList');
const resultCount = document.getElementById('resultCount');
const confThreshold = document.getElementById('confThreshold');
const iouThreshold = document.getElementById('iouThreshold');

// 統計元素
const statTotal = document.getElementById('statTotal');
const statAvgConf = document.getElementById('statAvgConf');
const statClasses = document.getElementById('statClasses');

// 類別顏色映射
const classColors = {
    0: '#FF6B6B', 1: '#4ECDC4', 2: '#45B7D1', 3: '#FFA07A',
    4: '#98D8C8', 5: '#F7DC6F', 6: '#BB8FCE', 7: '#85C1E2',
    8: '#F8B739', 9: '#52B788'
};

// 初始化
function init() {
    // 上傳區域點擊事件
    uploadArea.addEventListener('click', () => fileInput.click());

    // 檔案選擇事件
    fileInput.addEventListener('change', handleFileSelect);

    // 拖曳事件
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // 按鈕事件
    detectBtn.addEventListener('click', detectObjects);
    clearBtn.addEventListener('click', clearResults);

    // 檢查 API 連線
    checkAPIHealth();
}

// 檢查 API 健康狀態
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        if (data.status === 'healthy' && data.model_loaded) {
            console.log('✓ API 連線正常，模型已載入');
        } else {
            showError('API 服務異常，請檢查後端服務');
        }
    } catch (error) {
        showError('無法連接到 API 服務，請確認後端已啟動');
        console.error('API 連線錯誤:', error);
    }
}

// 處理檔案選擇
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

// 處理拖曳
function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');

    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        processFile(file);
    } else {
        showError('請上傳圖片檔案');
    }
}

// 處理檔案
function processFile(file) {
    selectedFile = file;

    // 顯示預覽
    const reader = new FileReader();
    reader.onload = (e) => {
        currentImage = new Image();
        currentImage.onload = () => {
            // 更新上傳區域顯示
            uploadArea.innerHTML = `
                <div class="upload-icon">✅</div>
                <div class="upload-text">${file.name}</div>
                <div class="upload-hint">點擊可更換圖片</div>
            `;

            // 啟用偵測按鈕
            detectBtn.disabled = false;

            // 清除之前的錯誤
            hideError();
        };
        currentImage.src = e.target.result;
    };
    reader.readAsDataURL(file);
}

// 偵測物件
async function detectObjects() {
    if (!selectedFile) {
        showError('請先選擇圖片');
        return;
    }

    // 顯示載入狀態
    loading.classList.add('active');
    results.classList.remove('active');
    detectBtn.disabled = true;
    hideError();

    try {
        // 準備表單資料
        const formData = new FormData();
        formData.append('file', selectedFile);

        // API 請求
        const response = await fetch(
            `${API_BASE_URL}/predict?conf_threshold=${confThreshold.value}&iou_threshold=${iouThreshold.value}`,
            {
                method: 'POST',
                body: formData
            }
        );

        if (!response.ok) {
            throw new Error(`API 錯誤: ${response.status}`);
        }

        const data = await response.json();

        // 顯示結果
        displayResults(data);

    } catch (error) {
        showError(`偵測失敗: ${error.message}`);
        console.error('偵測錯誤:', error);
    } finally {
        loading.classList.remove('active');
        detectBtn.disabled = false;
    }
}

// 顯示結果
function displayResults(data) {
    // 更新計數
    resultCount.textContent = `${data.detection_count} 個物件`;

    // 繪製圖片和偵測框
    drawDetections(data);

    // 顯示偵測列表
    displayDetectionsList(data.detections);

    // 更新統計
    updateStats(data);

    // 顯示結果區域
    results.classList.add('active');
}

// 繪製偵測結果
function drawDetections(data) {
    const canvas = resultCanvas;
    const ctx = canvas.getContext('2d');

    // 設定 canvas 尺寸
    canvas.width = currentImage.width;
    canvas.height = currentImage.height;

    // 繪製圖片
    ctx.drawImage(currentImage, 0, 0);

    // 繪製每個偵測框
    data.detections.forEach((detection, index) => {
        const bbox = detection.bbox;
        const color = classColors[detection.class_id] || '#FF0000';

        // 繪製邊界框
        ctx.strokeStyle = color;
        ctx.lineWidth = 3;
        ctx.strokeRect(bbox.x1, bbox.y1, bbox.x2 - bbox.x1, bbox.y2 - bbox.y1);

        // 繪製標籤背景
        const label = `${detection.class_name} ${(detection.confidence * 100).toFixed(1)}%`;
        ctx.font = 'bold 16px Arial';
        const textWidth = ctx.measureText(label).width;

        ctx.fillStyle = color;
        ctx.fillRect(bbox.x1, bbox.y1 - 25, textWidth + 10, 25);

        // 繪製標籤文字
        ctx.fillStyle = 'white';
        ctx.fillText(label, bbox.x1 + 5, bbox.y1 - 7);
    });
}

// 顯示偵測列表
function displayDetectionsList(detections) {
    detectionsList.innerHTML = '';

    if (detections.length === 0) {
        detectionsList.innerHTML = '<p style="text-align: center; color: #999;">未偵測到任何物件</p>';
        return;
    }

    // 按信心度排序
    const sortedDetections = [...detections].sort((a, b) => b.confidence - a.confidence);

    sortedDetections.forEach((detection, index) => {
        const item = document.createElement('div');
        item.className = 'detection-item';
        item.style.borderLeftColor = classColors[detection.class_id] || '#667eea';

        item.innerHTML = `
            <div class="detection-header">
                <div class="detection-class">類別 ${detection.class_name}</div>
                <div class="detection-confidence">${(detection.confidence * 100).toFixed(2)}%</div>
            </div>
            <div class="detection-bbox">
                位置: (${detection.bbox.x1.toFixed(0)}, ${detection.bbox.y1.toFixed(0)})
                → (${detection.bbox.x2.toFixed(0)}, ${detection.bbox.y2.toFixed(0)})
                <br>
                尺寸: ${detection.bbox.width.toFixed(0)} × ${detection.bbox.height.toFixed(0)} px
            </div>
        `;

        detectionsList.appendChild(item);
    });
}

// 更新統計
function updateStats(data) {
    // 總偵測數
    statTotal.textContent = data.detection_count;

    // 平均信心度
    if (data.detection_count > 0) {
        const avgConf = data.detections.reduce((sum, d) => sum + d.confidence, 0) / data.detection_count;
        statAvgConf.textContent = `${(avgConf * 100).toFixed(1)}%`;
    } else {
        statAvgConf.textContent = '0%';
    }

    // 類別數
    const uniqueClasses = new Set(data.detections.map(d => d.class_id));
    statClasses.textContent = uniqueClasses.size;
}

// 清除結果
function clearResults() {
    selectedFile = null;
    currentImage = null;

    // 重置上傳區域
    uploadArea.innerHTML = `
        <div class="upload-icon">📤</div>
        <div class="upload-text">點擊或拖曳圖片到此處</div>
        <div class="upload-hint">支援 JPG、PNG 格式</div>
    `;

    // 重置輸入
    fileInput.value = '';

    // 隱藏結果
    results.classList.remove('active');

    // 停用按鈕
    detectBtn.disabled = true;

    // 清除錯誤
    hideError();
}

// 顯示錯誤
function showError(message) {
    errorMsg.textContent = message;
    errorMsg.classList.add('active');
}

// 隱藏錯誤
function hideError() {
    errorMsg.classList.remove('active');
}

// 頁面載入完成後初始化
document.addEventListener('DOMContentLoaded', init);
