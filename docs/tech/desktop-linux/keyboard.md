# キーボード設定

## xkb
xserverでキーボードレイアウトを設定するおなじみのモジュール。

以下がNixOSでの設定例

```nix
  services.xserver.xkb = {
    layout = "us";
    variant = "";
    options = "terminate:ctrl_alt_bksp,ctrl:nocaps,fkeys:basic_13-24";
  };
```

キーボードレイアウトがUSであることを設定している。また、以下のオプションを設定している。

|オプション|説明|
|--|--|
|`terminate:ctrl_alt_bksp`|NixOSのxkbオプションでデフォルトで有効化されているので入れている。`<C-A-BS>` でXorgのセッションを強制終了するようだが、Waylandでは関係ない。|
|`ctrl:nocaps`|CapsLockをCtrlに変える。人権。|
|`fkeys:basic_13-24`|xkbではデフォルトで、F13がXF86Tools,F14がXF86Launch5などの特殊キーに再割り当てされていてアプリケーションに渡せないので、これで戻す。↓のkeydおよびfcitx5設定用。|

!!! note
    niriなどのコンポジタでxkb設定をするところがあったりするが、これを設定するとそのセッション内でオプションが上書きされる。例えばシステムで `ctrl:nocaps` 、コンポジタで `fkeys:basic_13-24` としていたら `ctrl:nocaps` は消えてしまうので、一番上のレイヤで全部設定しよう！
    システムとコンポジタのどっちで設定するかは好みかな。niriの設定をhome-managerに移植できたら自分もxkbはそっちに書くかも…？

## keyd
カーネルレベルのキーリマップ。[fcitx5](./fcitx5.md) のAltでの切り替えのために使用している。NixOSで以下のように設定している。

```nix
  services.keyd = {
    enable = true;
    keyboards.default = {
      ids = [ "*" ];
      settings.main = {
        rightalt = "overload(altgr, f13)";
        leftalt = "overload(alt, f14)";
      };
    };
  };
```
`overload` を使うことで、長押し(押下しながら他のキーを押下したとき)と単押しで挙動を変えられる。右Altの単押しをF13に、左Altの単押しをF14に変えている。右ALtは `altgr` となっているのでリマップ後も区別が残っている。

!!! note
    右AltはISO_Level3_Shiftとして特殊文字を打つために使われるキーコードになってることもあるらしい。これを使っている場合はむやみに上書きするべきではない。なお、keydの`altgr` はこれのことではなく通常の右Altを表す識別子なので、この設定では右Altから正しく右Altに戻せている。
