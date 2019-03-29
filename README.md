# tbls-util

## 作成の事前準備
- tblsのinstall
`go get github.com/k1low/tbls`
- direnvのinstall(Mac)
`brew install direnv`

## 接続情報の設定
.envrcを作成する

```bash
cat .envrc
export MYSQL_USER=username
export MYSQL_PASSWORD=password
export MYSQL_DATABASE=dbname
export MYSQL_HOST=localhost
```

## 作成 or 更新
```bash
make doc
```

## コメントの付与
```yaml
comments:
    -
        table:         test_table
        tableComment:  テストテーブル
        columnComments:
            test_column: 項目名テスト
```

- tableComment: テーブル名
- columnComments: 項目名
- [参考: tbls](https://github.com/k1LoW/tbls)

## リレーションの付与
```yaml
relations:
    -
        table:         test_table
        columns:
            - test_column
        parentTable:   test_parent_table
        parentColumns:
            - test_column
        def:           test_table->test_parent_table
```
- columns: 項目
- parentTable: 親テーブル
- parentColumns: 親テーブルの項目
- def: リレーション

## 差分チェック
```bash
make diff
```

## コメント・リレーションlint
```bash
make lint
cat lint_result
```

## 列名表記ゆれチェック
```bash
meke dupcheck
cat duplicate_column_comments.yml
```

## 列名・テーブル名補完
```bash
make completion
grep "###" comments.yml
```

- 列名コメントが不足している場合、既存の列名コメントを使用して補完する
- 既存の列名コメントがない場合は'###'が挿入されるので、変更する
- テーブル名コメントがない場合は'###'が挿入されるので、変更する
