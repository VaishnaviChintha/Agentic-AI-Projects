import os
import time
import markdown
from google import genai
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

# Initialize Rich console for beautiful terminal output
console = Console()

# Initialize the Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def run_research_agent():
    # Fancy Header
    console.print(Panel.fit(
        "[bold cyan]🤖 Autonomous AI Research Agent[/bold cyan]\n[dim]Powered by Gemini & Python[/dim]",
        border_style="cyan"
    ))
    
    # Prompt the user for a custom topic interactively
    console.print("\n")
    user_topic = Prompt.ask("[bold yellow]Enter the research topic you want to explore[/bold yellow]")
    
    console.print(f"\n[cyan]Target Topic:[/cyan] [italic]{user_topic}[/italic]\n")

    # Animated Spinner while waiting for Gemini
    with Progress(
        SpinnerColumn("dots", style="green"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="[cyan]Agent is researching and synthesizing report...", total=None)
        
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=f"Provide a structured, beautifully formatted summary on: {user_topic}"
        )
        time.sleep(0.5)

    report_text = response.text
    
    # Save the report to Markdown
    md_filename = "research_report.md"
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(report_text)

    # Save a styled HTML version for web view
    html_filename = "research_report.html"
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Research Report: {user_topic}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 20px; color: #333; background: #f9f9f9; }}
        h1, h2, h3 {{ color: #0284c7; }}
        code {{ background: #e2e8f0; padding: 2px 6px; border-radius: 4px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #cbd5e1; padding: 10px; text-align: left; }}
        th {{ background: #e0f2fe; }}
        .card {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
    </style>
</head>
<body>
    <div class="card">
        {markdown.markdown(report_text, extensions=['tables', 'fenced_code'])}
    </div>
</body>
</html>"""

    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Render Output nicely in terminal
    console.print("\n[bold green]✔ Research Complete & Successfully Compiled![/bold green]\n")
    console.print(Panel(Markdown(report_text), title="[bold]Final Agent Report[/bold]", border_style="green"))
    
    console.print(f"\n[dim]📁 Saved files:[/dim]")
    console.print(f"  • Markdown: [link={md_filename}]{md_filename}[/link]")
    console.print(f"  • HTML Report: [link={html_filename}]{html_filename}[/link] (Double-click to open in browser!)")

if __name__ == "__main__":
    run_research_agent()