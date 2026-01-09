#!/usr/bin/env python3
"""
API 測試腳本
用於測試 FastAPI endpoint
"""

import requests
from pathlib import Path
import json


def test_health():
    """測試健康檢查"""
    print("=" * 60)
    print("測試健康檢查 (/health)")
    print("=" * 60)

    response = requests.get("http://localhost:8000/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def test_model_info():
    """測試模型資訊"""
    print("=" * 60)
    print("測試模型資訊 (/model/info)")
    print("=" * 60)

    response = requests.get("http://localhost:8000/model/info")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def test_predict(image_path: str):
    """測試物件偵測"""
    print("=" * 60)
    print(f"測試物件偵測 (/predict)")
    print("=" * 60)

    img_path = Path(image_path)

    if not img_path.exists():
        print(f"[✗] 找不到圖片: {image_path}")
        return

    print(f"[上傳] {img_path.name}")

    with open(img_path, 'rb') as f:
        files = {'file': (img_path.name, f, 'image/jpeg')}
        response = requests.post(
            "http://localhost:8000/predict",
            files=files,
            params={'conf_threshold': 0.25}
        )

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\n[結果]")
        print(f"檔案名稱: {result['filename']}")
        print(f"圖片尺寸: {result['image_size']['width']} x {result['image_size']['height']}")
        print(f"偵測數量: {result['detection_count']}")

        if result['detections']:
            print(f"\n[偵測物件]")
            for i, det in enumerate(result['detections'], 1):
                print(f"{i}. {det['class_name']} - "
                      f"信心度: {det['confidence']:.2%} - "
                      f"位置: ({det['bbox']['x1']:.0f}, {det['bbox']['y1']:.0f}) "
                      f"到 ({det['bbox']['x2']:.0f}, {det['bbox']['y2']:.0f})")
        else:
            print("\n[無偵測結果]")
    else:
        print(f"Error: {response.text}")

    print()


def main():
    """主程式"""
    print("\n🚀 開始測試 YOLO Detection API\n")

    try:
        # 測試健康檢查
        test_health()

        # 測試模型資訊
        test_model_info()

        # 測試物件偵測（使用訓練集的一張圖片）
        test_image = "dataset/MBB_Dataset/images/train"
        test_images = list(Path(test_image).glob("*.jpg"))

        if test_images:
            test_predict(str(test_images[0]))
        else:
            print("[⚠] 找不到測試圖片")

        print("=" * 60)
        print("✅ API 測試完成")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n[✗] 無法連接到 API 伺服器")
        print("請確認伺服器已啟動: uvicorn src.api.main:app --reload")
    except Exception as e:
        print(f"\n[✗] 測試失敗: {e}")


if __name__ == "__main__":
    main()
