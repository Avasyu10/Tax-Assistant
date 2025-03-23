def calculate_capital_gains(asset_type, buy_price, sell_price, quantity, holding_period):
    total_short_term_stocks = 0
    total_long_term_stocks = 0
    total_crypto_gains = 0
    exemption_limit = 100000  # Exemption for LTCG on stocks (Section 112A)

    profit = (sell_price - buy_price) * quantity

    if asset_type == "stocks":
        if holding_period <= 365:
            total_short_term_stocks += profit
        else:
            total_long_term_stocks += profit
    elif asset_type == "crypto":
        total_crypto_gains += profit  # All crypto gains are taxed at 30%

    # Tax calculations
    stcg_stocks_tax = total_short_term_stocks * 0.15  # STCG for stocks at 15%
    ltcg_stocks_tax = max(0, (total_long_term_stocks - exemption_limit) * 0.10)  # LTCG after ₹1,00,000 exemption
    crypto_tax = total_crypto_gains * 0.30  # Crypto tax at 30% flat

    return {
        "short_term_gains_stocks": total_short_term_stocks,
        "long_term_gains_stocks": total_long_term_stocks,
        "crypto_gains": total_crypto_gains,
        "stcg_stocks_tax": stcg_stocks_tax,
        "ltcg_stocks_tax": ltcg_stocks_tax,
        "crypto_tax": crypto_tax
    }

