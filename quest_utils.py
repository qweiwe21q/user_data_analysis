
from datetime import datetime, timezone, timedelta
import requests
from tabulate import tabulate
from collections import defaultdict
from plot_trades_dashboard import plot_trades_dashboard

my_market = "0x322999d026d39aa1a4a458f0268c1e8620a6b6ccb10e9efdfdbed43a93b0b4f7"
def get_user_trades(user_address: str, limit=100, offset=0,market = my_market):
    url = "https://data-api.polymarket.com/trades"
    params = {
        "user": user_address.lower(),
        "limit": limit,
        "offset": offset,
        "side": "BUY",          # 可选
        "market": market,          # 可选
        # "start": 1710000000,    # 可选
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def summarize_yes_no(trades):
    stats = defaultdict(lambda: {"size": 0.0, "cost": 0.0})

    for t in trades:
        outcome = t.get("outcome") or "Unknown"
        size = float(t.get("size") or 0)
        price = float(t.get("price") or 0)
        side = t.get("side")

        # 只统计买入（你目前数据都是 BUY）
        if side == "BUY":
            stats[outcome]["size"] += size
            stats[outcome]["cost"] += size * price
        elif side == "SELL":
            # 如果有卖出，可以按需减去
            stats[outcome]["size"] -= size
            stats[outcome]["cost"] -= size * price

    print("\n===== 持仓汇总 =====")
    for outcome, data in stats.items():
        avg_price = data["cost"] / data["size"] if data["size"] != 0 else 0
        print(f"{outcome:6} | 数量: {data['size']:.2f} | 成本: {data['cost']:.2f} | 均价: {avg_price:.4f}")

def print_trades_table(trades):
    rows = []
    for t in trades:
        ts = t.get("timestamp")
        # 转成北京时间
        dt = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(timezone(timedelta(hours=8)))
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")

        rows.append([
            time_str,
            t.get("side"),
            t.get("size"),
            t.get("price"),
            (t.get("size") * t.get("price")),
            t.get("outcome"),  # Yes / No 或 Up / Down
            t.get("title"),
        ])

    headers = ["Time", "Side", "Size", "Price", "total_price", "Outcome", "Market"]
    # headers = ["时间", "方向", "数量", "价格", "结果", "市场"],
    print(tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".4f"))

import requests

def get_market_resolution(condition_id: str = None, slug: str = None):
    """获取市场最终结果"""
    if slug:
        url = f"https://gamma-api.polymarket.com/markets?slug={slug}&closed=true"
    elif condition_id:
        url = f"https://gamma-api.polymarket.com/markets?condition_ids={condition_id}&closed=true"
    else:
        raise ValueError("需要 condition_id 或 slug")

    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if not data:
        return None

    market = data[0] if isinstance(data, list) else data

    # 关键字段
    closed = market.get("closed")          # 是否已关闭/结算
    resolved = market.get("resolved")      # 有些版本有这个字段
    outcome_prices = market.get("outcomePrices")  # 结算后会是 ["1","0"] 或 ["0","1"]
    outcomes = market.get("outcomes")      # ["Up","Down"] 或 ["Yes","No"]

    return {
        "closed": closed,
        "outcomes": outcomes,
        "outcomePrices": outcome_prices,
        "title": market.get("question") or market.get("title"),
    }


# 使用
info = get_market_resolution(my_market)
is_up = None

if info and info["closed"]:
    prices = eval(info["outcomePrices"]) if isinstance(info["outcomePrices"], str) else info["outcomePrices"]
    outcomes = eval(info["outcomes"]) if isinstance(info["outcomes"], str) else info["outcomes"]

    if prices[0] == "1":
        print(f"最终结果：{is_up}", outcomes[0], "赢了")
        is_up = True
    elif prices[1] == "1":
        is_up = False
        print(f"最终结果：{is_up}", outcomes[1], "赢了")
    else:
        print("还未完全结算或特殊结果")
else:
    print("市场还没结算")

# trades = get_user_trades("0xce25e214d5cfe4f459cf67f08df581885aae7fdc")
trades = get_user_trades("0x3048d65321be3497164cdfc2996f94f98a2e7537")
# trades = get_user_trades("0xccc4e132674619c6faccfeb4e05d6173088f9267")
print_trades_table(trades)
summarize_yes_no(trades)

plot_trades_dashboard(trades)
