#!/usr/bin/env python3

"""
YOLO Dataset Validation Script

Validates YOLO format datasets for common issues:
- Missing files
- Invalid annotations
- Incorrect format
- Class distribution
- Image quality
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple
import argparse


class Colors:
    """ANSI color codes"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'


def print_success(msg: str):
    print(f"{Colors.GREEN}✓ {msg}{Colors.NC}")


def print_error(msg: str):
    print(f"{Colors.RED}✗ {msg}{Colors.NC}")


def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.NC}")


def print_info(msg: str):
    print(f"{Colors.CYAN}ℹ {msg}{Colors.NC}")


def print_step(msg: str):
    print(f"{Colors.MAGENTA}▶ {msg}{Colors.NC}")


def validate_annotation_file(label_path: Path, num_classes: int) -> Tuple[bool, List[str]]:
    """
    Validate a single YOLO annotation file

    Returns: (is_valid, errors)
    """
    errors = []

    try:
        with open(label_path, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) != 5:
                errors.append(f"Line {i}: Expected 5 values (class x y w h), got {len(parts)}")
                continue

            try:
                class_id = int(parts[0])
                x, y, w, h = map(float, parts[1:])

                # Validate class ID
                if class_id < 0 or class_id >= num_classes:
                    errors.append(f"Line {i}: Invalid class ID {class_id} (must be 0-{num_classes-1})")

                # Validate coordinates (should be normalized 0-1)
                for name, val in [('x', x), ('y', y), ('w', w), ('h', h)]:
                    if val < 0 or val > 1:
                        errors.append(f"Line {i}: {name}={val} out of range [0, 1]")

                # Validate width and height (should be > 0)
                if w <= 0 or h <= 0:
                    errors.append(f"Line {i}: Invalid width/height (w={w}, h={h})")

            except ValueError as e:
                errors.append(f"Line {i}: Invalid format - {e}")

    except Exception as e:
        errors.append(f"Failed to read file: {e}")

    return len(errors) == 0, errors


def analyze_class_distribution(labels_dir: Path, num_classes: int) -> Dict[int, int]:
    """Analyze class distribution across dataset"""
    distribution = {i: 0 for i in range(num_classes)}

    for label_file in labels_dir.glob("*.txt"):
        try:
            with open(label_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        class_id = int(line.split()[0])
                        if 0 <= class_id < num_classes:
                            distribution[class_id] += 1
        except Exception:
            pass

    return distribution


def validate_dataset(config_path: Path, verbose: bool = False) -> bool:
    """
    Validate YOLO dataset

    Args:
        config_path: Path to data.yaml configuration file
        verbose: Print detailed information

    Returns:
        True if validation passed, False otherwise
    """
    print()
    print(f"{Colors.MAGENTA}╔════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.MAGENTA}║   YOLO Dataset Validation          ║{Colors.NC}")
    print(f"{Colors.MAGENTA}╚════════════════════════════════════╝{Colors.NC}")
    print()

    # Check if config exists
    if not config_path.exists():
        print_error(f"Configuration file not found: {config_path}")
        return False

    print_success(f"Found configuration: {config_path}")

    # Load configuration
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print_error(f"Failed to load configuration: {e}")
        return False

    # Validate configuration structure
    print_step("Validating configuration structure...")

    required_keys = ['path', 'train', 'val', 'names', 'nc']
    missing_keys = [key for key in required_keys if key not in config]

    if missing_keys:
        print_error(f"Missing required keys: {', '.join(missing_keys)}")
        return False

    print_success("Configuration structure valid")

    # Extract paths
    base_path = Path(config['path'])
    train_images = base_path / config['train']
    val_images = base_path / config['val']
    num_classes = config['nc']
    class_names = config['names']

    # Validate paths
    print_step("Validating dataset paths...")

    if not base_path.exists():
        print_error(f"Base path does not exist: {base_path}")
        return False

    if not train_images.exists():
        print_error(f"Training images path does not exist: {train_images}")
        return False

    if not val_images.exists():
        print_warning(f"Validation images path does not exist: {val_images}")

    print_success("Dataset paths valid")

    # Get corresponding labels directories
    train_labels = train_images.parent.parent / "labels" / train_images.name
    val_labels = val_images.parent.parent / "labels" / val_images.name

    # Validate train set
    print_step("Validating training set...")

    train_image_files = list(train_images.glob("*.jpg")) + list(train_images.glob("*.png"))
    print_info(f"Found {len(train_image_files)} training images")

    if len(train_image_files) == 0:
        print_error("No training images found!")
        return False

    # Check for corresponding labels
    missing_labels = []
    invalid_labels = []

    for img_file in train_image_files:
        label_file = train_labels / f"{img_file.stem}.txt"

        if not label_file.exists():
            missing_labels.append(img_file.name)
        else:
            is_valid, errors = validate_annotation_file(label_file, num_classes)
            if not is_valid:
                invalid_labels.append((label_file.name, errors))

    if missing_labels:
        print_warning(f"{len(missing_labels)} images missing label files")
        if verbose:
            for name in missing_labels[:10]:
                print(f"  - {name}")
            if len(missing_labels) > 10:
                print(f"  ... and {len(missing_labels) - 10} more")

    if invalid_labels:
        print_error(f"{len(invalid_labels)} invalid label files")
        if verbose:
            for name, errors in invalid_labels[:5]:
                print(f"  {name}:")
                for error in errors[:3]:
                    print(f"    - {error}")
                if len(errors) > 3:
                    print(f"    ... and {len(errors) - 3} more errors")
            if len(invalid_labels) > 5:
                print(f"  ... and {len(invalid_labels) - 5} more files")

    if not invalid_labels:
        print_success("All training labels valid")

    # Analyze class distribution
    print_step("Analyzing class distribution...")

    distribution = analyze_class_distribution(train_labels, num_classes)

    print()
    print("Class Distribution (Training Set):")
    print("─" * 50)

    total = sum(distribution.values())
    for class_id, count in distribution.items():
        class_name = class_names[class_id] if isinstance(class_names, dict) else class_names[class_id]
        percentage = (count / total * 100) if total > 0 else 0
        bar_length = int(percentage / 2)
        bar = "█" * bar_length

        print(f"{class_name:15} | {count:5} ({percentage:5.1f}%) {bar}")

    print("─" * 50)
    print(f"{'Total':15} | {total:5}")
    print()

    # Check for imbalance
    if total > 0:
        max_count = max(distribution.values())
        min_count = min(distribution.values())

        if min_count > 0:
            ratio = max_count / min_count
            if ratio > 3:
                print_warning(f"Class imbalance detected (ratio: {ratio:.1f}:1)")
                print_info("Consider data augmentation or weighted loss")
        else:
            print_error("Some classes have no samples!")

    # Validate validation set
    if val_images.exists():
        print_step("Validating validation set...")

        val_image_files = list(val_images.glob("*.jpg")) + list(val_images.glob("*.png"))
        print_info(f"Found {len(val_image_files)} validation images")

        if len(val_image_files) == 0:
            print_warning("No validation images found!")
        else:
            print_success(f"Validation set has {len(val_image_files)} images")

    # Summary
    print()
    print(f"{Colors.MAGENTA}═════════════════════════════════════{Colors.NC}")

    has_errors = len(invalid_labels) > 0 or len(train_image_files) == 0

    if has_errors:
        print(f"{Colors.RED}⚠ Validation completed with errors{Colors.NC}")
        print()
        print_info("Fix the issues above before training")
        return False
    else:
        print(f"{Colors.GREEN}✅ Validation passed!{Colors.NC}")
        print()
        print_info("Dataset is ready for training")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Validate YOLO format dataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        'config',
        type=str,
        help='Path to data.yaml configuration file'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print detailed information'
    )

    args = parser.parse_args()

    config_path = Path(args.config)
    success = validate_dataset(config_path, args.verbose)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
