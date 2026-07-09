# プリンタ
## Linux
基本的に、印刷システムとしてCUPSの導入が必要。

NixOSなら以下の設定でサービス有効化される。今どきだいたい汎用ドライバ (AirPrint, IPP_Everywhere) が実装されているプリンタがほとんどで、ドライバを指定しなくても最低限動くが、機能を上げたいときは独自のドライバを入れる。これは`drivers`の配列に組み込めばいい。nixpkgsにあればラッキー。
```nix
  # Printing
  services.printing = {
    enable = true;
    drivers = [
      pkgs.cups-brother-mfcl2800dw # これはプリンタ独自のドライバ
    ];
  };
```

CUPSがネットワーク上のプリンタを見つけるために、[mDNSサービス](../network/mdns.md) の導入が必要なのを忘れず！
