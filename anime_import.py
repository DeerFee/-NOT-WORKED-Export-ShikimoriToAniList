import xml.etree.ElementTree as ET
import os

def read_shikimori_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def convert_to_anilist_format(shikimori_data):
    anilist_data = []
    for anime in shikimori_data.findall('anime'):
        tags = anime.find('my_tags')
        tags_str = tags.text if tags is not None and tags.text else ''
        
        # Проверка на существование элементов
        series_animedb_id = anime.find('series_animedb_id').text if anime.find('series_animedb_id') is not None else '0'
        series_title = anime.find('series_title').text if anime.find('series_title') is not None else ''
        series_type = anime.find('series_type').text if anime.find('series_type') is not None else ''
        series_episodes = anime.find('series_episodes').text if anime.find('series_episodes') is not None else '0'
        my_id = anime.find('my_id').text if anime.find('my_id') is not None else '0'
        my_watched_episodes = anime.find('my_watched_episodes').text if anime.find('my_watched_episodes') is not None else '0'
        my_score = anime.find('my_score').text if anime.find('my_score') is not None else '0'
        my_status = anime.find('my_status').text if anime.find('my_status') is not None else ''
        my_times_watched = anime.find('my_times_watched').text if anime.find('my_times_watched') is not None else '0'
        my_comments = anime.find('my_comments').text if anime.find('my_comments') is not None else ''

        anilist_entry = {
            'series_animedb_id': series_animedb_id,
            'series_title': series_title,
            'series_type': series_type,
            'series_episodes': series_episodes,
            'my_id': my_id,
            'my_watched_episodes': my_watched_episodes,
            'my_score': my_score,
            'my_status': my_status,
            'my_times_watched': my_times_watched,
            'my_tags': tags_str,
            'my_comments': my_comments,
            'update_on_import': '1'
        }
        anilist_data.append(anilist_entry)
    return anilist_data

def create_anilist_xml(anilist_data, output_file):
    root = ET.Element('myanimelist')
    
    myinfo = ET.SubElement(root, 'myinfo')
    ET.SubElement(myinfo, 'user_export_type').text = '1'
    
    for entry in anilist_data:
        anime = ET.SubElement(root, 'anime')
        for key, value in entry.items():
            ET.SubElement(anime, key).text = str(value)
    
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def main():
    input_dir = 'Shiki'
    output_dir = 'AniList'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    shikimori_file = os.path.join(input_dir, 'anime.xml')
    anilist_file = os.path.join(output_dir, 'AnimeForAniList.xml')
    
    shikimori_data = read_shikimori_xml(shikimori_file)
    anilist_data = convert_to_anilist_format(shikimori_data)
    create_anilist_xml(anilist_data, anilist_file)
    
    print("Конвертация аниме завершена. Файл для импорта в AniList создан.")

if __name__ == '__main__':
    main()
