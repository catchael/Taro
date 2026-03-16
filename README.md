[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/5PhkpLhw)
# HW2-Implementation-of-SDD-Specification-Optimization

# Taro - SDD Specification & Optimization

這是一個關於 **SDD (Software Design Description)** 規範實作與優化的專案。本專案旨在提供高效的規格定義與系統優化解決方案。

## 🚀 功能特點

* **規格實作**：精準對接 SDD 規範要求。
* **效能優化**：針對現有架構進行邏輯與資源分配優化。
* **環境隔離**：已配置 `.gitignore` 確保開發環境純淨。

## 📂 目錄結構

```text
.
├── v1/                 # 主要開發目錄 (Implementation)
├── .gitignore          # Git 忽略設定
└── README.md           # 專案說明文件
```
# 🛠️ 開始使用
## 1. 複製專案
```bash
git clone [https://github.com/catchael/Taro.git](https://github.com/catchael/Taro.git)
cd Taro
```

## 2. 建立環境
建議使用虛擬環境以避免套件衝突：
```bash
python -m venv venv
# Windows 啟動環境
.\venv\Scripts\activate
# Mac/Linux 啟動環境
source venv/bin/activate
```
## 3. 安裝依賴
```bash
pip install -r v1/requirements.txt
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