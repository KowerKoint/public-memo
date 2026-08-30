# DBus

プログラム間のメッセージパッシングに使われる経路。

現代のLinux環境で明示的に有効化しないといけないことがあるのかよくわからないが、NixOSでは以下で有効化できる。

```nix
  services.dbus.enable = true;
```
