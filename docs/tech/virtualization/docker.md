# Docker
コンテナプラットフォームの代表。

## インストール
NixOSでならかなり楽にシステムインストールできる。
```nix
  virtualisation = {
    docker = {
      enable = true;
    };
  };
```
virtuali"s"ationなのに注意。NixOSの設定個目はBritish spellingがちでかなり罠…

## `docker`グループへの追加
システムのデーモンとして動くので、ユーザーがそれを利用するなら `docker` グループに追加する必要があり。NixOSなら以下。

```nix
  users.users.<ユーザー名> = {
    extraGroups = [ "docker" ];
  };
```

## 雑記
podmanも使ってみたいし、rootless docker運用もしてみたい気持ちはある。
podmanをNixOSで一度試したところ、マウント時にownerがrootになってしまったのだが、解決を放置している。
