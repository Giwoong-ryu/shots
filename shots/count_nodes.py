import json
from collections import Counter

files = [
    r"C:\Users\user\Desktop\gpt\n8n-copilot\shots\쇼츠_고급.json",
    r"C:\Users\user\Desktop\gpt\n8n-copilot\shots\Shorts_NextLevel_v7_ULTIMATE.json"
]

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            nodes = data.get('nodes', [])
            
            print(f"\nAnalysis for: {file_path}")
            print(f"Total Nodes: {len(nodes)}")
            
            # Count by type
            type_counts = Counter(node['type'] for node in nodes)
            print("Node Types:")
            for type_name, count in type_counts.most_common():
                print(f"  {type_name}: {count}")
                
            # Count disabled nodes
            disabled_count = sum(1 for node in nodes if node.get('disabled') is True)
            print(f"Disabled Nodes: {disabled_count}")
            
            # Count Sticky Notes specifically
            sticky_count = sum(1 for node in nodes if 'stickyNote' in node['type'])
            print(f"Sticky Notes: {sticky_count}")

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
