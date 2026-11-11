# WezTerm

マルチプレクサ機能を持ったゴリゴリカスタマイザブルターミナルアプリ…なのだが、自分はZellijを基本的に使うのであまり使いこなせていない。Alacrittyでいいのだが、macOSのFn+Contrl+←のようなウィンドウメニューショートカットがなぜか使えない ([PR #9092に期待](https://github.com/alacritty/alacritty/pull/9092 に期待)) のでとりあえずこっちを使う。

## タブバー非表示
Zellijを使うのでWezTerm側のタブバー表示は邪魔。以下を `~/.wezterm.lua` に書いて消す。

```lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()

config.enable_tab_bar = false

return config
```
