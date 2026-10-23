import sys
import random
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

# Predefined static fallback stocks dataset architecture to avoid heavy API keys
STOCK_DATABASE = {
    "AAPL": {"name": "Apple Inc.", "price": 175.50, "history": [174.10, 173.80, 175.50]},
    "TSLA": {"name": "Tesla Inc.", "price": 180.20, "history": [182.40, 181.10, 180.20]},
    "GOOGL": {"name": "Alphabet Inc.", "price": 150.30, "history": [149.20, 148.90, 150.30]},
    "AMZN": {"name": "Amazon.com Inc.", "price": 178.40, "history": [176.50, 177.10, 178.40]},
    "MSFT": {"name": "Microsoft Corp.", "price": 420.10, "history": [418.50, 419.20, 420.10]}
}

class PortfolioPresenter:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        self.portfolio = {"AAPL": 10, "MSFT": 5} # Initial starting positions
        self.cash = 10000.00
        
    def calculate_metrics(self):
        total_value = self.cash
        shares_value = 0
        for symbol, qty in self.portfolio.items():
            shares_value += qty * STOCK_DATABASE[symbol]["price"]
        return total_value + shares_value, shares_value

    def generate_ui_blueprint(self, message):
        total_p, stock_p = self.calculate_metrics()
        
        # Define clean geometric dashboard slices
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=3)
        )
        self.layout["body"].split_row(
            Layout(name="market_grid", ratio=3),
            Layout(name="portfolio_grid", ratio=2)
        )
        
        # 1. Header Frame Component Configuration
        self.layout["header"].update(Panel(
            "[bold green]📈 CODEALPHA REAL-TIME ASSET INTERFACE[/bold green]", 
            style="bold cyan", 
            border_style="cyan"
        ))
        
        # 2. Market Values Component Configuration
        market_table = Table(title="Live Exchange Registry", expand=True)
        market_table.add_column("Symbol", style="cyan")
        market_table.add_column("Company")
        market_table.add_column("Price", justify="right")
        market_table.add_column("Trend", justify="center")
        
        for symbol, info in STOCK_DATABASE.items():
            prev = info["history"][-2] if len(info["history"]) > 1 else info["price"]
            change = info["price"] - prev
            trend_str = f"[green]+{change:.2f}[/green]" if change >= 0 else f"[red]{change:.2f}[/red]"
            market_table.add_row(symbol, info["name"], f"${info['price']:.2f}", trend_str)
            
        self.layout["body"]["market_grid"].update(Panel(market_table, border_style="blue"))
        
        # 3. Personal Positions Component Configuration
        user_table = Table(title="Active Inventory Positions", expand=True)
        user_table.add_column("Asset", style="yellow")
        user_table.add_column("Owned")
        user_table.add_column("Total Evaluation", justify="right")
        
        for symbol, qty in self.portfolio.items():
            val = qty * STOCK_DATABASE[symbol]["price"]
            user_table.add_row(symbol, str(qty), f"${val:.2f}")
            
        summary_text = f"\n[bold white]Liquid Cash Reserves:[/bold white] [green]${self.cash:.2f}[/green]\n"
        summary_text += f"[bold white]Net Wallet Value:[/bold white] [yellow]${total_p:.2f}[/yellow]"
        
        self.layout["body"]["portfolio_grid"].update(Panel(
            Layout_Group := f"{user_table}\n{summary_text}", 
            border_style="magenta"
        ))
        
        # 4. Footer Console Frame Component Configuration
        self.layout["footer"].update(Panel(f"💬 Prompt Update: {message}", border_style="white"))
        return self.layout

def main():
    presenter = PortfolioPresenter()
    status_msg = "Engine ready. Choose actions: [B] Buy | [S] Sell | [Q] Quit"
    
    # Clean system background thread initialization loop
    while True:
        # Simulate price ticks
        for symbol in STOCK_DATABASE:
            change_pct = random.uniform(-0.02, 0.02)
            STOCK_DATABASE[symbol]["price"] = round(STOCK_DATABASE[symbol]["price"] * (1 + change_pct), 2)
            STOCK_DATABASE[symbol]["history"].append(STOCK_DATABASE[symbol]["price"])

        # Display static screen cleanly
        presenter.console.clear()
        ui_layout = presenter.generate_ui_blueprint(status_msg)
        presenter.console.print(ui_layout)
        
        action = input("\nEnter Action Token (B/S/Q): ").strip().upper()
        
        if action == "Q":
            presenter.console.clear()
            print("🚀 Sessions tracking finalized successfully. Goodbye!\n")
            break
            
        elif action == "B":
            sym = input("Enter Stock Symbol to Buy: ").strip().upper()
            if sym in STOCK_DATABASE:
                try:
                    qty = int(input(f"How many shares of {sym}?: "))
                    cost = qty * STOCK_DATABASE[sym]["price"]
                    if presenter.cash >= cost:
                        presenter.cash -= cost
                        presenter.portfolio[sym] = presenter.portfolio.get(sym, 0) + qty
                        status_msg = f"[green]Success![/green] Bought {qty} shares of {sym}."
                    else:
                        status_msg = "[red]Error![/red] Insufficient liquid cash tokens."
                except ValueError:
                    status_msg = "[red]Error![/red] Input quantity must be a whole integer numeric value."
            else:
                status_msg = f"[red]Error![/red] Target asset symbol '{sym}' missing from registry database."
                
        elif action == "S":
            sym = input("Enter Stock Symbol to Sell: ").strip().upper()
            if sym in presenter.portfolio:
                try:
                    qty = int(input(f"How many shares of {sym} to liquidate?: "))
                    if presenter.portfolio[sym] >= qty:
                        presenter.cash += qty * STOCK_DATABASE[sym]["price"]
                        presenter.portfolio[sym] -= qty
                        if presenter.portfolio[sym] == 0:
                            del presenter.portfolio[sym]
                        status_msg = f"[green]Success![/green] Disposed {qty} shares of {sym}."
                    else:
                        status_msg = "[red]Error![/red] Cannot short asset position. Insufficient quantity owned."
                except ValueError:
                    status_msg = "[red]Error![/red] Input quantity must be a whole integer numeric value."
            else:
                status_msg = f"[red]Error![/red] You do not own any open layout positions in '{sym}'."
        else:
            status_msg = "[yellow]Notice:[/yellow] Action key unrecognized. Try [B], [S], or [Q]."

if __name__ == "__main__":
    main()
