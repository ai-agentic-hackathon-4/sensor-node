import RPi.GPIO as GPIO
import time

# ==========================================
# 設定エリア
# ==========================================
PUMP_PIN = 17

# キャリブレーション値 (3秒で170ml出るという実測値)
# 1秒あたり何ml出るかを計算しておきます
FLOW_RATE_PER_SEC = 170.0 / 3.0  # 約 56.67 ml/sec

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PUMP_PIN, GPIO.OUT)
    # 初期状態はOFF (LowトリガーのリレーなのでHIGHでOFF)
    GPIO.output(PUMP_PIN, GPIO.HIGH)

def pour_water(target_ml):
    """指定したml数だけ水を出す関数"""
    
    # 必要な秒数を計算
    duration = target_ml / FLOW_RATE_PER_SEC
    
    print(f"--- 水やり開始 ---")
    print(f"目標: {target_ml}ml")
    print(f"計算上の稼働時間: {duration:.2f}秒")

    # ポンプON (LOW)
    GPIO.output(PUMP_PIN, GPIO.LOW)
    
    # 計算した時間だけ待つ
    time.sleep(duration)

    # ポンプOFF (HIGH)
    GPIO.output(PUMP_PIN, GPIO.HIGH)
    print("--- 完了 ---")

def cleanup():
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        setup()
        
        # ★ここで水量を指定します
        # 例：50ml あげたい場合
        pour_water(50)

    except KeyboardInterrupt:
        print("\n中断")
        # 安全のため緊急停止
        GPIO.output(PUMP_PIN, GPIO.HIGH)
    finally:
        cleanup()
