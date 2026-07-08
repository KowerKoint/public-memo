# mDNSサーバー
LAN上のサービスホストの発見を自動で行う。Windows/macOSでは気にすることがないが、プリンターを自動検知するためにいつも必要になる。
## Linux
LinuxではAvahiが基本的に採用される。NixOSなら以下でセットアップ。
```nix
  # Enable mDNS/Bonjour so network printers are auto-discovered.
  services.avahi = {
    enable = true;
    nssmdns4 = true;
    openFirewall = true;
  };
```
