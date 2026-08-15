#!/usr/bin/env python3
"""
Future Mall - Image Product Classifier

An image classifier that sorts product photos into three distinct categories:
    Electronics, Groceries, Clothing.

The classifier is trained on labeled sample photos (image color features),
then can classify a photo or sort an entire folder of photos into the
three bins. Pure Python (PIL + numpy) - no external ML framework needed.

Usage:
    python image_classifier.py --classify photo.png
    python image_classifier.py --sort ./photos
    python image_classifier.py --train ./images --info
    python image_classifier.py --demo
"""

import os
import sys
import shutil
import argparse

from PIL import Image
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from constants import print_header, print_section

CATEGORIES = ["Electronics", "Groceries", "Clothing"]
IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")


class ImageClassifier:
    """Train a nearest-centroid classifier over HSV color histograms."""

    def __init__(self):
        self.centroids: dict = {c: None for c in CATEGORIES}
        self._feature_size = None

    # ------------------------------------------------------------------
    # Feature extraction
    # ------------------------------------------------------------------

    @staticmethod
    def _normalized_hist(array, bins, lo, hi):
        hist, _ = np.histogram(array, bins=bins, range=(lo, hi))
        norm = hist.astype(np.float64)
        total = norm.sum()
        return norm / total if total else norm

    def extract_features(self, image_path: str) -> np.ndarray:
        """Return a fixed-size HSV feature vector for an image."""
        with Image.open(image_path).convert("RGB") as im:
            im.thumbnail((96, 96))  # small but representative
            arr = np.asarray(im, dtype=np.float64) / 255.0
        hsv = np.asarray(Image.fromarray(((arr * 255).astype(np.uint8))).convert("HSV"),
                         dtype=np.float64)
        hue, sat, val = hsv[..., 0], hsv[..., 1] / 255.0, hsv[..., 2] / 255.0
        feats = [
            self._normalized_hist(hue, 24, 0, 255),
            float(np.mean(sat)),
            float(np.mean(val)),
        ]
        flat = np.concatenate([f if isinstance(f, np.ndarray) else np.array([f])
                               for f in feats])
        self._feature_size = flat.shape[0]
        return flat

    def _features_batch(self, files):
        feats, labels = [], []
        for img_path, label in files:
            feats.append(self.extract_features(img_path))
            labels.append(label)
        return np.vstack(feats), labels

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------

    def train(self, categories_dir: str) -> dict:
        """Learn the mean feature vector per category from labeled folders.

        categories_dir must contain one sub-folder per category name.
        """
        files = []
        for cat in CATEGORIES:
            folder = os.path.join(categories_dir, cat)
            if not os.path.isdir(folder):
                print(f"!! Missing training folder: {folder}")
                continue
            for name in sorted(os.listdir(folder)):
                if name.lower().endswith((".png", ".jpg", ".jpeg")):
                    files.append((os.path.join(folder, name), cat))
        if not files:
            raise ValueError("No training images found under " + categories_dir)

        feats, labels = self._features_batch(files)
        for cat in CATEGORIES:
            mask = np.array([lbl == cat for lbl in labels])
            if mask.any():
                self.centroids[cat] = feats[mask].mean(axis=0)

        summary = {cat: int((np.array(labels) == cat).sum()) for cat in CATEGORIES}
        print_header("TRAINING COMPLETE")
        for cat in CATEGORIES:
            ok = f"{summary[cat]} photo(s)" if summary[cat] else "NO DATA"
            print(f"  {cat:<14} -> {ok}")
        return summary

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    def classify(self, image_path: str) -> str:
        """Return the category name with the closest centroid."""
        feats = self.extract_features(image_path)
        best_cat, best_dist = None, float("inf")
        for cat, centroid in self.centroids.items():
            if centroid is None:
                continue
            dist = float(np.linalg.norm(feats - centroid))
            if dist < best_dist:
                best_cat, best_dist = cat, dist
        return best_cat or "Unknown"

    def classify_with_score(self, image_path: str):
        """Return (category, distance) for an image."""
        feats = self.extract_features(image_path)
        results = {c: float(np.linalg.norm(feats - m))
                   for c, m in self.centroids.items() if m is not None}
        if not results:
            return "Unknown", float("inf")
        return min(results, key=results.get), min(results.values())

    # ------------------------------------------------------------------
    # Folder sorting
    # ------------------------------------------------------------------

    def sort_folder(self, source_dir: str, out_root: str) -> list:
        """Sort every photo in source_dir into categorised output folders."""
        plan_created = False
        for cat in CATEGORIES:
            folder = os.path.join(out_root, cat)
            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
                plan_created = True
        report = []
        for name in sorted(os.listdir(source_dir)):
            if not name.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            src = os.path.join(source_dir, name)
            cat, _ = self.classify_with_score(src)
            dst_dir = os.path.join(out_root, cat) if cat in CATEGORIES else out_root
            dst = os.path.join(dst_dir, name)
            shutil.copy2(src, dst)
            report.append((name, cat))
        return report

    # ------------------------------------------------------------------
    # Convenience pipelines
    # ------------------------------------------------------------------

    def demo(self):
        """Train on the bundled sample photos and classify each of them."""
        self.train(IMAGES_DIR)
        print_section("CLASSIFICATION RESULTS (BUNDLED SAMPLE PHOTOS)")
        ok = total = 0
        for cat in CATEGORIES:
            folder = os.path.join(IMAGES_DIR, cat)
            for name in sorted(os.listdir(folder)):
                if not name.lower().endswith((".png", ".jpg", ".jpeg")):
                    continue
                path = os.path.join(folder, name)
                predicted = self.classify(path)
                match = "OK" if predicted == cat else "MISMATCH"
                ok += predicted == cat
                total += 1
                print(f"  {cat:<12} / {name:<28} -> {predicted:<12} {match}")
        print(f"\nAccuracy on sample photos: {ok}/{total} "
              f"({100 * ok / total if total else 0:.1f}%)")
        if ok < total:
            print("!! Re-run classifier; some samples do not match their folder.")


def main():
    parser = argparse.ArgumentParser(description="Future Mall image product classifier")
    parser.add_argument("--classify", metavar="IMG", help="Classify a single photo")
    parser.add_argument("--sort", metavar="DIR", help="Sort all photos in a folder")
    parser.add_argument("--out", default="classified")
    parser.add_argument("--train", metavar="DIR", help="Train from labeled folders")
    parser.add_argument("--demo", action="store_true", help="Run the bundled demo")
    args = parser.parse_args()

    model = ImageClassifier()
    default_train = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

    if args.demo:
        model.demo()
        return

    if args.train:
        model.train(args.train)
    else:
        model.train(default_train)

    if args.classify:
        cat, dist = model.classify_with_score(args.classify)
        print(f"\n'{os.path.basename(args.classify)}' -> category: {cat} "
              f"(distance {dist:.3f})")
        return

    if args.sort:
        report = model.sort_folder(args.sort, args.out)
        print(f"\nSorted {len(report)} photo(s) into '{args.out}/':")
        for name, cat in report:
            print(f"  {name:<30} -> {cat}")
        return

    print("Nothing to do. Use --classify, --sort, --train or --demo.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)