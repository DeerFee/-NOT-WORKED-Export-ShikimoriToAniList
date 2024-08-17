import xml.etree.ElementTree as ET
import xml.dom.minidom
import os

def read_shikimori_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def convert_to_anilist_format(shikimori_data):
    anilist_data = []
    for manga in shikimori_data.findall('manga'):
        tags = manga.find('my_tags')
        tags_str = tags.text if tags is not None and tags.text else ''
        
        anilist_entry = {
            'series_title': manga.find('series_title').text,
            'series_type': manga.find('series_type').text,
            'series_volumes': manga.find('series_volumes').text,
            'series_chapters': manga.find('series_chapters').text,
            'manga_mangadb_id': manga.find('manga_mangadb_id').text,
            'my_read_volumes': manga.find('my_read_volumes').text,
            'my_read_chapters': manga.find('my_read_chapters').text,
            'my_times_watched': manga.find('my_times_watched').text,
            'my_score': manga.find('my_score').text,
            'my_status': manga.find('my_status').text,
            'my_tags': tags_str,
            'my_comments': manga.find('my_comments').text or '',
            'update_on_import': manga.find('update_on_import').text or '1'
        }
        anilist_data.append(anilist_entry)
    return anilist_data

def create_anilist_xml(anilist_data, output_file):
    root = ET.Element('myanimelist')
    
    myinfo = ET.SubElement(root, 'myinfo')
    ET.SubElement(myinfo, 'user_export_type').text = '2'
    
    for entry in anilist_data:
        manga = ET.SubElement(root, 'manga')
        for key, value in entry.items():
            ET.SubElement(manga, key).text = str(value)
    
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

def main():
    input_dir = 'Shiki'
    output_dir = 'AniList'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    shikimori_file = os.path.join(input_dir, 'manga.xml')
    anilist_file = os.path.join(output_dir, 'MangaForAniList.xml')
    
    shikimori_data = read_shikimori_xml(shikimori_file)
    anilist_data = convert_to_anilist_format(shikimori_data)
    create_anilist_xml(anilist_data, anilist_file)
    
    print("Конвертация манги завершена. Файл для импорта в AniList создан.")

if __name__ == '__main__':
    main()