import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

# ★キャリブレーション値（※環境に合わせて書き換えてください）
# 乾燥しているほど値が大きい(High=Dry)前提の設定です
DRY_VAL = 16700  # 空気中の値 (0%)
WET_VAL = 4300   # 水中の値 (100%)

def get_moisture_percent(value):
    # 値が範囲を超えた場合の補正
    if value > DRY_VAL: value = DRY_VAL
    if value < WET_VAL: value = WET_VAL

    # パーセント計算 (線形変換)
    # 値が小さいほど濡れている(100%)計算
    span = DRY_VAL - WET_VAL
    percent = 100 * (DRY_VAL - value) / span
    return percent

print(f"水分率計測中... (Dry:{DRY_VAL} -> Wet:{WET_VAL})")

try:
    while True:
        raw_val = adc.read_adc(0, gain=GAIN)
        moisture = get_moisture_percent(raw_val)

        # グラフ風に表示
        bar_len = int(moisture / 5)
        bar = "#" * bar_len + "-" * (20 - bar_len)

        print(f"値: {raw_val:<5} | 水分量: {moisture:>3.0f}% [{bar}]")
        time.sleep(1)

except KeyboardInterrupt:
    print("終了")