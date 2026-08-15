import pytest
import sys
import os
import shutil
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python_modules'))

from image_classifier import ImageClassifier, CATEGORIES, IMAGES_DIR


class TestImageClassifier:
    def setup_method(self):
        self.clf = ImageClassifier()
        self.clf.train(IMAGES_DIR)

    def test_centroids_trained(self):
        for cat in CATEGORIES:
            assert self.clf.centroids[cat] is not None

    def test_three_categories(self):
        assert len(CATEGORIES) == 3

    def test_classify_all_sample_photos(self):
        ok = total = 0
        for cat in CATEGORIES:
            folder = os.path.join(IMAGES_DIR, cat)
            for name in os.listdir(folder):
                if not name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue
                path = os.path.join(folder, name)
                from PIL import Image
                Image.open(path).load()          # file is a real image
                assert self.clf.classify(path) == cat
                ok += 1
                total += 1
        assert total >= 18
        assert ok == total

    def test_extract_features_shape(self):
        img = os.path.join(IMAGES_DIR, "Groceries", os.listdir(
            os.path.join(IMAGES_DIR, "Groceries"))[0])
        feats = self.clf.extract_features(img)
        assert feats.ndim == 1
        assert feats.shape[0] > 0

    def test_sort_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "inbox")
            os.makedirs(src, exist_ok=True)
            for cat in CATEGORIES:
                folder = os.path.join(IMAGES_DIR, cat)
                shutil.copy2(os.path.join(folder, sorted(
                    os.listdir(folder))[0]), src)
            out = os.path.join(tmp, "sorted")
            report = self.clf.sort_folder(src, out)
            assert len(report) == len(CATEGORIES)
            for name, predicted in report:
                assert os.path.exists(os.path.join(out, predicted, name))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])