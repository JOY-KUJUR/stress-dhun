import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ================= USER INPUT =================
print("\n🧠 Daily Stress Analyzer\n")

rest = float(input("Hours of Rest/Sleep 💤: "))
study = float(input("Hours of Study 📚: "))
game = float(input("Hours of Games 🎮: "))
other = float(input("Hours of Other Activities 🧩: "))

# ================= STRESS CALCULATION =================
stress = 0

stress += study * 7          # study adds stress
stress += game * 3           # games add little stress
stress += other * 4          # neutral
stress -= rest * 8           # rest reduces stress

# Clamp value
stress = max(0, min(100, stress))

# ================= STRESS LEVEL =================
if stress < 30:
    level = "Low Stress 😌"
elif stress < 60:
    level = "Moderate Stress 😐"
else:
    level = "High Stress 😖"

print(f"\n📊 Stress Score: {stress:.1f}/100")
print(f"🧠 Stress Level: {level}")

# ================= AI RECOMMENDATION =================
print("\n🤖 AI Recommendation:")

if stress >= 60:
    print("- Reduce study load slightly")
    print("- Increase sleep/rest by 1–2 hours")
    print("- Light walk or music recommended")
elif stress >= 30:
    print("- Maintain balance")
    print("- Avoid long gaming sessions")
    print("- Short breaks during study")
else:
    print("- You're doing great!")
    print("- Maintain this routine")

# ================= SAVE DATA =================
data = {
    "Date": datetime.now().strftime("%Y-%m-%d"),
    "Rest": rest,
    "Study": study,
    "Game": game,
    "Other": other,
    "Stress": stress
}

df = pd.DataFrame([data])

try:
    old = pd.read_csv("stress_data.csv")
    df = pd.concat([old, df], ignore_index=True)
except FileNotFoundError:
    pass

df.to_csv("stress_data.csv", index=False)

print("\n💾 Data saved successfully")

# ================= GRAPH =================
plt.figure(figsize=(8, 5))
plt.plot(df["Date"], df["Stress"], marker='o')
plt.title("Stress Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Stress Level")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
