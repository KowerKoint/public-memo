# Catppuccin
有名カラースキーマ。最近の自分はかなりこれにハマっていて統一している。
GitHubで[スクショ](https://github.com/catppuccin/nvim)を見ると早いが、以下の4種類がある。

- Latte: ライトテーマ
- Frappe: 淡いダークテーマ
- Macchiato: 中くらいのダークテーマ
- Mocha: 高コントラストではっきりしたダークテーマ

このドキュメントも、CatppuccinのFrappeと同じカラースキームのCSSを用いている。(mkdocs用のテーマは公式には配布されていないので非公式だが…)

GitHubの[catppuccin Organization](https://github.com/catppuccin) を見ると、かなり多くのアプリケーション用のテーマが置かれている。

!!! note
    個人的には、catppuccin-frappeがかなり好みだが、最近なにもかもがこの色になると多様性がないと言うか、面白みがないような気もする。カラースキーマの統一は一長一短。

## Alacritty
[GitHub](https://github.com/catppuccin/alacritty)の通りに設定

## Neovim
[このプラグイン](https://github.com/catppuccin/nvim) を入れる。後で追記。

## Waybar
[このCSS](https://github.com/catppuccin/waybar) を入れる。後で追記。

## Zellij
[ここ](https://github.com/catppuccin/zellij) にある `catpuccin.kdl` を `~/.config/zellij/` に配置して、
```fish
zellij options --theme catpuccin-frappe
```

## Zenブラウザ
これはちょっとややこしい。

まず、`about:profiles` からプロファイルのRoot Directoryを知る (例: `~/.config/zen/<なんとか>.Default Profile`)。その中に `chrome/` ディレクトリを作る (すでにあるかも)。

[公式リポジトリ](https://github.com/catppuccin/zen-browser) にあるのだが、どうも最近のZenに追従できてなさそうなので[フォーク](https://github.com/code-irisnk/catppuccin-zen-browser/tree/main) のものを使った。これは状況によるかも。

`themes/Frappe/Blue/` などの場所にある3つのファイルを、先程の `chrome/` ディレクトリに置く。

`about:config` から、`toolkit.legacyUserProfileCustomizations.stylesheets` を有効化する。

補足:

- CSSインジェクションに注意です！結構なんでもされうるので一応脆弱性チェックしておくといいかも。
- CSS全体が `@media (prefers-color-scheme: dark)` で条件付けられている。
システムがダークテーマでそれがZenに伝わっていればいいだが、自分のniri環境ではそうはならななかったので、**うまくいかないときはここを `@media all` に変えよう！**
