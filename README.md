# sensor-node

Raspberry Pi カメラで撮影した JPEG 画像を FastAPI で base64 エンコードして返すサンプルです。

## 構成
```
.
├── app
│   ├── api
│   │   └── routes.py       # ルーティングとエンドポイント
│   ├── services
│   │   └── camera.py       # カメラ撮影ロジック
│   └── app.py              # FastAPI アプリ工場関数
├── main.py                 # uvicorn で読み込むエントリポイント
└── README.md
```

## 前提
- Raspberry Pi OS 環境で `rpicam-jpeg` コマンドが利用可能であること
- Python 3.9+ を想定

## セットアップ
```bash
pip install fastapi uvicorn
```

## サーバー起動
スクリプトを用意しています（デフォルトポート 8000）。
```bash
chmod +x scripts/run.sh
./scripts/run.sh
```

または直接 uvicorn を指定しても OK です。
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 画像取得
GET `/image` で最新フレームを取得します。クエリで `width` と `height` を指定可能です（デフォルト 800x600）。

例:
```bash
curl "http://localhost:8000/image?width=800&height=600"
```

レスポンス例:
```json
{
	"width": 800,
	"height": 600,
	"format": "jpeg",
	"data_base64": "...base64..."
}
```

## 参考: 手動撮影コマンド
FastAPI を介さずに撮影する場合の例です。
```bash
rpicam-jpeg -o test.jpg -t 2000 --width 800 --height 600
```