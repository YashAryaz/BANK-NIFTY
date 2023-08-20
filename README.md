# Trade Strategy based on SMA


## Requirements

To run this program, you need to have Python 3 installed on your system. You also need to install the following Python packages:

- pandas
- matplotlib

You can install them using pip:

```bash
pip install pandas matplotlib
```

## Usage

To run this program, you need to provide two arguments: the path to the index data file and the path to the option data file. For example:

```bash
python trade_strategy.py index_data.csv option_data.xlsx
```

The program will print some metrics on the console and show a plot of the trade outcomes. It will also create a file named `trades.csv` in the current directory, which contains the trade details.

## Explanation

The program defines a class named `TradeStrategy`, which has the following methods:

- `__init__(self, index_data_path, option_data_path)`: This is the constructor method that initializes the object with the index data and the option data. It reads the data from the given files and converts them to pandas dataframes. It also converts the date and time columns to datetime format and combines them into a single column named `Datetime`.
- `apply_sma_strategy(self)`: This method applies the SMA strategy to the index data and generates trade records. The SMA strategy is based on comparing the closing price of the index with its SMA value. If the SMA value is greater than or equal to the closing price, then a long position is taken. If the SMA value is less than the closing price, then a short position is taken. The position is closed when either a profit of 30 or a loss of 20 is reached. The trade records are stored in a list of dictionaries, each containing the entry time, entry price, exit time, exit price, type (long or short), and profit/loss of each trade.
- `calculate_metrics(self)`: This method calculates some metrics based on the trade records, such as total trades, success trades, success rate, and total profit. A success trade is defined as one that has a profit of 30 or more. The success rate is calculated as the ratio of success trades to total trades.
- `visualize_trade_outcomes(self)`: This method visualizes the trade outcomes using matplotlib. It plots the profit/loss of each trade against its entry time using green dots and gray lines. It also labels the axes and adds a title and a legend to the plot.
- `export_trade_details(self)`: This method exports the trade details to a CSV file named `trades.csv`. It converts the list of dictionaries to a pandas dataframe and writes it to the file.
- `print_metrics_and_insights(self)`: This function will print all the insights and metrices for evaluation.
- `run_strategy(self)`:This method runs the entire trade strategy from start to finish.
