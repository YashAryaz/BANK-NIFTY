#importing libraries
import pandas as pd
import matplotlib.pyplot as plt

class TradeStrategy:
    def __init__(self, index_data_path, option_data_path):
        self.index_data = pd.read_csv(index_data_path)
        self.option_data = pd.read_excel(option_data_path)
        self.index_data['sma_20']=self.index_data['<close>'].rolling(20).mean()
        self.index_data['Datetime'] = pd.to_datetime(self.index_data['<date>'] + ' ' + self.index_data['<time>'])
        # Convert <date> column to datetime format for option_data
        self.option_data['<date>'] = pd.to_datetime(self.option_data['<date>'])
        # Convert <time> column to timedelta format for option_data
        self.option_data['<time>'] = pd.to_timedelta(self.option_data['<time>'].astype(str))
        # Combine datetime information for option_data
        self.option_data['Datetime'] = self.option_data['<date>'] + self.option_data['<time>']
    import pandas as pd


    def apply_sma_strategy(self):
        active_trade = None
        trade_records = []
        prev_sma_value = None
        prev_close = None
        for idx, row in self.index_data.iterrows():
            if pd.to_datetime('09:30:00').time() <= row['Datetime'].time() <= pd.to_datetime('15:00:00').time():
                if prev_sma_value is None or prev_close is None:
                    prev_sma_value = row['SMA_value']
                    prev_close = row['<close>']
                    continue

                if active_trade is None:
                # Long Selling condition
                     if prev_sma_value >= prev_close and row['SMA_value'] < row['sma_20']:
                        active_trade = {'entry_time': row['Datetime'], 'entry_price': row['<close>'], 'type': 'Long'}
                        print("Entering Long trade at {}: Entry price: {}".format(active_trade['entry_time'], active_trade['entry_price']))
                # Short Selling condition
                     elif prev_sma_value < prev_close and row['SMA_value'] >= row['sma_20']:
                        active_trade = {'entry_time': row['Datetime'], 'entry_price': row['<close>'], 'type': 'Short'}
                        print("Entering Short trade at {}: Entry price: {}".format(active_trade['entry_time'], active_trade['entry_price']))
                else:
                    exit_price = row['<close>']
                    if active_trade['type'] == 'Long':
                        profit_loss = exit_price - active_trade['entry_price']
                        if profit_loss >= 30 or profit_loss <= -20:
                            active_trade['exit_time'] = row['Datetime']
                            active_trade['exit_price'] = exit_price
                            active_trade['profit/loss'] = profit_loss
                            trade_records.append(active_trade)
                            print("Exiting Long trade at {}: Exit price: {}, Profit/Loss: {}".format(active_trade['exit_time'], exit_price, profit_loss))
                            active_trade = None
                    elif active_trade['type'] == 'Short':
                        profit_loss = active_trade['entry_price'] - exit_price
                        if profit_loss >= 30 or profit_loss <= -20:
                            active_trade['exit_time'] = row['Datetime']
                            active_trade['exit_price'] = exit_price
                            active_trade['profit/loss'] = profit_loss
                            trade_records.append(active_trade)
                            print("Exiting Short trade at {}: Exit price: {}, Profit/Loss: {}".format(active_trade['exit_time'], exit_price, profit_loss))
                            active_trade = None


        self.trade_df = pd.DataFrame(trade_records)
        

    def calculate_metrics(self):
        self.total_trades = len(self.trade_df)
        self.success_trades = self.trade_df[self.trade_df['profit/loss'] >= 30]
        self.success_rate = len(self.success_trades) / self.total_trades if self.total_trades > 0 else 0
        self.total_profit = self.trade_df['profit/loss'].sum()

    def visualize_trade_outcomes(self):
      plt.figure(figsize=(12, 6))
      plt.plot(self.trade_df['entry_time'], self.trade_df['profit/loss'], marker='o', linestyle='', color='green', label='Profit')
      plt.plot(self.trade_df['entry_time'], self.trade_df['profit/loss'], linestyle='-', color='gray')
      plt.xlabel('Entry Time')
      plt.ylabel('Profit / Loss')
      plt.title('Trade Outcomes')
      plt.legend()
      plt.grid(True)
      plt.xticks(rotation=45)
      plt.tight_layout()
      plt.show()

    def export_trade_details(self):
        self.trade_df.to_csv("trades.csv", index=False)

    def print_metrics_and_insights(self):
        print("Analysis of Simple Moving Average (SMA) Strategy")
        print("Total Trades:", self.total_trades)
        print("Success Rate:", self.success_rate)
        print("Total Profit:", self.total_profit)
        print("Average Trade Duration:", self.trade_df['exit_time'].sub(self.trade_df['entry_time']).mean())
        print("Maximum Drawdown:", (self.trade_df['exit_price'] - self.trade_df['entry_price']).min())
        print("Average Risk-Reward Ratio:", (self.trade_df['profit/loss'] / 20).mean())

    def run_strategy(self):
        self.apply_sma_strategy()
        self.calculate_metrics()
        self.export_trade_details()
        self.print_metrics_and_insights()
        self.visualize_trade_outcomes()

if __name__ == "__main__":
    strategy = TradeStrategy("banknifty_data.csv",
                             "option_contract_data.xlsx")
    strategy.run_strategy()


