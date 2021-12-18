# Misskey Updater Bot
MisskeyなどのFediverse系SNS経由でインスタンスのMisskeyをアップデートできます。

# 設定
`bot.py` があるディレクトリに `config.py` を作成します。

以下のように記述してください。

```python
MISSKEY_INSTANCE='YOUR_INSTANCE_DOMAIN_HERE'
MISSKEY_TOKEN='bOtT0keninY0uR1nstanCeHERe'
MISSKEY_DIR='/path/to/misskey'

UPDATE_SCRIPT_PATH='/path/to/misskey/update.sh'
RESTART_SCRIPT_PATH='/path/to/misskey/restart.sh' # if needed (optional, nullable)

ALLOWED_USERS = [
    'xxxxxxxxxxxx' # Your Account IDs here... (separate with ',')
]
```

|項目名|説明|
|------|------|
|MISSKEY_INSTANCE|インスタンスのへのホスト名|
|MISSKEY_TOKEN|ボットアカウントのトークン|
|MISSKEY_DIR|Misskeyソフトウェアが配置されているディレクトリ ※1|
|UPDATE_SCRIPT_PATH|アップデートスクリプトへの絶対パス ※1|
|RESTART_SCRIPT_PATH|再起動スクリプトへの絶対パス（任意。空にできます）|
|ALLOWED_USERS|操作できるユーザーのIDリスト(`,`で区切る)|
※1: スクリプトの実行時、作業ディレクトリは`MISSKEY_DIR`になります

# 使い方

`@ボットへのメンション v(バージョン番号)にアップデートして` と話しかけると「アップデートやっとく」と返信します。
完了時は再度返信「アップデートできたよ　（実行時間: XX分XX秒...」にてお知らせします。
アップデートできなかった場合は「アップデートできなかった」「アップデートできなかった(終了コード)」と返信してきます。
※終了コードはアップデートスクリプトが返してきたものになります。

