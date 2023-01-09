# Misskey Updater Bot
MisskeyなどのFediverse系SNS経由でインスタンスのMisskeyをアップデートできます。

# 要件
Python 3.7以降<br>
必須パッケージ: `websockets` v9.0, `Misskey.py` v4.0.1, `aiohttp` v3.7.4.post0<br>
※ `pip install -U -r requirements.txt` で一括インストールできます

その他**アップデートスクリプトが必要**です。

# 設定
`bot.py` があるディレクトリに `config.py` を作成します。

以下のように記述してください。

```python
MISSKEY_INSTANCE='YOUR_INSTANCE_DOMAIN_HERE'
MISSKEY_TOKEN='bOtT0keninY0uR1nstanCeHERe'
MISSKEY_DIR='/path/to/misskey'

GITHUB_RESPOSITORY_NAME='misskey-dev/misskey'

UPDATE_SCRIPT_PATH='/path/to/misskey/update.sh'
RESTART_SCRIPT_PATH='/path/to/misskey/restart.sh' # if needed (optional, nullable)

ALLOWED_USERS = [
    'xxxxxxxxxxxx', 'yyyyyyyyyyyyy' # Your Account IDs here... (separate with ',')
]
```

|項目名|説明|
|------|------|
|MISSKEY_INSTANCE|インスタンスのホスト名 ※1|
|MISSKEY_TOKEN|ボットアカウントのトークン|
|MISSKEY_DIR|Misskeyソフトウェアが配置されているディレクトリ|
|GITHUB_REPOSITORY_NAME|バージョンチェックに使用するGitHubリポジトリ (`ユーザー(またはOrg)名/リポジトリ名` の形式で記述)|
|UPDATE_SCRIPT_PATH|アップデートスクリプトへの絶対パス ※2|
|RESTART_SCRIPT_PATH|再起動スクリプトへの絶対パス（任意。空にできます） ※2|
|ALLOWED_USERS|操作できるユーザーのIDリスト(Python配列形式)。**ボットを動作させるインスタンスから見たユーザーIDでなければならない**|

※1: ローカルで動かす場合は `localhost:3000` という風に指定しても大丈夫です。<br>
※2: スクリプトの実行時、作業ディレクトリは`MISSKEY_DIR`になります

# メモ

## アップデートスクリプトの引数について
ボットは、アップデートスクリプトを実行する際にユーザーが指定したバージョン番号を引数として渡します。<br>
自動化の際に役立ちます。（この引数への対応は任意です）

`/path/to/misskey/update.sh 12.xxx.xx`

## バージョンチェックについて
ボットは、ユーザーが指定したバージョンが存在するかを確認しますが、確認先は[本家Misskeyのリポジトリ](https://github.com/misskey-dev/misskey)です。<br>
他の方のカスタマイズ版を使用している場合は設定の `GITHUB_REPOSITORY_PATH` を変更してください。<br>
ただし、リリースが行われていることが前提となっています。

# 使い方

`@ボットへのメンション v(バージョン番号)にアップデートして` と話しかけると「アップデートやっとく」と返信します。<br>
`最新にアップデートして` `最新バージョンにアップデートして` にすると自動で最新のものを選択します。

完了時は再度返信「アップデートできたよ　（実行時間: XX分XX秒...」にてお知らせします。<br>
アップデート正常終了後、30秒後に再起動スクリプトを実行します。

アップデートできなかった場合は「アップデートできなかった」「アップデートできなかった(終了コード)」と返信してきます。

※終了コードはアップデートスクリプトが返してきたものになります。

# ライセンス
MIT License<br>
(c)CyberRex