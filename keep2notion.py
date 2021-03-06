import json
import os
from pprint import pprint

KEEP_PATH = 'takeout-20210306T143034Z-001\\Takeout\\Keep'
NOTION_PATH = 'notion_export'


def main():
    if not os.path.isdir(NOTION_PATH):
        os.makedirs(NOTION_PATH)

    for file_name in os.listdir(KEEP_PATH):
        _, ext = os.path.splitext(file_name)
        if ext != '.json':
            continue

        print(f'Processing {file_name}...')
        with open(os.path.join(KEEP_PATH, file_name), encoding='utf-8') as f:
            json_obj = json.load(f)

        title = json_obj['title']
        if 'attachments' in json_obj:
            title = f'*** {title}'
        time = json_obj['userEditedTimestampUsec']
        output_path = os.path.join(NOTION_PATH, f'{time}.md')
        f = open(output_path, 'w', encoding='utf-8')
        f.write(f'# {title}\n\n')

        if 'attachments' in json_obj:
            attachments = json_obj['attachments']
            for item in attachments:
                item_path = item['filePath']
                f.write(f'*** {item_path}\n\n')
        
        if 'listContent' in json_obj:
            content = json_obj['listContent']
            for item in content:
                text = item['text']
                is_checked = item['isChecked']
                checked_char = 'x' if is_checked else ' '
                f.write(f'- [{checked_char}] {text}\n')

        else:
            content = json_obj['textContent']
            f.write(content.replace('\n', '\n\n'))

        f.close()

if __name__ == '__main__':
    main()
