
#只负责"把数据画成表格"

from rich.console import Console
from rich.table import Table

def print_table(items, top):
    console = Console()
    table = Table(title=f"单词频率 Top {top}", show_lines=True)
    table.add_column("排名", justify="right", style="cyan")
    table.add_column("单词", style="magenta")
    table.add_column("次数", justify="right", style="green")
    for i, (w, n) in enumerate(items, start=1):
        table.add_row(str(i), w, str(n))
    console.print(table)