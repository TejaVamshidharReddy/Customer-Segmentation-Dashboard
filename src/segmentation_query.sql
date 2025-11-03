-- Customer Segmentation Query for Power BI Dashboard
-- This SQL script creates customer segments based on RFM (Recency, Frequency, Monetary) analysis

-- Calculate RFM metrics for each customer
WITH CustomerRFM AS (
    SELECT 
        c.CustomerID,
        c.FirstName,
        c.LastName,
        c.Email,
        c.Age,
        c.Gender,
        c.Location,
        c.JoinDate,
        -- Recency: Days since last purchase
        DATEDIFF(day, MAX(t.TransactionDate), GETDATE()) AS Recency,
        -- Frequency: Number of purchases
        COUNT(DISTINCT t.TransactionID) AS Frequency,
        -- Monetary: Total amount spent
        SUM(t.Amount) AS Monetary,
        -- Additional metrics
        AVG(t.Amount) AS AvgTransactionValue,
        MAX(t.TransactionDate) AS LastPurchaseDate,
        MIN(t.TransactionDate) AS FirstPurchaseDate
    FROM 
        Customers c
    LEFT JOIN 
        Transactions t ON c.CustomerID = t.CustomerID
    GROUP BY 
        c.CustomerID, c.FirstName, c.LastName, c.Email, 
        c.Age, c.Gender, c.Location, c.JoinDate
),

-- Calculate RFM scores (1-5 scale)
RFMScores AS (
    SELECT 
        *,
        -- Recency Score (lower recency = higher score)
        NTILE(5) OVER (ORDER BY Recency DESC) AS R_Score,
        -- Frequency Score
        NTILE(5) OVER (ORDER BY Frequency ASC) AS F_Score,
        -- Monetary Score
        NTILE(5) OVER (ORDER BY Monetary ASC) AS M_Score
    FROM 
        CustomerRFM
),

-- Combine RFM scores and create segments
CustomerSegments AS (
    SELECT 
        *,
        (R_Score + F_Score + M_Score) / 3.0 AS RFM_Average,
        CASE 
            WHEN R_Score >= 4 AND F_Score >= 4 AND M_Score >= 4 THEN 'High-Value'
            WHEN R_Score >= 3 AND F_Score >= 3 AND M_Score >= 3 THEN 'Medium-Value'
            WHEN R_Score >= 4 AND F_Score <= 2 THEN 'New Customers'
            WHEN R_Score <= 2 AND F_Score >= 4 THEN 'At-Risk'
            WHEN R_Score <= 2 AND F_Score <= 2 THEN 'Lost'
            ELSE 'Low-Value'
        END AS CustomerSegment,
        -- Customer Lifetime (in days)
        DATEDIFF(day, FirstPurchaseDate, GETDATE()) AS CustomerLifetimeDays,
        -- Purchase frequency (purchases per day)
        CASE 
            WHEN DATEDIFF(day, FirstPurchaseDate, GETDATE()) > 0 
            THEN CAST(Frequency AS FLOAT) / DATEDIFF(day, FirstPurchaseDate, GETDATE())
            ELSE 0 
        END AS PurchaseFrequencyRate
    FROM 
        RFMScores
)

-- Final output with all customer segmentation data
SELECT 
    CustomerID,
    FirstName,
    LastName,
    Email,
    Age,
    Gender,
    Location,
    JoinDate,
    Recency,
    Frequency,
    Monetary,
    AvgTransactionValue,
    LastPurchaseDate,
    FirstPurchaseDate,
    R_Score,
    F_Score,
    M_Score,
    RFM_Average,
    CustomerSegment,
    CustomerLifetimeDays,
    PurchaseFrequencyRate,
    -- Additional calculated fields for dashboard
    CASE 
        WHEN Recency <= 30 THEN 'Active'
        WHEN Recency <= 90 THEN 'Occasional'
        WHEN Recency <= 180 THEN 'Dormant'
        ELSE 'Inactive'
    END AS ActivityStatus,
    CASE 
        WHEN DATEDIFF(day, JoinDate, GETDATE()) <= 90 THEN 'New'
        WHEN DATEDIFF(day, JoinDate, GETDATE()) <= 365 THEN 'Growing'
        ELSE 'Established'
    END AS CustomerMaturity
FROM 
    CustomerSegments
ORDER BY 
    Monetary DESC, Frequency DESC, Recency ASC;
