from utils.bond import bond_price

face_value = float(input("Enter Face Value: "))
coupon_rate = float(input("Enter Coupon Rate (%): "))
market_yield = float(input("Enter Market Yield (%): "))
years = int(input("Enter Years to Maturity: "))

price = bond_price(
    face_value,
    coupon_rate,
    market_yield,
    years
)

print("\nBond Price =", price)