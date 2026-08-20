# home-manager

LinuxやmacOSのユーザー設定のあれこれ (インストールするパッケージ、設定ファイルなど) をNixで記述できる。

要するに、おおよそユーザー向けに小さなNixOSのようなことができるということ。

flake化されたNixOSの設定と出力をまとめるなら、`flake.nix` 内で入力に `home-manager` を追加し、`nixosSystem` のモジュールとして以下のように追加する。

```nix
{
  description = "NixOS configuration for nixos";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    home-manager = {
      url = "github:nix-community/home-manager/release-26.05";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, home-manager, ... }:
    {
      nixosConfigurations.nixos = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
          ./configuration.nix
          home-manager.nixosModules.home-manager
          {
            home-manager.useGlobalPkgs = true;
            home-manager.useUserPackages = true;
            home-manager.users.<ユーザ名> = import ./home.nix;
          }
        ];
      };
    };
}
```

以下は最低限の設定。これを `home.nix` として保存する。
NixOSであっても、 `configuration.nix` の `stateVersion` と `home-manger` のものを合わせる必要はない。
home-managerの `programs.home-manager.enable = true;` によって自身を有効化している。
```nix
{ ... }:

{
  home.username = "<ユーザ名>";
  home.homeDirectory = "/home/<ユーザ名>";
  home.stateVersion = "26.05";

  programs.home-manager.enable = true;
}
```

flakeに入力を追加したなら評価前に一度 `sudo nix flake lock` で新入力分を `flake.lock` に反映して多くとよい。その後リビルド。
