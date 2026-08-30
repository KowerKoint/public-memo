# Android 開発

- 書いてあること、できればプロジェクトのflakeでやったほうがきれいです。ここサボるの良くないなーと思いつつ、Android Studioはデスクトップアプリなのでグローバルに入れたかったり `kvm` グループはシステムレベルで設定する必要があったりなので、思い切ってAndroid用の開発環境全部OS設定に組み込んでます……

## JDK
当然JDKは必要。

Nixなら `jdk21` パッケージを追加。

`JAVA_HOME` 環境変数も設定する。home-managerなら以下。

```nix
  home.sessionVariables = {
    JAVA_HOME = "${pkgs.jdk21}";
  };
```

## Android SDK
SDK自体はAndroid Studioからダウンロードするが、動かすための設定をしておく。

環境変数の設定。
```nix
  androidSdkRoot = "${config.home.homeDirectory}/Android/Sdk";
```
を `let` しておいて、
```
  home.sessionVariables = {
    ANDROID_HOME = androidSdkRoot;
    ANDROID_SDK_ROOT = androidSdkRoot;
  };

  home.sessionPath = [
    "${androidSdkRoot}/platform-tools"
    "${androidSdkRoot}/emulator"
    "${androidSdkRoot}/cmdline-tools/latest/bin"
  ];
```

また、Android StudioによるSDKバイナリをNixOSで動かすために [nix-ld](../os/nix-ld.md) が必要。

## kvm グループへの追加
エミュレータのハードウェア高速化のためにユーザを `kvm` グループに追加する必要があるらしい。NixOSなら `users.users.<ユーザ名>.extraGroups` に `"kvm"` を追加。

## Android Studioとandroid-toolsの追加
Android Studio (必須IDE) とandroid-tools (`adb` や `fastboolt` を提供) を導入。Nixなら `android-studio` `android-tools` パッケージを追加すればOK。
