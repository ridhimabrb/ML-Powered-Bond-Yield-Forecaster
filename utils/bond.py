def bond_price(face_value, coupon_rate, market_yield, years):

    coupon = face_value * coupon_rate / 100

    price = 0

    for t in range(1, years + 1):
        price += coupon / ((1 + market_yield / 100) ** t)

    price += face_value / ((1 + market_yield / 100) ** years)

    return round(price, 2)