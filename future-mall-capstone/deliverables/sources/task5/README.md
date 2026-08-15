# Smart Garage Gate (Task 5)

A simulated smart garage gate for **Future Mall** built on the **ESP32** with
**MicroPython** and simulated in **Wokwi**.

## Contents

```
task5/
├── README.md
└── esp32_wokwi/
    ├── wokwi.toml          # Wokwi project config (board = ESP32 DevKit V1)
    ├── diagram.json        # Wokwi circuit: ESP32 + 4 LEDs + 2 buttons
    ├── truth_table.txt     # Truth table (required deliverable)
    ├── wiring_diagram.txt  # Connection table + ASCII circuit (required deliverable)
    └── src/
        └── main.py         # MicroPython firmware (upload to the ESP32)
```

## What the gate does

- **IN button**  (GPIO16) — a car enters → counter **+1**, yellow LED flashes.
- **OUT button** (GPIO17) — a car exits → counter **-1**, blue LED flashes.
- The counter is clamped between **0 and 15** cars.
- **Green LED** (GPIO13) is ON while there is free space (`count < 15`).
- **Red LED**   (GPIO14) is ON when the garage is FULL (`count == 15`).
- Every change is logged over serial so the logic can be verified.

| LED    | GPIO | Meaning                            |
|--------|------|------------------------------------|
| Green  | 13   | Free space available (count < 15)  |
| Red    | 14   | Garage FULL (count == 15)          |
| Yellow | 26   | Flash when a car enters            |
| Blue   | 27   | Flash when a car exits             |

## Run it in Wokwi

1. Go to <https://wokwi.com> → **New project**.
2. Replace `diagram.json`, `wokwi.toml` and `src/main.py` with the files here.
3. Click **Start Simulation**.
4. Press the green button (IN) to add cars — watch the LEDs and the serial
   console; press until 15 cars and the red LED turns on, then use OUT.

## Truth table & diagrams

See `truth_table.txt` for the state/event truth table, and
`wiring_diagram.txt` for the connection table + ASCII circuit.

## Verify from a PC (optional)

`src/main.py` is plain MicroPython — syntax can be checked locally with:

```bash
python -m py_compile esp32_wokwi/src/main.py
```

---

*Part of the Future Mall capstone project — Shopping for Tomorrow.*