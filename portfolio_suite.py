import csv
import os
import random

# --- STYLING & UTILITY CONSTANTS ---
COLOR_CYAN = "\033[96m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"

# Stock Constants
BASE_STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "NVDA": 480.00,
    "MSFT": 370.00,
    "AMZN": 145.00
}

def clear_screen():
    """Clears the terminal workspace dynamically across operating systems."""
    os.system('cls' if os.name == 'nt' else 'clear')

def render_header(title: str, size: int = 60, color: str = COLOR_CYAN):
    """Draws a premium styled dashboard panel border block."""
    print(f"{color}" + "=" * size)
    print(f"{title.center(size)}")
    print("=" * size + f"{COLOR_RESET}")


# ==========================================
# 📊 MODULE 1: STOCK PORTFOLIO ENGINE
# ==========================================
class StockPortfolioEngine:
    def __init__(self):
        self.portfolio = {}
        
    def get_simulated_market_prices(self):
        current_market = {}
        for ticker, base_price in BASE_STOCK_PRICES.items():
            volatility = random.uniform(-0.015, 0.015)
            current_market[ticker] = round(base_price * (1 + volatility), 2)
        return current_market

    def add_or_update_stock(self, market_prices):
        clear_screen()
        render_header("➕ ADD / UPDATE ASSET TRANSACTION")
        print(f"\n{COLOR_CYAN}Supported Market Tickers:{COLOR_RESET} {', '.join(BASE_STOCK_PRICES.keys())}")
        ticker = input("Enter Stock Ticker Symbol: ").strip().upper()
        
        if ticker not in market_prices:
            print(f"\n{COLOR_RED}❌ Asset Denied: Ticker '{ticker}' is not listed.{COLOR_RESET}")
            input("\nPress Enter to return...")
            return

        try:
            shares = float(input(f"Enter number of shares for {ticker}: "))
            buy_price = float(input(f"Enter purchase price per share ($): "))
            if shares <= 0 or buy_price <= 0:
                print(f"\n{COLOR_RED}❌ Numeric Error: Input metrics must be greater than zero.{COLOR_RESET}")
                input("\nPress Enter to return...")
                return
        except ValueError:
            print(f"\n{COLOR_RED}❌ Formatting Error: Input valid numbers.{COLOR_RESET}")
            input("\nPress Enter to return...")
            return

        if ticker in self.portfolio:
            total_shares = self.portfolio[ticker]["shares"] + shares
            total_cost = (self.portfolio[ticker]["shares"] * self.portfolio[ticker]["buy_price"]) + (shares * buy_price)
            self.portfolio[ticker]["shares"] = total_shares
            self.portfolio[ticker]["buy_price"] = round(total_cost / total_shares, 2)
        else:
            self.portfolio[ticker] = {"shares": shares, "buy_price": buy_price}

        print(f"\n{COLOR_GREEN}✅ Transaction Recorded Successfully!{COLOR_RESET}")
        input("\nPress Enter to return...")

    def view_dashboard(self, market_prices):
        clear_screen()
        render_header("📊 PORTFOLIO INVESTMENT DASHBOARD")
        if not self.portfolio:
            print(f"\n{COLOR_YELLOW}⚠️ Your asset registry is empty.{COLOR_RESET}")
            input("\nPress Enter to return...")
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
            calculated_rows.append({"ticker": ticker, "qty": qty, "buy": avg_buy, "curr": curr_price, "val": current_value, "pl": profit_loss})

        print(f"{COLOR_CYAN}{'TICKER':<8}{'SHARES':<10}{'AVG BUY':<12}{'MARKET':<12}{'VALUE':<12}{'PROFIT/LOSS':<12}{COLOR_RESET}")
        print("-" * 68)
        for row in calculated_rows:
            pl_color = COLOR_GREEN if row["pl"] >= 0 else COLOR_RED
            pl_sign = "+" if row["pl"] >= 0 else ""
            print(f"{row['ticker']:<8}{row['qty']:<10.2f}${row['buy']:<11.2f}${row['curr']:<11.2f}${row['val']:<11.2f}{pl_color}{pl_sign}${row['pl']:<11.2f}{COLOR_RESET}")
        print("-" * 68)
        
        total_pl = total_current_value - total_cost_basis
        summary_color = COLOR_GREEN if total_pl >= 0 else COLOR_RED
        print(f"{COLOR_CYAN}Total Invested:{COLOR_RESET}  ${total_cost_basis:.2f}  |  {COLOR_CYAN}Current Value:{COLOR_RESET} ${total_current_value:.2f}")
        print(f"{COLOR_CYAN}Total net Profit/Loss:{COLOR_RESET} {summary_color}${total_pl:.2f}{COLOR_RESET}")
        input("\nPress Enter to return...")

    def export_portfolio_statement(self, market_prices):
        clear_screen()
        render_header("💾 EXPORT STATEMENT PROCESSING")
        if not self.portfolio:
            print(f"\n{COLOR_RED}❌ Export Denied: No tracked data blocks.{COLOR_RESET}")
            input("\nPress Enter to return...")
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
            print(f"\n{COLOR_GREEN}✅ Success! Report exported to: {COLOR_YELLOW}'{filename}'{COLOR_RESET}")
        except IOError:
            print(f"\n{COLOR_RED}❌ Processing Error: Could not write statement file.{COLOR_RESET}")
        input("\nPress Enter to return...")

    def run_sub_menu(self):
        while True:
            live_market = self.get_simulated_market_prices()
            clear_screen()
            render_header("📈 STOCK SYSTEM INTERFACE MATRIX")
            print("\n  [1] View Live Portfolio Dashboard")
            print("  [2] Register Buy Transaction / Update Position")
            print("  [3] Export Current Financial Statement (.csv)")
            print("  [4] Back to Main System Suite Menu")
            print("-" * 60)
            choice = input("Enter Choice (1-4): ").strip()
            if choice == "1":
                self.view_dashboard(live_market)
            elif choice == "2":
                self.add_or_update_stock(live_market)
            elif choice == "3":
                self.export_portfolio_statement(live_market)
            elif choice == "4":
                break


# ==========================================
# 🎮 MODULE 2: REFACTORED HANGMAN GAME ENGINE
# ==========================================
class LegacyGameEngine:
    def __init__(self):
        self.words = ["python", "variable", "compiler", "function", "database"]

    def start_game(self):
        secret_word = random.choice(self.words)
        guessed_letters = []
        lives_left = 6
        status_msg = "Game initialization complete. Type a letter!"

        while lives_left > 0:
            clear_screen()
            render_header("🎮 TERMINAL HANGMAN ENVIRONMENT", color=COLOR_YELLOW)
            
            mask_display = [char if char in guessed_letters else "_" for char in secret_word]
            print(f"\nWord Target sequence:  {COLOR_GREEN}{' '.join(mask_display)}{COLOR_RESET}\n")
            print(f"Remaining Lives Allowed: {COLOR_RED}{lives_left}{COLOR_RESET}")
            print(f"Letters Guessed: {COLOR_CYAN}{', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}{COLOR_RESET}")
            print("-" * 60)
            print(f"System Message: {status_msg}")
            print("-" * 60)

            if "_" not in mask_display:
                print(f"\n{COLOR_GREEN}🎉 VICTORY! You guessed the word: {secret_word.upper()}{COLOR_RESET}\n")
                break

            user_guess = input("Submit Letter: ").strip().lower()
            if len(user_guess) != 1 or not user_guess.isalpha():
                status_msg = f"{COLOR_RED}⚠️ Error: Entry requires a single alphabetic character.{COLOR_RESET}"
                continue
            if user_guess in guessed_letters:
                status_msg = f"{COLOR_YELLOW}⚠️ Warning: '{user_guess.upper()}' was already processed.{COLOR_RESET}"
                continue

            guessed_letters.append(user_guess)
            if user_guess in secret_word:
                status_msg = f"{COLOR_GREEN}✅ Correct choice!{COLOR_RESET}"
            else:
                status_msg = f"{COLOR_RED}❌ Incorrect choice!{COLOR_RESET}"
                lives_left -= 1

        if lives_left == 0:
            clear_screen()
            render_header("💀 DEFEAT DIAGNOSTIC", color=COLOR_RED)
            print(f"\nOut of runtime attempts. Word was: {COLOR_YELLOW}{secret_word.upper()}{COLOR_RESET}\n")
        
        input("Press Enter to return to main menu...")


# ==========================================
# 🚀 CORE SYSTEM ORCHESTRATOR
# ==========================================
def main_suite_runtime():
    portfolio_module = StockPortfolioEngine()
    game_module = LegacyGameEngine()

    while True:
        clear_screen()
        render_header("🚀 CODEALPHA UNIFIED MULTI-UTILITY ENGINE SUITE")
        print("\n⚡ Select System Engine Application to Boot:")
        print(f"  [{COLOR_CYAN}1{COLOR_RESET}] Launch Real-Time Stock Portfolio Tracker Engine")
        print(f"  [{COLOR_YELLOW}2{COLOR_RESET}] Launch Terminal Hangman Game Engine Instance")                 
        print(f"  [{COLOR_RED}3{COLOR_RESET}] Safely Close Core Session & Terminate Runtimes")
        print(f"  [{COLOR_RED}Q{COLOR_RESET}] Exit CodeAlpha Suite")   
        print("-" * 60)
        user_selection = input("Enter System Option Selection (1-3): ").strip().upper()
        if user_selection == "1":
            portfolio_module.run_sub_menu()
        elif user_selection == "2":
            game_module.start_game()
        elif user_selection in ("3", "Q"):
            clear_screen()
            render_header("🏁 CORE TERMINATION SEQUENCE COMPLETE")
            print("All active software submodules detached safely. Goodbye!\n")
            break
        else:
            print(f"\n{COLOR_RED}❌ System Entry Error: Selection target must map exactly to choices [1-3].{COLOR_RESET}")
        input("Press Enter to refresh structural system choices...")
if __name__ == "__main__":
    main_suite_runtime()