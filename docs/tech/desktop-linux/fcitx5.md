# Fcitx5

インプットメソッドフレームワーク。IMEを司る。

home-managerの設定例が以下。

```nix
  i18n.inputMethod = {
    enable = true;
    type = "fcitx5";
    fcitx5 = {
      waylandFrontend = true;
      addons = with pkgs; [
        fcitx5-mozc
        fcitx5-gtk
      ];
      settings.globalOptions = {
        "Hotkey/ActivateKeys"."0" = "F13";
        "Hotkey/DeactivateKeys"."0" = "F14";
      };
      settings.inputMethod = {
        GroupOrder."0" = "Default";
        "Groups/0" = {
          Name = "Default";
          "Default Layout" = "us";
          DefaultIM = "mozc";
        };
        "Groups/0/Items/0".Name = "keyboard-us";
        "Groups/0/Items/1".Name = "mozc";
      };
    };
  };
```

日本語IMEとしてMozc、LinuxのGUIで使うためにGTKのプラグインを入れている。

設定もhome-managerでやっちゃっている。
F13キーでIMEをON、F14キーでOFFできるようにしている。[キーボード設定](./keyboard.md) でやってるAltの置換と合わせることで、macOS日本語版のような親指1方向切り替えを実現している。

キーボードの順序もここで設定している。通常の生キー配列もIMEもここにいれるのだが、`keyboard-us` のようなキー配列設定を先頭に持っていくことが必須。
