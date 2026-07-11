# Devcontainer CLI
VSCodeでよく使われるRemote - Containers。すごい技術ではあるが、安定しないし、開発コンテナが決まってるせいでVSCodeを強要されるのは進まない。

この機能は今ではDevelopment Containers Specificationとして切り出されており、CLIも出ている。

Devcontainer CLIは、`devcontainer.json` のビルドと起動をCLIでできるため、VSCode (Remote - Containers)を標準としたプロジェクトにおいてこのストレスをある程度緩和できる。

ただ、Neovimにアタッチできるとかそういうことではないので、開発は自分でdevShellを立てるなりしてコンテナ無しで工面して、最終のビルド確認だけ所定のコンテナでやるとかそういう使い道になると思う。

## インストール
Nixなら `devcontainer` パッケージを入れるだけ。コンテナランタイムは別でインストールしている必要があると思う。[Docker](./docker.md)しか試していない。
