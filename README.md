# LOL Report Tool
![version](https://img.shields.io/github/v/release/SivWatt/LOL_report_tool)
![Test Status](https://github.com/SivWatt/LOL_report_tool/actions/workflows/BuildExecutable.yaml/badge.svg)  
Automatically report players after a game at statistic window.

## Download
Go to [Release](https://github.com/SivWatt/LOL_report_tool/releases/latest) page and download __LOL_report_tool.zip__

## Usage
### English
Run `League.exe` as administrator and the GUI will show.  
![GUI](/doc/main-window.PNG?raw=true)
  - Press `TEAM` to report __ALL__ of the players in your team  
  - Press `ENEMY` to report __ALL__ of the players in opponent team  
  - Press `ALL` to report literally all players except yourself  

The report message is copied from `reportText.txt`.  
User can modify the content to whatever he wants to meet his need.  
_Note that modifying `reportText.txt` takes effect after next time you restart `League.exe`_

### 中文
以系統管理員執行 `League.exe` 即可看到圖形化介面。  
![GUI](/doc/main-window.PNG?raw=true)
  - 按下 `TEAM` 以檢舉**所有**同隊的隊友  
  - 按下 `ENEMY` 以檢舉**所有**同隊的隊友  
  - 按下 `ALL`  以檢舉**所有**同隊的隊友  

檢舉的訊息來自 `reportText.txt`，使用者可以自行編輯其內容以達到個人的需求。  
_注意：如果更改了`reportText.txt`的內容，必須重新啟動`League.exe`，檢舉訊息的更改才會生效。_

## Supported Modes
Currently, this tool recognizes game mode image on the upper-left corner of __League of Legend Client__ window.  
If the game mode image is not included, it won't start reporting players.  
### Supports
- ARAM

## Troubleshooting
Most of the problems users come into are about images recognizing.  
You can take a look at `debuglog.log` to see which image the tool mismatches.  
And for image issues, it can simply be fixed by replacing image with screenshoted one by user himself/herself.

## Development
If you encounter any problem, feel free to let me know via creating [issues](https://github.com/SivWatt/LOL_report_tool/issues).
