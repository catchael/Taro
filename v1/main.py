import typer
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm


# 路徑初始化
root_path = Path(__file__).resolve().parent
sys.path.append(str(root_path))

load_dotenv()

# 初始化 Typer
app = typer.Typer(help="CLI Tarot Divination Tool", add_completion=False)

def get_app_components():
    try:
        from core.deck import Deck
        from core.spreads import SpreadEngine
        from core.ui import Renderer, console
        from core.database import HistoryManager
        from api.llm_client import TarotAI
    except ImportError as e:
        pass
    
    try:
        deck_path = os.path.join(root_path, "data", "cards.json")
        db_path = os.path.join(root_path, "database", "history.db")
        
        deck = Deck(deck_path)
        engine = SpreadEngine(deck)
        db = HistoryManager(db_path)
        return engine, db
    except Exception as e:
        console.print(f"[bold red]❌ 系統初始化失敗：{e}[/bold red]")
        raise typer.Exit(code=1)

# 工具介紹與用戶須知
def show_welcome_msg():
    welcome_content = """
[bold gold1]🔮 歡迎來到 CLI 神祕學塔羅占卜系統[/bold gold1]
--------------------------------------------------
本工具結合傳統塔羅牌陣與 [bold cyan]Gemini AI[/bold cyan] 提供深度命運解析。

[bold green]● 主要功能：[/bold green]
  - [white]即時占卜[/white]：支援單牌與三牌陣（過去/現在/未來）。
  - [white]紀錄追蹤[/white]：自動儲存您的占卜歷史。
  - [white]AI 諮詢[/white]：針對您的問題提供溫暖且具啟發性的建議。

[bold yellow]🛡️ 用戶須知 (隱私與資安)：[/bold yellow]
1. [white]資料本地化[/white]：紀錄僅存在本地資料庫，程式不會上傳您的私密問題。
2. [white]API 安全[/white]：Key 僅用於官方通訊，本程式不記錄、不側錄您的金鑰。
--------------------------------------------------
    """
    console.print(Panel(welcome_content, border_style="bright_magenta", expand=False))

    example_text = """
[bold gold1]🚀 快速上手指令範例：[/bold gold1]

  [cyan]● 每日運勢 (單牌)：[/cyan] [green]python main.py draw "我今天的運勢如何？"[/green]
  [cyan]● 深度解析 (三牌陣)：[/cyan] [green]python main.py draw "面試是否會錄取？" --type three[/green]
  [cyan]● 歷史紀錄：[/cyan] [green]python main.py history[/green]
  [cyan]● 清除紀錄：[/cyan] [red]python main.py clear[/red]
  [cyan]● 離開系統：[/cyan] [white]python main.py exit[/white]
    """
    console.print(Panel(example_text, title="使用手冊", border_style="blue", expand=False))

# API Key 取得 
def get_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        console.print("\n[yellow]⚠ 偵測到未設定 API Key，AI 功能將受限。[/yellow]")
        if Confirm.ask("您想要手動輸入 API Key 嗎？"):
            console.print("[grey50]提示：您可以直接按 Ctrl+V (或滑鼠右鍵) 貼上金鑰，然後按 Enter。[/grey50]")
            key = Prompt.ask("請貼上您的 Gemini API Key")
        else:
            return None
    return key

# 指令：占卜
@app.command()
def draw(
    question: str = typer.Argument(..., help="The question you want to ask"),
    type: str = typer.Option("single", "--type", "-t", help="Spread type: single or three")
):
    """執行占卜功能"""
    engine, db = get_app_components() # 執行指令時才載入資源
    
    if len(question.strip()) < 2:
        console.print("[bold red]❌ 錯誤：問題太短。[/bold red]")
        return

    try:
        current_key = get_api_key()
        
        with console.status("[cyan]正在洗牌並讀取靈性能量...", spinner="moon"):
            spread_results = engine.three_cards() if type == "three" else engine.daily_one()
        
        flat_results = [item[1] for item in spread_results]
        db.save_record(type, flat_results)
        
        Renderer.render_spread(spread_results)
        
        if current_key:
            if Confirm.ask("🔮 需要 AI 占卜師為您深度解析嗎？"):
                ai_advisor = TarotAI(current_key)
                with console.status("[bold purple]占卜師正在讀取星象...", spinner="moon"):
                    analysis = ai_advisor.analyze_spread(question, spread_results)
                
                console.print("\n[bold gold1]─── AI 占卜師的私語 ───[/bold gold1]")
                console.print(analysis, style="italic")
                console.print("[bold gold1]───────────────────────[/bold gold1]\n")
        
        console.print(f"✅ 紀錄已成功存入本地資料庫。")

    except Exception as e:
        console.print(f"[bold red]❌ 占卜過程發生錯誤：{e}[/bold red]")

# 指令：清除 (Clear)
@app.command()
def clear():
    """🧹 永久清除所有本地占卜紀錄"""
    engine, db = get_app_components()
    if Confirm.ask("[bold red]⚠️ 確定要刪除所有歷史紀錄嗎？此動作無法還原！[/bold red]"):
        if db.clear_all():
            console.print("[bold green]✨ 紀錄已清空。[/bold green]")

# 指令：歷史(History)
@app.command()
def history(limit: int = typer.Option(5, "--limit", "-l", help="顯示最近幾筆紀錄")):
    """📜 查看過去的占卜紀錄"""
    _, db = get_app_components()
    records = db.get_recent_history(limit)
    
    if not records:
        console.print("[yellow]目前還沒有任何占卜紀錄。[/yellow]")
        return

    table = Table(title="📜 最近的占卜紀錄", box=None)
    table.add_column("時間", style="cyan")
    table.add_column("類型", style="magenta")
    table.add_column("抽中卡片", style="white")

    for rec in records:
        # 這裡簡單處理 cards_json 的顯示（例如取名稱）
        # 假設你的 cards_json 儲存的是字串化的 JSON
        table.add_row(
            rec["timestamp"],
            rec["spread_type"],
            rec["cards_json"][:50] + "..." # 避免太長
        )

    console.print(table)

# 指令：離開 (Exit)
@app.command()
def exit():
    """🚪 關閉占卜系統"""
    console.print("\n[bold purple]🔮 感謝您的諮詢。願星辰指引您的道路，再會。[/bold purple]\n")
    raise typer.Exit()

# 程式入口回呼
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    這是程式入口。
    當使用者只打 python main.py（沒指令也沒參數）時，才顯示歡迎訊息。
    當使用者打 --help 時，Typer 會自動處理，不會進入這裡執行歡迎訊息。
    """
    # 如果有子指令或是打 --help，ctx.invoked_subcommand 就不會是 None
    if ctx.invoked_subcommand is None:
        # 二次確認：檢查 sys.argv 裡有沒有 help 相關字眼
        if not any(h in sys.argv for h in ["--help", "-h"]):
            show_welcome_msg()


if __name__ == "__main__":
    app()