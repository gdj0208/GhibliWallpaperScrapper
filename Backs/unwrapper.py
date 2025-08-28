import json

def unwrap_json(json_file):
    try:
        # JSON 파일을 열어서 딕셔너리로 로드합니다.
        with open(json_file, 'r', encoding='utf-8') as f:
            new_file = json.load(f)
    except FileNotFoundError:
        print(f"❌ 오류: '{json_file}' 파일을 찾을 수 없습니다.")
        return

    return new_file