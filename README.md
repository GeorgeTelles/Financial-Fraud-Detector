# Real-Time Fraud Detection System  
A financial transaction monitoring system designed to identify suspicious activities and potential fraud in real time. Using behavioral analysis and anomaly rules, the system evaluates transaction patterns to generate immediate alerts, enabling rapid response to potential risks.  

---  

## Key Features  
1. **User Behavioral Profiling**  
   - Creates dynamic profiles based on transaction history, including:  
     - Average spending amount  
     - Most frequent locations and devices  
     - Transaction frequency  
     - Typical activity hours  

2. **Anomaly Detection Criteria**  
   - **Atypical Value:** Transactions exceeding 3x the user's historical average.  
   - **Geographic Deviation:** Transactions from a country outside the user's usual pattern.  
   - **Unrecognized Device:** Use of devices not linked to the user's profile.  
   - **Suspicious Timeframe:** Transactions between 12 AM and 5 AM (low-activity hours).  
   - **High-Risk Categories:** Transactions in sensitive categories (e.g., Travel, Electronics).  

3. **Real-Time Simulation**  
   - Sequential transaction processing with configurable delays to mimic realistic workflows.  
   - Continuous user profile updates as new transactions are processed.  

4. **Visual Alert System**  
   - Color-coded terminal notifications (via `colorama`) highlighting:  
     - Suspicious transaction details  
     - Alert triggers  
     - Progressive alert counts  

---  

## Technologies and Libraries  
- **Pandas:** Transaction data processing and analysis.  
- **Colorama:** Colored terminal alerts for enhanced visibility.  
- **Datetime:** Timestamp handling and detection of unusual timings.  
- **Object-Oriented Design:** Modular code structure for scalability.  

---  

## Workflow  
1. **Data Input:**  
   - Load transactions from an Excel file (`transactions.xlsx`).  
   - Sort transactions chronologically to simulate real-time flow.  

2. **Profile Updates:**  
   - Maintain a dictionary of user profiles, updating metrics per transaction.  

3. **Anomaly Verification:**  
   - Apply predefined rules to each new transaction.  
   - Combine multiple criteria to improve alert accuracy.  

4. **Alert Output:**  
   - Display transaction details and alert reasons in red highlights.  
   - Provide periodic progress statistics (transactions analyzed/alerts triggered).  

---  

## Practical Applications  
- **Fraud Prevention:** Proactive identification of unusual transactions.  
- **Account Monitoring:** Detection of compromised accounts (e.g., unauthorized device access).  
- **Risk Analysis:** Flagging high-risk transactions for manual review.  
