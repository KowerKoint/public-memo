# Windows デュアルブート

Windowsを含めてデュアルブートする場合の注意点

## ディスクを分けよう
同一ディスクにWindowsとLinuxを混在させると、Windows UpdateによってEFIパーティションが書き換わってLinuxが起動できなくなりGrub Rescue沙汰になりがち。突然のGrub Rescue対応をしたくなければ、SSD2枚目を買って大人しく分けましょう。

ただ、別ディスクのWindowsをGrubに認識させる方法が今のところわかっていないため切替時に毎回UEFIファームウェアの起動順序を変更している…なんとかしたい。

## 時刻問題
Linuxでは標準でハードウェアクロック (RTC) をUTCとして扱うが、Windowsではデフォルトでローカルタイム扱い。

結果として、OSを切り替えたときに時刻が9時間ズレます。

WindowsでRTCをUTC扱いするにはレジストリの `RealTimeUniversal` を変更しよう！管理者権限で以下を実行

```ps
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\TimeZoneInformation" /v RealTimeIsUniversal /t REG_DWORD /d 1 /f
```
