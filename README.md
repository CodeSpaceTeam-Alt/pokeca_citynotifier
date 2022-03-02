# City League Notifier

ポケモンカードゲームにおけるシティリーグのキャンセル待ち補助ツール  
Linuxで動作確認

## Install
```
$ python setup.py sdist
$ pip install dist/*.tar.gz
```

## Usage

```
usage: util.py [-h] [--token TOKEN] [-v] [-c CONFIG] [--ev_list]

City League Notifier

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN         LINE token to notify
  -c CONFIG, --config CONFIG
  -v, --version         show version
  --ev_list             get event list
```

## Configuration

|項目       | 設定箇所        |設定内容|
|:---:      | :---:           |:---:   |
|Line Token | --token <XXX>   | [LINE Notify Bot](https://notify-bot.line.me/ja/)で通知するためのToken | 
|driver_fn  | JSONファイル内  | [Chromium Driver](https://chromedriver.chromium.org/downloads) のファイルパス | 
|log_fn     | JSONファイル内  | 前回情報の保存用ファイルパス | 
|city_url   | JSONファイル　  | [ポケモンカードゲームプレイヤークラブ](https://event.pokemon-card.com/events/) のイベントサイトURL (例: https://event.pokemon-card.com/events/1203) | 
|tournament_filter   | JSONファイル　  | シティリーグの情報フィルター(*1)|  


(*1) シティリーグの情報フィルターについては、以下を「完全一致」で指定可能です。  

```text
{
    "都道府県": "例：東京都",
    "店舗": "例：東京都",
    "日付": "例：2022年02月23日(水)",
    "時間": "例：12:00",
    "ステータス": "例：エントリー",}})
}
```
