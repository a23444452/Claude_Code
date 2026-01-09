#!/usr/bin/env python3
"""
YOLO Training Script with MPS (Apple Silicon) Support
支援 MPS 加速的 YOLO 訓練腳本
"""

import torch
from ultralytics import YOLO
import sys
import argparse
from pathlib import Path


def check_mps_availability():
    """檢查 MPS (Metal Performance Shaders) 是否可用"""
    print("=" * 60)
    print("MPS 加速環境檢測")
    print("=" * 60)

    # PyTorch 版本
    print(f"\n[✓] PyTorch 版本: {torch.__version__}")

    # MPS 可用性檢測
    if torch.backends.mps.is_available():
        print("[✓] MPS 裝置可用！")
        device = torch.device("mps")

        # MPS 是否已建置
        if torch.backends.mps.is_built():
            print("[✓] MPS 已正確建置")
        else:
            print("[✗] MPS 未正確建置")
            return None

    else:
        print("[✗] MPS 不可用，將使用 CPU")
        device = torch.device("cpu")

    print(f"\n[✓] 選定裝置: {device}")
    return device


def test_mps_performance():
    """簡單的 MPS 性能測試"""
    print("\n" + "=" * 60)
    print("MPS 性能測試")
    print("=" * 60)

    device = check_mps_availability()
    if device is None:
        return False

    try:
        # 建立測試張量
        print("\n[測試] 建立測試張量 (1000x1000)...")
        x = torch.randn(1000, 1000, device=device)
        y = torch.randn(1000, 1000, device=device)

        # 矩陣乘法測試
        print("[測試] 執行矩陣乘法...")
        z = torch.matmul(x, y)

        print(f"[✓] 計算成功！結果形狀: {z.shape}")
        print(f"[✓] 張量裝置: {z.device}")

        return True

    except Exception as e:
        print(f"[✗] MPS 測試失敗: {e}")
        return False


def test_yolo_with_mps():
    """使用 YOLO 測試 MPS 加速"""
    print("\n" + "=" * 60)
    print("YOLO 模型 MPS 測試")
    print("=" * 60)

    try:
        # 載入預訓練模型（nano 版本，較小）
        print("\n[載入] 下載/載入 YOLO11n 模型...")
        model = YOLO('yolo11n.pt')

        # 檢測可用裝置
        device = 'mps' if torch.backends.mps.is_available() else 'cpu'
        print(f"[✓] YOLO 將使用裝置: {device}")

        # 移動模型到 MPS
        print(f"[測試] 將模型移至 {device}...")
        model.to(device)

        # 建立假影像進行推論測試
        print("[測試] 建立測試影像並執行推論...")
        import numpy as np
        dummy_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)

        # 執行推論
        results = model(dummy_image, device=device, verbose=False)

        print(f"[✓] 推論成功！")
        print(f"[✓] 結果數量: {len(results)}")

        return True

    except Exception as e:
        print(f"[✗] YOLO 測試失敗: {e}")
        return False


def train_model(
    data_yaml: str = 'config/data.yaml',
    model_size: str = 'n',
    epochs: int = 100,
    imgsz: int = 640,
    batch: int = 16,
    patience: int = 50,
    project: str = 'runs/train',
    name: str = 'exp',
    augment: bool = False
):
    """
    訓練 YOLO 模型

    Args:
        data_yaml: 資料配置檔路徑
        model_size: 模型大小 (n/s/m/l/x)
        epochs: 訓練輪數
        imgsz: 圖片大小
        batch: 批次大小
        patience: 早停耐心值
        project: 專案目錄
        name: 實驗名稱
        augment: 是否啟用強化資料增強
    """
    print("\n" + "=" * 60)
    print("開始 YOLO 模型訓練")
    print("=" * 60)

    # 檢查 MPS 可用性
    device = 'mps' if torch.backends.mps.is_available() else 'cpu'
    print(f"\n[裝置] 使用: {device}")

    # 檢查資料檔案
    data_path = Path(data_yaml)
    if not data_path.exists():
        print(f"[✗] 找不到資料配置檔: {data_yaml}")
        return False

    print(f"[✓] 資料配置檔: {data_yaml}")

    try:
        # 載入預訓練模型
        model_name = f'yolo11{model_size}.pt'
        print(f"\n[載入] 模型: {model_name}")
        model = YOLO(model_name)

        # 訓練參數
        print(f"\n[訓練參數]")
        print(f"  - Epochs: {epochs}")
        print(f"  - Image Size: {imgsz}")
        print(f"  - Batch Size: {batch}")
        print(f"  - Patience: {patience}")
        print(f"  - Device: {device}")
        print(f"  - Augmentation: {'強化' if augment else '標準'}")

        # 資料增強參數
        if augment:
            print(f"\n[資料增強參數]")
            print(f"  - HSV 色調調整: 0.02")
            print(f"  - HSV 飽和度調整: 0.7")
            print(f"  - HSV 亮度調整: 0.4")
            print(f"  - 旋轉角度: ±10°")
            print(f"  - 平移: ±0.2")
            print(f"  - 縮放: ±0.5")
            print(f"  - 上下翻轉: 50%")
            print(f"  - 左右翻轉: 50%")
            print(f"  - Mosaic 拼接: 啟用")

        print(f"\n[開始訓練] 請耐心等待...\n")

        # 基礎訓練參數
        train_args = {
            'data': data_yaml,
            'epochs': epochs,
            'imgsz': imgsz,
            'batch': batch,
            'device': device,
            'patience': patience,
            'project': project,
            'name': name,
            'verbose': True,
            'plots': True,
            'save': True,
            'save_period': 5,  # 每 5 輪儲存一次
            'val': True,  # 啟用驗證
            'cache': False,  # 資料集較小，不需快取
            'dropout': 0.1,  # 防止過擬合
        }

        # 如果啟用強化增強，添加增強參數
        if augment:
            train_args.update({
                'hsv_h': 0.02,  # 色調增強
                'hsv_s': 0.7,   # 飽和度增強
                'hsv_v': 0.4,   # 亮度增強
                'degrees': 10.0,  # 旋轉角度
                'translate': 0.2,  # 平移
                'scale': 0.5,      # 縮放
                'flipud': 0.5,     # 上下翻轉機率
                'fliplr': 0.5,     # 左右翻轉機率
                'mosaic': 1.0,     # Mosaic 增強
                'mixup': 0.1,      # Mixup 增強
            })

        # 開始訓練
        results = model.train(**train_args)

        print("\n" + "=" * 60)
        print("✅ 訓練完成！")
        print("=" * 60)

        # 顯示結果路徑
        save_dir = Path(project) / name
        print(f"\n[結果儲存於] {save_dir}")
        print(f"[最佳模型] {save_dir}/weights/best.pt")
        print(f"[最後模型] {save_dir}/weights/last.pt")

        return True

    except Exception as e:
        print(f"\n[✗] 訓練失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_model(model_path: str, data_yaml: str = 'config/data.yaml'):
    """
    驗證模型效能

    Args:
        model_path: 模型權重檔路徑
        data_yaml: 資料配置檔路徑
    """
    print("\n" + "=" * 60)
    print("模型驗證")
    print("=" * 60)

    # 檢查模型檔案
    if not Path(model_path).exists():
        print(f"[✗] 找不到模型檔: {model_path}")
        return False

    try:
        # 載入模型
        print(f"\n[載入] 模型: {model_path}")
        model = YOLO(model_path)

        # 檢測裝置
        device = 'mps' if torch.backends.mps.is_available() else 'cpu'
        print(f"[裝置] 使用: {device}")

        # 執行驗證
        print(f"\n[驗證中]...\n")
        metrics = model.val(data=data_yaml, device=device)

        print("\n" + "=" * 60)
        print("驗證結果")
        print("=" * 60)
        print(f"mAP50: {metrics.box.map50:.4f}")
        print(f"mAP50-95: {metrics.box.map:.4f}")

        return True

    except Exception as e:
        print(f"\n[✗] 驗證失敗: {e}")
        return False


def main():
    """主程式"""
    parser = argparse.ArgumentParser(description='YOLO 訓練腳本')
    parser.add_argument('--mode', type=str, default='test',
                       choices=['test', 'train', 'validate'],
                       help='執行模式: test(測試環境) / train(訓練) / validate(驗證)')
    parser.add_argument('--data', type=str, default='config/data.yaml',
                       help='資料配置檔路徑')
    parser.add_argument('--model', type=str, default='n',
                       help='模型大小: n/s/m/l/x')
    parser.add_argument('--epochs', type=int, default=100,
                       help='訓練輪數')
    parser.add_argument('--imgsz', type=int, default=640,
                       help='圖片大小')
    parser.add_argument('--batch', type=int, default=16,
                       help='批次大小')
    parser.add_argument('--augment', action='store_true',
                       help='啟用強化資料增強（適合小資料集）')
    parser.add_argument('--weights', type=str, default=None,
                       help='驗證用的模型權重檔路徑')

    args = parser.parse_args()

    if args.mode == 'test':
        # 測試模式
        print("\n🚀 開始 MPS 加速環境測試\n")

        device = check_mps_availability()
        if device is None:
            print("\n❌ MPS 環境檢測失敗")
            sys.exit(1)

        if not test_mps_performance():
            print("\n❌ MPS 性能測試失敗")
            sys.exit(1)

        if not test_yolo_with_mps():
            print("\n⚠️  YOLO 測試失敗（但 MPS 基本功能正常）")
            sys.exit(1)

        print("\n" + "=" * 60)
        print("✅ 所有測試通過！MPS 加速環境已就緒")
        print("=" * 60)
        print("\n💡 接下來可以使用以下指令開始訓練：")
        print("   python src/training/train.py --mode train")
        print("\n")

    elif args.mode == 'train':
        # 訓練模式
        success = train_model(
            data_yaml=args.data,
            model_size=args.model,
            epochs=args.epochs,
            imgsz=args.imgsz,
            batch=args.batch,
            augment=args.augment
        )
        if not success:
            sys.exit(1)

    elif args.mode == 'validate':
        # 驗證模式
        if args.weights is None:
            print("[✗] 請使用 --weights 指定模型權重檔")
            sys.exit(1)
        success = validate_model(args.weights, args.data)
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()
