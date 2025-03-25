import pandas as pd
import time
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True) 

class FraudDetector:
    def __init__(self, data_path):
        self.data = pd.read_excel(data_path)
        self.user_profiles = {}
        self.alert_count = 0
        
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data = self.data.sort_values('timestamp')
        
    def _update_user_profile(self, transaction):
        user_id = transaction['user_id']
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'transaction_count': 0,
                'avg_amount': 0,
                'common_country': transaction['country'],
                'common_device': transaction['device'],
                'last_transaction_time': None
            }
        
        profile = self.user_profiles[user_id]
        
        profile['transaction_count'] += 1
        profile['avg_amount'] = ((profile['avg_amount'] * (profile['transaction_count'] - 1) + 
                                transaction['amount']) / profile['transaction_count'])
        
        if transaction['country'] != profile['common_country']:
            profile['common_country'] = max(
                [profile['common_country'], transaction['country']],
                key=lambda x: list(self.data[self.data['user_id'] == user_id]['country']).count(x)
            )
        
        if transaction['device'] != profile['common_device']:
            profile['common_device'] = max(
                [profile['common_device'], transaction['device']],
                key=lambda x: list(self.data[self.data['user_id'] == user_id]['device']).count(x)
            )
        
        profile['last_transaction_time'] = transaction['timestamp']

    def _check_anomalies(self, transaction):
        alerts = []
        user_id = transaction['user_id']
        profile = self.user_profiles.get(user_id, {})

        # 1. Amount significantly above average
        if transaction['amount'] > 3 * profile.get('avg_amount', 0):
            alerts.append(f"Amount {transaction['amount']} > 3x user average ({profile['avg_amount']:.2f})")

        # 2. Country change
        if transaction['country'] != profile.get('common_country', 'N/A'):
            alerts.append(f"Unusual country: {transaction['country']} (expected: {profile['common_country']})")

        # 3. Different device
        if transaction['device'] != profile.get('common_device', 'N/A'):
            alerts.append(f"Unusual device: {transaction['device']}")

        # 4. Unusual time (00:00-05:00)
        if transaction['timestamp'].hour < 5:
            alerts.append(f"Suspicious time: {transaction['timestamp'].strftime('%H:%M')}")

        # 5. High-risk categories
        if transaction['category'] in ['Travel', 'Electronics']:
            alerts.append(f"High-risk category: {transaction['category']}")

        return alerts

    def simulate_real_time_detection(self, delay=1):
        print(Fore.CYAN + "\nStarting real-time transaction monitoring...\n")
        
        for idx, row in self.data.iterrows():
            transaction = row.to_dict()
            
            # Simulate real-time flow
            time.sleep(delay)
            
            # Update user profile
            self._update_user_profile(transaction)
            
            # Check for anomalies
            alerts = self._check_anomalies(transaction)
            
            if alerts:
                self.alert_count += 1
                self._print_alert(transaction, alerts)
                
            if (idx + 1) % 10 == 0:
                print(Fore.YELLOW + f"\nProgress: {idx + 1}/{len(self.data)} transactions analyzed | Alerts: {self.alert_count}")

        print(Fore.GREEN + "\nMonitoring completed!")

    def _print_alert(self, transaction, reasons):
        print(Fore.RED + "\n" + "═" * 60)
        print(Fore.RED + Style.BRIGHT + "⚠ POTENTIAL FRAUD ALERT ⚠")
        print(Fore.WHITE + f"Transaction ID: {transaction['transaction_id']}")
        print(Fore.WHITE + f"User: {transaction['user_id']} | Amount: {transaction['amount']} | Date: {transaction['timestamp']}")
        print(Fore.WHITE + f"Merchant: {transaction['merchant']} ({transaction['category']})")
        
        print(Fore.YELLOW + "\nAlert reasons:")
        for i, reason in enumerate(reasons, 1):
            print(Fore.YELLOW + f"{i}. {reason}")
        
        print(Fore.RED + "═" * 60 + "\n")

if __name__ == "__main__":
    detector = FraudDetector("transactions.xlsx")
    detector.simulate_real_time_detection(delay=2)