# Steam
ゲームプラットフォーム。

## NixOSでのセットアップ
Remote Play (リモートのゲーミングPCで処理してクライアント画面に描画)、Source Dedicated Server (サーバとして動作) はファイアウォールを開ける必要がある…が自分は別に使ってないのでいらない。

マウスがうまく動かない問題があるので、NixOS Wikiにある通り `extest.enable = true` で解決してるが、本当に必要だったのかは忘れてしまった。

```nix
  programs.steam = {
    enable = true;
    remotePlay.openFirewall = true;
    dedicatedServer.openFirewall = true;
    extest.enable = true;
  };
```

## Steam外のアプリの追加
メニューバーの「Games→Add a non Steam Game to My Library」で、Steam外のアプリをSteamで管理できる。
Steamヘビーユーザーなら他で買ったパッケージ版ソフトとかもこっちにまとまってると便利なのかもしれない。

それ以上に、Steam Play を使えるのでLinuxでWindowsゲームを遊ぶときに重宝する。
個人的には、別にSteamが好きなわけではないし、フレンドにオンラインが見えたりしてめんどくさいので、Bottlesでもいいなと思ってる。ほとんど試していないが、今のところproton (on Steam) soda (on Bottles) では同等の安定感という印象。

## 互換レイヤの使用
macOSやLinuxでゲームをやるには、Steam Playの互換レイヤ機能を使うことになる。
Steamで購入したゲームではたぶん自動的に適用されるが、外部から追加したやつだと設定が必要。
ゲームごとの「Properties」メニューの「Compatibility」から、「Force the use of a specific Steam Play compatibility tool」にチェックする。ランタイムはProton系の良さそうなのを適当に使えばよい。

起動オプションは「Shortcut」の「LAUNCH OPTIONS」に設定する (例: `PROTON_LOG=1 %command%` で `PROTON_LOG` 環境変数が設定され、Protonのログが `~/` 直下に置かれてトラブルシューティングに役立つ)。

Steam Playに限らない一般的な互換レイヤの解決は [互換レイヤ](../cross-platform/wine.md) を参照。
