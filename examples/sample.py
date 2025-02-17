from easy_pil import load_image, Canvas, Editor, Font
from io import BytesIO

import re

artists = [{'name': 'OH MY GIRL', 'image': 'https://i.scdn.co/image/ab6761610000e5eb5cd460490fb1c55b8ed8c40b', 'popularity': 51}, {'name': 'Red Velvet', 'image': 'https://i.scdn.co/image/ab6761610000e5eb02a562ea6b1dc718394010ac', 'popularity': 69}, {'name': 'The Weeknd', 
'image': 'https://i.scdn.co/image/ab6761610000e5eb9e528993a2820267b97f6aae', 'popularity': 96}, {'name': 'Taylor Swift', 'image': 'https://i.scdn.co/image/ab6761610000e5ebe672b5f553298dcdccb0e676', 'popularity': 96}, {'name': 'TWICE', 'image': 'https://i.scdn.co/image/ab6761610000e5ebca6c145421fa9ceb58d6f9d4', 'popularity': 78}, {'name': 'NewJeans', 'image': 'https://i.scdn.co/image/ab6761610000e5eb80668ba2b15094d083780ea9', 'popularity': 78}, {'name': 'fromis_9', 'image': 'https://i.scdn.co/image/ab6761610000e5ebd6af403be25256e1fdf15eca', 'popularity': 60}, {'name': 'Metro Boomin', 'image': 'https://i.scdn.co/image/ab6761610000e5ebdf9a1555f53a20087b8c5a5c', 'popularity': 86}, {'name': 'IVE', 'image': 'https://i.scdn.co/image/ab6761610000e5eb8939960e5144b51d7903899f', 'popularity': 74}, {'name': 'LOONA', 'image': 'https://i.scdn.co/image/ab6761610000e5eb80584436e5726afb70cee7f8', 'popularity': 53}]

month = "February"

def format_duration(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"

def detect_lang(name, artist, layout):
    KOREAN_REGEX = re.compile(r'[\uAC00-\uD7AF]')
    JAPANESE_REGEX = re.compile(r'[\u3040-\u30FF\u4E00-\u9FFF]') # Supports Hiragana, Katakana, and Kanji
    CHINESE_REGEX = re.compile(r'[\u4E00-\u9FFF]') # Supports Traditional and Simplified Chinese
    THAI_REGEX = re.compile(r'[\u0E00-\u0E7F]')
    VIETNAMESE_REGEX = re.compile(r'[\u00C0-\u1EF9]')

    match layout:
        case "story":
            font_size = (35, 27)
        case "post":
            font_size = (20, 17)
        case "trend-story":
            font_size = (50, 30)
        case "trend-post":
            font_size = (45, 25)
        case _:
            font_size = (0, 0)

    df_track_font, df_artist_font = Font.poppins("bold", size=font_size[0]), Font.poppins(size=font_size[1])
    kr_track_font, kr_artist_font = Font("./wydm_app/static/font/Noto_Sans_KR/static/NotoSansKR-Bold.ttf", size=font_size[0]), Font("./wydm_app/static/font/Noto_Sans_KR/static/NotoSansKR-Regular.ttf", size=font_size[1])
    jp_track_font, jp_artist_font = Font("./wydm_app/static/font/Noto_Sans_JP/static/NotoSansJP-Bold.ttf", size=font_size[0]), Font("./wydm_app/static/font/Noto_Sans_JP/static/NotoSansJP-Regular.ttf", size=font_size[1])
    cn_track_font, cn_artist_font = Font("./wydm_app/static/font/Noto_Sans_TC/static/NotoSansTC-Bold.ttf", size=font_size[0]), Font("./wydm_app/static/font/Noto_Sans_TC/static/NotoSansTC-Regular.ttf", size=font_size[1])
    th_track_font, th_artist_font = Font("./wydm_app/static/font/Noto_Sans_Thai/static/NotoSansThai-Bold.ttf", size=font_size[0]), Font("./wydm_app/static/font/Noto_Sans_Thai/static/NotoSansThai-Regular.ttf", size=font_size[1])
    vi_track_font, vi_artist_font = Font("./wydm_app/static/font/Noto_Sans/static/NotoSans-Bold.ttf", size=font_size[0]), Font("./wydm_app/static/font/Noto_Sans/static/NotoSans-Regular.ttf", size=font_size[1])

    if KOREAN_REGEX.search(name):
        font_track = kr_track_font
    elif JAPANESE_REGEX.search(name):
        font_track = jp_track_font
    elif CHINESE_REGEX.search(name):
        font_track = cn_track_font
    elif THAI_REGEX.search(name):
        font_track = th_track_font
    elif VIETNAMESE_REGEX.search(name):
        font_track = vi_track_font
    else:
        font_track = df_track_font

    if KOREAN_REGEX.search(artist):
        font_artist = kr_artist_font
    elif JAPANESE_REGEX.search(artist):
        font_artist = jp_artist_font
    elif CHINESE_REGEX.search(artist):
        font_artist = cn_artist_font
    elif THAI_REGEX.search(artist):
        font_artist = th_artist_font
    elif VIETNAMESE_REGEX.search(artist):
        font_artist = vi_artist_font
    else:
        font_artist = df_artist_font

    return font_track, font_artist

def generate_artist_post(artists, month):
    img = Canvas((1080, 1320), color=(255, 255, 255))
    draw = Editor(img)

    y_box_value, y_text_value, y_image_value = 193, 217, 200
    top_start_color, top_end_color = (255, 65, 108), (238, 126, 130)

    shadow_intensity, shadow_offset = 40, 8
    shadow_color = (0, 0, 0, int(255 * (shadow_intensity / 100)))

    spotify_logo = Editor("./wydm_app/static/img/spotify_black.png").resize((135, 37))
    title_font, rank_font, listener_font = Font("./wydm_app/static/font/Dancing_Script/static/DancingScript-Bold.ttf", size=80), Font.poppins("bold", size=40), Font.poppins(size=25)

    draw.text((540, 70), f"My Serenade {month} Recap", color="#e03070", font=title_font, align='center')

    default_box, gradient_box, shadow_box = Canvas(width=1000, height=80, color="white"), Canvas(width=1000, height=80, color="white"), Canvas((1000 + shadow_offset, 80 + shadow_offset), color=(0, 0, 0, 0))
    box, gbox, sbox = Editor(default_box).rounded_corners(radius=20), Editor(gradient_box).rounded_corners(radius=20), Editor(shadow_box).rounded_corners(radius=20)

    sbox.rectangle(position=(shadow_offset, shadow_offset), width=1000, height=120, fill=shadow_color).blur(amount=15).rounded_corners(radius=20)

    for x in range(1000):
        blend_factor = x / 1000
        r = int(top_start_color[0] * (1 - blend_factor) + top_end_color[0] * blend_factor)
        g = int(top_start_color[1] * (1 - blend_factor) + top_end_color[1] * blend_factor)
        b = int(top_start_color[2] * (1 - blend_factor) + top_end_color[2] * blend_factor)
        gbox.rectangle(position=(x, 0), width=1, height=100, fill=(r, g, b)).rounded_corners(radius=20)

    for i, track in enumerate(artists[:10]):
        draw.paste(sbox, (40, y_box_value))
        track_font, pop_font = detect_lang(track['name'], track['name'], "post")
        name = f"{track['name'][:40]}..." if len(track['name']) > 40 else track['name']
        if i == 0:
            draw.paste(gbox, (40, y_box_value))
            draw.text((90, y_text_value), f"{i+1}", color="white", font=rank_font, align='center')
            draw.text((205, y_text_value - 5), f"{name}", color="white", font=track_font, align='left')
            draw.text((205, y_text_value + 25), f"{track['popularity']} Pop Points", color="white", font=pop_font, align='left')
            draw.text((950, y_text_value + 5), f"#{i+1}", color="white", font=rank_font, align='center')
        else:
            draw.paste(box, (40, y_box_value))
            draw.text((90, y_text_value), f"{i+1}", color="#ff416c", font=rank_font, align='center')
            draw.text((205, y_text_value - 5), f"{name}", color="#222222", font=track_font, align='left')
            draw.text((205, y_text_value + 25), f"{track['popularity']} Pop Points", color="#222222", font=pop_font, align='left')
            draw.text((950, y_text_value + 5), f"#{i+1}", color="#ff416c", font=rank_font, align='center')
        
        cover = load_image(track['image'])
        img = Editor(cover).resize((65, 65)).rounded_corners(radius=10)
        draw.paste(img, (130, y_image_value))
        y_box_value += 105
        y_image_value += 105
        y_text_value += 105

    draw.text((70, 1260), f"{month} | © Serenade, 2025", color="#e03070", font=Font.poppins(size=25), align='left')
    draw.paste(spotify_logo, (881, 1255))

    return draw.show()

generate_artist_post(artists, month)