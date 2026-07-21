# Nix flake

## git addしたくないとき
他のコントリビュータがflakeのことをよく知らない / 押し付けたくないときに泣く泣く取る方法。

パス指定なしの `nix develop` などは `flake.nix` がaddされていないと使えないが、 `nix develop path:.` のように指定すれば使える。

逆に、誤ってaddしないように `.git/info/exclude` に `/flake.nix` を追加しておくとよい。

## nix-direnv
いちいち `nix develop` するのめんどくさくて、ディレクトリに入っただけで自動でdevShellに入りたい。[nix-direnv](https://github.com/nix-community/nix-direnv) を使えばこれを実現できる。

NixOSなら、
```
programs.direnv.enable = true;
```
でセットアップできる。

普通に `nixpkgs#direnv` を追加してもつかえるはず (未検証)。

ディレクトリ内でdevShellを有効化するには、
```
use flake
```
と書いた `.envrc` を置く。
パスを指定する場合は
```
use flake path:.
```
。
```
direnv allow
```
を実行して有効化。

`.envrc` と `.direnv/` はあまり人に押し付けるものではないので、`.gitignore` か `.git/info/exclude` に含めたほうが良さげ。
