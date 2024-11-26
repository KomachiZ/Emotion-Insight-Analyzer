import requests
import os
import sys

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将music_recommendations.py所在的目录添加到Python路径
sys.path.append(current_dir)

from music_recommendations import MusicRecommender

def test_spotify_ids():
    recommender = MusicRecommender()
    invalid_songs = []
    total_songs = 0
    
    # 遍历所有情感类型
    for sentiment_type in recommender.recommendations:
        # 遍历所有分数范围
        for score_range, songs in recommender.recommendations[sentiment_type].items():
            # 遍历该范围内的所有歌曲
            for song in songs:
                total_songs += 1
                name = song['name']
                spotify_id = song['spotify_id']
                
                # 构建 Spotify 歌曲链接
                url = f"https://open.spotify.com/track/{spotify_id}"
                
                try:
                    # 发送请求检查链接是否有效
                    response = requests.get(url)
                    if response.status_code != 200:
                        invalid_songs.append({
                            'name': name,
                            'id': spotify_id,
                            'sentiment': sentiment_type,
                            'range': score_range,
                            'status': response.status_code
                        })
                        print(f"❌ Invalid: {name} ({spotify_id}) - Status: {response.status_code}")
                    else:
                        print(f"✅ Valid: {name}")
                except Exception as e:
                    invalid_songs.append({
                        'name': name,
                        'id': spotify_id,
                        'sentiment': sentiment_type,
                        'range': score_range,
                        'error': str(e)
                    })
                    print(f"❌ Error checking {name}: {e}")
    
    # 打印总结
    print("\n=== Summary ===")
    print(f"Total songs checked: {total_songs}")
    print(f"Valid songs: {total_songs - len(invalid_songs)}")
    print(f"Invalid songs: {len(invalid_songs)}")
    
    if invalid_songs:
        print("\nInvalid songs list:")
        for song in invalid_songs:
            print(f"- {song['name']} ({song['id']}) in {song['sentiment']} {song['range']}")
            if 'status' in song:
                print(f"  Status code: {song['status']}")
            if 'error' in song:
                print(f"  Error: {song['error']}")

if __name__ == "__main__":
    test_spotify_ids()