---
name: fortune-pdf-design
description: 毎朝の占いPDFのデザインシステム（現行 v2）。案D「クリア・モダン」を基調に、読みやすさとタイポグラフィ階層を担保するレイアウト規則。
---

# Fortune PDF Design System（現行 v2）

このファイルが、毎朝の占いPDFにおける現行 v2 の唯一の仕様である。日次占いは v2 を使う。
テンプレートは日次が `~/workspace/goals/goal-4/hidden_files/fortune-template-v2.html`（平日・休日共通、項目名もトークン）、週間ページは `fortune-template-v2-weekly.html` を正本とし、日付と占い内容だけを差し替える。

## 基本
- フォントは Noto Sans CJK JP。
- 色・文字サイズ・余白の値は「デザイントークン」節の一覧で管理し、本文ではトークンを参照する（トークン化）。場当たり的な値を増やさない。
- 補足テキストも含め、背景に対して十分なコントラスト（目安 4.5:1）を確保する。
- ページ数: 通常 4ページ、月曜は週間1ページを足して 5ページ（cron本文の想定も同じ）。ページ数が増えた場合は文字ではなく余白で調整する（文字を小さくしない）。

## デザイントークン

### カラー

| トークン | 値 | 用途 |
|---|---|---|
| `bg` | #F5F7FA | 背景 |
| `text` | #000000 | 本文（純黒・K2、本体・週間とも） |
| `navy` | #14324A | 見出し／チップ地／名言ブロック地／M3「仕事」バー／T3夜ノード／`.slabel`・`.tl`・`.wt` の色 |
| `accent` | #FF7A1A | アクセント／ヘッダーの星とテーマ／2・3ページ目見出しの下線／アドバイス帯地／`.slabel` の縦バー |
| `label-blue` | #1C7FB8 | ラベル青（補助要素のみ）／M3「今日の天気」バー／T3昼ノード／週バー「軽い・回復」 |
| `header-gray` | #8CA0B0 | ヘッダーのブランド行 |
| `card` | 白 | カード地／ヘッダー背景／2・3ページ目見出しの背景／T3パネル地 |
| `card-shadow` | 0 1px 4px rgba(20,50,74,.10) | カードの影 |
| `quote-author` | #FFB37E | 名言ブロックの著者 |
| `family-green` | #2E8B6E | M3「家族」バー／週バー「特に良い」 |
| `gym-orange` | #E08A2E | M3「ジム運」バー／T3朝ノード／週バー「やや重い」 |
| `caution-red` | #B54434 | M3「今日の注意」バー／週バー「重い週」 |
| `week-normal` | #C9A227 | 週バー「普通」 |
| `rest-purple` | #8E6BC8 | M3「休息と楽しみ」バー |
| `panel-grad-from` | #EAF1F7 | O4パネルのグラデーション開始色 |
| `panel-grad-to` | #FDF0E4 | O4パネルのグラデーション終了色 |
| `panel-border` | #D8E4EE | O4パネルの枠色 |
| `ctxnote-color` | #444444 | `.ctxnote`（命式コンテキスト下の注記）の色 |

### 文字サイズ

| トークン | 値 | 用途 |
|---|---|---|
| `date-size` | 35px | ヘッダーの日付 |
| `body-size` | 16.5px（行間 1.56） | 本文（週間ページも同じ） |
| `mb-size` | 16.2px | 中項目 `.mb` |
| `box-p-size` | 15.9px | 今月/今年 `.box p`（週間ページの `.box p`・表 `td` も同じ） |
| `fb-size` | 15.4px | 流れ `.fb` |
| `wb-size` | 15.1px | 週バー `.wb` |
| `ctxnote-size` | 15.3px | 注記 `.ctxnote` |
| `qn-size` | 16px | 名言ひと言 `.qn` |
| `mt-size` | 15px | 項目名 `.mt` |
| `ft-wt-size` | 14.5px | 流れ見出し `.ft`・週見出し `.wt` |
| `slabel-size` | 14px（太字 900） | 項目タイトル `.slabel` |
| `tl-size` | 11px | 命式タイルの小ラベル `.tl` |

### 余白・形状

| トークン | 値 | 用途 |
|---|---|---|
| `page-margin` | 8mm/9mm（週間は 7mm/9mm） | `@page` マージン |
| `midgrid-gap` | 4px | midgrid の gap |
| `icard-padding` | 3px 9px | icard の padding |
| `overview-padding` | 4px 11px 5px | overview の padding |
| `flow-padding` | 4px 11px 0 | flow の padding |
| `box-padding` | 2px 9px 6px | box の padding |
| `quote-padding` | 13px 15px | quote の padding |
| `slabel-margin` | 6px 0 3px | `.slabel` の margin |
| `slabel-bar` | 6px | `.slabel` 左の縦バー幅（色は `accent`、padding-left 9px） |
| `vbody-padding-bottom` | 1px | vbody の padding-bottom |
| `crow-margin-bottom` | 4px | crow の margin-bottom |
| `card-radius` | 14〜16px | カードの角丸 |
| `panel-radius` | 14px | O4パネルの角丸 |
| `panel-border-width` | 1px | O4パネルの枠幅（色は `panel-border`） |
| `header-rule` | 1px | ヘッダー下の淡い罫線 |
| `section-underline` | 3px | 2・3ページ目見出しの下線（色は `accent`） |
| `m3-bar` | 5px | M3アイコンカード左の色バー幅 |

## デザイン（案D「クリア・モダン」＋H4ヘッダー）
- ベース色: 背景は `bg`、本文は `text`、見出しは `navy`、アクセントは `accent`、ラベル青は `label-blue`
- ヘッダーは H4 型: 帯なしで背景は `card`、ブランド行は `header-gray` の小文字、日付は `date-size` の特大タイポ、星とテーマは `accent`、チップは `navy` 地に白文字、下に `header-rule` の淡い罫線
- 2・3ページ目の見出し: 背景は `card`、下線は `section-underline`（色は `accent`）
- カード: 地は `card`、角丸は `card-radius`、影は `card-shadow`
- 名言ブロック: 地は `navy` に白の明朝、著者は `quote-author`
- アドバイス帯: 地は `accent` に白文字

## 構成
- 1ページ目: ヘッダー（日付・総合★・テーマ・チップ）／①今日の概要（全占いのアンサンブル、約300字）／②中項目×5（各150字まで）／今日の流れ（午前・午後・夜の3コマ）
- 2ページ目: ③四柱推命だけの今日の概要（約300字）／④四柱推命だけの中項目×5
- 3ページ目: ⑤四柱推命の今月の運気（約300字）／⑥四柱推命の今年の運気（約300字）／今月の流れ（週ごと・F4カレンダー帯型）／⑦今日の名言／ラッキーポイント／今日の一言
- 中項目の並び（平日）: 仕事・家族・ジム運・今日の注意・今日の天気。休日は「仕事」を外し、休息・楽しみ系に差し替える
- 四柱推命は通変星を軸にし、表面的な一言コメントで済ませない

## 今月の流れ（F4 カレンダー帯型）
- 週ごとに「色バー（週ラベル＋日付範囲）＋短文」の行で表す。文字サイズは `wb-size`
- バーの色は週の重さで選ぶ: 重い週=`caution-red`、やや重い=`gym-orange`、普通=`week-normal`、軽い・回復=`label-blue`、特に良い=`family-green`
- 週の区切りは暦週（その月の1日を含む週から）。節の切り替わり・冲の日・通変星の山谷を根拠にする

## 今日の名言
- 配置: 3ページ目の ⑦今日の名言として置く。装飾は「デザイン」節の名言ブロックに従い、ひと言のサイズは `qn-size`
- 著者ローテーション: ニーチェ／シオラン／ストア派（セネカ・マルクス・アウレリウス・エピクテトス）／ペシミズム系（ショーペンハウアー等）／吉田松陰／有名な禅僧（一休・道元・良寛・白隠など）の6系統から日替わりで選ぶ
- 実在の有名な言葉のみ。出典（著作名）を併記し、その日の運勢に結ぶ短いひと言を添える。出典が曖昧なものは使わない

## コンポーネント
- 中項目は M3 アイコンカードで ②④共通: 地は `card`＋左に `m3-bar` の色バー＋丸アイコン（一文字）。対応: 仕事=仕/`navy`、家族=家/`family-green`、ジム運=筋/`gym-orange`、今日の注意=注/`caution-red`、今日の天気=天/`label-blue`、休息と楽しみ=休/`rest-purple`
- 大項目（①③の概要と⑤⑥の箱）は O4 色パネル: 淡いグラデーション（`panel-grad-from`→`panel-grad-to`）＋`panel-border-width` 枠（色は `panel-border`）＋角丸 `panel-radius`
- 今日の流れは T3 縦フロー: 地は `card` のパネル内に丸ノード（朝=`gym-orange`／昼=`label-blue`／夜=`navy`）＋↓で連結
- 2ページ目下部に「命式コンテキスト」4タイル（日干／大運／今月／今日）を置く

## 項目タイトル等の可読性（A案）
- `.slabel`（項目タイトル）: サイズは `slabel-size`、色は `navy`、左に `slabel-bar`（色は `accent`）。週間ページの `.slabel` も同じ
- `.tl`（命式タイルの小ラベル）: サイズは `tl-size`、色は `navy`
- `.wt`（週カードのタイトル）: サイズは `ft-wt-size`、色は `navy`
- `.ctxnote`（命式コンテキスト下の注記）: サイズは `ctxnote-size`、色は `ctxnote-color`
