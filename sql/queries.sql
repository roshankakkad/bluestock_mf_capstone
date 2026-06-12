-- 1. Top 5 fund houses by latest AUM
SELECT fund_house, date, aum_crore
FROM fact_aum
WHERE date = (SELECT MAX(date) FROM fact_aum)
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV per month
SELECT amfi_code, strftime('%Y-%m', date) AS nav_month, ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
GROUP BY amfi_code, nav_month
ORDER BY amfi_code, nav_month;

-- 3. SIP inflow YoY growth
SELECT month, sip_inflow_crore, yoy_growth_pct
FROM fact_sip_industry
ORDER BY month;

-- 4. Transactions by state
SELECT state, COUNT(*) AS transaction_count, ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;

-- 5. Funds with expense ratio below 1%
SELECT amfi_code, scheme_name, fund_house, category, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;

-- 6. Top 10 schemes by Sharpe ratio
SELECT scheme_name, fund_house, category, sharpe_ratio
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 10;

-- 7. Total transaction amount by transaction type
SELECT transaction_type, COUNT(*) AS tx_count, ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount_inr DESC;

-- 8. Average SIP amount by age group
SELECT age_group, ROUND(AVG(amount_inr), 2) AS avg_sip_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY age_group
ORDER BY avg_sip_amount DESC;

-- 9. Best 5 funds by 3-year return
SELECT scheme_name, fund_house, category, return_3yr_pct
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 5;

-- 10. Funds with maximum drawdown worse than -20%
SELECT scheme_name, fund_house, category, max_drawdown_pct
FROM fact_performance
WHERE max_drawdown_pct < -20
ORDER BY max_drawdown_pct ASC;
