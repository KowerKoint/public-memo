# NixOS設定のflake化

NixOSのconfigurationは [flake](../package-manager/nix-flake.md) として定義することができる。

私は素朴な設定を好んでいるので、以前はこれをやっていなかったのだが、多くのプロジェクトがflakeとしてビルドできる形で存在していて(例: [Zen](../apps/zen.md))、それをそのままのconfigurationから取り入れるのが面倒だと感じたので素直にflake化したほうが良いと思っている。

メリットは以下
- 入力をflakeで管理できる
    - nixpkgsしか使わないとしても、もともとのNixOSだとconfiguration.nixにあるnixpkgsは `nix-channel` というマシン固有の状態に依存しているが、flake化すると `inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";` と直接宣言でき、また解決された実体は `flake.lock` で固定される
- 外部のNixプロジェクトを扱いやすい
    - ↑のZenの話もそうだし、[home-manager](./home-manager.md)もそう
- 1つのプロジェクトで複数のマシンの設定を管理
    - そもそもflakeは自然にGitで管理できる
- 複数の `output` を指定できるので、一部を共通化したうえで、デスクトップマシン用、ラップトップ用、サーバー用…と変化をつけられる
    - [nix-darwin](./nix-darwin.md)などを使えばmacOSでさえも管理可能！
  
設定方法はかなり簡単。
今回は `~/.nixos/` にセットアップしていくことにする
- OS全体の設定だが、いつも使ってる管理ユーザのホームディレクトリに置いておいたほうがエディタで開きやすいしAIも使いやすいのでそうしておこう

とりあえずもとの `/etc/nixos/configuration.nix` `/etc/nixos/hardware-configuration.nix` を `~/.nixos/` にコピーする。その後、以下の `flake.nix` を作成。

```nix
{
  description = "NixOS configuration for nixos";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
  };

  outputs = { self, nixpkgs, ... }:
    {
      nixosConfigurations.nixos = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
          ./configuration.nix
        ];
      };
    };
}
```

gitで管理していないとflakeにローカルツリーとして管理されるので、最初からgit配下に入れておこう。dirty状態にはなるもののコミットは一旦しなくてもOK。 `git init` `git add . -v` しておいて、以下で一旦テスト。

```
sudo nixos-rebuild test --flake #.nixos
```

`#.nixos` の部分は `outputs` に入れた名前。

エラーが出なければ、

```
sudo nixos-rebuild switch --flake #.nixos
```

で実際に適用。
