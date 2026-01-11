#!/usr/bin/env python3
"""
Data Pipeline - 資料預處理腳本
將原始資料集隨機切分為 train/val 並轉換為 YOLO 格式
"""

import os
import shutil
import random
from pathlib import Path
from typing import Tuple, List, Dict
import argparse

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("請安裝必要套件: pip install Pillow numpy")
    exit(1)


class YOLODataPreprocessor:
    """YOLO 資料預處理器"""

    def __init__(
        self,
        source_dir: str,
        output_dir: str,
        train_ratio: float = 0.8,
        seed: int = 42
    ):
        """
        初始化預處理器

        Args:
            source_dir: 原始資料目錄
            output_dir: 輸出目錄
            train_ratio: 訓練集比例（0-1）
            seed: 隨機種子
        """
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.train_ratio = train_ratio
        self.seed = seed

        random.seed(seed)

        # 支援的圖片格式
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}

        # 統計資訊
        self.stats = {
            'total_images': 0,
            'valid_images': 0,
            'corrupted_images': 0,
            'converted_to_rgb': 0,
            'invalid_labels': 0,
            'train_count': 0,
            'val_count': 0
        }

    def check_image_integrity(self, image_path: Path) -> Tuple[bool, Image.Image]:
        """
        檢查圖片是否損毀

        Args:
            image_path: 圖片路徑

        Returns:
            (是否有效, PIL Image 物件)
        """
        try:
            img = Image.open(image_path)
            img.verify()  # 驗證圖片完整性

            # 重新開啟（verify 後需要重新載入）
            img = Image.open(image_path)
            img.load()  # 確保圖片可以載入

            return True, img

        except Exception as e:
            print(f"  [✗] 圖片損毀: {image_path.name} - {e}")
            return False, None

    def convert_to_rgb(self, img: Image.Image) -> Image.Image:
        """
        轉換非 RGB 圖片為 RGB

        Args:
            img: PIL Image 物件

        Returns:
            RGB 格式的 PIL Image
        """
        if img.mode != 'RGB':
            self.stats['converted_to_rgb'] += 1
            return img.convert('RGB')
        return img

    def validate_yolo_label(
        self,
        label_path: Path,
        image_width: int,
        image_height: int
    ) -> bool:
        """
        驗證 YOLO 格式標註

        Args:
            label_path: 標註檔路徑
            image_width: 圖片寬度
            image_height: 圖片高度

        Returns:
            標註是否有效
        """
        try:
            with open(label_path, 'r') as f:
                lines = f.readlines()

            if not lines:
                print(f"  [⚠] 標註檔為空: {label_path.name}")
                return False

            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                if len(parts) != 5:
                    print(f"  [✗] 標註格式錯誤 ({label_path.name}:{line_num}): 應為 5 個值")
                    return False

                try:
                    class_id = int(parts[0])
                    center_x = float(parts[1])
                    center_y = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])

                    # 檢查座標範圍（YOLO 格式應在 0-1 之間）
                    if not (0 <= center_x <= 1 and 0 <= center_y <= 1 and
                            0 < width <= 1 and 0 < height <= 1):
                        print(f"  [✗] 座標超出範圍 ({label_path.name}:{line_num}): "
                              f"x={center_x}, y={center_y}, w={width}, h={height}")
                        return False

                    # 檢查邊界框是否超出圖片邊界
                    x1 = center_x - width / 2
                    y1 = center_y - height / 2
                    x2 = center_x + width / 2
                    y2 = center_y + height / 2

                    if x1 < 0 or y1 < 0 or x2 > 1 or y2 > 1:
                        print(f"  [✗] 邊界框超出圖片 ({label_path.name}:{line_num})")
                        return False

                except ValueError as e:
                    print(f"  [✗] 數值轉換錯誤 ({label_path.name}:{line_num}): {e}")
                    return False

            return True

        except Exception as e:
            print(f"  [✗] 讀取標註失敗: {label_path.name} - {e}")
            return False

    def get_image_label_pairs(self) -> List[Tuple[Path, Path]]:
        """
        取得所有圖片和對應標註的配對

        Returns:
            [(image_path, label_path), ...]
        """
        pairs = []

        # 查找所有圖片
        for img_path in self.source_dir.iterdir():
            if img_path.suffix.lower() not in self.image_extensions:
                continue

            # 尋找對應的標註檔（.txt）
            label_path = img_path.with_suffix('.txt')

            if not label_path.exists():
                print(f"  [⚠] 找不到標註檔: {label_path.name}")
                continue

            pairs.append((img_path, label_path))

        return pairs

    def split_dataset(
        self,
        pairs: List[Tuple[Path, Path]]
    ) -> Tuple[List[Tuple[Path, Path]], List[Tuple[Path, Path]]]:
        """
        隨機切分資料集為 train/val

        Args:
            pairs: 圖片標註配對列表

        Returns:
            (train_pairs, val_pairs)
        """
        random.shuffle(pairs)
        split_idx = int(len(pairs) * self.train_ratio)

        train_pairs = pairs[:split_idx]
        val_pairs = pairs[split_idx:]

        return train_pairs, val_pairs

    def process_and_save(
        self,
        pairs: List[Tuple[Path, Path]],
        split: str
    ):
        """
        處理並保存圖片和標註

        Args:
            pairs: 圖片標註配對列表
            split: 'train' 或 'val'
        """
        # 建立輸出目錄
        img_dir = self.output_dir / 'images' / split
        label_dir = self.output_dir / 'labels' / split

        img_dir.mkdir(parents=True, exist_ok=True)
        label_dir.mkdir(parents=True, exist_ok=True)

        valid_count = 0

        for img_path, label_path in pairs:
            self.stats['total_images'] += 1

            # 檢查圖片完整性
            is_valid, img = self.check_image_integrity(img_path)
            if not is_valid:
                self.stats['corrupted_images'] += 1
                continue

            # 轉換為 RGB
            img = self.convert_to_rgb(img)

            # 驗證標註
            if not self.validate_yolo_label(label_path, img.width, img.height):
                self.stats['invalid_labels'] += 1
                continue

            # 保存處理後的圖片
            output_img_path = img_dir / img_path.name
            img.save(output_img_path, quality=95)

            # 複製標註檔
            output_label_path = label_dir / label_path.name
            shutil.copy2(label_path, output_label_path)

            valid_count += 1
            self.stats['valid_images'] += 1

        if split == 'train':
            self.stats['train_count'] = valid_count
        else:
            self.stats['val_count'] = valid_count

    def create_classes_file(self):
        """
        建立 classes.txt 檔案
        從來源目錄複製（如果存在），否則從標註檔自動偵測類別
        """
        source_classes = self.source_dir / 'classes.txt'
        output_classes = self.output_dir / 'classes.txt'

        if source_classes.exists():
            # 從來源複製 classes.txt
            shutil.copy2(source_classes, output_classes)
            with open(source_classes, 'r') as f:
                class_names = [line.strip() for line in f if line.strip()]
            print(f"\n[✓] 從來源複製類別檔: {output_classes}")
            print(f"    類別數量: {len(class_names)}")
            print(f"    類別名稱: {', '.join(class_names)}")
        else:
            # 從標註檔自動偵測類別 ID
            print(f"\n[⚠] 來源目錄沒有 classes.txt，嘗試自動偵測...")
            class_ids = set()

            for label_file in self.source_dir.glob('*.txt'):
                try:
                    with open(label_file, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                class_id = int(line.split()[0])
                                class_ids.add(class_id)
                except:
                    continue

            if class_ids:
                # 建立類別檔（只包含 class_id）
                with open(output_classes, 'w') as f:
                    for class_id in sorted(class_ids):
                        f.write(f"{class_id}\n")
                print(f"[✓] 自動偵測到 {len(class_ids)} 個類別: {sorted(class_ids)}")
                print(f"[✓] 建立類別檔: {output_classes}")
            else:
                print(f"[✗] 無法偵測類別，請手動建立 classes.txt")

    def run(self):
        """執行完整的預處理流程"""
        print("=" * 60)
        print("YOLO 資料預處理")
        print("=" * 60)

        # 檢查來源目錄
        if not self.source_dir.exists():
            print(f"[✗] 來源目錄不存在: {self.source_dir}")
            return False

        print(f"\n[來源] {self.source_dir}")
        print(f"[輸出] {self.output_dir}")
        print(f"[切分] Train: {self.train_ratio:.0%}, Val: {(1-self.train_ratio):.0%}")

        # 取得所有圖片標註配對
        print(f"\n[步驟 1] 掃描圖片和標註...")
        pairs = self.get_image_label_pairs()

        if not pairs:
            print("[✗] 找不到有效的圖片標註配對")
            return False

        print(f"[✓] 找到 {len(pairs)} 組圖片標註配對")

        # 切分資料集
        print(f"\n[步驟 2] 隨機切分資料集...")
        train_pairs, val_pairs = self.split_dataset(pairs)
        print(f"[✓] Train: {len(train_pairs)} 組, Val: {len(val_pairs)} 組")

        # 處理訓練集
        print(f"\n[步驟 3] 處理訓練集...")
        self.process_and_save(train_pairs, 'train')
        print(f"[✓] 訓練集處理完成: {self.stats['train_count']} 張")

        # 處理驗證集
        print(f"\n[步驟 4] 處理驗證集...")
        self.process_and_save(val_pairs, 'val')
        print(f"[✓] 驗證集處理完成: {self.stats['val_count']} 張")

        # 建立 classes.txt
        print(f"\n[步驟 5] 建立類別檔...")
        self.create_classes_file()

        # 顯示統計資訊
        self.print_statistics()

        return True

    def print_statistics(self):
        """印出統計資訊"""
        print("\n" + "=" * 60)
        print("處理統計")
        print("=" * 60)
        print(f"總圖片數:       {self.stats['total_images']}")
        print(f"有效圖片:       {self.stats['valid_images']}")
        print(f"損毀圖片:       {self.stats['corrupted_images']}")
        print(f"轉換為 RGB:     {self.stats['converted_to_rgb']}")
        print(f"無效標註:       {self.stats['invalid_labels']}")
        print(f"-" * 60)
        print(f"訓練集:         {self.stats['train_count']}")
        print(f"驗證集:         {self.stats['val_count']}")
        print("=" * 60)


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='YOLO 資料預處理 - 切分 train/val 並驗證格式'
    )
    parser.add_argument(
        '--source',
        type=str,
        required=True,
        help='原始資料目錄（包含圖片和 .txt 標註）'
    )
    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='輸出目錄'
    )
    parser.add_argument(
        '--train-ratio',
        type=float,
        default=0.8,
        help='訓練集比例（預設: 0.8）'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='隨機種子（預設: 42）'
    )

    args = parser.parse_args()

    # 驗證參數
    if not 0 < args.train_ratio < 1:
        print("[✗] train-ratio 必須在 0 到 1 之間")
        return

    # 執行預處理
    preprocessor = YOLODataPreprocessor(
        source_dir=args.source,
        output_dir=args.output,
        train_ratio=args.train_ratio,
        seed=args.seed
    )

    success = preprocessor.run()

    if success:
        print("\n✅ 資料預處理完成！")
        print(f"\n💡 接下來請更新 config/data.yaml 指向新的資料集：")
        print(f"   train: {Path(args.output).absolute()}/images/train")
        print(f"   val: {Path(args.output).absolute()}/images/val")
    else:
        print("\n❌ 資料預處理失敗")
        exit(1)


if __name__ == "__main__":
    main()
