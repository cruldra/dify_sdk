if __name__ == '__main__':
    json_str = """data: {"event": "text_chunk", "workflow_run_id": "ca2418bb-f632-40f5-9e41-40631b41bce4", "task_id": "aa10a505-e917-4ede-adea-457c4e895f0c", "data": {"text": "\\n\\n", "from_variable_selector": ["1741574867294", "text"]}}\n\ndata: {"event": "text_chunk", "workflow_run_id": "ca2418bb-f632-40f5-9e41-40631b41bce4", "task_id": "aa10a505-e917-4ede-adea-457c4e895f0c", "data": {"text": "\\ud83d\\udc49", "from_variable_selector": ["1741574867294", "text"]}}\n\n"""

    import json

    # 按SSE事件格式拆分
    events = []
    for line in json_str.split('\n\n'):
        if line.startswith('data: '):
            # 提取data后的JSON部分
            json_data = line[6:]  # 去掉"data: "前缀
            try:
                parsed_data = json.loads(json_data)
                events.append(parsed_data)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")

    print(f"Successfully parsed {len(events)} events:")
    for i, event in enumerate(events):
        print(f"\nEvent {i + 1}:")
        print(json.dumps(event, indent=2))

        # 显示表情符号
        if 'data' in event and 'text' in event['data']:
            text = event['data']['text']
            print(f"Text content: {text}")