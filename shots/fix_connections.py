import json

# Paths
workflow_file = r"C:\Users\user\Desktop\gpt\n8n-copilot\shots\Shorts_NextLevel_v7_ULTIMATE.json"
reference_file = r"C:\Users\user\Desktop\gpt\n8n-copilot\shots\쇼츠_고급.json"

# Load files
with open(workflow_file, 'r', encoding='utf-8') as f:
    try:
        workflow = json.load(f)
    except json.JSONDecodeError:
        print("Current workflow is corrupted, loading from backup...")
        # Read the file as text and try to extract nodes
        f.seek(0)
        content = f.read()
        # Find the nodes array
        nodes_start = content.find('"nodes": [')
        if nodes_start == -1:
            print("Error: Could not find nodes array")
            exit(1)
        # Extract up to the connections section
        nodes_end = content.find('"connections": {', nodes_start)
        if nodes_end == -1:
            print("Error: Could not find connections section")
            exit(1)
        # Create a minimal valid JSON
        nodes_section = content[nodes_start:nodes_end-2]  # Remove trailing comma
        temp_json = '{' + nodes_section + ']}'
        workflow = json.loads(temp_json)

with open(reference_file, 'r', encoding='utf-8') as f:
    reference = json.load(f)

# Define the correct connections
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

# Rebuild the workflow
final_workflow = {
    "name": "Shorts_NextLevel_v7_ULTIMATE",
    "nodes": workflow['nodes'],
    "connections": connections,
    "meta": {
        "templateCredsSetupCompleted": True,
        "instanceId": "restored_v7_ultimate_final"
    }
}

# Save
with open(workflow_file, 'w', encoding='utf-8') as f:
    json.dump(final_workflow, f, indent=2, ensure_ascii=False)

print("✅ Workflow connections fixed!")
print(f"Total nodes: {len(workflow['nodes'])}")
print("\nConnection flow:")
print("1. Narration Script Generate → Script Parser")
print("2. Script Parser → Log Script (AutoMap)")
print("3. Log Script (AutoMap) → Prepare Sentences")
print("... (rest of the workflow)")
