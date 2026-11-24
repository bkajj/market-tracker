CREATE SCHEMA IF NOT EXISTS workspace.market_bronze
    COMMENT 'unprocessed stock data from StockData API';
CREATE VOLUME IF NOT EXISTS workspace.market_bronze.raw
    COMMENT 'raw JSON responses partitioned by interval and ticker, one file per date';

CREATE SCHEMA IF NOT EXISTS workspace.market_silver
    COMMENT 'flattened, deduplicated and typed intraday data';

CREATE SCHEMA IF NOT EXISTS workspace.market_gold
    COMMENT 'aggregated daily OHLCV with additional metrics';