import json
import os
import re

# Paths
broken_file_path = r"C:\Users\user\Desktop\gpt\n8n-copilot\shots\Shorts_NextLevel_v7_ULTIMATE.json"
reference_file_path = r"C:\Users\user\Desktop\gpt\n8n-copilot\shots\쇼츠_고급.json"

# Load the broken file
with open(broken_file_path, 'r', encoding='utf-8') as f:
    broken_content = f.read()

# Load the reference file
with open(reference_file_path, 'r', encoding='utf-8') as f:
    ref_data = json.load(f)

ref_nodes = ref_data['nodes']

def get_node_by_name(name):
    for node in ref_nodes:
        if node['name'] == name:
            return node
    return None

# Nodes to add
nodes_to_add = []

# 1. Data Aggregator
data_agg = get_node_by_name("Data Aggregator")
if data_agg:
    data_agg['position'] = [400, -1000]
    nodes_to_add.append(data_agg)

# 2. FFmpeg Script Gen
ffmpeg_gen = get_node_by_name("Simple Video Processor1")
if ffmpeg_gen:
    ffmpeg_gen['name'] = "FFmpeg Script Gen"
    ffmpeg_gen['position'] = [600, -1000]
    nodes_to_add.append(ffmpeg_gen)

# 3. Prep Script File
prep_script = get_node_by_name("File-based Script Executor1")
if prep_script:
    prep_script['name'] = "Prep Script File"
    prep_script['position'] = [800, -1000]
    nodes_to_add.append(prep_script)

# 4. Write Script File
write_script = get_node_by_name("Read/Write Files from Disk3")
if write_script:
    write_script['name'] = "Write Script File"
    write_script['position'] = [1000, -1000]
    nodes_to_add.append(write_script)

# 5. Execute FFmpeg Command
exec_ffmpeg = get_node_by_name("Execute Command3")
if exec_ffmpeg:
    exec_ffmpeg['name'] = "Execute FFmpeg Command"
    exec_ffmpeg['position'] = [1200, -1000]
    nodes_to_add.append(exec_ffmpeg)

# 6. Generate Metadata (GPT-5)
gen_meta = get_node_by_name("Metadata Generate1")
if gen_meta:
    gen_meta['name'] = "Generate Metadata (GPT-5)"
    gen_meta['position'] = [1400, -1000]
    if 'parameters' in gen_meta and 'modelId' in gen_meta['parameters']:
         gen_meta['parameters']['modelId']['value'] = "gpt-5.1-preview-2025-11-14"
         gen_meta['parameters']['modelId']['cachedResultName'] = "GPT-5.1-Preview"
    nodes_to_add.append(gen_meta)

# 7. YouTube Upload (KR)
yt_upload = get_node_by_name("Upload a video")
if yt_upload:
    yt_upload['name'] = "YouTube Upload (KR)"
    yt_upload['position'] = [1600, -1000]
    yt_upload['parameters']['regionCode'] = "KR"
    nodes_to_add.append(yt_upload)

# 8. Blotato Multi-Platform
blotato_node = {
    "parameters": {
        "method": "POST",
        "url": "https://api.blotato.com/v1/publish",
        "sendHeaders": True,
        "headerParameters": {
            "parameters": [
                {
                    "name": "blotato-api-key",
                    "value": "YOUR_BLOTATO_KEY"
                },
                {
                    "name": "Content-Type",
                    "value": "application/json"
                }
            ]
        },
        "sendBody": True,
        "jsonBody": "={\n  \"videoUrl\": \"{{ $json.videoUrl }}\",\n  \"title\": \"{{ $json.title }}\",\n  \"description\": \"{{ $json.description }}\",\n  \"platforms\": [\"instagram\", \"tiktok\", \"facebook\"]\n}",
        "options": {}
    },
    "name": "Blotato Multi-Platform",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": [1800, -1000],
    "id": "blotato_node"
}
nodes_to_add.append(blotato_node)

# 9. Log Final (AutoMap)
log_final = get_node_by_name("Update row in sheet3")
if log_final:
    log_final['name'] = "Log Final (AutoMap)"
    log_final['position'] = [2000, -1000]
    nodes_to_add.append(log_final)

# Fix the broken content
fixed_content = broken_content.strip()

# Find "Generate ASS Subtitles"
loc = fixed_content.rfind('"name": "Generate ASS Subtitles"')
if loc == -1:
    print("Error: Could not find Generate ASS Subtitles node")
    exit(1)

# Find the closing brace of the node
# We look for the next '}' after the name property
# But we need to be careful. The name property is inside the node object.
# The node object ends with '}'.
# Let's find the '}' that corresponds to the node object.
# Since we don't have nested objects AFTER the name property in this specific node (it's usually the last property or close to it),
# finding the next '}' should work, UNLESS "name" is followed by "credentials": { ... } or something.
# In the view_file output, "name" was the last property.
# 412: "name": "Generate ASS Subtitles"
# 413: }
# So finding the next '}' is safe.

end_of_node = fixed_content.find('}', loc)
if end_of_node == -1:
    print("Error: Could not find closing brace for node")
    exit(1)

# Cut the content there
valid_json_part = fixed_content[:end_of_node+1]

# Close the nodes array and the main object
valid_json_part += "]}"

# Parse it
try:
    current_data = json.loads(valid_json_part)
    current_nodes = current_data['nodes']
    print(f"Successfully parsed {len(current_nodes)} nodes from broken file.")
except json.JSONDecodeError as e:
    print(f"Error parsing fixed content: {e}")
    # Debug: print context around error
    print("Context around error:")
    print(valid_json_part[max(0, e.pos-100):min(len(valid_json_part), e.pos+100)])
    exit(1)

# Combine nodes
all_nodes = current_nodes + nodes_to_add

# Define Connections
connections = {
    "Daily Trigger": {
        "main": [[{"node": "Prepare New Data", "type": "main", "index": 0}]]
    },
    "Webhook": {
        "main": [[{"node": "If: Generate New?", "type": "main", "index": 0}]]
    },
    "If: Generate New?": {
        "main": [
            [{"node": "Prepare New Data", "type": "main", "index": 0}],
            []
        ]
    },
    "Prepare New Data": {
        "main": [[{"node": "Narration Script Generate", "type": "main", "index": 0}]]
    },
    "Narration Script Generate": {
        "main": [[{"node": "Script Parser", "type": "main", "index": 0}]]
    },
    "GPT-5.1 Model": {
        "ai_languageModel": [[{"node": "Narration Script Generate", "type": "ai_languageModel", "index": 0}]]
    },
    "Script Parser": {
        "main": [[{"node": "Log Script (AutoMap)", "type": "main", "index": 0}]]
    },
    "Log Script (AutoMap)": {
        "main": [[{"node": "Prepare Sentences", "type": "main", "index": 0}]]
    },
    "Prepare Sentences": {
        "main": [[{"node": "Split Sentences", "type": "main", "index": 0}]]
    },
    "Split Sentences": {
        "main": [[{"node": "Wait 3s", "type": "main", "index": 0}]]
    },
    "Wait 3s": {
        "main": [[{"node": "Generate Image Prompt", "type": "main", "index": 0}]]
    },
    "Generate Image Prompt": {
        "main": [[{"node": "NanoBanana Image Gen", "type": "main", "index": 0}]]
    },
    "GPT-5.1 Model (Image)": {
        "ai_languageModel": [[{"node": "Generate Image Prompt", "type": "ai_languageModel", "index": 0}]]
    },
    "NanoBanana Image Gen": {
        "main": [[{"node": "Sora-2 (OpenAI)", "type": "main", "index": 0}]]
    },
    "Sora-2 (OpenAI)": {
        "main": [[{"node": "OpenAI TTS", "type": "main", "index": 0}]]
    },
    "OpenAI TTS": {
        "main": [[{"node": "Whisper (Word-Level)", "type": "main", "index": 0}]]
    },
    "Whisper (Word-Level)": {
        "main": [[{"node": "Generate ASS Subtitles", "type": "main", "index": 0}]]
    },
    "Generate ASS Subtitles": {
        "main": [[{"node": "Data Aggregator", "type": "main", "index": 0}]]
    },
    "Data Aggregator": {
        "main": [[{"node": "FFmpeg Script Gen", "type": "main", "index": 0}]]
    },
    "FFmpeg Script Gen": {
        "main": [[{"node": "Prep Script File", "type": "main", "index": 0}]]
    },
    "Prep Script File": {
        "main": [[{"node": "Write Script File", "type": "main", "index": 0}]]
    },
    "Write Script File": {
        "main": [[{"node": "Execute FFmpeg Command", "type": "main", "index": 0}]]
    },
    "Execute FFmpeg Command": {
        "main": [[{"node": "Generate Metadata (GPT-5)", "type": "main", "index": 0}]]
    },
    "Generate Metadata (GPT-5)": {
        "main": [[{"node": "YouTube Upload (KR)", "type": "main", "index": 0}]]
    },
    "YouTube Upload (KR)": {
        "main": [[{"node": "Blotato Multi-Platform", "type": "main", "index": 0}]]
    },
    "Blotato Multi-Platform": {
        "main": [[{"node": "Log Final (AutoMap)", "type": "main", "index": 0}]]
    }
}

# Construct final JSON
final_workflow = {
    "name": "Shorts_NextLevel_v7_ULTIMATE",
    "nodes": all_nodes,
    "connections": connections,
    "meta": {
        "templateCredsSetupCompleted": True,
        "instanceId": "restored_v7_ultimate"
    }
}

# Write to file
with open(broken_file_path, 'w', encoding='utf-8') as f:
    json.dump(final_workflow, f, indent=2, ensure_ascii=False)

print("Successfully restored workflow file!")
print(f"Total nodes: {len(all_nodes)}")
