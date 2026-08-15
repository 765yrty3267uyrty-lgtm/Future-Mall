# Python Modules

Console and desktop applications of the Future Mall capstone project.

## Apps

| Script | Description | Run |
|--------|-------------|-----|
| `cashier_program.py` | Shop simulator: cart, 10% discount over 500 EGP, tax, receipts | `python cashier_program.py` |
| `visitors_analysis.py` | Reads mall visitors from Excel, finds busiest/quietest day, chart | `python visitors_analysis.py` |
| `image_classifier.py` | **Image classifier**: sorts product photos into 3 categories | `python image_classifier.py --demo` |
| `product_classifier.py` | Attribute-based classification (price/weight/stock) | `python product_classifier.py` |
| `attendance_system/` | Tkinter + SQLite desktop app | see below |

## Image Classifier

Sorts product photos into three distinct categories: **Electronics,
Groceries, Clothing**.

```bash
# bundled demo (trains on photos/ and classifies them)
python image_classifier.py --demo

# classify one photo
python image_classifier.py --classify photos/camera.png

# train from labeled folders, then sort a whole folder
python image_classifier.py --train images --sort ./new_photos --out classified
```

Training data lives in `images/{Electronics,Groceries,Clothing}/`. Add your
own product photos to these folders and the classifier retrains on them.

## Visitors Analysis (Excel)

```bash
python visitors_analysis.py
```

- Loads `data/visitors_data.xlsx` (a real sample of one mall week)
- Prints the **busiest** and **quietest** day
- Generates `data/visitors_chart.png` (bar chart)
- Writes `data/visitors_analysis.xlsx` (report) + optional CSV/JSON

## Cashier

Rule: the customer gets a **10% discount** whenever the subtotal is **above
500 EGP**.

## Attendance System

```bash
cd attendance_system
pip install -r requirements.txt
python main.py
```

Features:
- 3 roles (Employee, Supervisor, Admin)
- Check-in/check-out with validation
- Role-based dashboards with reports
- CSV/Excel export
- Dark mode

See `attendance_system/requirements.txt` and `docs/ARCHITECTURE.md`.

## Shared Tokens

All Python apps import shared constants from `shared/constants.py`
(e.g., brand colors, tax rate, discount threshold/rate) to keep values
consistent.
