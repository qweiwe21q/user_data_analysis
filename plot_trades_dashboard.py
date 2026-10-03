import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timezone, timedelta
import pandas as pd

# 设置中文字体（避免中文乱码，Mac 适用）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

down_color = 'green'
up_color = 'red'

def plot_trades_dashboard(trades):
    if not trades:
        print("没有交易数据可供画图")
        return

    # 1. 整理数据为 Pandas DataFrame 并按时间正序排列（从早到晚）
    data = []
    for t in trades:
        ts = t.get("timestamp")
        dt = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(timezone(timedelta(hours=8)))
        data.append({
            "Time": dt,
            "Price": float(t.get("price") or 0),
            "Size": float(t.get("size") or 0),
            "Outcome": t.get("outcome"),
            "Side": t.get("side")
        })

    df = pd.DataFrame(data)
    df = df.sort_values("Time").reset_index(drop=True)

    # 2. 计算累计持仓量 (Cumulative Size)
    df['Up_Size'] = df.apply(lambda row: row['Size'] if row['Outcome'] == 'Up' else 0, axis=1)
    df['Down_Size'] = df.apply(lambda row: row['Size'] if row['Outcome'] == 'Down' else 0, axis=1)

    df['Cum_Up_Size'] = df['Up_Size'].cumsum()
    df['Cum_Down_Size'] = df['Down_Size'].cumsum()

    # 3. 创建双子图画布
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    fig.suptitle('Polymarket 交易与持仓可视化面板', fontsize=16, fontweight='bold')

    # --- 子图 1：成交价格与买入点位 ---
    up_trades = df[df['Outcome'] == 'Up']
    down_trades = df[df['Outcome'] == 'Down']

    # 画出价格折线趋势
    ax1.plot(df['Time'], df['Price'], color='gray', linestyle='--', alpha=0.5, label='成交价轨迹')

    # 标注 Up 买入点（绿点/绿色三角）
    ax1.scatter(up_trades['Time'], up_trades['Price'], color=up_color, s=up_trades['Size'] * 3,
                alpha=0.7, label='BUY Up (点大小代表数量)', marker='^')

    # 标注 Down 买入点（红点/红色三角）
    ax1.scatter(down_trades['Time'], down_trades['Price'], color=down_color, s=down_trades['Size'] * 3,
                alpha=0.7, label='BUY Down (点大小代表数量)', marker='v')

    ax1.set_ylabel('成交价格 ($)', fontsize=12)
    ax1.set_title('交易价格与分布点位', fontsize=13)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper left')

    # --- 子图 2：Up / Down 累计持仓变化 ---
    ax2.plot(df['Time'], df['Cum_Up_Size'], color=up_color, linewidth=2, label='Up 累计持仓数量')
    ax2.plot(df['Time'], df['Cum_Down_Size'], color=down_color, linewidth=2, label='Down 累计持仓数量')

    ax2.set_xlabel('时间 (北京时间)', fontsize=12)
    ax2.set_ylabel('累计持仓数量 (Shares)', fontsize=12)
    ax2.set_title('累计持仓演变过程', fontsize=13)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper left')

    # 4. 优化 X 轴时间格式显示
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=30)
    plt.tight_layout()

    # 展示图表
    plt.show()


# ==================== 调用方式 ====================
# 在你原有代码的最后加上这行：
