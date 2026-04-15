import csv
import os
import random
from faker import Faker
from datetime import datetime

def generate_data(filename="data/seed_data.csv", row_count=1000):
    fake = Faker()
    
    print("="*50)
    print("DISCORD DATA GENERATOR")
    print("="*50)

    if not os.path.exists('data'):
        os.makedirs('data')

    headers = [
        'owner_name', 'owner_email', 'owner_since', 
        'server_name', 'invite_code', 'role_name', 
        'member_nickname', 'member_email', 
        'channel_title', 'is_locked', 'slow_mode', 
        'message_content', 'message_timestamp'
    ]

    print(f"[1/2] Pre-generating 15 servers and 200 unique users...")
    
    servers = []
    for _ in range(15):  
        owner_email = fake.unique.email()
        servers.append({
            'owner_name': fake.name(),
            'owner_email': owner_email,
            'owner_since': fake.date_time_this_decade().isoformat(),
            'server_name': f"{fake.company()} Official Discord",
            'invite_code': fake.bothify(text='??-####').upper(),
            'channels': [
                {'title': 'general', 'locked': 'False', 'slow': '0'},
                {'title': 'rules', 'locked': 'True', 'slow': '0'},
                {'title': 'announcements', 'locked': 'True', 'slow': '0'},
                {'title': 'voice-chat', 'locked': 'False', 'slow': '0'},
                {'title': 'dev-logs', 'locked': 'False', 'slow': '15'},
                {'title': 'memes', 'locked': 'False', 'slow': '5'}
            ],
            'roles': ['Admin', 'Moderator', 'VIP', 'Veteran', 'Contributor', 'Newbie']
        })

    users = []
    for _ in range(200): 
        users.append({
            'name': fake.user_name(),
            'email': fake.unique.email()
        })

    print(f"[2/2] Synthesizing {row_count} activity rows...")
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        for i in range(row_count):
            server = random.choice(servers)
            channel = random.choice(server['channels'])
            user = random.choice(users)
            
            writer.writerow({
                'owner_name': server['owner_name'],
                'owner_email': server['owner_email'],
                'owner_since': server['owner_since'],
                'server_name': server['server_name'],
                'invite_code': server['invite_code'],
                'role_name': random.choice(server['roles']),
                'member_nickname': user['name'],
                'member_email': user['email'],
                'channel_title': channel['title'],
                'is_locked': channel['locked'],
                'slow_mode': channel['slow'],
                'message_content': fake.sentence(nb_words=random.randint(5, 20)),
                'message_timestamp': fake.date_time_this_year().isoformat()
            })

    print("-" * 50)
    print(f"GENERATION STATUS: SUCCESS")
    print(f"Output File: {filename}")
    print(f"Total Rows:  {row_count}")
    print("="*50)

if __name__ == "__main__":
    generate_data()