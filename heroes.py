import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import variables, get_api_riot

font_path = "arial.ttf"


def create_champion_image(info_champ: dict):
    image_url = info_champ['url_image_champion']
    response = requests.get(image_url)
    champ_image = Image.open(BytesIO(response.content))
    
    champ_image = champ_image.resize((300, 300))
    
    width, height = 900, 350
    background_color_image = (39, 38, 43)
    new_champ_image = Image.new("RGB", (width, height), background_color_image)
    
    new_champ_image.paste(champ_image, (10, (height - champ_image.height) // 2))
    
    draw = ImageDraw.Draw(new_champ_image)
    try:
        font = ImageFont.truetype(font_path, 15)
        title_font = ImageFont.truetype(font_path, 20)
    except IOError:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    def draw_text(draw, text, position, font, max_width):
        lines = []
        words = text.split()
        line = ''
        for word in words:
            test_line = f"{line} {word}".strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)
        
        y_text = position[1]
        for line in lines:
            draw.text((position[0], y_text), line, font=font, fill="white")
            bbox = draw.textbbox((0, 0), line, font=font)
            y_text += bbox[3] - bbox[1]
    
    text_x = champ_image.width + 20
    text_y = 25

    draw_text(draw, f"Имя и прозвище: {info_champ['name_champion']} ({info_champ['title_champion']})", (text_x, text_y), title_font, width - champ_image.width - 30)
    text_y += 35
    draw_text(draw, f"Описание: {info_champ['description_champion']}\n", (text_x, text_y), font, width - champ_image.width - 30)
    text_y += 70
    draw_text(draw, f"Класс: {info_champ['tag_champion']}", (text_x, text_y), font, width - champ_image.width - 30)

    return new_champ_image.save(f"{variables.dir_link}{info_champ['name_champion']}_info.png")
