# XDG Desktop Portal

アプリがOSの機能にアクセスするために必要なもの。

[waybar](./waybar.md)の各機能を使ったり画面共有をするときに必要なはず。

メッセージ経路として [DBus](../os/dbus.md) の有効化を明示的にしないといけないかもしれない (要調査)。

NixOS (niri) なら以下で設定する。

niri用にportalは用意されていないので、GNOMEを使うのが慣例らしい。Waylandのための反映のportalとして wlr も必要。特にZoomなどでウィンドウを選んで画面共有する場合この2つともがこの順番にあることが重要 (wlrが手前だとウィンドウ選択のUIが用意されていなくて選べなくなってしまうのでGNOMEを使うが、実際の画面転送はwlrがやってそう (間違ってるかも))。

```nix
  xdg.portal = {
    enable = true;
    extraPortals = with pkgs; [
      xdg-desktop-portal-gnome
      xdg-desktop-portal-wlr
    ];
    config.common.default = [ "gnome" "wlr" ];
  };
```
