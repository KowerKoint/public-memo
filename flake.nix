{
  description = "mkDocs development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          mkdocs
          mkdocs-material
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            pythonEnv
          ];

          shellHook = ''
            echo "mkDocs dev environment ready"
            echo "  mkdocs serve    - start dev server at http://localhost:8000"
            echo "  mkdocs build    - build static site to ./site/"
          '';
        };
      });
}
