# WezTerm

マルチプレクサ機能を持ったゴリゴリカスタマイザブルターミナルアプリ…なのだが、自分はZellijを基本的に使うのであまり使いこなせていない。Alacrittyでいいのだが、macOSのFn+Contrl+←のようなウィンドウメニューショートカットがなぜか使えない ([PR #9092に期待](https://github.com/alacritty/alacritty/pull/9092 に期待)) のでとりあえずこっちを使う。

## コンフィグ
`~/.config/wezterm.lua` に書く。 `~/.wezterm.lua` でもいいけど `~/.config/` にあってほしいので。


```lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()

-- ここで `config` をいじる

return config
```

## タブバー非表示
Zellijを使うのでWezTerm側のタブバー表示は邪魔。

```lua
config.enable_tab_bar = false
```

普通に2重にタブ使うメリットあるので表示しててもいいかもという説もある。

## フォント
```lua
config.font = wezterm.font 'UDEV Gothic NFRG'
```
[リストを与えてfallback](https://wezterm.org/config/fonts.html)もできるっぽい。

## macOSのIMEにCtrlを渡す
IMEの Ctrl+I (カタカナ) や Ctrl+T (半角英数) などを使いたいのに、IMEに渡らずにターミナルで止められてしまうので以下で変更

```lua
config.macos_forward_to_ime_modifier_mask = 'SHIFT|CTRL'
```
