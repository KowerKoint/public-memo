# Wayland

古き良き(?)X11に代わる現代的なディスプレイサーバ。とはいっても、私が大学生になったころにはもうこっちのほうが標準的になった記憶。
Ubuntuは21.10から標準化されてるらしい。

こっちのほうが、ほかアプリの入力を盗聴できなくなってセキュリティが向上したり、パフォーマンスが改善したりしてるらしい。
正直詳しいことはあまり知らないが、よくわからないのに今更X11を使いたいなどとは私は思わない。

## X11アプリケーション への対応

とはいえ、2026年現在、未だにX11を必要とするアプリケーションが存在する。

特に、Electron系アプリ (Discord, Spotify, VSCodeなど) は長らくX11だった。
- どうもElectron 38 (2025/09) からWaylandネイティブが既定になったらしい。
- ちなみに、Electronを使っているところは、私はVSCodeをあまり好まない理由の1つだ。

Electronの他に、Wine/Proton は未だにX11に依存している面が大きい。
いずれ解消されそうではあるが…

Electron系なら `--enable-features=UseOzonePlatform --ozone-platform=wayland` とかをつけて強制的にWaylandネイティブにできたりするが、不安定な印象。
悔しながらの万能薬が下記 [XWayland](#xwayland)。

## XWayland
X11アプリケーションをWayland環境で表示する救いの互換レイヤ。

niriだと、コンポジタの外でWaylandに変換できる `xwayland-satellite` を推奨している。他のWMならそれにあったやつを調べるのが良さそう。Nixなら `xwayland-satellite` パッケージを追加する。

niriのconfigに
```
spawn-at-startup "xwayland-satellite"
```
を書いてたんだが、どうもniri 25.08以降では不要になったらしい。
- X11アプリが接続した時点でオンデマンド起動してくれる

### IsUnMappedになっていたときの復帰
かなりマニアックだが経験したトラブルシューティングなのでメモ。

前回外部ディスプレイで起動したフローティングのXWaylandウィンドウ、ディスプレイを外してサイド起動すると迷子に。niriのウィンドウ一覧を確認しても見つからない…
というときの原因と対処。

XWaylandでウィンドウを起動しようとしたとき、画面外だったりでうまくいかなかったとき、描画をしない `IsUnMapped` 状態になってしまう。
```
nix run nixpkgs#xdotool -- search --name <名前>
```
でX11ウィンドウIDを得てから
```
nix run nixpkgs#xdotool -- windowmap <ID>
```
でmapできる。

おそらくまだ画面外なので、コンポジタ側で移動しよう。niriなら、
```
niri msg action center-window --id <niriのウィンドウID>
```
で画面中央へ。
