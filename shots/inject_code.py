import json
import os

source_path = r"C:\Users\user\Desktop\gpt\n8n-copilot\shots\쇼츠_고급.json"
target_path = r"C:\Users\user\Desktop\gpt\n8n-copilot\shots\Shorts_NextLevel_v7_ULTIMATE.json"

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def find_node_by_name(nodes, name):
    for node in nodes:
        if node.get('name') == name:
            return node
    return None

def main():
    print(f"Loading source: {source_path}")
    source_data = load_json(source_path)
    print(f"Loading target: {target_path}")
    target_data = load_json(target_path)

    # Mappings: (Source Node Name, Target Node Name)
    mappings = [
        ("Data Aggregator", "Data Aggregator"),
        ("Simple Video Processor1", "FFmpeg Script Gen"),
        ("whisper data processor1", "Generate ASS Subtitles")
    ]

    for source_name, target_name in mappings:
        source_node = find_node_by_name(source_data['nodes'], source_name)
        target_node = find_node_by_name(target_data['nodes'], target_name)

        if source_node and target_node:
            print(f"Injecting code from '{source_name}' to '{target_name}'...")
            
            # Extract jsCode
            js_code = source_node['parameters'].get('jsCode')
            
            if js_code:
                # Inject into target
                if 'parameters' not in target_node:
                    target_node['parameters'] = {}
                target_node['parameters']['jsCode'] = js_code
                print("  -> Success")
            else:
                print(f"  -> Warning: No jsCode found in source node '{source_name}'")
        else:
            print(f"  -> Error: Could not find node(s). Source: {source_name} ({'Found' if source_node else 'Missing'}), Target: {target_name} ({'Found' if target_node else 'Missing'})")

    print("Saving updated workflow...")
    save_json(target_path, target_data)
    print("Done.")

if __name__ == "__main__":
    main()
