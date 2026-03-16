from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.table import Table
from rich.box import SIMPLE

# 這行建議放在 class 外面，作為全域物件使用
console = Console()

class Renderer:
    @staticmethod
    def render_spread(spread_results):
        card_panels = []
        
        for position, card in spread_results:
            # 1. 預先初始化變數，防止出現 NameError
            status_text = ""
            meaning_text = ""
            border_style = "white"

            # 2. 根據正逆位決定狀態
            is_rev = card.get("is_reversed", False)
            if is_rev:
                status_text = Text("(逆位)", style="bold red")
                meaning_text = card.get("meaning_rev", "查無牌義")
                border_style = "red"
            else:
                status_text = Text("(正位)", style="bold green")
                meaning_text = card.get("meaning_up", "查無牌義")
                border_style = "green"

            # 3. 組合卡片內容 
            card_content = Text(justify="left", overflow="fold") # overflow="fold"：Rich 在處理「長中文」時，如果沒有遇到空格，它會認為這是一個超長單字，而不願意主動切斷它。
            card_content.append(f"🔮 {position}\n\n", style="bold cyan")
            card_content.append(f"{meaning_text}\n", style="italic")

            # 4. 建立卡片面板
            card_panel = Panel(
                card_content,
                title=f"[bold gold1]{card.get('name', '未知卡牌')}[/bold gold1]",
                subtitle=status_text,
                border_style=border_style,
                width=35,       # 寬度固定以利並排
                height=None,    # 💡 強制高度為自動（不限制高度）
                expand=False, 
                padding=(1, 2)
            )
            card_panels.append(card_panel)

        # 5. 最後輸出
        console.print("\n✨ [bold purple]命運的指引已降臨：[/bold purple]\n")
        # 建立一個隱形邊框的表格來放置卡片
        table = Table(show_header=False, box=None, padding=1)
        
        # 根據卡片數量增加欄位
        for _ in card_panels:
            table.add_column()
            
        # 將所有卡片放入同一列
        table.add_row(*card_panels)
        
        console.print(table)