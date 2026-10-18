import sys
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from models import CodeReviewReport
from agent import review_code

console = Console()

SAMPLE_CODE = """
def get_user_data(user_id):
    import sqlite3
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchall()
    
    formatted = []
    for row in result:
        for item in row:
            formatted.append(str(item))
            
    conn.close()
    return formatted
"""

if __name__ == "__main__":
    code_to_review = SAMPLE_CODE
    lang = "python"
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if len(sys.argv) > 2:
            lang = sys.argv[2]
        with open(file_path, "r", encoding="utf-8") as f:
            code_to_review = f.read()
        console.print(f"[bold cyan]🔍 Analyzing file:[/] [yellow]{file_path}[/] ([cyan]{lang}[/])...\n")
    else:
        console.print("[bold cyan]🔍 No file path provided. Running on built-in sample code...\n[/]")

    with console.status("[bold green]Agent is analyzing and refactoring code...", spinner="dots"):
        report = review_code(code_to_review, language=lang)
    
    # 1. Summary Panel
    console.print(Panel(report.summary, title="[bold blue]✨ Code Review Summary[/]", border_style="blue", padding=(1, 2)))
    
    # 2. Findings Table
    table = Table(title="[bold magenta]🛠️ Identified Findings & Recommendations[/]", show_header=True, header_style="bold cyan", border_style="dim")
    table.add_column("Severity", justify="center", style="bold", width=10)
    table.add_column("Category", style="yellow", width=12)
    table.add_column("Line", justify="center", style="dim", width=6)
    table.add_column("Issue & Recommended Fix", style="white")

    for item in report.findings:
        sev_color = "red" if item.severity == "High" else "yellow" if item.severity == "Medium" else "blue"
        severity_badge = f"[{sev_color}]● {item.severity.upper()}[/]"
        
        content = f"[bold red]Issue:[/] {item.issue}\n[bold green]Fix:[/] {item.recommendation}"
        table.add_row(severity_badge, item.category, str(item.line_number), content)

    console.print(table)
    console.print()

    # 3. Refactored Code with Syntax Highlighting
    console.print("[bold green]✨ Fully Refactored & Optimized Code:[/]")
    syntax = Syntax(report.refactored_code, lang, theme="monokai", line_numbers=True, word_wrap=True)
    console.print(Panel(syntax, border_style="green"))