# メモリのスワップ
RAMが足りなくなったときに他の場所を使う設定。
現代では16 GBマシンだと必須と思われる。

Windowsでは仮想メモリと呼ばれるものがあって、macOSでも勝手に設定されてるっぽい。
これらの設定は今のところやったことがない。

## Linuxでのswap
自分の知る限りのスワップ手法は以下の3種類。

- zram swap: RAMの中で使ってない領域を圧縮
- swapfile: RAMが足りなくなったらSSDを使う。この領域はファイルシステムの中の1つのファイルとして扱われ、普通にストレージ用のパーティションの中の一角を使う。
- swapパーティション: 一番レガシーなスワップ。ストレージのパーティションをスワップようにあらかじめ切り分けて使う。

以下はNixOSでの設定例。設定内容は、

- zram→swapfileの順で優先
- RAMの半分をzramに
- swapfileは16GiB

```nix
  zramSwap = {
    enable = true;
    memoryPercent = 50;
    priority = 100;
  };

  swapDevices = [
    {
      device = "/var/lib/swapfile";
      size = 16384; # 16GiB
      priority = 10;
    }
  ];
```
