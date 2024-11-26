class MusicRecommender:
    def __init__(self):
        # 针对不同情绪和分数范围的音乐推荐
        self.recommendations = {
            'positive': {
                (90, 100): [
                    {
                        'name': "Happy - Pharrell Williams",
                        'spotify_id': "60nZcImufyMA1MKQY3dcCH"
                    },
                    {
                        'name': "I Gotta Feeling - The Black Eyed Peas",
                        'spotify_id': "2H1047e0oMSj10dgp7p2VG"
                    },
                    {
                        'name': "Walking on Sunshine - Katrina & The Waves",
                        'spotify_id': "05wIrZSwuaVWhcv5FfqeH0"
                    }
                ],
                (80, 90): [
                    {
                        'name': "Uptown Funk - Mark Ronson ft. Bruno Mars",
                        'spotify_id': "32OlwWuMpZ6b0aN2RZOeMS"
                    },
                    {
                        'name': "Can't Stop the Feeling! - Justin Timberlake",
                        'spotify_id': "1WkMMavIMc4JZ8cfMmxHkI"
                    },
                    {
                        'name': "Good Time - Owl City & Carly Rae Jepsen",
                        'spotify_id': "1kPpge9JDLpcj15qgrPbYX"
                    }
                ],
                (70, 80): [
                    {
                        'name': "Shake It Off - Taylor Swift",
                        'spotify_id': "0cqRj7pUJDkTCEsJkx8snD"
                    },
                    {
                        'name': "Best Day of My Life - American Authors",
                        'spotify_id': "5Hroj5K7vLpIG4FNCRIjbP"
                    },
                    {
                        'name': "Counting Stars - OneRepublic",
                        'spotify_id': "2tpWsVSb9UEmDRxAl1zhX1"
                    }
                ],
                (60, 70): [
                    {
                        'name': "Hey Ya! - OutKast",
                        'spotify_id': "2PpruBYCo4H7WOBJ7Q2EwM"
                    },
                    {
                        'name': "Sugar - Maroon 5",
                        'spotify_id': "2iuZJX9X9P0GKaE93xcPjk"
                    },
                    {
                        'name': "On Top of the World - Imagine Dragons",
                        'spotify_id': "6KuHjfXHkfnIjdmcIvt9r0"
                    }
                ],
                (50, 60): [
                    {
                        'name': "Going Bad - Meek Mill",
                        'spotify_id': "2IRZnDFmlqMuOrYOLnZZyc"
                    },
                    {
                        'name': "Rather Be - Clean Bandit",
                        'spotify_id': "3s4U7OHV7gnj42VV72eSZ6"
                    },
                    {
                        'name': "Sunflower - Post Malone & Swae Lee",
                        'spotify_id': "3KkXRkHbMCARz0aVfEt68P"
                    }
                ],
                (40, 50): [
                    {
                        'name': "High Hopes - Panic! At The Disco",
                        'spotify_id': "1rqqCSm0Qe4I9rUvWncaom"
                    },
                    {
                        'name': "Thunder - Imagine Dragons",
                        'spotify_id': "1zB4vmk8tFRmM9UULNzbLB"
                    },
                    {
                        'name': "Ride - Twenty One Pilots",
                        'spotify_id': "2Z8WuEywRWYTKe1NybPQEW"
                    }
                ],
                (30, 40): [
                    {
                        'name': "Perfect - Ed Sheeran",
                        'spotify_id': "0tgVpDi06FyKpA1z0VMD4v"
                    },
                    {
                        'name': "Beautiful Day - U2",
                        'spotify_id': "1VuBmEauSZywQVtqbxNqka"
                    },
                    {
                        'name': "Viva La Vida - Coldplay",
                        'spotify_id': "1mea3bSkSGXuIRvnydlB5b"
                    }
                ]
            },
            'negative': {
                (90, 100): [
                    {
                        'name': "I Don't Wanna Live Forever - ZAYN, Taylor Swift",
                        'spotify_id': "3NdDpSvN911VPGivFlV5d0"
                    },
                    {
                        'name': "Happiness is a butterfly - Lana Del Ray",
                        'spotify_id': "3lG6OtGDsYAOALxEmubQQm"
                    },
                    {
                        'name': "All By Myself - Celine Dion",
                        'spotify_id': "0gsl92EMIScPGV1AU35nuD"
                    }
                ],
                (80, 90): [
                    {
                        'name': "Fix You - Coldplay",
                        'spotify_id': "7LVHVU3tWfcxj5aiPFEW4Q"
                    },
                    {
                        'name': "Mad World - Gary Jules",
                        'spotify_id': "3JOVTQ5h8HGFnDdp4VT3MP"
                    },
                    {
                        'name': "The Sound of Silence - Disturbed",
                        'spotify_id': "0eZBeB2xFIS65jQHerispi"
                    }
                ],
                (70, 80): [
                    {
                        'name': "Hello - Adele",
                        'spotify_id': "4sPmO7WMQUAf45kwMOtONw"
                    },
                    {
                        'name': "Yesterday - The Beatles",
                        'spotify_id': "3BQHpFgAp4l80e1XslIjNI"
                    },
                    {
                        'name': "Hurt - Johnny Cash",
                        'spotify_id': "28cnXtME493VX9NOw9cIUh"
                    }
                ],
                (60, 70): [
                    {
                        'name': "Stay With Me - Sam Smith",
                        'spotify_id': "5Nm9ERjJZ5oyfXZTECKmRt"
                    },
                    {
                        'name': "All of Me - John Legend",
                        'spotify_id': "3U4isOIWM3VvDubwSI3y7a"
                    },
                    {
                        'name': "When I Was Your Man - Bruno Mars",
                        'spotify_id': "0nJW01T7XtvILxQgC5J7Wh"
                    }
                ],
                (50, 60): [
                    {
                        'name': "The Scientist - Coldplay",
                        'spotify_id': "75JFxkI2RXiU7L9VXzMkle"
                    },
                    {
                        'name': "Let Her Go - Passenger",
                        'spotify_id': "2jyjhRf6DVbMPU5zxagN2h"
                    },
                    {
                        'name': "Say You Love Me - Jessie Ware",
                        'spotify_id': "71AATBHZGo82EnjZnG53Zx"
                    }
                ],
                (40, 50): [
                    {
                        'name': "Skinny Love - Bon Iver",
                        'spotify_id': "3B3eOgLJSqPEA0RfboIQVM"
                    },
                    {
                        'name': "Fast Car - Tracy Chapman",
                        'spotify_id': "2M9ro2krNb7nr7HSprkEgo"
                    },
                    {
                        'name': "Gravity - John Mayer",
                        'spotify_id': "3SktMqZmo3M9zbB7oKMIF7"
                    }
                ],
                (30, 40): [
                    {
                        'name': "Chasing Cars - Snow Patrol",
                        'spotify_id': "11bD1JtSjlIgKgZG2134DZ"
                    },
                    {
                        'name': "Behind Blue Eyes - The Who",
                        'spotify_id': "0cKk8BKEi7zXbdrYdyqBP5"
                    },
                    {
                        'name': "Bridge Over Troubled Water - Simon & Garfunkel",
                        'spotify_id': "6l8EbYRtQMgKOyc1gcDHF9"
                    }
                ]
            },
            'neutral': {
                (90, 100): [
                    {
                        'name': "Breathe - Pink Floyd",
                        'spotify_id': "2ctvdKmETyOzPb2GiJJT53"
                    },
                    {
                        'name': "Weightless - Marconi Union",
                        'spotify_id': "6kkwzB6hXLIONkEk9JciA6"
                    },
                    {
                        'name': "Claire de Lune - Debussy",
                        'spotify_id': "6Er8Fz6fuZNi5cvwQjv1ya"
                    }
                ],
                (80, 90): [
                    {
                        'name': "River Flows in You - Yiruma",
                        'spotify_id': "2agBDIr9MYDUducQPC1sFU"
                    },
                    {
                        'name': "Time - Hans Zimmer",
                        'spotify_id': "6ZFbXIJkuI1dVNWvzJzown"
                    },
                    {
                        'name': "Experience - Ludovico Einaudi",
                        'spotify_id': "1BncfTJAWxrsxyT9culBrj"
                    }
                ],
                (70, 80): [
                    {
                        'name': "The Piano Duet - Danny Elfman",
                        'spotify_id': "2CPnPnfbCMESaNpBQbeA0X"
                    },
                    {
                        'name': "Divenire - Ludovico Einaudi",
                        'spotify_id': "6KpO4neDXxGdiEgsivZieY"
                    },
                    {
                        'name': "Gymnopédie No.1 - Erik Satie",
                        'spotify_id': "5NGtFXVpXSvwunEIGeviY3"
                    }
                ],
                (60, 70): [
                    {
                        'name': "Saturn - Sleeping At Last",
                        'spotify_id': "3tJjZMHLqhD8DaGgdBICnc"
                    },
                    {
                        'name': "Light of the Seven - Ramin Djawadi",
                        'spotify_id': "1SbsbLsUMnAKWHx1zAV6ER"
                    },
                    {
                        'name': "Nuvole Bianche - Ludovico Einaudi",
                        'spotify_id': "3weNRklVDqb4Rr5MhKBR3D"
                    }
                ],
                (50, 60): [
                    {
                        'name': "Thriller - Micheal Jackson",
                        'spotify_id': "2LlQb7Uoj1kKyGhlkBf9aC"
                    },
                    {
                        'name': "Ocean - John Butler",
                        'spotify_id': "59tcQJiHwApzE4h6yVnL9i"
                    },
                    {
                        'name': "The Heart Asks Pleasure First - Michael Nyman",
                        'spotify_id': "4RW7EZi7SHSLRwvn1Q8Mqj"
                    }
                ],
                (40, 50): [
                    {
                        'name': "One Summer Day - Joe Hisaishi",
                        'spotify_id': "3gFQOMoUwlR6aUZj81gCzu"
                    },
                    {
                        'name': "Avril 14th - Aphex Twin",
                        'spotify_id': "1uaGSDFsLdReQgg8p7Obwh"
                    },
                    {
                        'name': "Welcome to the Machine - Pink Floyd",
                        'spotify_id': "5VWC7v2dC2K0SIIjT9WTLN"
                    }
                ],
                (30, 40): [
                    {
                        'name': "Morning Passages - Philip Glass",
                        'spotify_id': "5U7vahMkL41gueMDNtoLhp"
                    },
                    {
                        'name': "Spiegel im Spiegel - Arvo Pärt",
                        'spotify_id': "7zHd9LxIZB8WKosSWN9Umj"
                    },
                    {
                        'name': "On the Nature of Daylight - Max Richter",
                        'spotify_id': "56oReVXIfUO9xkX7pHmEU0"
                    }
                ]
            }
        }
    
    def get_recommendations(self, sentiment, score):
        """
        根据情感和分数获取音乐推荐
        sentiment: 情感类型 ('positive', 'negative', 'neutral')
        score: 情感分数 (0-100)
        """
        score = float(score)
        if sentiment not in self.recommendations:
            return []
            
        # 找到对应分数范围的推荐
        for score_range, songs in self.recommendations[sentiment].items():
            if score_range[0] <= score <= score_range[1]:
                return songs
                
        return []