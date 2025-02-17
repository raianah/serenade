from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseServerError, HttpResponse
from easy_pil import load_image, Canvas, Editor, Font
from .models import Invitation
from spotipy import SpotifyOAuth, Spotify
from spotipy.cache_handler import CacheFileHandler
from dotenv import load_dotenv
from io import BytesIO
from collections import defaultdict, Counter
import uuid, random, os, datetime, re
from PIL import _imagingft

load_dotenv()

SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_CLIENT_ID"), os.getenv("SPOTIPY_CLIENT_SECRET"), os.getenv("SPOTIPY_REDIRECT_URI")

ROMANTIC_QUOTES = [
    "Will you date me?",
    "Every love story is beautiful, but ours will be my favorite.",
    "You are the missing piece to my heart.",
    "Life is better when we’re together.",
    "I fell in love with you, and I am still falling.",
    "You make my heart skip a beat. Will you be mine?",
    "Meeting you was fate, becoming your friend was a choice, but falling for you was beyond my control.",
    "I don’t need a superhero, I just need you.",
    "With you, every moment is special.",
    "You are the dream I never want to wake up from."
]

OPTION_CHOICES = {
    "love-letter": 1,
    "prom-date": 2,
    "wydm": 3,
    "long-sweet-message": 4,
    "your-monthly-spotify": 5
}

def color_picker(color):
    # Color 
    colors = {}
    match color:
        case "yellow":
            colors['story_base_color'] = (255, 200, 87)
            colors['top_start_color'] = (255, 180, 60)
            colors['top_end_color'] = (255, 220, 130)
            colors['title_color'] = "black"
            colors['text_color'] = "white"
            colors['box_color'] = "white"
            colors['rank_color'] = "#5A3E36"
            colors['story_nontext_color'] = "#5A3E36"

            colors['post_base_color'] = (255, 255, 255)
            colors['post_title_color'] = "#3F2B21"
        case "aquablue":
            colors['story_base_color'] = (0, 180, 216)
            colors['top_start_color'] = (0, 150, 199)
            colors['top_end_color'] = (102, 210, 234)
            colors['title_color'] = "white"
            colors['text_color'] = "white"
            colors['box_color'] = "white"
            colors['rank_color'] = "#065A82"
            colors['story_nontext_color'] = "#065A82"

            colors['post_base_color'] = (255, 255, 255)
            colors['post_title_color'] = "#002A51"
        case "green":
            colors['story_base_color'] = (34, 153, 84)
            colors['top_start_color'] = (46, 204, 113)
            colors['top_end_color'] = (120, 224, 143)
            colors['title_color'] = "white"
            colors['text_color'] = "white"
            colors['box_color'] = "white"
            colors['rank_color'] = "#145A32"
            colors['story_nontext_color'] = "#145A32"

            colors['post_base_color'] = (255, 255, 255)
            colors['post_title_color'] = "#092D01"
        case "purple":
            colors['story_base_color'] = (136, 78, 160)
            colors['top_start_color'] = (155, 89, 182)
            colors['top_end_color'] = (197, 144, 210)
            colors['title_color'] = "white"
            colors['text_color'] = "white"
            colors['box_color'] = "white"
            colors['rank_color'] = "#4A235A"
            colors['story_nontext_color'] = "#2E1A47"

            colors['post_base_color'] = (255, 255, 255)
            colors['post_title_color'] = "#1E1235"
        case "default":
            colors['story_base_color'] = (255, 117, 140)
            colors['top_start_color'] = (255, 65, 108)
            colors['top_end_color'] = (238, 126, 130)
            colors['title_color'] = "white"
            colors['text_color'] = "white"
            colors['box_color'] = "white"
            colors['rank_color'] = "#ff416c"
            colors['story_nontext_color'] = "#ff416c"

            colors['post_base_color'] = (255, 255, 255)
            colors['post_title_color'] = "#e03070"
    
    return colors

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
    cn_track_font, cn_artist_font = Font("./wydm_app/static/font/Noto_Sans_SC/static/NotoSansSC-Bold.ttf", size=font_size[0]), Font("./wydm_app/static/font/Noto_Sans_SC/static/NotoSansSC-Regular.ttf", size=font_size[1])
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

# Image Generation
def generate_story_recap(tracks, month, color):
    colors = color_picker(color)
    img = Canvas((1080, 1920), color=colors['story_base_color'])
    draw = Editor(img)

    y_box_value, y_text_value, y_image_value = 390, 425, 400
    top_start_color, top_end_color = colors['top_start_color'], colors['top_end_color']

    shadow_intensity, shadow_offset = 40, 8
    shadow_color = (0, 0, 0, int(255 * (shadow_intensity / 80)))

    title_font, rank_font = Font("./wydm_app/static/font/Dancing_Script/static/DancingScript-Bold.ttf", size=100), Font.poppins("bold", size=60)

    draw.text((540, 80), "My Serenade", color=colors['title_color'], font=title_font, align='center')
    draw.text((540, 200), f"{month} Recap", color=colors['title_color'], font=title_font, align='center')

    default_box, gradient_box, shadow_box = Canvas(width=1000, height=120, color=colors['box_color']), Canvas(width=1000, height=120, color=colors['box_color']), Canvas((1000 + shadow_offset, 120 + shadow_offset), color=(0, 0, 0, 0))
    box, gbox, sbox = Editor(default_box).rounded_corners(radius=20), Editor(gradient_box).rounded_corners(radius=20), Editor(shadow_box).rounded_corners(radius=20)

    sbox.rectangle(position=(shadow_offset, shadow_offset), width=1000, height=120, fill=shadow_color).blur(amount=15).rounded_corners(radius=20)

    for x in range(1000):
        blend_factor = x / 1000
        r = int(top_start_color[0] * (1 - blend_factor) + top_end_color[0] * blend_factor)
        g = int(top_start_color[1] * (1 - blend_factor) + top_end_color[1] * blend_factor)
        b = int(top_start_color[2] * (1 - blend_factor) + top_end_color[2] * blend_factor)
        gbox.rectangle(position=(x, 0), width=1, height=120, fill=(r, g, b)).rounded_corners(radius=20)

    for i, track in enumerate(tracks[:10]):
        draw.paste(sbox, (40, y_box_value))
        track_font, artist_font = detect_lang(track['name'], track['artist'], layout="story")
        track_name = f"{track['name'][:30]}..." if len(track['name']) > 30 else track['name']
        track_artist = f"{track['artist'][:30]}..." if len(track['artist']) > 30 else track['artist']
        if i == 0:
            draw.paste(gbox, (40, y_box_value))
            draw.text((950, y_text_value), f"#{i+1}", color=colors['text_color'], font=rank_font, align='center')
            draw.text((170, y_text_value - 10), f"{track_name}", color=colors['text_color'], font=track_font, align='left')
            draw.text((170, y_text_value + 40), f"{track_artist}", color=colors['text_color'], font=artist_font, align='left')
        else:
            draw.paste(box, (40, y_box_value))
            draw.text((950, y_text_value), f"#{i+1}", color=colors['rank_color'], font=rank_font, align='center')
            draw.text((170, y_text_value - 10), f"{track_name}", color=colors['story_nontext_color'], font=track_font, align='left')
            draw.text((170, y_text_value + 40), f"{track_artist}", color=colors['story_nontext_color'], font=artist_font, align='left')
        
        cover = load_image(track['album_cover'])
        album_cover = Editor(cover).resize((100, 100)).rounded_corners(radius=20)
        draw.paste(album_cover, (50, y_image_value))
        y_box_value += 140
        y_image_value += 140
        y_text_value += 140

    draw.text((540, 1825), f"{month} | © Serenade, 2025", color=colors['title_color'], font=Font.poppins("bold", size=30), align='center')

    # Save & return image
    img_io = BytesIO()
    draw.save(img_io, format="PNG")
    img_io.seek(0)
    return img_io

def generate_post_recap(tracks, month, color):
    colors = color_picker(color)
    img = Canvas((1080, 1320), color=colors['post_base_color'])
    draw = Editor(img)

    y_box_value, y_text_value, y_image_value = 193, 217, 200
    top_start_color, top_end_color = colors['top_start_color'], colors['top_end_color']

    shadow_intensity, shadow_offset = 40, 8
    shadow_color = (0, 0, 0, int(255 * (shadow_intensity / 100)))

    title_font, rank_font, listener_font = Font("./wydm_app/static/font/Dancing_Script/static/DancingScript-Bold.ttf", size=80), Font.poppins("bold", size=40), Font.poppins(size=25)

    draw.text((540, 70), f"My Serenade {month} Recap", color=colors['post_title_color'], font=title_font, align='center')

    default_box, gradient_box, shadow_box = Canvas(width=1000, height=80, color="white"), Canvas(width=1000, height=80, color="white"), Canvas((1000 + shadow_offset, 80 + shadow_offset), color=(0, 0, 0, 0))
    box, gbox, sbox = Editor(default_box).rounded_corners(radius=20), Editor(gradient_box).rounded_corners(radius=20), Editor(shadow_box).rounded_corners(radius=20)

    sbox.rectangle(position=(shadow_offset, shadow_offset), width=1000, height=120, fill=shadow_color).blur(amount=15).rounded_corners(radius=20)

    for x in range(1000):
        blend_factor = x / 1000
        r = int(top_start_color[0] * (1 - blend_factor) + top_end_color[0] * blend_factor)
        g = int(top_start_color[1] * (1 - blend_factor) + top_end_color[1] * blend_factor)
        b = int(top_start_color[2] * (1 - blend_factor) + top_end_color[2] * blend_factor)
        gbox.rectangle(position=(x, 0), width=1, height=100, fill=(r, g, b)).rounded_corners(radius=20)

    for i, track in enumerate(tracks[:10]):
        draw.paste(sbox, (40, y_box_value))
        track_font, artist_font = detect_lang(track['name'], track['artist'], "post")
        track_name = f"{track['name'][:40]}..." if len(track['name']) > 40 else track['name']
        track_artist = f"{track['artist'][:40]}..." if len(track['artist']) > 40 else track['artist']
        if i == 0:
            draw.paste(gbox, (40, y_box_value))
            draw.text((90, y_text_value), f"{i+1}", color=colors['text_color'], font=rank_font, align='center')
            draw.text((205, y_text_value - 5), f"{track_name}", color=colors['text_color'], font=track_font, align='left')
            draw.text((205, y_text_value + 25), f"{track_artist}", color=colors['text_color'], font=artist_font, align='left')
            draw.text((1000, y_text_value + 5), f"{track['duration']}", color=colors['text_color'], font=listener_font, align='right')
        else:
            draw.paste(box, (40, y_box_value))
            draw.text((90, y_text_value), f"{i+1}", color=colors['story_nontext_color'], font=rank_font, align='center')
            draw.text((205, y_text_value - 5), f"{track_name}", color=colors['story_nontext_color'], font=track_font, align='left')
            draw.text((205, y_text_value + 25), f"{track_artist}", color=colors['story_nontext_color'], font=artist_font, align='left')
            draw.text((1000, y_text_value + 5), f"{track['duration']}", color=colors['story_nontext_color'], font=listener_font, align='right')
        
        cover = load_image(track['album_cover'])
        album_cover = Editor(cover).resize((65, 65)).rounded_corners(radius=10)
        draw.paste(album_cover, (130, y_image_value))
        y_box_value += 105
        y_image_value += 105
        y_text_value += 105

    draw.text((540, 1250), f"{month} | © Serenade, 2025", color=colors["post_title_color"], font=Font.poppins("bold", size=30), align='center')

    # Save & return image
    img_io = BytesIO()
    draw.save(img_io, format="PNG")
    img_io.seek(0)
    return img_io

def generate_trend_story(stats, color):
    colors = color_picker(color)
    img = Canvas((1080, 1920), color=colors['story_base_color'])
    draw = Editor(img)

    title_font, rank_font = Font("./wydm_app/static/font/Dancing_Script/static/DancingScript-Bold.ttf", size=120), Font.poppins(size=40)

    draw.text((540, 80), "My Serenade", color=colors['title_color'], font=title_font, align='center')
    draw.text((540, 210), f"Trends", color=colors['title_color'], font=title_font, align='center')

    default_box = Canvas(width=1000, height=364, color="white")
    box = Editor(default_box).rounded_corners(radius=20)

    short_term_track_font, short_term_artist_font = detect_lang(stats['short_term'][0][0], stats['short_term'][0][1]['artist'], layout="trend-story")
    medium_term_track_font, medium_term_artist_font = detect_lang(stats['medium_term'][0][0], stats['medium_term'][0][1]['artist'], layout="trend-story")
    long_term_track_font, long_term_artist_font = detect_lang(stats['long_term'][0][0], stats['long_term'][0][1]['artist'], layout="trend-story")

    short_term_track_name = stats['short_term'][0][0] if len(stats['short_term'][0][0]) <= 14 else f"{stats['short_term'][0][0][:14]}..."
    short_term_artist_name = stats['short_term'][0][1]['artist'] if len(stats['short_term'][0][1]['artist']) <= 14 else f"{stats['short_term'][0][1]['artist'][:14]}..."
    medium_term_track_name = stats['medium_term'][0][0] if len(stats['medium_term'][0][0]) <= 14 else f"{stats['medium_term'][0][0][:14]}..."
    medium_term_artist_name = stats['medium_term'][0][1]['artist'] if len(stats['medium_term'][0][1]['artist']) <= 14 else f"{stats['medium_term'][0][1]['artist'][:14]}..."
    long_term_track_name = stats['long_term'][0][0] if len(stats['long_term'][0][0]) <= 14 else f"{stats['long_term'][0][0][:14]}..."
    long_term_artist_name = stats['long_term'][0][1]['artist'] if len(stats['long_term'][0][1]['artist']) <= 14 else f"{stats['long_term'][0][1]['artist'][:14]}..."

    draw.paste(box, (40, 400))
    draw.paste(box, (40, 800))
    draw.paste(box, (40, 1200))

    short_term_cover = load_image(stats['short_term'][0][1]['album_cover'])
    short_term_album_cover = Editor(short_term_cover).resize((250, 250)).rounded_corners(radius=20)
    draw.text((540, 427), text="A month ago, you have listened to", color=colors['story_nontext_color'], font=rank_font, align='center')
    draw.paste(short_term_album_cover, (200, 485))
    draw.text((480, 510), text=f"{short_term_track_name}", color=colors['post_title_color'], font=short_term_track_font)
    draw.text((480, 570), text=f"{short_term_artist_name}", color=colors['post_title_color'], font=short_term_artist_font)
    draw.text((480, 670), text=f"{stats['short_term'][0][1]['short_term']} time/s", color=colors['post_title_color'], font=short_term_track_font)

    medium_term_cover = load_image(stats['medium_term'][0][1]['album_cover'])
    medium_term_album_cover = Editor(medium_term_cover).resize((250, 250)).rounded_corners(radius=20)
    draw.text((540, 827), text="6 months ago, you have listened to", color=colors['story_nontext_color'], font=rank_font, align='center')
    draw.paste(medium_term_album_cover, (200, 885))
    draw.text((480, 910), text=f"{medium_term_track_name}", color=colors['post_title_color'], font=medium_term_track_font)
    draw.text((480, 970), text=f"{medium_term_artist_name}", color=colors['post_title_color'], font=medium_term_artist_font)
    draw.text((480, 1070), text=f"{stats['medium_term'][0][1]['medium_term']} time/s", color=colors['post_title_color'], font=medium_term_track_font)

    long_term_cover = load_image(stats['long_term'][0][1]['album_cover'])
    long_term_album_cover = Editor(long_term_cover).resize((250, 250)).rounded_corners(radius=20)
    draw.text((540, 1227), text="Last year, you have listened to", color=colors['story_nontext_color'], font=rank_font, align='center')
    draw.paste(long_term_album_cover, (200, 1285))
    draw.text((480, 1310), text=f"{long_term_track_name}", color=colors['post_title_color'], font=long_term_track_font)
    draw.text((480, 1370), text=f"{long_term_artist_name}", color=colors['post_title_color'], font=long_term_artist_font)
    draw.text((480, 1470), text=f"{stats['long_term'][0][1]['long_term']} time/s", color=colors['post_title_color'], font=long_term_track_font)

    draw.text((540, 1800), text="© Serenade, 2025", color=colors['title_color'], font=Font.poppins("bold", size=40), align='center')

    img_io = BytesIO()
    draw.save(img_io, format="PNG")
    img_io.seek(0)
    return img_io

def generate_trend_post(stats, color):
    colors = color_picker(color)
    img = Canvas((1080, 1320), color=colors['post_base_color'])
    draw = Editor(img)

    title_font, rank_font = Font("./wydm_app/static/font/Dancing_Script/static/DancingScript-Bold.ttf", size=100), Font.poppins(size=30)
    top_start_color, top_end_color = colors['top_start_color'], colors['top_end_color']

    draw.text((540, 80), "My Serenade Trends", color=colors['post_title_color'], font=title_font, align='center')

    default_box = Canvas(width=1000, height=296, color="white")
    box = Editor(default_box).rounded_corners(radius=20)

    short_term_track_font, short_term_artist_font = detect_lang(stats['short_term'][0][0], stats['short_term'][0][1]['artist'], layout="trend-post")
    medium_term_track_font, medium_term_artist_font = detect_lang(stats['medium_term'][0][0], stats['medium_term'][0][1]['artist'], layout="trend-post")
    long_term_track_font, long_term_artist_font = detect_lang(stats['long_term'][0][0], stats['long_term'][0][1]['artist'], layout="trend-post")

    short_term_track_name = stats['short_term'][0][0] if len(stats['short_term'][0][0]) <= 14 else f"{stats['short_term'][0][0][:14]}..."
    short_term_artist_name = stats['short_term'][0][1]['artist'] if len(stats['short_term'][0][1]['artist']) <= 14 else f"{stats['short_term'][0][1]['artist'][:14]}..."
    medium_term_track_name = stats['medium_term'][0][0] if len(stats['medium_term'][0][0]) <= 14 else f"{stats['medium_term'][0][0][:14]}..."
    medium_term_artist_name = stats['medium_term'][0][1]['artist'] if len(stats['medium_term'][0][1]['artist']) <= 14 else f"{stats['medium_term'][0][1]['artist'][:14]}..."
    long_term_track_name = stats['long_term'][0][0] if len(stats['long_term'][0][0]) <= 14 else f"{stats['long_term'][0][0][:14]}..."
    long_term_artist_name = stats['long_term'][0][1]['artist'] if len(stats['long_term'][0][1]['artist']) <= 14 else f"{stats['long_term'][0][1]['artist'][:14]}..."

    for x in range(1000):
        blend_factor = x / 1000
        r = int(top_start_color[0] * (1 - blend_factor) + top_end_color[0] * blend_factor)
        g = int(top_start_color[1] * (1 - blend_factor) + top_end_color[1] * blend_factor)
        b = int(top_start_color[2] * (1 - blend_factor) + top_end_color[2] * blend_factor)
        box.rectangle(position=(x, 0), width=1, height=296, fill=(r, g, b)).rounded_corners(radius=20)

    draw.paste(box, (40, 250))
    draw.paste(box, (40, 570))
    draw.paste(box, (40, 890))

    short_term_cover = load_image(stats['short_term'][0][1]['album_cover'])
    short_term_album_cover = Editor(short_term_cover).resize((190, 190)).rounded_corners(radius=20)
    draw.text((540, 277), text="A month ago, you have listened to", color=colors['text_color'], font=rank_font, align='center')
    draw.paste(short_term_album_cover, (225, 335))
    draw.text((430, 340), text=f"{short_term_track_name}", color=colors['text_color'], font=short_term_track_font)
    draw.text((430, 390), text=f"{short_term_artist_name}", color=colors['text_color'], font=short_term_artist_font)
    draw.text((430, 470), text=f"{stats['short_term'][0][1]['short_term']} time/s", color=colors['text_color'], font=short_term_track_font)

    medium_term_cover = load_image(stats['medium_term'][0][1]['album_cover'])
    medium_term_album_cover = Editor(medium_term_cover).resize((190, 190)).rounded_corners(radius=20)
    draw.text((540, 597), text="6 months ago, you have listened to", color=colors['text_color'], font=rank_font, align='center')
    draw.paste(medium_term_album_cover, (225, 655))
    draw.text((430, 660), text=f"{medium_term_track_name}", color=colors['text_color'], font=medium_term_track_font)
    draw.text((430, 710), text=f"{medium_term_artist_name}", color=colors['text_color'], font=medium_term_artist_font)
    draw.text((430, 790), text=f"{stats['medium_term'][0][1]['medium_term']} time/s", color=colors['text_color'], font=medium_term_track_font)

    long_term_cover = load_image(stats['long_term'][0][1]['album_cover'])
    long_term_album_cover = Editor(long_term_cover).resize((190, 190)).rounded_corners(radius=20)
    draw.text((540, 917), text="Last year, you have listened to", color=colors['text_color'], font=rank_font, align='center')
    draw.paste(long_term_album_cover, (225, 975))
    draw.text((430, 980), text=f"{long_term_track_name}", color=colors['text_color'], font=long_term_track_font)
    draw.text((430, 1030), text=f"{long_term_artist_name}", color=colors['text_color'], font=long_term_artist_font)
    draw.text((430, 1110), text=f"{stats['long_term'][0][1]['long_term']} time/s", color=colors['text_color'], font=long_term_track_font)

    draw.text((540, 1240), text=f"© Serenade, 2025", color=colors['post_title_color'], font=Font.poppins("bold", size=30), align='center')

    img_io = BytesIO()
    draw.save(img_io, format="PNG")
    img_io.seek(0)
    return img_io

def generate_genre_story(genre, color):
    colors = color_picker(color)
    img = Canvas((1080, 1920), color=colors['story_base_color'])
    draw = Editor(img)

    title_font, rank_font = Font("./wydm_app/static/font/Dancing_Script/static/DancingScript-Bold.ttf", size=120), Font.poppins(size=35)
    genre_font, count_font = Font.poppins(size=30), Font.poppins("bold", size=130)

    draw.text((540, 80), "My Serenade", color=colors['title_color'], font=title_font, align='center')
    draw.text((540, 210), "Top Genres", color=colors['title_color'], font=title_font, align='center')

    default_box = Canvas(width=1000, height=364, color="white")
    box = Editor(default_box).rounded_corners(radius=20)

    draw.paste(box, (40, 400))
    draw.paste(box, (40, 800))
    draw.paste(box, (40, 1200))

    draw.text((540, 427), text="A month ago, you have listened to these genres", color=colors['story_nontext_color'], font=rank_font, align='center')
    if genre['short_term'] != []:
        draw.text((200, 540), text=f"{genre['short_term'][0][1]}", color="black", font=count_font, align='center')
        draw.text((200, 690), text=f"{genre['short_term'][0][0].upper()}", color="black", font=genre_font, align='center')
        draw.text((540, 540), text=f"{genre['short_term'][1][1]}", color="black", font=count_font, align='center')
        draw.text((540, 690), text=f"{genre['short_term'][1][0].upper()}", color="black", font=genre_font, align='center')
        draw.text((880, 540), text=f"{genre['short_term'][2][1]}", color="black", font=count_font, align='center')
        draw.text((880, 690), text=f"{genre['short_term'][2][0].upper()}", color="black", font=genre_font, align='center')

    draw.text((540, 827), text="6 months ago, you have listened to these genres", color=colors['story_nontext_color'], font=rank_font, align='center')
    if genre['medium_term'] != []:
        draw.text((200, 940), text=f"{genre['medium_term'][0][1]}", color="black", font=count_font, align='center')
        draw.text((200, 1090), text=f"{genre['medium_term'][0][0].upper()}", color="black", font=genre_font, align='center')
        draw.text((540, 940), text=f"{genre['medium_term'][1][1]}", color="black", font=count_font, align='center')
        draw.text((540, 1090), text=f"{genre['medium_term'][1][0].upper()}", color="black", font=genre_font, align='center')
        draw.text((880, 940), text=f"{genre['medium_term'][2][1]}", color="black", font=count_font, align='center')
        draw.text((880, 1090), text=f"{genre['medium_term'][2][0].upper()}", color="black", font=genre_font, align='center')

    draw.text((540, 1227), text="Last year, you have listened to these genres", color=colors['story_nontext_color'], font=rank_font, align='center')
    if genre['long_term'] != []:
        draw.text((200, 1340), text=f"{genre['long_term'][0][1]}", color="black", font=count_font, align='center')
        draw.text((200, 1490), text=f"{genre['long_term'][0][0].upper()}", color="black", font=genre_font, align='center')
        draw.text((540, 1340), text=f"{genre['long_term'][1][1]}", color="black", font=count_font, align='center')
        draw.text((540, 1490), text=f"{genre['long_term'][1][0].upper()}", color="black", font=genre_font, align='center')
        draw.text((880, 1340), text=f"{genre['long_term'][2][1]}", color="black", font=count_font, align='center')
        draw.text((880, 1490), text=f"{genre['long_term'][2][0].upper()}", color="black", font=genre_font, align='center')

    draw.text((540, 1800), text="© Serenade, 2025", color=colors['title_color'], font=Font.poppins("bold", size=40), align='center')

    # Save & return image
    img_io = BytesIO()
    draw.save(img_io, format="PNG")
    img_io.seek(0)
    return img_io

def generate_genre_post(genre, color):
    colors = color_picker(color)
    img = Canvas((1080, 1320), color=colors['post_base_color'])
    draw = Editor(img)

    title_font, rank_font = Font("./wydm_app/static/font/Dancing_Script/static/DancingScript-Bold.ttf", size=100), Font.poppins(size=30)
    genre_font, count_font = Font.poppins(size=25), Font.poppins("bold", size=100)
    top_start_color, top_end_color = colors['top_start_color'], colors['top_end_color']

    draw.text((540, 80), "My Serenade Top Genres", color=colors['post_title_color'], font=title_font, align='center')

    default_box = Canvas(width=1000, height=296, color="white")
    box = Editor(default_box).rounded_corners(radius=20)

    for x in range(1000):
        blend_factor = x / 1000
        r = int(top_start_color[0] * (1 - blend_factor) + top_end_color[0] * blend_factor)
        g = int(top_start_color[1] * (1 - blend_factor) + top_end_color[1] * blend_factor)
        b = int(top_start_color[2] * (1 - blend_factor) + top_end_color[2] * blend_factor)
        box.rectangle(position=(x, 0), width=1, height=296, fill=(r, g, b)).rounded_corners(radius=20)

    draw.paste(box, (40, 250))
    draw.paste(box, (40, 570))
    draw.paste(box, (40, 890))

    draw.text((540, 277), text="A month ago, you have listened to these genres", color="white", font=rank_font, align='center')
    if genre['short_term'] != []:
        draw.text((200, 360), text=f"{genre['short_term'][0][1]}", color="white", font=count_font, align='center')
        draw.text((200, 480), text=f"{genre['short_term'][0][0].upper()}", color="white", font=genre_font, align='center')
        draw.text((540, 360), text=f"{genre['short_term'][1][1]}", color="white", font=count_font, align='center')
        draw.text((540, 480), text=f"{genre['short_term'][1][0].upper()}", color="white", font=genre_font, align='center')
        draw.text((880, 360), text=f"{genre['short_term'][2][1]}", color="white", font=count_font, align='center')
        draw.text((880, 480), text=f"{genre['short_term'][2][0].upper()}", color="white", font=genre_font, align='center')

    draw.text((540, 597), text="6 months ago, you have listened to these genres", color="white", font=rank_font, align='center')
    if genre['medium_term'] != []:
        draw.text((200, 680), text=f"{genre['medium_term'][0][1]}", color="white", font=count_font, align='center')
        draw.text((200, 800), text=f"{genre['medium_term'][0][0].upper()}", color="white", font=genre_font, align='center')
        draw.text((540, 680), text=f"{genre['medium_term'][1][1]}", color="white", font=count_font, align='center')
        draw.text((540, 800), text=f"{genre['medium_term'][1][0].upper()}", color="white", font=genre_font, align='center')
        draw.text((880, 680), text=f"{genre['medium_term'][2][1]}", color="white", font=count_font, align='center')
        draw.text((880, 800), text=f"{genre['medium_term'][2][0].upper()}", color="white", font=genre_font, align='center')

    draw.text((540, 917), text="Last year, you have listened to these genres", color="white", font=rank_font, align='center')
    if genre['long_term'] != []:
        draw.text((200, 1000), text=f"{genre['long_term'][0][1]}", color="white", font=count_font, align='center')
        draw.text((200, 1120), text=f"{genre['long_term'][0][0].upper()}", color="white", font=genre_font, align='center')
        draw.text((540, 1000), text=f"{genre['long_term'][1][1]}", color="white", font=count_font, align='center')
        draw.text((540, 1120), text=f"{genre['long_term'][1][0].upper()}", color="white", font=genre_font, align='center')
        draw.text((880, 1000), text=f"{genre['long_term'][2][1]}", color="white", font=count_font, align='center')
        draw.text((880, 1120), text=f"{genre['long_term'][2][0].upper()}", color="white", font=genre_font, align='center')

    draw.text((540, 1240), text=f"© Serenade, 2025", color=colors['post_title_color'], font=Font.poppins("bold", size=30), align='center')

    img_io = BytesIO()
    draw.save(img_io, format="PNG")
    img_io.seek(0)
    return img_io

def generate_artist_story(artists, month, color):
    colors = color_picker(color)
    img = Canvas((1080, 1920), color=colors['story_base_color'])
    draw = Editor(img)

    y_box_value, y_text_value, y_image_value = 390, 425, 400
    top_start_color, top_end_color = colors['top_start_color'], colors['top_end_color']

    shadow_intensity, shadow_offset = 40, 8
    shadow_color = (0, 0, 0, int(255 * (shadow_intensity / 80)))

    title_font, rank_font = Font("./wydm_app/static/font/Dancing_Script/static/DancingScript-Bold.ttf", size=100), Font.poppins("bold", size=60)

    draw.text((540, 80), "My Serenade", color=colors['title_color'], font=title_font, align='center')
    draw.text((540, 200), f"{month} Recap", color=colors['title_color'], font=title_font, align='center')

    default_box, gradient_box, shadow_box = Canvas(width=1000, height=120, color=colors['box_color']), Canvas(width=1000, height=120, color=colors['box_color']), Canvas((1000 + shadow_offset, 120 + shadow_offset), color=(0, 0, 0, 0))
    box, gbox, sbox = Editor(default_box).rounded_corners(radius=20), Editor(gradient_box).rounded_corners(radius=20), Editor(shadow_box).rounded_corners(radius=20)

    sbox.rectangle(position=(shadow_offset, shadow_offset), width=1000, height=120, fill=shadow_color).blur(amount=15).rounded_corners(radius=20)

    for x in range(1000):
        blend_factor = x / 1000
        r = int(top_start_color[0] * (1 - blend_factor) + top_end_color[0] * blend_factor)
        g = int(top_start_color[1] * (1 - blend_factor) + top_end_color[1] * blend_factor)
        b = int(top_start_color[2] * (1 - blend_factor) + top_end_color[2] * blend_factor)
        gbox.rectangle(position=(x, 0), width=1, height=120, fill=(r, g, b)).rounded_corners(radius=20)

    for i, track in enumerate(artists[:10]):
        draw.paste(sbox, (40, y_box_value))
        artist_font, pop_font = detect_lang(track['name'], track['name'], layout="story")
        name = f"{track['name'][:30]}..." if len(track['name']) > 30 else track['name']
        if i == 0:
            draw.paste(gbox, (40, y_box_value))
            draw.text((950, y_text_value), f"#{i+1}", color=colors['text_color'], font=rank_font, align='center')
            draw.text((170, y_text_value - 10), f"{name}", color=colors['text_color'], font=artist_font, align='left')
            draw.text((170, y_text_value + 40), f"{track['popularity']} Pop Points", color=colors['text_color'], font=pop_font, align='left')
        else:
            draw.paste(box, (40, y_box_value))
            draw.text((950, y_text_value), f"#{i+1}", color=colors['rank_color'], font=rank_font, align='center')
            draw.text((170, y_text_value - 10), f"{name}", color=colors['story_nontext_color'], font=artist_font, align='left')
            draw.text((170, y_text_value + 40), f"{track['popularity']} Pop Points", color=colors['story_nontext_color'], font=pop_font, align='left')
        
        cover = load_image(track['image'])
        img = Editor(cover).resize((100, 100)).rounded_corners(radius=20)
        draw.paste(img, (50, y_image_value))
        y_box_value += 140
        y_image_value += 140
        y_text_value += 140

    draw.text((540, 1825), f"{month} | © Serenade, 2025", color=colors['title_color'], font=Font.poppins("bold", size=30), align='center')

    img_io = BytesIO()
    draw.save(img_io, format="PNG")
    img_io.seek(0)
    return img_io

def generate_artist_post(artists, month, color):
    colors = color_picker(color)
    img = Canvas((1080, 1320), color=colors['post_base_color'])
    draw = Editor(img)

    y_box_value, y_text_value, y_image_value = 193, 217, 200
    top_start_color, top_end_color = colors['top_start_color'], colors['top_end_color']

    shadow_intensity, shadow_offset = 40, 8
    shadow_color = (0, 0, 0, int(255 * (shadow_intensity / 100)))

    title_font, rank_font = Font("./wydm_app/static/font/Dancing_Script/static/DancingScript-Bold.ttf", size=80), Font.poppins("bold", size=40)

    draw.text((540, 70), f"My Serenade {month} Recap", color=colors['post_title_color'], font=title_font, align='center')

    default_box, gradient_box, shadow_box = Canvas(width=1000, height=80, color=colors['box_color']), Canvas(width=1000, height=80, color=colors['box_color']), Canvas((1000 + shadow_offset, 80 + shadow_offset), color=(0, 0, 0, 0))
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
            draw.text((90, y_text_value), f"{i+1}", color=colors['text_color'], font=rank_font, align='center')
            draw.text((205, y_text_value - 5), f"{name}", color=colors['text_color'], font=track_font, align='left')
            draw.text((205, y_text_value + 25), f"{track['popularity']} Pop Points", color=colors['text_color'], font=pop_font, align='left')
            draw.text((950, y_text_value + 5), f"#{i+1}", color=colors['text_color'], font=rank_font, align='center')
        else:
            draw.paste(box, (40, y_box_value))
            draw.text((90, y_text_value), f"{i+1}", color=colors['rank_color'], font=rank_font, align='center')
            draw.text((205, y_text_value - 5), f"{name}", color=colors['story_nontext_color'], font=track_font, align='left')
            draw.text((205, y_text_value + 25), f"{track['popularity']} Pop Points", color=colors['story_nontext_color'], font=pop_font, align='left')
            draw.text((950, y_text_value + 5), f"#{i+1}", color=colors['story_nontext_color'], font=rank_font, align='center')
        
        cover = load_image(track['image'])
        img = Editor(cover).resize((65, 65)).rounded_corners(radius=10)
        draw.paste(img, (130, y_image_value))
        y_box_value += 105
        y_image_value += 105
        y_text_value += 105

    draw.text((540, 1250), f"{month} | © Serenade, 2025", color=colors['post_title_color'], font=Font.poppins("bold", size=30), align='center')

    img_io = BytesIO()
    draw.save(img_io, format="PNG")
    img_io.seek(0)
    return img_io

def generate_recap_image(request):
    layout = request.GET.get("layout", "story")
    metric = request.GET.get("metric", "tracks")
    period = request.GET.get("period", "short_term")
    color = request.GET.get("color", "default")
    access_token = request.COOKIES.get("access_token")
    # if not access_token:
    #     return redirect("auth")

    try:
        sp = Spotify(auth=access_token)
        top_tracks = sp.current_user_top_tracks(time_range=period, limit=10)
        top_artists = sp.current_user_top_artists(time_range=period, limit=10)
        month = datetime.datetime.now().strftime("%B")

        formatted_tracks, formatted_artists, top_tracks_by_period = [], [], {}
        top_tracks_by_period = {}

        time_ranges = ["short_term", "medium_term", "long_term"]
        track_history = defaultdict(lambda: {"short_term": (0, False), "medium_term": (0, False), "long_term": (0, False)})
        genre_history = defaultdict(lambda: {"short_term": None, "medium_term": None, "long_term": None})

        # Generate the image based on the selected layout
        if layout == "story":
            if metric == "tracks":
                for i, track in enumerate(top_tracks["items"]):
                    artist_name = track["artists"][0]["name"]
                    track_name = track["name"]
                    album_cover = track["album"]["images"][0]["url"] if track["album"]["images"] else None
                    duration = track["duration_ms"]
                    _duration = format_duration(duration // 1000)

                    formatted_tracks.append({
                        "name": track_name,
                        "artist": artist_name,
                        "album_cover": album_cover,
                        "duration": _duration
                })
                img_io = generate_story_recap(formatted_tracks, month, color)
            elif metric == "artists":
                for i, track in enumerate(top_artists["items"]):
                    artist_name = track["name"]
                    artist_image = track["images"][0]["url"] if track["images"] else None
                    popularity = track["popularity"]

                    formatted_artists.append({
                        "name": artist_name,
                        "image": artist_image,
                        "popularity": popularity
                })
                img_io = generate_artist_story(formatted_artists, month, color)
            elif metric == "trends":
                for period in time_ranges:
                    top_tracks_by_period[period] = sp.current_user_top_tracks(limit=50, time_range="long_term")["items"]

                for period in time_ranges:
                    for rank, track in enumerate(top_tracks_by_period[period], start=1):
                        track_name = track["name"]
                        album_cover = track["album"]["images"][0]["url"] if track["album"]["images"] else None

                        track_history[track_name]["artist"] = track["artists"][0]["name"]
                        track_history[track_name]["album_cover"] = album_cover
                        track_history[track_name][period] = (rank, rank == 50)

                sorted_tracks = {
                    "short_term": sorted(
                        track_history.items(),
                        key=lambda x: (x[1]["short_term"][0] if x[1]["short_term"][0] > 0 else float('inf'), x[1]["short_term"][1]),
                        reverse=True
                    ),
                    "medium_term": sorted(
                        track_history.items(),
                        key=lambda x: (x[1]["medium_term"][0] if x[1]["medium_term"][0] > 0 else float('inf'), x[1]["medium_term"][1]),
                        reverse=True
                    ),
                    "long_term": sorted(
                        track_history.items(),
                        key=lambda x: (x[1]["long_term"][0] if x[1]["long_term"][0] > 0 else float('inf'), x[1]["long_term"][1]),
                        reverse=True
                    ),
                }

                filtered_sorted_tracks = {
                    period: [track for track in tracks if track[1][period][0] > 0]
                    for period, tracks in sorted_tracks.items()
                }

                for period, tracks in filtered_sorted_tracks.items():
                    for track in tracks:
                        if track[1][period][1]:
                            track[1][period] = "50+"
                        else:
                            track[1][period] = track[1][period][0]

                img_io = generate_trend_story(filtered_sorted_tracks, color)
            elif metric == "genres":
                for period in time_ranges:
                    top_tracks_by_period[period] = sp.current_user_top_tracks(limit=10, time_range=period)["items"]

                for period in time_ranges:
                    all_genres = []
                    for track in top_tracks_by_period[period]:
                        genres = sp.artist(track["artists"][0]["id"])["genres"]
                        all_genres.extend(genres)

                    genre_counts = Counter(all_genres)
                    genre_history[period] = genre_counts.most_common(3)
                
                img_io = generate_genre_story(genre_history, color)
        elif layout == "list":
            if metric == "tracks":
                for i, track in enumerate(top_tracks["items"]):
                    artist_name = track["artists"][0]["name"]
                    track_name = track["name"]
                    album_cover = track["album"]["images"][0]["url"] if track["album"]["images"] else None
                    duration = track["duration_ms"]
                    _duration = format_duration(duration // 1000)

                    formatted_tracks.append({
                        "name": track_name,
                        "artist": artist_name,
                        "album_cover": album_cover,
                        "duration": _duration
                })
                img_io = generate_post_recap(formatted_tracks, month, color)
            elif metric == "artists":
                for i, track in enumerate(top_artists["items"]):
                    artist_name = track["name"]
                    artist_image = track["images"][0]["url"] if track["images"] else None
                    popularity = track["popularity"]

                    formatted_artists.append({
                        "name": artist_name,
                        "image": artist_image,
                        "popularity": popularity
                })
                img_io = generate_artist_post(formatted_artists, month, color)
            elif metric == "trends":
                for period in time_ranges:
                    top_tracks_by_period[period] = sp.current_user_top_tracks(limit=50, time_range=period)["items"]

                for period in time_ranges:
                    for rank, track in enumerate(top_tracks_by_period[period], start=1):
                        track_name = track["name"]
                        album_cover = track["album"]["images"][0]["url"] if track["album"]["images"] else None

                        track_history[track_name]["artist"] = track["artists"][0]["name"]
                        track_history[track_name]["album_cover"] = album_cover
                        track_history[track_name][period] = (rank, rank == 50)

                sorted_tracks = {
                    "short_term": sorted(
                        track_history.items(),
                        key=lambda x: (x[1]["short_term"][0] if x[1]["short_term"][0] > 0 else float('inf'), x[1]["short_term"][1]),
                        reverse=True
                    ),
                    "medium_term": sorted(
                        track_history.items(),
                        key=lambda x: (x[1]["medium_term"][0] if x[1]["medium_term"][0] > 0 else float('inf'), x[1]["medium_term"][1]),
                        reverse=True
                    ),
                    "long_term": sorted(
                        track_history.items(),
                        key=lambda x: (x[1]["long_term"][0] if x[1]["long_term"][0] > 0 else float('inf'), x[1]["long_term"][1]),
                        reverse=True
                    ),
                }

                filtered_sorted_tracks = {
                    period: [track for track in tracks if track[1][period][0] > 0]
                    for period, tracks in sorted_tracks.items()
                }

                for period, tracks in filtered_sorted_tracks.items():
                    for track in tracks:
                        if track[1][period][1]:
                            track[1][period] = "50+"
                        else:
                            track[1][period] = track[1][period][0]

                img_io = generate_trend_post(filtered_sorted_tracks, color)
            elif metric == "genres":
                for period in time_ranges:
                    top_tracks_by_period[period] = sp.current_user_top_tracks(limit=10, time_range=period)["items"]

                for period in time_ranges:
                    all_genres = []
                    for track in top_tracks_by_period[period]:
                        genres = sp.artist(track["artists"][0]["id"])["genres"]
                        all_genres.extend(genres)

                    genre_counts = Counter(all_genres)
                    genre_history[period] = genre_counts.most_common(3)
                
                img_io = generate_genre_post(genre_history, color)

        return HttpResponse(img_io.getvalue(), content_type="image/png")

    except Exception as e:
        print(f"Error: {e}")
    #     return redirect("auth")




# Spotify Authentication
def spotify_auth(request):
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='user-top-read')
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def spotify_callback(request):
    try:
        sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='user-top-read')
        token_info = sp_oauth.get_access_token(request.GET['code'])

        if not token_info:
            return HttpResponseServerError("Failed to retrieve access token.")
        
        access_token = token_info['access_token']
        response = redirect('toptracks')
        response.set_cookie('access_token', access_token, max_age=3600, httponly=True, samesite="Lax", secure=False)
        return response
    except Exception as e:
        return HttpResponseServerError(f"An error occurred: {str(e)}")

def toptracks(request):
    access_token = request.COOKIES.get('access_token')
    # if not access_token:
    #     return redirect('auth')
    try:
        current_month = datetime.datetime.now().strftime('%B')
        return render(request, 'toptracks.html', {'current_month': current_month})
    except Exception as e:
        print(f"Error: {e}")
        # return redirect('auth')



# Redirection
def index(request):
    return render(request, "index.html")

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def auth_view(request):
    return render(request, 'auth.html')

def form_page(request, option):
    if option == "auth":
        return render(request, 'auth.html')
    else:
        return render(request, "wydm.html", {"option": option})

def response_page(request, slug):
    invite = get_object_or_404(Invitation, slug=slug)

    if request.method == "POST":
        action = request.POST.get("response")

        if action == "accept":
            message = f"{invite.recipient_name} has accepted {invite.sender_name}'s date invitation!"
            response_text = "Good job! You'll take it from here. Good luck!"
        else:
            message = f"{invite.recipient_name} has declined {invite.sender_name}'s date invitation."
            response_text = "Awww, but don't lose hope. There's still someone who would like to go out with you!"

        return render(request, "response.html", {
            "invite": invite,
            "message": message,
            "response_text": response_text
        })

    return render(request, "wydm.html", {"invite": invite})

def about(request):
    return render(request, "about.html")

def privacy(request):
    return render(request, "privacy.html")

def creator(request):
    return render(request, "creator.html")

def create_invite(request):
    if request.method == "POST":
        sender_name = request.POST.get("sender_name")
        recipient_name = request.POST.get("recipient_name")
        option_choice = request.POST.get("option_choice")
        _message = request.POST.get("message")

        if not _message or _message == "":
            _message = f"I really like you, {recipient_name}. Can we go out?"

        option_value = OPTION_CHOICES.get(option_choice, 0)
        invite = Invitation.objects.create(sender_name=sender_name, recipient_name=recipient_name, slug=uuid.uuid4().hex[:6], option=option_value, message=_message)
        invite_link = f"{request.scheme}://{request.get_host()}/wydm/{invite.slug}/"
        return render(request, "success.html", {"invite_link": invite_link, "message": _message})
    return render(request, "wydm.html")

def view_invite(request, slug):
    invite = get_object_or_404(Invitation, slug=slug)
    random_quote = random.choice(ROMANTIC_QUOTES)
    return render(request, "date.html", {"invite": invite, "random_quote": random_quote})