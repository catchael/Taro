[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/5PhkpLhw)
# HW2-Implementation-of-SDD-Specification-Optimization
```markdown
├── v1/
│   ├── sdd_v1.md            ← v1.0 規格文件（必要）
│   ├── main.py              ← v1.0 主程式（必要）
│   ├── requirements.txt     ← Python 套件清單（optionally）
│   └── ...                  ← 其他 v1.0 程式模組
├── v2/
│   ├── requirements_v2.md   ← 由助教 Agent 自動產生（請勿自行建立）
│   ├── sdd_v2.md            ← v2.0 規格文件（必要）
│   ├── main.py              ← v2.0 主程式（必要）
│   ├── requirements.txt     ← Python 套件清單（optionally）
│   └── ...                  ← 其他 v2.0 程式模組
└── README.md                ← 完整說明文件（必要


tarot-cli/
├── data/
│   ├── cards.json       # 完整的 78 張牌義資料
│   └── ascii_art.py     # 儲存每張牌的 ASCII 圖形
├── core/
│   ├── __init__.py
│   ├── deck.py          # 洗牌、抽牌邏輯
│   ├── spreads.py       # 牌陣定義 (三牌陣、凱爾特十字等)
│   └── ui.py           # 負責 Rich 美化渲染
├── api/
│   └── llm_client.py    # 串接 AI 解牌接口
├── database/
│   └── history.db       # 使用者紀錄
└── main.py              # CLI 入口
```

```mermaid
graph TD
    %% 使用者介面層
    subgraph UI ["使用者介面層 (Presentation)"]
        A[CLI 指令解析 - Typer/Click] --> B{指令類型}
        B -->|抽牌| C[占卜介面]
        B -->|紀錄| D[歷史查詢介面]
        B -->|設定| E[配置管理介面]
    end

    %% 業務邏輯層
    subgraph Logic ["業務邏輯層 (Business Logic)"]
        C --> F[Deck Manager<br/>洗牌與抽牌邏輯]
        C --> G[Spread Engine<br/>牌陣定義]
        F --> H{是否啟用 AI?}
        H -->|是| I[AI Interpreter<br/>LLM API 整合]
        H -->|否| J[靜態牌義解析]
    end

    %% 資料與配置層
    subgraph Data ["資料與配置層 (Data & Persistence)"]
        F -.-> K[(Card DB<br/>JSON/YAML)]
        I -.-> L[API Keys / Config]
        D <--> M[(History DB<br/>SQLite)]
    end

    %% 樣式設定
    style UI fill:#f9f,stroke:#333,stroke-width:2px
    style Logic fill:#bbf,stroke:#333,stroke-width:2px
    style Data fill:#dfd,stroke:#333,stroke-width:2px
```
