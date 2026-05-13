# 🧮 BMI Calculator

A **professional-grade BMI Health Analyzer** built with Python and Tkinter.  
Designed with a polished two-page UI, real-time BMI calculation, a visual speedometer gauge, and personalised health suggestions — all without any external libraries.

---

## ✨ Features

- 🖥️ **Full-screen two-page app** — clean Input Page and scrollable Result Page
- 📊 **Semi-circular speedometer gauge** — colour-coded needle that points to your exact BMI
- 🗂️ **8-category BMI classification** — from Very Severely Underweight to Obese Class III (WHO standard)
- 💡 **Personalised health & diet tips** — 5 tailored suggestions based on your BMI result
- ⚖️ **Healthy weight range** — calculates the ideal weight range for your exact height
- 👤 **User summary chips** — Age, Height and Weight displayed clearly on the result page
- 🎨 **Card-based UI** — shadow cards, coloured accent stripes, and a consistent orange brand theme
- 📜 **Fully scrollable result page** — all information always visible regardless of screen size
- ✅ **Input validation** — clear error messages for invalid or out-of-range values
- 🔁 **Back button** — return to the input page and recalculate instantly
- 💬 **Well-commented code** — every section explained for learning and presentation

---

## 🧠 BMI Formula

```
BMI = Weight (kg) ÷ Height² (m²)
```

**Example:** Weight = 70 kg, Height = 175 cm (1.75 m)  
→ BMI = 70 ÷ (1.75 × 1.75) = **22.9 → Normal**

---

## 📋 BMI Categories (WHO Standard)

| Category                    | BMI Range     |
|-----------------------------|---------------|
| Very Severely Underweight   | ≤ 15.9        |
| Severely Underweight        | 16.0 – 16.9   |
| Underweight                 | 17.0 – 18.4   |
| ✅ Normal                   | 18.5 – 24.9   |
| Overweight                  | 25.0 – 29.9   |
| Obese Class I               | 30.0 – 34.9   |
| Obese Class II              | 35.0 – 39.9   |
| Obese Class III             | ≥ 40.0        |

---

## 🖼️ App Pages

### Page 1 — Input
- Orange header banner with app branding
- Left card: Age, Height, and Weight input fields with styled borders
- Right card: Full BMI reference table with colour-coded categories
- Instant validation and clear error messages

### Page 2 — Result (Scrollable)
- Orange header with Back button
- Age / Height / Weight summary chips
- **Semi-circular gauge** with Blue / Green / Red zones and a needle
- Large BMI number and category name in matching colour
- Highlighted category table — your row stands out
- Healthy weight range for your height
- 5 personalised diet and health suggestions

---

## 📂 Built With

| Tool       | Purpose                        |
|------------|--------------------------------|
| Python 3   | Core programming language      |
| Tkinter    | GUI framework (built-in)       |
| Math       | Gauge needle angle calculation |

> No external libraries required — runs on any standard Python installation.

---

## ▶️ How to Run

1. Make sure **Python 3** is installed → [python.org](https://www.python.org/)
2. Download or clone this repository
3. Open a terminal in the project folder
4. Run the app:

```bash
python bmi_calculator.py
```

> The window opens in **full-screen mode** automatically.  
> Press the **← Back** button on the result page to recalculate.

---


## 🎓 About

This project was built to demonstrate:
- Python GUI development with Tkinter
- Mathematical calculations and formula implementation
- Multi-page app navigation without external frameworks
- Clean UI design principles using only built-in tools
- Input validation and error handling

---


