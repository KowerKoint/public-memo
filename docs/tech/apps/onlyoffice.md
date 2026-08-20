# ONLYOFFICE

Microsoft Officeとの互換性がめっちゃ高いと噂のオープンソースオフィススイート。UIもリボンUIっぽい感じになってて心配なくらい似てる。

nixpkgsに `onlyoffice-desktopeditors` として存在していて簡単にインストールできるのだが、PowerPointで作られた日本語スライドを開くには色々フォントを入れなければならない。 (特に、Windows標準フォントとしてnixpkgsの `corefonts` `vistafonts` は必ず入れておきたい)

私がPowerPointで使用しているテンプレートでは日本語に源ノ角ゴシックが採用されているので、これをインストールする。`source-han-sans` としてnixpkgsに存在しているのだが、そのまま使うと中華のほうが優先されてしまって悲しいので、自分でGitHubから取得する形式にしている。以下に[home-manager](../os/home-manager.md)での設定を記述する。まず、`let` 内で

```nix
  sourceHanSansJP = with pkgs; [
    (fetchurl {
      url = "https://raw.githubusercontent.com/adobe-fonts/source-han-sans/release/SubsetOTF/JP/SourceHanSansJP-ExtraLight.otf";
      hash = "sha256-GVVdmvxntT9tJmuwJo3TuIkLuMiMJBrIXgN6b/ZqPGA=";
    })
    (fetchurl {
      url = "https://raw.githubusercontent.com/adobe-fonts/source-han-sans/release/SubsetOTF/JP/SourceHanSansJP-Light.otf";
      hash = "sha256-rdVmnz67ac4hz/h6ikwoOIQG+we9gbI9BsI9ZGFFSYg=";
    })
    (fetchurl {
      url = "https://raw.githubusercontent.com/adobe-fonts/source-han-sans/release/SubsetOTF/JP/SourceHanSansJP-Normal.otf";
      hash = "sha256-USDi2I12HEBccG6bPcvLifuIjkGt+lodFwwUZAH4p5U=";
    })
    (fetchurl {
      url = "https://raw.githubusercontent.com/adobe-fonts/source-han-sans/release/SubsetOTF/JP/SourceHanSansJP-Regular.otf";
      hash = "sha256-QNG3YNETVTn2tuDuK59BXebZdXb3Z2hAsGMGx8GQwHQ=";
    })
    (fetchurl {
      url = "https://raw.githubusercontent.com/adobe-fonts/source-han-sans/release/SubsetOTF/JP/SourceHanSansJP-Medium.otf";
      hash = "sha256-XTn46qqa0q7ZMWawpPxKQ6yC3opcYRKZJEbCTYi1lfk=";
    })
    (fetchurl {
      url = "https://raw.githubusercontent.com/adobe-fonts/source-han-sans/release/SubsetOTF/JP/SourceHanSansJP-Bold.otf";
      hash = "sha256-Oici+UyXpTsXJXmhDvj8NLP6imu095R6LscJq2R/t1U=";
    })
    (fetchurl {
      url = "https://raw.githubusercontent.com/adobe-fonts/source-han-sans/release/SubsetOTF/JP/SourceHanSansJP-Heavy.otf";
      hash = "sha256-+HXenGKs4ggrkKsdqUDz6M7/qTP1AOSdIFy3Tm5dA7s=";
    })
  ];
  officeFontPackages = with pkgs; [
    corefonts
    vista-fonts
  ];
  officeFontSources = officeFontPackages ++ sourceHanSansJP;
  onlyofficeFontDir = "${config.xdg.dataHome}/fonts/onlyoffice";
  officeFontSourceArgs = lib.concatMapStringsSep " " lib.escapeShellArg officeFontSources;
```

と宣言する。必要なotfをダウンロードして、コマンドラインに渡す用の空白区切りファイル名を `officeFontSourceArgs` に準備している。

`officeFontPackages` とONLYOFFICEを両方ともパッケージに追加する。

```
  home.packages = with pkgs; [
    onlyoffice-desktopeditors
  ] ++ officeFontPackages;
```

home-managerの `activation` を使うと、各ファイル配置後にコマンドを実行できる。以下のように登録する。

```nix
  home.activation.onlyofficeFonts = lib.hm.dag.entryAfter [ "writeBoundary" ] ''
    set -eu
    target=${lib.escapeShellArg onlyofficeFontDir}

    rm -rf "$target"
    mkdir -p "$target"
    for source in ${officeFontSourceArgs}; do
      ${pkgs.findutils}/bin/find -L "$source" -type f \
        \( -iname '*.ttf' -o -iname '*.ttc' -o -iname '*.otf' -o -iname '*.otc' \) \
        -exec ${pkgs.coreutils}/bin/cp -L -n {} "$target"/ \; 2>/dev/null || true
    done
    ${pkgs.findutils}/bin/find "$target" -type f -exec ${pkgs.coreutils}/bin/chmod 0644 {} \;
    ${pkgs.fontconfig}/bin/fc-cache -f "$target" >/dev/null 2>&1 || true

    # Rebuild ONLYOFFICE's cached font index after changing the font set.
    rm -rf ${lib.escapeShellArg "${config.xdg.dataHome}/onlyoffice/desktopeditors/data/fonts"}
  '';
```

`$XDG_CONFIG_HOME/fonts/onlyoffice` にフォントをインストールする。
はじめにターゲットディレクトリの古いフォントを削除した後、フォントファイルの実体をコピーする。 **(リンクではなくそこに実体がないとうまくロードされない仕様となっているため必ずリンクを辿って (`-L`オプションで) コピーする)** また、[パーミッションが644でないと読み込まれない](https://www.onlyoffice.com/blog/2020/04/how-to-add-new-fonts-to-onlyoffice-desktop-editors) ので変更する。 `fc-cache -f` で再読込し、 `$HOME/.local/share/onlyoffice/desktopdeditors/data/fonts` にあるONLYOFFICE側の古いキャッシュを削除している。

PowerPointから持ってきたファイルを読み込む場合、フォントの名前違いをエイリアスで解決しないといけないので、`$XDG_CONFIG_HOME/fontconfig/conf.d/` にエイリアスを準備する。home-managerなら以下のように管理できる。

```nix
  xdg.configFile."fontconfig/conf.d/99-office-font-aliases.conf".text = ''
    <?xml version="1.0"?>
    <!DOCTYPE fontconfig SYSTEM "fonts.dtd">
    <fontconfig>
      <alias binding="same">
        <family>源ノ角ゴシック JP</family>
        <accept><family>Source Han Sans JP</family></accept>
      </alias>
      <alias binding="same">
        <family>源ノ角ゴシック JP Heavy</family>
        <accept><family>Source Han Sans JP</family></accept>
      </alias>
      <alias binding="same">
        <family>Noto Sans JP Medium</family>
        <accept><family>Source Han Sans JP Medium</family></accept>
      </alias>
      <alias binding="same">
        <family>游ゴシック</family>
        <accept><family>Source Han Sans JP</family></accept>
      </alias>
      <alias binding="same">
        <family>游ゴシック Light</family>
        <accept><family>Source Han Sans JP Light</family></accept>
      </alias>
    </fontconfig>
  '';
```

ところで、数式はレンダリングが下手くそなのか同じCambria MathでもPowerPointより見栄えが悪く感じる。数式のフォントも変更できない設定になるようで、研究発表に向くかどうかは正直絶妙であった…
