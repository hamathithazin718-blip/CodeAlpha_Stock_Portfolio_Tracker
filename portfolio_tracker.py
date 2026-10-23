import csv
import os
import random

# --- CORE DATA MATRIX & PRICE SIMULATION ---
BASE_STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "NVDA": 480.00,
    "MSFT": 370.00,
    "AMZN": 145.00
}

# Professional ANSI color constants for terminal styling
COLOR_CYAN = "\033[96m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"

def clear_screen():
    """Clears the terminal workspace dynamically across operating systems."""
    os.system('cls' if os.name == 'nt' else 'clear')

def render_header(title: str, size: int = 60, color: str = COLOR_CYAN):
    """Draws a premium styled dashboard panel border block."""
    print(f"{color}" + "=" * size)
    print(f"{title.center(size)}")
    print("=" * size + f"{COLOR_RESET}")

def get_simulated_market_prices():
    """Simulates live market prices with random volatility (-1.5% to +1.5%)."""
    current_market = {}
    for ticker, base_price in BASE_STOCK_PRICES.items():
        volatility = random.uniform(-0.015, 0.015)
        current_market[ticker] = round(base_price * (1 + volatility), 2)
    return current_market

class PortfolioTracker:
    def __init__(self):
        # User portfolio tracking dictionary: { TICKER: {"shares": Qty, "buy_price": Price} }
        self.portfolio = {}
        
    def add_or_update_stock(self, market_prices):
        """Validates input maps and attaches asset entries to the tracking map."""
        clear_screen()
        render_header("➕ ADD / UPDATE ASSET TRANSACTION")
        
        print(f"\n{COLOR_CYAN}Supported Market Tickers:{COLOR_RESET} {', '.join(BASE_STOCK_PRICES.keys())}")
        ticker = input("Enter Stock Ticker Symbol: ").strip().upper()
        
        if ticker not in market_prices:
            print(f"\n{COLOR_RED}❌ Asset Denied: Ticker '{ticker}' is not listed in our market matrix.{COLOR_RESET}")
            input("\nPress Enter to return to main menu...")
            return

        try:
            shares = float(input(f"Enter number of shares for {ticker}: "))
            buy_price = float(input(f"Enter your average purchase price per share ($): "))
            
            if shares <= 0 or buy_price <= 0:
                print(f"\n{COLOR_RED}❌ Numeric Error: Input metrics must be greater than zero.{COLOR_RESET}")
                input("\nPress Enter to return to main menu...")
                return
        except ValueError:
            print(f"\n{COLOR_RED}❌ Formatting Error: Please type valid numerical digits.{COLOR_RESET}")
            input("\nPress Enter to return to main menu...")
            return

        if ticker in self.portfolio:
            total_shares = self.portfolio[ticker]["shares"] + shares
            total_cost = (self.portfolio[ticker]["shares"] * self.portfolio[ticker]["buy_price"]) + (shares * buy_price)
            self.portfolio[ticker]["shares"] = total_shares
            self.portfolio[ticker]["buy_price"] = round(total_cost / total_shares, 2)
        else:
            self.portfolio[ticker] = {"shares": shares, "buy_price": buy_price}

        print(f"\n{COLOR_GREEN}✅ Transaction Recorded Successfully! Portfolio updated.{COLOR_RESET}")
        input("\nPress Enter to return to main menu...")

    def view_dashboard(self, market_prices):
        """Performs math calculations and outputs a clean tabular data dashboard."""
        clear_screen()
        render_header("📊 REAL-TIME INVESTMENT PORTFOLIO DASHBOARD")
        
        if not self.portfolio:
            print(f"\n{COLOR_YELLOW}⚠️ Your asset registry is empty. Add a stock position first!{COLOR_RESET}")
            input("\nPress Enter to return to main menu...")
            return

        total_cost_basis = 0.0
        total_current_value = 0.0
        calculated_rows = []
        
        for ticker, data in self.portfolio.items():
            qty = data["shares"]
            avg_buy = data["buy_price"]
            curr_price = market_prices[ticker]
            
            cost_basis = qty * avg_buy
            current_value = qty * curr_price
            profit_loss = current_value - cost_basis
            
            total_cost_basis += cost_basis
            total_current_value += current_value
            
            calculated_rows.append({
                "ticker": ticker, "qty": qty, "buy": avg_buy, 
                "curr": curr_price, "val": current_value, "pl": profit_loss
            })

        print(f"{COLOR_CYAN}{'TICKER':<8}{'SHARES':<10}{'AVG BUY':<12}{'MARKET':<12}{'VALUE':<12}{'PROFIT/LOSS':<12}{COLOR_RESET}")
        print("-" * 68)
        
        for row in calculated_rows:
            pl_color = COLOR_GREEN if row["pl"] >= 0 else COLOR_RED
            pl_sign = "+" if row["pl"] >= 0 else ""
            
            print(f"{row['ticker']:<8}"
                  f"{row['qty']:<10.2f}"
                  f"${row['buy']:<11.2f}"
                  f"${row['curr']:<11.2f}"
                  f"${row['val']:<11.2f}"
                  f"{pl_color}{pl_sign}${row['pl']:<11.2f}{COLOR_RESET}")
        
        print("-" * 68)
        
        total_pl = total_current_value - total_cost_basis
        summary_color = COLOR_GREEN if total_pl >= 0 else COLOR_RED
        summary_sign = "+" if total_pl >= 0 else ""
        
        print(f"{COLOR_CYAN}Total Cost Invested:{COLOR_RESET}  ${total_cost_basis:.2f}")
        print(f"{COLOR_CYAN}Current Portfolio Value:{COLOR_RESET} ${total_current_value:.2f}")
        print(f"{COLOR_CYAN}Total Net Returns: {COLOR_RESET}      {summary_color}{summary_sign}${total_pl:.2f}{COLOR_RESET}")
        
        print(f"\n{COLOR_CYAN}Portfolio Asset Allocations Matrix:{COLOR_RESET}")
        for row in calculated_rows:
            allocation_pct = (row["val"] / total_current_value) * 100
            bar_graph_ticks = int(allocation_pct / 5)
            print(f"  {row['ticker']:<5} [{COLOR_GREEN}{'#' * bar_graph_ticks:<20}{COLOR_RESET}] {allocation_pct:.1f}%")
            
        input("\nPress Enter to return to main menu...")

    def export_portfolio_statement(self, market_prices):
        """Exports the active tracker matrix into a clean external spreadsheet report."""
        clear_screen()
        render_header("💾 EXPORT STATEMENT PROCESSING")
        
        if not self.portfolio:
            print(f"\n{COLOR_RED}❌ Export Denied: No tracked data blocks inside the engine workspace.{COLOR_RESET}")
            input("\nPress Enter to return to main menu...")
            return
            
        filename = "CodeAlpha_Stock_Report.csv"
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Ticker", "Shares Held", "Avg Cost Basis ($)", "Market Price ($)", "Current Value ($)", "Net Gains ($)"])
                
                for ticker, data in self.portfolio.items():
                    qty = data["shares"]
                    avg_buy = data["buy_price"]
                    curr_price = market_prices[ticker]
                    val = qty * curr_price
                    pl = val - (qty * avg_buy)
                    writer.writerow([ticker, qty, avg_buy, curr_price, round(val, 2), round(pl, 2)])
                    
            print(f"\n{COLOR_GREEN}✅ Success! Report exported to file: {COLOR_YELLOW}'{filename}'{COLOR_RESET}")
        except IOError:
            print(f"\n{COLOR_RED}❌ Processing Error: Could not write statement log out to the external workspace.{COLOR_RESET}")
            
        input("\nPress Enter to return to main menu...")

def run_application_runtime():
    """Orchestrates runtime menus, active loops, and user actions."""
    tracker_instance = PortfolioTracker()
    
    while True:
        live_market = get_simulated_market_prices()
        clear_screen()
        render_header("📈 CODEALPHA PREMIUM STOCK ENGINE CONSOLE INTERFACE")
        print("\n📊 Select Operational Metric Control Trigger:")
        print("  [1] View Live Portfolio Dashboard & Allocations")
        print("  [2] Register Buy Transaction / Update Position")
        print("  [3] Export Current Financial Statement (.csv)")
        print("  [4] Terminate Active Tracking Session & Exit")
        print("-" * 60)
        
        user_selection = input("Enter Option Selection (1-4): ").strip()
        
        if user_selection == "1":
            tracker_instance.view_dashboard(live_market)
        elif user_selection == "2":
            tracker_instance.add_or_update_stock(live_market)
        elif user_selection == "3":
            tracker_instance.export_portfolio_statement(live_market)
        elif user_selection == "4":
            clear_screen()
            render_header("👋 TRACKING CONTROL PANEL CLOSED")
            print("Session metrics cleared from memory. Good luck investing!\n")
            break
        else:
            print(f"\n{COLOR_RED}❌ Entry Error: Option selection must be between 1 and 4.{COLOR_RESET}")
            input("Press Enter to refresh runtime screen options...")

if __name__ == "__main__":
    run_application_runtime()
