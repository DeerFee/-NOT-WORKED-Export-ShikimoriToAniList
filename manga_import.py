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
        
        # Проверка и обработка данных
        series_title = manga.find('series_title').text if manga.find('series_title') is not None else ''
        series_type = manga.find('series_type').text if manga.find('series_type') is not None else '0'
        series_volumes = manga.find('series_volumes').text if manga.find('series_volumes') is not None else '0'
        series_chapters = manga.find('series_chapters').text if manga.find('series_chapters') is not None else '0'
        manga_mangadb_id = manga.find('manga_mangadb_id').text if manga.find('manga_mangadb_id') is not None else '0'
        my_read_volumes = manga.find('my_read_volumes').text if manga.find('my_read_volumes') is not None else '0'
        my_read_chapters = manga.find('my_read_chapters').text if manga.find('my_read_chapters') is not None else '0'
        my_times_watched = manga.find('my_times_watched').text if manga.find('my_times_watched') is not None else '0'
        my_score = manga.find('my_score').text if manga.find('my_score') is not None else '0'
        my_comments = manga.find('my_comments').text if manga.find('my_comments') is not None else ''

        # Преобразование статусов в соответствующий формат AniList
        status_mapping = {
            'reading': '1',
            'completed': '2',
            'on_hold': '3',
            'dropped': '4',
            'plan_to_read': '6'
        }
        my_status = manga.find('my_status').text if manga.find('my_status') is not None else 'plan_to_read'
        my_status = status_mapping.get(my_status, '6')  # Если статус не определен, по умолчанию 'plan_to_read'

        anilist_entry = {
            'series_title': series_title,
            'series_type': series_type,
            'series_volumes': series_volumes,
            'series_chapters': series_chapters,
            'manga_mangadb_id': manga_mangadb_id,
            'my_read_volumes': my_read_volumes,
            'my_read_chapters': my_read_chapters,
            'my_times_watched': my_times_watched,  # Возможно, стоит заменить это поле на другое, специфичное для манги
            'my_score': my_score,
            'my_status': my_status,
            'my_tags': tags_str,
            'my_comments': my_comments,
            'update_on_import': '1'
        }
        anilist_data.append(anilist_entry)
    return anilist_data

def create_anilist_xml(anilist_data, output_file):
    root = ET.Element('myanimelist')
    
    myinfo = ET.SubElement(root, 'myinfo')
    ET.SubElement(myinfo, 'user_export_type').text = '2'  # Для манги используем '2' вместо '1'
    
    for entry in anilist_data:
        manga = ET.SubElement(root, 'manga')
        for key, value in entry.items():
            ET.SubElement(manga, key).text = str(value)
    
    # Красивое форматирование XML
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
