CREATE VIEW ohlcv AS
WITH opens AS (
    SELECT DISTINCT ON(ticker, DATE(timestamp)) open, DATE(timestamp) AS day, ticker FROM intraday_prices ORDER BY ticker, day, timestamp ASC
),
closes AS (
    SELECT DISTINCT ON(ticker, DATE(timestamp)) close, DATE(timestamp) AS day, ticker FROM intraday_prices ORDER BY ticker, day, timestamp DESC
),
rest AS (
    SELECT ticker, DATE(timestamp) AS day, MAX(high) AS max, MIN(low) AS min, SUM(volume) AS volume FROM intraday_prices GROUP BY day, ticker ORDER BY ticker, day
)
SELECT rest.ticker, rest.day, opens.open, closes.close, rest.max, rest.min, rest.volume 
FROM opens JOIN closes ON opens.ticker = closes.ticker AND opens.day = closes.day
JOIN rest ON opens.ticker = rest.ticker AND opens.day = rest.day;