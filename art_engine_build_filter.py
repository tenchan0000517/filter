import os
import json
import shutil

def ensure_directory_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def clear_directory_content(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            os.remove(os.path.join(root, file))

def copy_files_based_on_property_patterns(json_folder, other_folder, property_patterns):
    base_folder = "filterbuild"
    ensure_directory_exists(base_folder)
    
    target_json_folder = os.path.join(base_folder, "filterjson")
    ensure_directory_exists(target_json_folder)
    clear_directory_content(target_json_folder)

    target_other_folder = os.path.join(base_folder, "filterimages")
    ensure_directory_exists(target_other_folder)
    clear_directory_content(target_other_folder)

    copied_files = []
    for file_name in os.listdir(json_folder):
        if file_name.endswith('.json'):
            try:
                with open(os.path.join(json_folder, file_name), 'r') as f:
                    data = json.load(f)
                    attribute_values = {item["value"] for item in data.get("attributes", [])}
                    if any(pattern.issubset(attribute_values) for pattern in property_patterns):
                        shutil.copy2(os.path.join(json_folder, file_name), target_json_folder)
                        copied_files.append(os.path.splitext(file_name)[0])
                        print(f"コピー完了：{file_name}")
            except json.JSONDecodeError:
                print(f"スキップ：ファイル '{file_name}' は不正なJSONフォーマットか、空のファイルの可能性があります。")
            except Exception as e:
                print(f"スキップ：ファイル '{file_name}' で予期しないエラーが発生しました。エラーメッセージ：{e}")

    for file_name in os.listdir(other_folder):
        base_name = os.path.splitext(file_name)[0]
        if base_name in copied_files:
            shutil.copy2(os.path.join(other_folder, file_name), target_other_folder)
            print(f"2つ目のフォルダからコピー完了：{file_name}")

    print("処理完了")

if __name__ == "__main__":
    print("こちらを実行するとfilterjsonフォルダとfilterimagesフォルダは上書きされます。")
    print("必要な場合はバックアップを取ってにゃ！")
    input("続行するにはエンターキーを押してください...")
    # ユーザー入力
    json_folder = input("buildされたjsonフォルダのパスを入力してください（元データ）：")
    other_folder = input("buildされたimagesのフォルダのパスを入力してください（元データ）：")
    
    # 以下の部分でプロパティパターンを直接コード上で指定
    property_patterns = [
        {'Water Ripples', 'Mallet of Luck'},  # プロパティパターン１
        {'Crane', 'Straw Sandals'}   # プロパティパターン２
        # 必要に応じて、他のパターンも追加できます
    ]

    copy_files_based_on_property_patterns(json_folder, other_folder, property_patterns)
