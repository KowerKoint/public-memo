# Neovim

## 設定の方針

- Luaを使う
- IDEに比べて不便だとは思わないようにしたいが、IDE同然なものにはしない (Vimだからこその手軽さを大事にする)
- いわゆる「盆栽」と言えるほどのオリジナリティ高いconfigにせず、1年ぶりに見るようなことになっても理解できる範囲に留める
- keymapもあまり味を出さない (デフォルトのkeymapはよく考えられていて、他のものとも被りにくいのでできるだけその考え方を引き継ぐ)
    - オリジナルのやつは基本的に `<leader>` を噛ませる

## 構造

`~/.config/nvim/` 以下に以下のようなツリーを作る

```
.
├── init.lua
└── lua
    ├── keymaps.lua
    ├── lazy_nvim.lua
    ├── options.lua
    └── plugins
        └── commentary.lua
        └── ...
```

## 基本ファイルたち

`init.lua` は、単に `keymaps` `options` `lazy_nvim` をロード

```lua
require("options")
require('keymaps')
require("lazy_nvim")
```

`options.lua`

```lua
-- netrwを無効化 (ファイルエクスプローラーは別のプラグインを用意する)
vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

local options = {
  -- 表示
  title = true,
  number = true,

  -- 挙動
  wildmode = { "longest", "full" },
  mouse = "nv",
  smartindent = true,

  -- コーディングスタイル
  expandtab = true,
  shiftwidth = 2,
  softtabstop = 2,
  encoding = "utf-8",
  fileencodings = { "utf-8", "cp932" },
  
  -- .nvim.lua の読み取り
  exrc = true;
}

for k, v in pairs(options) do
    vim.opt[k] = v
end

-- LSPなどで表示されるエラーや警告の内容
vim.diagnostic.config({
  virtual_text = true,
})
```

`keymaps.lua` は以下。 `mapleader` は `lazy.nvim` を読み込むより前に設定しないとプラグインのconfigに反映されない。

```lua
vim.keymap.set('i', 'jj', '<Esc>', { noremap = true })
vim.keymap.set('n', 'x', '"_x', { noremap = true })
vim.keymap.set('t', '<Esc>', '<C-\\><C-n>', { noremap = true })
vim.keymap.set('n', 'ge', vim.diagnostic.open_float)

vim.g.mapleader = " "
vim.g.maplocalleader = "\\"
```

`lazy_nvim.lua` は [https://lazy.folke.io/installation](https://lazy.folke.io/installation) を使う。

`lua/plugins/` 以下にspecを置いていけば自動でプラグインがロードされる。シンプルでいい。

以前は `defaults` に  `lazy = true` を入れていたが、プラグイン追加のたびにイベントを考えるのが億劫なので やめた。とはいえ起動時間は大切にしたい。

```lua
-- Bootstrap lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local lazyrepo = "https://github.com/folke/lazy.nvim.git"
  local out = vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath })
  if vim.v.shell_error ~= 0 then
    vim.api.nvim_echo({
      { "Failed to clone lazy.nvim:\n", "ErrorMsg" },
      { out, "WarningMsg" },
      { "\nPress any key to exit..." },
    }, true, {})
    vim.fn.getchar()
    os.exit(1)
  end
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  spec = {
    { import = "plugins" },
  },
  -- automatically check for plugin updates
  checker = { enable = true };
})
```

## プラグイン

### Comment.nvim

`gcc` で行コメント、 `gc` でコメントトグルのoperator
`commentstring` という標準機能はあるものの実装がプラグイン依存になっているので必要

```lua
return {
  'numToStr/Comment.nvim',
}
```

### catppuccin

カラーテーマ。以前はtokyonightを使っていたが、ダーク系が好きでももっとかわいいのがいいのでcatppuccin-frappeを使ってみる

```lua
return {
  "catppuccin/nvim",
  name = "catppuccin",
  config = function()
    vim.cmd.colorscheme 'catppuccin-frappe'
  end,
}
```

### lualine

ステータスバー。個性はないが、これでいい感がある。表示がファイル名だけなのは嫌なので `path = 1` でカレントディレクトリからの相対パスに。

```lua
return {
  'nvim-lualine/lualine.nvim',
  opts = {
    options = {
      path = 1,
    }
  },
}
```

### fzf.lua

無限の可能性を秘めたプラグイン。これがないとデカいリポジトリの編集はさすがに捗らない。

`fzf` コマンドが使える必要があり、 `ripgrep` , `fd` が入ってるともっと高速になるし、 `bat` が入ってるとハイライトがよくなる。

定期的にここに帰ってきて深みを追求したい。

キーバインドは他のプラグインと混ざらないように `<leader>f` 始まりにした。

```lua
return {
  "ibhagwan/fzf-lua",
  dependencies = { "nvim-tree/nvim-web-devicons" },
  config = function()
    require('fzf-lua').setup{}
    vim.keymap.set('n', '<leader>ff', function()
      require('fzf-lua').files()
    end)
    vim.keymap.set('n', '<leader>fo', function()
      require('fzf-lua').oldfiles()
    end)
    vim.keymap.set('n', '<leader>fb', function()
      require('fzf-lua').buffers()
    end)
    vim.keymap.set('n', '<leader>fg', function()
      require('fzf-lua').grep()
    end)
    vim.keymap.set('v', '<leader>fg', function()
      require('fzf-lua').grep_visual()
    end)
    vim.keymap.set('n', '<leader>fw', function()
      require('fzf-lua').grep_cword()
    end)
    vim.keymap.set('n', '<leader>fW', function()
      require('fzf-lua').grep_cWORD()
    end)
    vim.keymap.set('n', '<leader>fF', function()
      require('fzf-lua').git_files()
    end)
    vim.keymap.set('n', '<leader>fs', function()
      require('fzf-lua').git_status()
    end)
    vim.keymap.set('n', '<leader>fd', function()
      require('fzf-lua').git_diff()
    end)
    vim.keymap.set('n', '<leader>fr', function()
      require('fzf-lua').lsp_references()
    end)
    vim.keymap.set('n', '<leader>fk', function()
      require('fzf-lua').keymaps()
    end)
    vim.keymap.set('n', '<leader>fc', function()
      require('fzf-lua').command_history()
    end)
  end
}
```

### nvim-tree

ファイルツリー表示のプラグイン。シングルファイルメインのシンプルなタスクなら `:e` で直接開いちゃうし、複雑でも `fzf.lua` で探しに行くほうが早いがちなので、これはWeb系アプリ開発のときなどに見やすくする用。

```lua
return {
  'nvim-tree/nvim-tree.lua',
  dependencies = {
    'nvim-tree/nvim-web-devicons',
  },
  config = function()
    require('nvim-tree').setup{}
    vim.keymap.set('n', '<leader>t', function()
      require('nvim-tree.api').tree.toggle()
    end)
  end,
}
```

### blink.cmp

補完プラグイン。nvim-cmpより今はこっちのほうが良さそう。高速だし、nvim-cmpと違って他のプラグインを入れなくてもパスの補完やLSPの補完に対応できるので自分の理想に合ってる。

```lua
return {
  'saghen/blink.cmp',
  version = '1.*', -- 本体のバイナリをダウンロードするのに必要
  opts = {},
}
```

### nvim-lspconfig

Neovim 0.11以降では `vim.lsp` がコアAPIになっているのでもはや必須ではないのだが、このプラグインを入れることで各LSPのよいデフォルト設定が供給される。

デフォルト設定ではエラーや警告に対してマーカーが出ないので、書斎なエラー内容を確認しやすくするために `keymaps.lua` や `options.lua` に書いた通り `vim.diagnostic`  の設定をしておく。(ただこれは本来LSP専用の設定ではないはずなのでプラグインのconfigではなく全体に書いたよ)

```lua
return {
  'neovim/nvim-lspconfig',
}
```

## LSP設定

nvim-lspconfigがあるからほぼデフォルト設定で問題ない。必要なものをenableすると、各LSPの設定にあるfiletypeが開かれたときに起動する。手動で設定したいときは `vim.lsp.config['pyright'] = ...` をする。

```lua
vim.lsp.enable('pyright')
vim.lsp.enable('clangd')
```

私は開発対象特有のやつはデフォルトでは何もせずにプロジェクトごとに設定を書きたいので `.nvim.lua` を置いて書くようにしている。( `vim.o.exrc = true` ならカレントディレクトリから読み込まれる ) nixならdevshellのshellhookで生成。以下はC++とPythonの例。こういう感じにするならnvim-lspconfigに依存せずに `.nvim.lua` にフルの設定を書くのがより安定的だが、小さな設定で同じ挙動をしてほしいので私はnvim-lspconfig前提で書いてる。

```nix
{
  description = "C++ and Python standard development";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system}; in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            gcc
            gdb
            clang-tools
            python3
            pyright
          ];
          shellHook = ''
            cat << 'EOF' > .nvim.lua
            vim.lsp.enable('pyright')
            vim.lsp.enable('clangd')
            EOF
          '';
        };
      }
    );
}
```
