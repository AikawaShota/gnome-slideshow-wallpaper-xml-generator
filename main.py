import os
import random
import xml.etree.ElementTree as ET
import click

def extract_image_paths(directory_path):
    """
    指定されたディレクトリ内の画像ファイルの絶対パスを抽出します。

    Args:
        directory_path (str): 画像ファイルを検索するディレクトリのパス。

    Returns:
        list: 見つかった画像ファイルの絶対パスのリスト。
    """
    image_extensions = ('.jpg', '.jpeg', '.png', '.svg')
    image_paths = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(image_extensions):
                absolute_path = os.path.abspath(os.path.join(root, file))
                image_paths.append(absolute_path)

    return image_paths

def get_random_images(image_paths):
    shuffled_list = random.sample(image_paths, len(image_paths))
    return shuffled_list

def create_background_xml(image_paths, start_year="2000", start_month="00", start_day="00", start_hour="00", start_minute="00", start_second="00", static_duration=300.0, transition_duration=5.0):
    """
    指定された画像パスリストからbackground.xmlファイルを生成します。

    Args:
        image_paths (list): 画像ファイルのパスのリスト。
        start_year (str): 開始年。
        start_month (str): 開始月。
        start_day (str): 開始日。
        start_hour (str): 開始時。
        start_minute (str): 開始分。
        start_second (str): 開始秒。
        static_duration (float): static要素のduration（秒）。
        transition_duration (float): transition要素のduration（秒）。

    Returns:
        str: 生成されたXML文字列。
    """
    # ルート要素を作成
    background = ET.Element("background")

    # starttime要素を作成
    starttime = ET.SubElement(background, "starttime")
    ET.SubElement(starttime, "year").text = str(start_year)
    ET.SubElement(starttime, "month").text = str(start_month)
    ET.SubElement(starttime, "day").text = str(start_day)
    ET.SubElement(starttime, "hour").text = str(start_hour)
    ET.SubElement(starttime, "minute").text = str(start_minute)
    ET.SubElement(starttime, "second").text = str(start_second)

    # 画像パスリストに基づいてstaticとtransition要素を作成
    for i in range(len(image_paths)):
        # static要素
        static = ET.SubElement(background, "static")
        ET.SubElement(static, "duration").text = str(static_duration)
        ET.SubElement(static, "file").text = image_paths[i]

        # transition要素（最後の画像以外）
        if i < len(image_paths) - 1:
            transition = ET.SubElement(background, "transition")
            ET.SubElement(transition, "duration").text = str(transition_duration)
            ET.SubElement(transition, "from").text = image_paths[i]
            ET.SubElement(transition, "to").text = image_paths[i+1]
    
    # transition要素（最後）
    transition = ET.SubElement(background, "transition")
    ET.SubElement(transition, "duration").text = str(transition_duration)
    ET.SubElement(transition, "from").text = image_paths[i]
    ET.SubElement(transition, "to").text = image_paths[0]

    # XMLツリーを文字列に変換
    tree = ET.ElementTree(background)
    # インデント付きで整形
    ET.indent(tree, space="  ")
    xml_string = ET.tostring(background, encoding='unicode')

    return xml_string

@click.command()
@click.option(
    "--target-directory",
    "-t",
    required=True,
    type=click.Path(exists=True, file_okay=False, readable=True, path_type=str),
    help="画像ファイルを検索するディレクトリ",
)
@click.option(
    "--output-file",
    "-o",
    default="./output.xml",
    show_default=True,
    type=click.Path(dir_okay=False, writable=True, path_type=str),
    help="生成するXMLの出力先ファイルパス",
)
def cli(target_directory, output_file):
    """GNOME スライドショー用 background.xml を生成する CLI。"""

    if not os.path.isdir(target_directory):
        raise click.ClickException(f"指定されたディレクトリが存在しません: {target_directory}")

    found_image_paths = extract_image_paths(target_directory)
    if not found_image_paths:
        raise click.ClickException(f"画像ファイルが見つかりませんでした: {target_directory}")

    shuffled_image_paths = get_random_images(found_image_paths)
    xml_output = create_background_xml(image_paths=shuffled_image_paths)

    output_dir = os.path.dirname(os.path.abspath(output_file))
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(xml_output)
    except OSError as e:
        raise click.ClickException(f"ファイルを書き込めませんでした: {output_file} ({e})")

    click.echo(f"生成完了: {output_file}  画像数: {len(shuffled_image_paths)}")

if __name__ == "__main__":
    cli()
