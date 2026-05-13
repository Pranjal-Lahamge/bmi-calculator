# ==============================================================
#         BMI HEALTH ANALYZER  — Premium Edition
#              Created with Python Tkinter
#                  College Project 2024
# ==============================================================
#
#  DESIGN :
#  -----------------------------------------------------------
#  PAGE 1  -  Input Page
#    LEFT  BOX  :  App branding + input fields + calculate btn
#    RIGHT BOX  :  BMI category reference table
#
#  PAGE 2  -  Result Page  (scrollable)
#    TOP   BOX  :  Age / Height / Weight chips + Gauge + BMI
#    RIGHT BOX  :  Full category table (highlighted)
#    BOTTOM BOX :  Healthy range card + Diet tips card
#
#  COLOUR SCHEME :
#    Orange brand (#ff6b00) headers / accents
#    White cards with soft shadow illusion
#    Blue / Green / Amber / Red for BMI zones
#
#  BMI FORMULA :
#    BMI = Weight(kg) / Height(m)^2
#
#  SCROLL :
#    Both pages use Canvas + Scrollbar + inner Frame.
#    The inner Frame is always stretched to canvas width.
#    No pack_propagate(False) — causes blank screens.
#

# ==============================================================


import tkinter as tk
import math


# ==============================================================
# SECTION 1 :  COLOUR PALETTE
# ==============================================================

ORANGE     = "#ff6b00"          # Primary brand orange
ORANGE_DK  = "#cc5500"          # Darker orange for hover states
ORANGE_LT  = "#fff0e6"          # Very light orange tint (page bg)
WHITE      = "#ffffff"
CARD_BG    = "#ffffff"          # White card background
LIGHT      = "#f4f5f7"          # Light grey for input / chip bg
BORDER     = "#e2e4e8"          # Subtle border colour
DARK       = "#1a1a2e"          # Deep navy-black for main text
MID        = "#4a5568"          # Medium grey for body text
MUTED      = "#9aa3b0"          # Grey for secondary labels

# BMI zone colours
BLUE       = "#3b82f6"          # Underweight  (cool blue)
GREEN      = "#22c55e"          # Normal       (vivid green)
AMBER      = "#f59e0b"          # Overweight   (warm amber)
RED_C      = "#ef4444"          # Obese        (alert red)


# ==============================================================
# SECTION 2 :  ROOT WINDOW
# ==============================================================

root = tk.Tk()
root.title("BMI Health Analyzer — Premium Edition")
root.state("zoomed")                    # Full screen on Windows
# root.attributes("-zoomed", True)      # Full screen on Linux
root.configure(bg=ORANGE_LT)
root.resizable(True, True)


# ==============================================================
# SECTION 3 :  SCROLLABLE PAGE BUILDER
# ==============================================================

def make_scrollable_page(bg=ORANGE_LT):
    """
    Creates a full-screen scrollable page.
    Returns (outer_frame, inner_frame, canvas).
    All page content goes inside inner_frame.

    KEY FIX: canvas <Configure> binding stretches inner_frame
    to always match canvas width — prevents blank/empty pages.
    """
    outer  = tk.Frame(root, bg=bg)
    canvas = tk.Canvas(outer, bg=bg, highlightthickness=0)
    sb     = tk.Scrollbar(outer, orient="vertical",
                           command=canvas.yview)
    inner  = tk.Frame(canvas, bg=bg)

    # Update scroll region when inner content changes size
    inner.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all"))
    )

    win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    # Stretch inner frame to fill canvas width on every resize
    def _resize(event):
        canvas.itemconfig(win_id, width=event.width)
    canvas.bind("<Configure>", _resize)

    canvas.configure(yscrollcommand=sb.set)
    canvas.pack(side="left",  fill="both", expand=True)
    sb.pack(    side="right", fill="y")

    # Mouse-wheel scrolling
    def _wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind("<MouseWheel>", _wheel)

    return outer, inner, canvas


# ==============================================================
# SECTION 4 :  REUSABLE WIDGET BUILDERS
# ==============================================================

def styled_card(parent, bg=CARD_BG):
    """
    Simulates a card with shadow by nesting frames:
      shadow frame (1px dark border) → white inner frame.
    Returns (shadow_frame, inner_frame).
    Pack content into inner_frame.
    """
    shadow = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
    inner  = tk.Frame(shadow, bg=bg)
    inner.pack(fill="both", expand=True)
    return shadow, inner


def input_field(parent, label_text, bg=CARD_BG):
    """
    Builds a premium styled input field:
      - Bold label above
      - Entry box with border wrapper
    Returns the Entry widget.
    """
    # Label
    tk.Label(
        parent,
        text=label_text,
        font=("Segoe UI", 11, "bold"),      # INCREASED from 9
        bg=bg, fg=MUTED, anchor="w"
    ).pack(fill="x", padx=28, pady=(14, 4))

    # Border wrapper around entry
    wrap = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
    wrap.pack(fill="x", padx=28)

    e = tk.Entry(
        wrap,
        font=("Segoe UI", 16),              # INCREASED from 14
        bg=LIGHT, fg=DARK,
        relief="flat", justify="left", bd=0
    )
    e.pack(ipady=14, fill="x", padx=12)    # INCREASED ipady from 12
    return e


def cat_row(parent, name, rng, color, highlight, bg=CARD_BG):
    """
    One row in the BMI category table.
    Highlighted = coloured background + white bold text.
    Normal      = white background + colour dot + grey text.
    """
    row_bg = color  if highlight else bg
    row_fg = WHITE  if highlight else MID
    fw     = "bold" if highlight else "normal"

    row = tk.Frame(parent, bg=row_bg)
    row.pack(fill="x", pady=2)              # INCREASED pady from 1

    # Colour dot indicator on left
    dot_color = WHITE if highlight else color
    tk.Label(
        row, text="●",
        font=("Segoe UI", 12),              # INCREASED from 10
        bg=row_bg, fg=dot_color, padx=14
    ).pack(side="left")

    # Category name
    tk.Label(
        row, text=name,
        font=("Segoe UI", 13, fw),          # INCREASED from 10
        bg=row_bg, fg=row_fg,
        anchor="w", pady=11                 # INCREASED pady from 8
    ).pack(side="left", expand=True, fill="x")

    # BMI range value on right
    tk.Label(
        row, text=rng,
        font=("Segoe UI", 13),              # INCREASED from 10
        bg=row_bg, fg=row_fg, padx=16
    ).pack(side="right")


# All 8 BMI categories
CATEGORIES = [
    ("Very Severely Underweight", "≤ 15.9",    BLUE),
    ("Severely Underweight",      "16.0–16.9", BLUE),
    ("Underweight",               "17.0–18.4", BLUE),
    ("Normal",                    "18.5–24.9", GREEN),
    ("Overweight",                "25.0–29.9", AMBER),
    ("Obese Class I",             "30.0–34.9", RED_C),
    ("Obese Class II",            "35.0–39.9", RED_C),
    ("Obese Class III",           "40.0 +",    RED_C),
]


# ==============================================================
# SECTION 5 :  GAUGE DRAWING
# ==============================================================

def draw_gauge(canvas, bmi_value):
    """
    Draws the filled semi-circular speedometer gauge.

    Three colour zones across 180° (left = BMI 0, right = BMI 40):
      Blue   = Underweight  ( 0    – 18.5 )
      Green  = Normal       ( 18.5 – 25   )
      Red    = Overweight+  ( 25   – 40   )

    Drawing steps:
      1. Three pieslice arcs fill the semicircle zones
      2. White rectangle hides the flat bottom of the pieslices
      3. White oval punches the inner donut hole
      4. Zone text labels centred inside each coloured band
      5. Boundary tick labels around the outer rim
      6. Triangle needle pointing at the exact BMI angle
      7. Pivot circles at needle base (outer dark + inner white)
      8. "Category" and "Difference" corner labels
    """
    canvas.delete("all")

    cw = canvas.winfo_width()
    ch = canvas.winfo_height()
    if cw < 10: cw = 560          # Fallback before widget renders
    if ch < 10: ch = 260

    cx   = cw // 2                # Horizontal centre
    cy   = ch - 28                # Vertical origin (near bottom)
    R    = min(cw // 2 - 30, ch - 36)   # Arc outer radius
    HOLE = int(R * 0.52)          # Inner hole radius (donut)

    def b2a(b):
        """
        Converts a BMI value (0–40) to a tkinter canvas angle.
        BMI 0  → 180°  (left  / 9 o'clock)
        BMI 40 →   0°  (right / 3 o'clock)
        """
        return 180 - (min(max(b, 0), 40) / 40) * 180

    # Boundary angles for zone edges
    a_185 = b2a(18.5)             # Blue / Green boundary
    a_25  = b2a(25)               # Green / Red boundary
    bb    = (cx - R, cy - R, cx + R, cy + R)   # Bounding box

    # ── Step 1 : Three filled colour zones ──────────────────────
    # Blue zone  : BMI 0 → 18.5  (left portion)
    canvas.create_arc(*bb, start=a_185, extent=180 - a_185,
                      fill=BLUE,  outline=BLUE,  style="pieslice")
    # Green zone : BMI 18.5 → 25  (middle portion)
    canvas.create_arc(*bb, start=a_25,  extent=a_185 - a_25,
                      fill=GREEN, outline=GREEN, style="pieslice")
    # Red zone   : BMI 25 → 40   (right portion)
    canvas.create_arc(*bb, start=0,     extent=a_25,
                      fill=RED_C, outline=RED_C, style="pieslice")

    # ── Step 2 : Mask the flat bottom edge of the pieslices ──────
    canvas.create_rectangle(cx - R - 4, cy, cx + R + 4, cy + ch,
                             fill=CARD_BG, outline=CARD_BG)

    # ── Step 3 : White donut hole in the centre ──────────────────
    canvas.create_oval(cx - HOLE, cy - HOLE, cx + HOLE, cy + HOLE,
                       fill=CARD_BG, outline=CARD_BG)

    # ── Step 4 : Zone text labels inside each coloured band ──────
    # Angles are midpoints of each zone so labels sit centred
    lr = int(R * 0.72)
    for text, deg in [("Underweight", 155), ("Normal", 108), ("Overweight", 28)]:
        rad = math.radians(deg)
        canvas.create_text(
            cx + lr * math.cos(rad),
            cy - lr * math.sin(rad),
            text=text, font=("Segoe UI", 9, "bold"),
            fill=WHITE, angle=0
        )

    # ── Step 5 : Boundary tick labels on the outer rim ───────────
    tr = R + 18
    for val, deg in [("0", 180), ("18.5", a_185), ("25", a_25), ("40", 0)]:
        rad = math.radians(deg)
        canvas.create_text(
            cx + tr * math.cos(rad),
            cy - tr * math.sin(rad),
            text=val, font=("Segoe UI", 9, "bold"), fill=MUTED
        )

    # ── Step 6 : Needle triangle pointing at the BMI value ───────
    ang   = math.radians(b2a(bmi_value))
    nlen  = int(R * 0.82)
    tip_x = cx + nlen * math.cos(ang)
    tip_y = cy - nlen * math.sin(ang)
    perp  = ang + math.pi / 2
    base  = 10
    canvas.create_polygon(
        tip_x, tip_y,
        cx + base * math.cos(perp), cy - base * math.sin(perp),
        cx - base * math.cos(perp), cy + base * math.sin(perp),
        fill=DARK, outline=""
    )

    # ── Step 7 : Pivot circles at needle base ────────────────────
    canvas.create_oval(cx - 15, cy - 15, cx + 15, cy + 15,
                       fill=DARK,    outline="")
    canvas.create_oval(cx -  6, cy -  6, cx +  6, cy +  6,
                       fill=CARD_BG, outline="")

    # ── Step 8 : Corner labels ────────────────────────────────────
    canvas.create_text(cx - int(R * 0.82), cy + 18,
                       text="Category",   font=("Segoe UI", 9), fill=MUTED)
    canvas.create_text(cx + int(R * 0.82), cy + 18,
                       text="Difference", font=("Segoe UI", 9), fill=MUTED)


# ==============================================================
# SECTION 6 :  CALCULATE BMI
# ==============================================================

def calculate_bmi():
    """
    Reads and validates the three input fields.
    Calculates BMI using the formula: weight / (height_m)^2
    Determines BMI category and personalised health tips.
    Updates all result page widgets.
    Switches to the result page.
    """
    err_lbl.config(text="")

    a = age_entry.get().strip()
    h = height_entry.get().strip()
    w = weight_entry.get().strip()

    # Validation: all fields filled
    if not a or not h or not w:
        err_lbl.config(text="⚠  Please fill in all three fields.")
        return

    # Validation: numeric values
    try:
        age    = int(float(a))
        height = float(h)
        weight = float(w)
    except ValueError:
        err_lbl.config(text="⚠  Please enter valid numbers only.")
        return

    # Validation: realistic ranges
    if not (50 <= height <= 280):
        err_lbl.config(text="⚠  Height must be between 50 and 280 cm.")
        return
    if not (1 <= weight <= 500):
        err_lbl.config(text="⚠  Weight must be between 1 and 500 kg.")
        return

    # ── BMI Formula ─────────────────────────────────────────────
    hm  = height / 100.0                       # Convert cm → metres
    bmi = round(weight / (hm * hm), 1)         # BMI = kg / m²

    # ── Healthy weight range for this height ────────────────────
    min_w = round(18.5 * hm * hm, 1)
    max_w = round(24.9 * hm * hm, 1)

    # ── Category + colour + tips ─────────────────────────────────
    if bmi <= 15.9:
        cat, col = "Very Severely Underweight", BLUE
        tips = [
            "Eat calorie-dense whole foods: nuts, avocados, whole milk, cheese",
            "Have 5–6 small meals spread evenly throughout the day",
            "Add protein shakes or smoothies between main meals",
            "Begin very gentle exercise such as short daily walks",
            "See a doctor or nutritionist immediately for a plan",
        ]
    elif bmi <= 16.9:
        cat, col = "Severely Underweight", BLUE
        tips = [
            "Increase your daily calorie intake by 500–700 extra calories",
            "Eat protein-rich foods: eggs, chicken, lentils, dairy products",
            "Never skip any meal — eat at consistent times every day",
            "Include healthy fats in meals: peanut butter, olive oil, nuts",
            "Consult a healthcare professional for a personalised plan",
        ]
    elif bmi <= 18.4:
        cat, col = "Underweight", BLUE
        tips = [
            "Eat more frequently — aim for a meal or snack every 3 hours",
            "Include whole grains, lean meats and legumes in every meal",
            "Add strength training exercises 3 times a week to build muscle",
            "Track your daily calories to ensure a healthy calorie surplus",
            "Drink fortified milk or protein beverages daily",
        ]
    elif bmi <= 24.9:
        cat, col = "Normal", GREEN
        tips = [
            "Excellent — your BMI is perfectly in the healthy range!",
            "Keep eating a balanced diet covering all food groups daily",
            "Exercise at least 30 minutes per day, 5 days per week",
            "Stay well hydrated: aim for 8–10 glasses of water daily",
            "Schedule annual health check-ups to stay on track long-term",
        ]
    elif bmi <= 29.9:
        cat, col = "Overweight", AMBER
        tips = [
            "Reduce refined carbohydrates, fried foods and sugary drinks",
            "Add 30–45 minutes of cardio daily: walking, cycling, swimming",
            "Fill half your plate with vegetables and fruits at every meal",
            "Limit restaurant and fried food to a maximum of once a week",
            "Keep a food diary to track your calorie intake vs expenditure",
        ]
    elif bmi <= 34.9:
        cat, col = "Obese Class I", RED_C
        tips = [
            "Start a structured low-calorie meal plan with professional help",
            "Aim for at least 150 minutes of moderate exercise each week",
            "Cut out all sugary beverages, alcohol and processed snacks",
            "Consult a certified nutritionist or registered dietitian",
            "Set small, achievable monthly weight-loss goals (1–2 kg/month)",
        ]
    elif bmi <= 39.9:
        cat, col = "Obese Class II", RED_C
        tips = [
            "Seek combined guidance from a doctor and registered dietitian",
            "Begin low-impact exercise: swimming, walking, stationary cycling",
            "Follow a medically supervised calorie-reduction meal plan",
            "Avoid crash diets — focus on gradual sustainable lifestyle change",
            "Monitor blood pressure, blood sugar and cholesterol monthly",
        ]
    else:
        cat, col = "Obese Class III", RED_C
        tips = [
            "Consult a doctor immediately for a full health assessment",
            "A medically supervised programme or intervention may be needed",
            "Start with gentle daily movement such as 10-minute walks",
            "Eliminate junk food, soft drinks and alcohol from your diet",
            "Track health metrics weekly with professional medical support",
        ]

    # ── Update result page widgets ────────────────────────────────
    r_age_val.config(    text=str(age))
    r_height_val.config( text=str(height))
    r_weight_val.config( text=str(weight))
    r_bmi_num.config(    text=str(bmi),   fg=col)
    r_bmi_cat.config(    text=cat,         fg=col)
    r_hw_val.config(     text=f"{min_w} kg  –  {max_w} kg")
    r_tips_lbl.config(   text="\n\n".join(
        f"  {i+1}.  {t}" for i, t in enumerate(tips)
    ))

    # Rebuild category table — highlight the user's row
    for widget in cat_table_frame.winfo_children():
        widget.destroy()
    for name, rng, color in CATEGORIES:
        cat_row(cat_table_frame, name, rng, color,
                highlight=(name == cat), bg=CARD_BG)

    # Switch to result page and reset scroll to top
    input_outer.pack_forget()
    result_outer.pack(fill="both", expand=True)
    result_canvas_widget.yview_moveto(0)

    # Draw gauge after page renders (needs real canvas pixel size)
    root.after(80, lambda: draw_gauge(gauge_cv, bmi))


# ==============================================================
# SECTION 7 :  BACK BUTTON
# ==============================================================

def go_back():
    """Switches from result page back to the input page."""
    result_outer.pack_forget()
    input_outer.pack(fill="both", expand=True)


# ==============================================================
# SECTION 8 :  PAGE 1  —  INPUT PAGE
# ==============================================================

input_outer, input_inner, _ = make_scrollable_page(bg=ORANGE_LT)
input_outer.pack(fill="both", expand=True)   # Shown on startup

# ── Full-width orange header banner ──────────────────────────
banner = tk.Frame(input_inner, bg=ORANGE)
banner.pack(fill="x")

banner_inner = tk.Frame(banner, bg=ORANGE)
banner_inner.pack(pady=32)

tk.Label(
    banner_inner,
    text="◉  BMI Health Analyzer",
    font=("Segoe UI", 30, "bold"),          
    bg=ORANGE, fg=WHITE
).pack()

tk.Label(
    banner_inner,
    text="Know your body  •  Track your health  •  Live better",
    font=("Segoe UI", 12),                 
    bg=ORANGE, fg="#ffe0c8"
).pack(pady=(8, 0))

# ── Two-column card layout ────────────────────────────────────
columns = tk.Frame(input_inner, bg=ORANGE_LT)
columns.pack(fill="x", padx=44, pady=30)
columns.columnconfigure(0, weight=55, uniform="cols")
columns.columnconfigure(1, weight=45, uniform="cols")

# ============================================================
# LEFT CARD  :  Input form
# ============================================================
left_shadow, left_card = styled_card(columns)
left_shadow.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

# Orange title bar at top of left card
left_title_bar = tk.Frame(left_card, bg=ORANGE)
left_title_bar.pack(fill="x")

tk.Frame(left_title_bar, bg=ORANGE, height=18).pack()

lt_inner = tk.Frame(left_title_bar, bg=ORANGE)
lt_inner.pack(padx=28, fill="x")

tk.Label(
    lt_inner,
    text="Enter Your Details",
    font=("Segoe UI", 17, "bold"),          
    bg=ORANGE, fg=WHITE
).pack(anchor="w")

tk.Label(
    lt_inner,
    text="Fill in the fields below to calculate your BMI",
    font=("Segoe UI", 11),
    bg=ORANGE, fg="#ffe0c8"
).pack(anchor="w", pady=(4, 0))

tk.Frame(left_title_bar, bg=ORANGE, height=18).pack()

# Input fields
age_entry    = input_field(left_card, "👤  AGE  (years)")
height_entry = input_field(left_card, "📏  HEIGHT  (centimetres)")
weight_entry = input_field(left_card, "⚖️  WEIGHT  (kilograms)")

# Error label
err_lbl = tk.Label(
    left_card, text="",
    font=("Segoe UI", 11),                 
    bg=CARD_BG, fg=RED_C, wraplength=380
)
err_lbl.pack(pady=(10, 0), padx=28, anchor="w")

# Calculate button
btn_frame = tk.Frame(left_card, bg=CARD_BG)
btn_frame.pack(fill="x", padx=28, pady=(14, 0))

tk.Button(
    btn_frame,
    text="  Calculate BMI  →",
    font=("Segoe UI", 14, "bold"),         
    bg=ORANGE, fg=WHITE,
    relief="flat", padx=28, pady=16,       
    cursor="hand2",
    activebackground=ORANGE_DK,
    activeforeground=WHITE,
    command=calculate_bmi
).pack(fill="x")

tk.Label(
    left_card,
    text="BMI is a screening estimate. Always consult a health professional.",
    font=("Segoe UI", 10),                
    bg=CARD_BG, fg=MUTED, wraplength=380
).pack(pady=(12, 24), padx=28)


# ============================================================
# RIGHT CARD  :  BMI reference table
# ============================================================
right_shadow, right_card = styled_card(columns)
right_shadow.grid(row=0, column=1, sticky="nsew", padx=(14, 0))

# Dark title bar
right_title_bar = tk.Frame(right_card, bg=DARK)
right_title_bar.pack(fill="x")

tk.Frame(right_title_bar, bg=DARK, height=18).pack()

rt_inner = tk.Frame(right_title_bar, bg=DARK)
rt_inner.pack(padx=20, fill="x")

tk.Label(
    rt_inner,
    text="BMI Categories",
    font=("Segoe UI", 17, "bold"),        
    bg=DARK, fg=WHITE
).pack(anchor="w")

tk.Label(
    rt_inner,
    text="WHO International Standard Classification",
    font=("Segoe UI", 11),                  
    bg=DARK, fg=MUTED
).pack(anchor="w", pady=(4, 0))

tk.Frame(right_title_bar, bg=DARK, height=18).pack()

# Column headers
col_hdr = tk.Frame(right_card, bg=LIGHT)
col_hdr.pack(fill="x")

tk.Label(
    col_hdr, text="Category",
    font=("Segoe UI", 11, "bold"),         
    bg=LIGHT, fg=MID,
    padx=28, pady=10, anchor="w"          
).pack(side="left", fill="x", expand=True)

tk.Label(
    col_hdr, text="BMI Range",
    font=("Segoe UI", 11, "bold"),          
    bg=LIGHT, fg=MID, padx=16, pady=10     
).pack(side="right")

# All 8 category rows (none highlighted on input page)
for name, rng, color in CATEGORIES:
    cat_row(right_card, name, rng, color, highlight=False, bg=CARD_BG)

tk.Label(
    right_card,
    text="Source: WHO Global BMI Classification",
    font=("Segoe UI", 10),                 
    bg=CARD_BG, fg=MUTED
).pack(pady=12)

# Bottom page padding
tk.Frame(input_inner, bg=ORANGE_LT, height=32).pack()


# ==============================================================
# SECTION 9 :  PAGE 2  —  RESULT PAGE  (scrollable)
# ==============================================================

result_outer, result_inner, result_canvas_widget = \
    make_scrollable_page(bg=ORANGE_LT)
# Not packed yet — shown after calculate_bmi()

# ── Orange header banner with Back button ──────────────────────
res_banner = tk.Frame(result_inner, bg=ORANGE)
res_banner.pack(fill="x")

res_top = tk.Frame(res_banner, bg=ORANGE)
res_top.pack(fill="x", pady=18, padx=24)

tk.Button(
    res_top,
    text="  ←  Back  ",
    font=("Segoe UI", 12, "bold"),         
    bg=WHITE, fg=ORANGE,
    relief="flat", padx=12, pady=8,
    cursor="hand2",
    activebackground=ORANGE_LT,
    command=go_back
).pack(side="left")

tk.Label(
    res_top,
    text="Your BMI Report",
    font=("Segoe UI", 20, "bold"),         
    bg=ORANGE, fg=WHITE
).pack(side="left", padx=22)

# ── Two-column top section (Gauge + Category table) ──────────
res_cols = tk.Frame(result_inner, bg=ORANGE_LT)
res_cols.pack(fill="x", padx=44, pady=26)
res_cols.columnconfigure(0, weight=55, uniform="res")
res_cols.columnconfigure(1, weight=45, uniform="res")

# ============================================================
# TOP-LEFT CARD  :  Info chips + Gauge + BMI value
# ============================================================
top_shadow, top_card = styled_card(res_cols)
top_shadow.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

# Orange top stripe
tk.Frame(top_card, bg=ORANGE, height=6).pack(fill="x")

tk.Label(
    top_card,
    text="  BMI Overview",
    font=("Segoe UI", 15, "bold"),          
    bg=CARD_BG, fg=DARK
).pack(anchor="w", padx=18, pady=(14, 6))

# Info chips row (Age / Height / Weight)
chips_outer = tk.Frame(top_card, bg=CARD_BG)
chips_outer.pack(fill="x", padx=18, pady=(0, 4))

def make_result_chip(parent, icon, title, unit):
    """Creates a styled info chip with icon, label, value, unit."""
    chip = tk.Frame(parent, bg=LIGHT)
    chip.pack(side="left", expand=True, fill="x", padx=5)

    # Orange accent bar at top of each chip
    tk.Frame(chip, bg=ORANGE, height=4).pack(fill="x")

    tk.Label(
        chip,
        text=icon + "  " + title,
        font=("Segoe UI", 10, "bold"),      
        bg=LIGHT, fg=MUTED
    ).pack(pady=(10, 2))

    val = tk.Label(
        chip, text="–",
        font=("Segoe UI", 22, "bold"),      
        bg=LIGHT, fg=DARK
    )
    val.pack()

    tk.Label(
        chip, text=unit,
        font=("Segoe UI", 10),             
        bg=LIGHT, fg=MUTED
    ).pack(pady=(2, 10))

    return val

r_age_val    = make_result_chip(chips_outer, "👤", "Age",    "years")
r_height_val = make_result_chip(chips_outer, "📏", "Height", "cm")
r_weight_val = make_result_chip(chips_outer, "⚖️", "Weight", "kg")

# Gauge canvas (semi-circular speedometer)
gauge_cv = tk.Canvas(top_card, bg=CARD_BG,
                     highlightthickness=0, height=260)  
gauge_cv.pack(fill="x", padx=10, pady=(14, 0))

# BMI number block
bmi_disp = tk.Frame(top_card, bg=CARD_BG)
bmi_disp.pack(pady=(6, 0))

tk.Label(
    bmi_disp, text="Your BMI",
    font=("Segoe UI", 12, "bold"),         
    bg=CARD_BG, fg=MUTED
).pack()

r_bmi_num = tk.Label(
    bmi_disp, text="–",
    font=("Segoe UI", 60, "bold"),         
    bg=CARD_BG, fg=GREEN
)
r_bmi_num.pack()

r_bmi_cat = tk.Label(
    bmi_disp, text="–",
    font=("Segoe UI", 16, "bold"),         
    bg=CARD_BG, fg=GREEN
)
r_bmi_cat.pack(pady=(0, 22))


# ============================================================
# TOP-RIGHT CARD  :  Full category table (with highlight)
# ============================================================
right_res_shadow, right_res_card = styled_card(res_cols)
right_res_shadow.grid(row=0, column=1, sticky="nsew", padx=(14, 0))

# Dark top stripe
tk.Frame(right_res_card, bg=DARK, height=6).pack(fill="x")

tk.Label(
    right_res_card,
    text="  BMI Categories",
    font=("Segoe UI", 15, "bold"),         
    bg=CARD_BG, fg=DARK
).pack(anchor="w", padx=18, pady=(14, 4))

tk.Label(
    right_res_card,
    text="  Your category is highlighted below",
    font=("Segoe UI", 11),                 
    bg=CARD_BG, fg=MUTED
).pack(anchor="w", padx=18, pady=(0, 10))

# Table column headers
tbl_hdr = tk.Frame(right_res_card, bg=LIGHT)
tbl_hdr.pack(fill="x", pady=(0, 2))

tk.Label(
    tbl_hdr, text="Category",
    font=("Segoe UI", 11, "bold"),          
    bg=LIGHT, fg=MID,
    padx=28, pady=10, anchor="w"            
).pack(side="left", expand=True, fill="x")

tk.Label(
    tbl_hdr, text="BMI Range",
    font=("Segoe UI", 11, "bold"),         
    bg=LIGHT, fg=MID, padx=14, pady=10   
).pack(side="right")

# Category rows container — rebuilt on each calculation
cat_table_frame = tk.Frame(right_res_card, bg=CARD_BG)
cat_table_frame.pack(fill="x")

# Initial state: no row highlighted
for name, rng, color in CATEGORIES:
    cat_row(cat_table_frame, name, rng, color, highlight=False, bg=CARD_BG)

tk.Label(
    right_res_card,
    text="Source: WHO Global BMI Classification",
    font=("Segoe UI", 10),                  
    bg=CARD_BG, fg=MUTED
).pack(pady=12)


# ============================================================
# BOTTOM SECTION  :  Healthy range + Diet tips
# ============================================================
bottom_cols = tk.Frame(result_inner, bg=ORANGE_LT)
bottom_cols.pack(fill="x", padx=44, pady=(0, 26))
bottom_cols.columnconfigure(0, weight=38, uniform="bot")
bottom_cols.columnconfigure(1, weight=62, uniform="bot")

# ── Healthy weight range card ──────────────────────────────
hw_shadow, hw_card = styled_card(bottom_cols)
hw_shadow.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

# Green top stripe
tk.Frame(hw_card, bg=GREEN, height=6).pack(fill="x")

tk.Label(
    hw_card,
    text="  Healthy Weight Range",
    font=("Segoe UI", 14, "bold"),          
    bg=CARD_BG, fg=DARK
).pack(anchor="w", padx=18, pady=(14, 2))

tk.Label(
    hw_card,
    text="  Based on your height",
    font=("Segoe UI", 11),                 
    bg=CARD_BG, fg=MUTED
).pack(anchor="w", padx=18)

r_hw_val = tk.Label(
    hw_card, text="–",
    font=("Segoe UI", 20, "bold"),          
    bg=CARD_BG, fg=GREEN
)
r_hw_val.pack(pady=(18, 10), padx=18)

tk.Label(
    hw_card,
    text="Maintaining this range significantly\nreduces risk of chronic illness.",
    font=("Segoe UI", 11),                  
    bg=CARD_BG, fg=MUTED, justify="center"
).pack(pady=(0, 18), padx=18)

# ── Diet & tips card ───────────────────────────────────────
tips_shadow, tips_card = styled_card(bottom_cols)
tips_shadow.grid(row=0, column=1, sticky="nsew", padx=(14, 0))

# Orange top stripe
tk.Frame(tips_card, bg=ORANGE, height=6).pack(fill="x")

tk.Label(
    tips_card,
    text="  💡  Diet & Health Suggestions",
    font=("Segoe UI", 14, "bold"),          
    bg=CARD_BG, fg=DARK
).pack(anchor="w", padx=18, pady=(14, 4))

tk.Label(
    tips_card,
    text="  Personalised advice based on your BMI result",
    font=("Segoe UI", 11),                  
    bg=CARD_BG, fg=MUTED
).pack(anchor="w", padx=18, pady=(0, 12))

r_tips_lbl = tk.Label(
    tips_card, text="",
    font=("Segoe UI", 12),                  
    bg=CARD_BG, fg=MID,
    justify="left", wraplength=520          
)
r_tips_lbl.pack(anchor="w", padx=18, pady=(0, 22))

# Bottom page padding
tk.Frame(result_inner, bg=ORANGE_LT, height=32).pack()


# ==============================================================
# SECTION 10 :  LAUNCH APPLICATION
# ==============================================================

root.mainloop()

# ==============================================================
#  END OF FILE
# ==============================================================
