import matplotlib.pyplot as plt

from utils.bond import bond_price

face_value = 1000
coupon_rate = 8
years = 10

yields = []
prices = []

for y in range(1, 21):

    price = bond_price(
        face_value,
        coupon_rate,
        y,
        years
    )

    yields.append(y)
    prices.append(price)

plt.figure(figsize=(8,5))

plt.plot(
    yields,
    prices,
    marker='o'
)

plt.title("Bond Price vs Yield")
plt.xlabel("Yield (%)")
plt.ylabel("Bond Price")

plt.grid(True)

plt.show()