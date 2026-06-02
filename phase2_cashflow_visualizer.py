import pandas as pd
import matplotlib.pyplot as plt

face_value = 1000
coupon_rate = 8
market_yield = 10
years = 5

coupon = face_value * coupon_rate / 100

cashflows = []
present_values = []

for t in range(1, years + 1):

    if t == years:
        cashflow = coupon + face_value
    else:
        cashflow = coupon

    pv = cashflow / ((1 + market_yield / 100) ** t)

    cashflows.append(cashflow)
    present_values.append(pv)

df = pd.DataFrame({
    "Year": range(1, years + 1),
    "Cashflow": cashflows,
    "Present Value": present_values
})

print(df)

plt.figure(figsize=(8,5))
plt.bar(df["Year"], df["Present Value"])

plt.title("Present Value of Bond Cashflows")
plt.xlabel("Year")
plt.ylabel("Present Value")

plt.show()