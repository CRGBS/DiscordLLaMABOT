# Discord LLAMA BOT

這個項目是一個 Discord 機器人，能讓你將 LLAMA 語言模型運行再 Discord 上，使其能夠參與對話並回應使用者的輸入。它利用 LLAMA 語言模型的強大功能生成智能且具有上下文的回應。
#### 功能

    與 Discord 伺服器無縫集成
    與 LLAMA 語言模型進行即時對話
    

#### 先決條件

    Python 3.7 或更高版本
    Discord.py 庫
    LLAMA 語言模型
    LLAMACPP 程式

#### 開始使用

    下載本bot.py檔案：

    bash
    安裝所需的依賴項：

    pip install discord

    準備你的語言模型以及llamacpp。
    可以在以下網址下載
    https://github.com/ggerganov/llama.cpp

    通過修改 bot.py 文件自定義機器人配置。
    BOT_TOKEN, CHANNEL_ID , ROLE, command
    BOT_TOKEN 請向Discord申請
    CHANNEL_ID 為允許使用的頻道
    ROLE 是允許使用的權限組
    command 是運行的參數，切記要將llamacpp修改為你的路徑
    
#### 運行機器人：

    python bot.py

    使用為您的機器人生成的 OAuth2 URL 邀請它加入到您的 Discord 伺服器。

#### 使用方法

    一旦機器人運行並連接到您的 Discord 伺服器，您可以使用 @您所設定的機器人名稱 來和他進行對話

   您可以根據需要自定義和擴展機器人的功能。
#### 許可證

  該項目在 APACHE-2.0 許可證下發布 - 請參閱 LICENSE 文件瞭解詳細信息。
  鳴謝

    ggerganov 提供的 llamacpp 應用程式，網址：[LLAMA AI](https://github.com/ggerganov/llama.cpp)
    Rapptz 開發的 Discord.py 庫，網址：[Rapptz](https://github.com/Rapptz/discord.py)


#### 貢獻

歡迎對該項目進行貢獻。請隨時提出問題或提交拉取請求以提出改進意見或報告錯誤。

