# WireGuard
クライアントサイドの話だけ。

Nixならnixpkgsの `wireguard-tools` パッケージを使う。NixOSならconfigurationに追加しておいていいと思う。

wireguardのconfファイルがあれば、 `wg-quick up /path/to/conf` でVPNを起動できる。切断するときは `wg-quick down /path/to/conf` 。
