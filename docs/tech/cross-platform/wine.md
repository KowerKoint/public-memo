# Windows 互換レイヤ
Windows互換レイヤはエミュレータではなく、WindowsのシステムAPIをホストOSのAPIに変換することで高速に動作させるという素晴らしい取り組み。
昔はWineが主流だったが、今はWineを直接使うことはあまりなさそう。懐かしき時代だったなぁ。

## Steam Play
Valveがかなり気合い入れて、Protonというかなりいい互換レイヤを実装している。
Protonは基本的にSteam Playで使える。Steam Playでは、ゲームごとに使用する互換レイヤのバージョンを選べて、ゲーム部分をマウントして使う。
[Steam](../apps/steam.md) 参照。

## Bottles
Steam Playと似た感じで、ゲームとレイヤを1対1対応する感じの、Steamより簡素なデスクトップアプリ。ゲーム用に互換レイヤを使いたくて、Steamに依存したくないならたぶんこれが一番有用。sodaとかwine-geとかのレイヤが使える。どれがいいのかはよくわからんが、色々試してみてちゃんと動いたのを使うべし。

使ってたときの記録がないのであまり自信はないけど、Nixならパッケージ `bottles` を入れるだけ (たぶん)。

## Gamescope
分離型コンポジタ。指定した解像度を偽装したウィンドウを作れる。Waylandとかでマウスが使えない問題を解決できる可能性がある。
Nixならパッケージ `gamescope` を入れるだけ。

## ゲームごとの自分流トラブルシューティング
互換レイヤはだいぶんおま環なので結局毎回トラブルシューティング粘ることになりがちだが、同じことで苦しまないように気が向くだけログを残す。

### 東方神霊廟 パッケージ版
- 動作環境: NixOS/Wayland/Niri/Steam Play (Proton 9.0)
  - デフォルトのディレクトリ構造だと「東方神霊廟」などの日本語がパスに含まれるが、それだと動作せず
  - 起動時の、ウィンドウサイズを選択するダイアログでは、マウスが効かずキーボード操作もできないが、Enterで入れる
  - ウィンドウサイズを変更したい場合は、`custom.exe` のほうから変更すると動作
    - こっちもマウスが効かないが、Gamescopeでコンポジタを分離することで使えるようになる (`gamescope -w 640 -h 480 -W 640 -H 480 -- %command%`)
    - Steam Playなどでは別々のWINE_PREFIXになるので、`custom.exe`のほうで作った設定ファイル (`~/.local/share/Steam/steamapps/compatdata/<APP ID>/pfx/drive_c/users/steamuser/AppData/Roaming/ShanghaiAlice/th13/th13.cfg`) を、`th13.exe`用のプレフィックスにコピーすると良い
      - APP IDはどこから見るのが一番楽なのかはよくわからないが、更新日時で判別できる
  - `custom.exe` などのダイアログは豆腐化してるが、ウィンドウサイズくらいなら数字だけ見て変更可。たぶんwinetricks/protontricksとかでフォント入れると解決するが


