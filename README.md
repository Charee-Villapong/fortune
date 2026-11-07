# fortune

毎朝届く「今日の占い」PDF の生成まわりです。四柱推命・九星気学・西洋占星術・数秘術・六曜・タロット・血液型を組み合わせて、Claude の VM 側で毎朝生成し、チャットとメールで届けています。

## 構成

- **skill/** — 占いPDFのデザインと生成手順（SKILL.md）
- **output/** — 出力サンプル（fortune-2026-10-31-big.pdf）

マスターは Claude の VM 側にあり、変更はこのリポジトリへプッシュされます。Mac 側は pull で受け取ります。

## SKILL.md の正本と同期

- 正本は実働側 `~/workspace/custom-skills/fortune-pdf-design/SKILL.md` です。このリポジトリの `skill/SKILL.md` は同期コピーで、両者はバイト一致が前提です。
- 同期手順: ①正本を編集する ②正本の内容を `skill/SKILL.md` へコピーする ③`python3 tools/check_skill_sync.py` で一致を確認する ④コミットして push する

## 仕様値チェック

- `python3 tools/check_spec_values.py` で、固定リスト由来のデザイン確定値（55件）が正本 SKILL.md に存在するかを確認します。引数で対象ファイルを指定できます。
- 終了コード: 0=全件存在、1=欠落あり、2=エラー（ファイルなし・引数不正など）。
- 月次棚卸しで、正本の確定値が変わっていないかの確認に使います。
