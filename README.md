# smart-lock
スマートロックシステム用のリポジトリ

# APIについて
アクセスキーと、利用するAPIに関する情報をヘッダーに書き込む。
## セサミ一覧 - GET /sesames
アカウントにリンクされている Sesame の情報が JSON 形式で返ってくる。  

### リクエスト
```
curl -H "Authorization: YOUR_AUTH_TOKEN" \
  https://api.candyhouse.co/public/sesames
```

### レスポンス

```
[
    {
      "device_id": "00000000-0000-0000-0000-000000000000",
      "serial": "ABC1234567",
      "nickname": "Front door"
    },
    {
      "device_id": "00000000-0000-0000-0000-000000000001",
      "serial": "DEF7654321",
      "nickname": "Back door"
    }
  ]
```

## セサミの状態 - GET /sesame/{device_id}
GET /sesames からも分かるセサミそれぞれに割り当てられている device_id を使って、鍵がロックされているか否かを返す。  
### リクエスト
```zsh
$ curl -H "Authorization: YOUR_AUTH_TOKEN" \
  https://api.candyhouse.co/public/sesame/00000000-0000-0000-0000-000000000001
```
/sesamesではなく/sesameであることに注意

## セサミの制御 - POST /sesame/{device_id}
Body に command プロパティを渡してそのコマンドの操作を、 URI で指定した device id のセサミに対して行う。

### Body
以下のコマンドがある.
- lock
- unlock
- sync  
syncはサーバー側にある情報と同期するようにする。ただしバッテリーの持ちが悪くなるらしいのであまり使わない方が得策かもしれない。

### result
タスクidが返ってくる
### リクエスト

```zsh
curl -H "Authorization: YOUR_AUTH_TOKEN" \
    -H "Content-Type: application/json" \
    -X POST -d '{"command":"lock"}' \
    https://api.candyhouse.co/public/sesame/00000000-0000-0000-0000-000000000001
```

### レスポンス
```
  {
    "task_id": "01234567-890a-bcde-f012-34567890abcd"
  }
```

## 捜査結果の問合せ - GET /action-result?task_id={task_id}
### リクエスト
```
curl -H "Authorization: YOUR_AUTH_TOKEN" \
    https://api.candyhouse.co/public/action-result?task_id=01234567-890a-bcde-f012-34567890abcd
```
### レスポンス
```
 {
    "task_id": "01234567-890a-bcde-f012-34567890abcd",
    "status": "terminated",
    "successful": true
  }
```
