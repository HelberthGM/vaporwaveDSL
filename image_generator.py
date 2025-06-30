from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

class ImageGenerator:
    """Genera imágenes a partir de tokens VaporLang"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance()
        self.img = Image.new('RGB', (800, 600), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.img, 'RGBA')
        self.current_color = "#FFFFFF"
        self.vapor_palette = [
            "#FF00FF", "#00FFFF", "#FF9900", "#290033", "#00A2FF",
            "#FF0066", "#33CCCC", "#663399", "#FF66CC", "#00FF99"
        ]
    
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def generate(self):
        """Genera la imagen basada en los tokens"""
        try:
            while self.current_token:
                token_type, token_value = self.current_token
                
                if token_type == 'FONDO':
                    self.process_background()
                elif token_type == 'FIGURA':
                    self.process_figure()
                elif token_type == 'TEXTO':
                    self.process_text()
                elif token_type == 'EFECTO':
                    self.process_effect()
                elif token_type == 'ELEMENTO':
                    self.process_elemento()
                else:
                    self.advance()  # Ignorar tokens no procesables
            
            return self.img
        except Exception as e:
            print(f"Error generando imagen: {e}")
            return None
    
    def process_background(self):
        # Consumir tokens en secuencia
        self.advance()  # FONDO
        self.advance()  # DEGRADADO
        color1 = self.current_token[1]  # COLOR_VALUE
        self.advance()
        self.advance()  # OPERADOR
        color2 = self.current_token[1]  # COLOR_VALUE
        self.advance()
        
        # Crear fondo degradado
        width, height = 800, 600
        for y in range(height):
            r = int(int(color1[1:3], 16) * (1 - y/height) + int(color2[1:3], 16) * (y/height))
            g = int(int(color1[3:5], 16) * (1 - y/height) + int(color2[3:5], 16) * (y/height))
            b = int(int(color1[5:7], 16) * (1 - y/height) + int(color2[5:7], 16) * (y/height))
            self.draw.line((0, y, width, y), fill=(r, g, b))
    
    def process_figure(self):
        self.advance()  # FIGURA
        figure_type = self.current_token[1]  # FIGURA_TYPE
        self.advance()
        position = self.current_token[1]  # POS
        self.advance()
        
        # Parámetros por defecto
        size = 50
        color = self.current_color
        alpha = 1.0
        
        # Procesar parámetros opcionales
        while self.current_token and self.current_token[0] in ['TAM', 'COLOR_KEYWORD', 'ALPHA']:
            token_type, token_value = self.current_token
            
            if token_type == 'TAM':
                size = token_value
                self.advance()
            elif token_type == 'COLOR_KEYWORD':
                self.advance()  # COLOR_KEYWORD
                color = self.current_token[1]  # COLOR_VALUE
                self.advance()
            elif token_type == 'ALPHA':
                alpha = token_value
                self.advance()
        
        # Dibujar figura
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        fill = (r, g, b, int(alpha * 255))
        
        if figure_type == "piramide":
            self.draw_pyramid(position, size, fill)
        elif figure_type == "sol":
            self.draw_sun(position, size, fill)
        elif figure_type == "grid":
            self.draw_grid(position, size, fill)
    
    def draw_pyramid(self, pos, size, fill):
        """Dibuja una pirámide con estilo vaporwave"""
        x, y = pos
        self.draw.polygon([
            (x, y - size),         # Vértice superior
            (x - size, y + size),  # Esquina inferior izquierda
            (x + size, y + size)   # Esquina inferior derecha
        ], fill=fill)
    
    def draw_sun(self, pos, size, fill):
        """Dibuja un sol con rayos vaporwave"""
        x, y = pos
        # Círculo central
        self.draw.ellipse(
            (x - size//2, y - size//2, x + size//2, y + size//2),
            fill=fill
        )
        
        # Rayos con efecto vaporwave
        for i in range(12):
            angle = math.radians(i * 30)
            # Variación aleatoria para efecto "glitch"
            offset = random.randint(-size//10, size//10)
            start_x = x + (size//2 + offset) * math.cos(angle)
            start_y = y + (size//2 + offset) * math.sin(angle)
            end_x = x + (size * 1.8) * math.cos(angle)
            end_y = y + (size * 1.8) * math.sin(angle)
            self.draw.line((start_x, start_y, end_x, end_y), fill=fill, width=3)
    
    def draw_grid(self, pos, size, fill):
        """Dibuja una rejilla 3D estilo vaporwave"""
        x, y = pos
        # Líneas horizontales
        for i in range(-3, 4):
            self.draw.line(
                (x - size*3, y + i*size, x + size*3, y + i*size),
                fill=fill, width=2
            )
        
        # Líneas verticales con perspectiva
        for i in range(-3, 4):
            start_x = x + i*size
            self.draw.line(
                (start_x, y - size*2, start_x - size*0.7, y + size*2),
                fill=fill, width=2
            )
    
    def process_text(self):
        self.advance()  # TEXTO
        content = self.current_token[1]  # CADENA
        self.advance()
        position = self.current_token[1]  # POS
        self.advance()

        # Parámetros por defecto
        font_size = 40  # Cambiado de 'size' a 'font_size' para claridad
        color = self.current_color

        # Procesar parámetros opcionales
        while self.current_token and self.current_token[0] in ['COLOR_KEYWORD', 'TAM']:
            token_type, token_value = self.current_token

            if token_type == 'COLOR_KEYWORD':
                self.advance()  # COLOR_KEYWORD
                color = self.current_token[1]  # COLOR_VALUE
                self.advance()
            elif token_type == 'TAM':
                font_size = token_value  # Guardar el tamaño de fuente
                self.advance()

        # Dibujar texto
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)

        # Intentar cargar fuente vaporwave CON EL TAMAÑO CORRECTO
        try:
            font = ImageFont.truetype("fonts/VCR_OSD_MONO.ttf", font_size) # Usar font_size aquí
        except:
            # Fuente por defecto si no se encuentra
            font = ImageFont.load_default()
            # Para fuentes por defecto, necesitamos escalar manualmente
            if hasattr(font, 'getsize'):
                # Calcular posición ajustada para fuentes por defecto
                text_width, text_height = font.getsize(content)
                position = (position[0], position[1] - text_height//2)

        # Texto principal con sombra para efecto neón
        self.draw.text((position[0]+2, position[1]+2), content, fill=(0, 0, 0, 128), font=font)
        self.draw.text(position, content, fill=(r, g, b), font=font)
    
    def process_effect(self):
        self.advance()  # EFECTO
        effect_type = self.current_token[1]  # EFECTO_TYPE
        self.advance()
        
        # Parámetro opcional
        intensity = 2
        if self.current_token and self.current_token[0] in ['INTENSIDAD', 'GROSOR']:
            self.advance()  # INTENSIDAD/GROSOR
            intensity = self.current_token[1]  # NUMERO
            self.advance()
        
        # Aplicar efecto
        if effect_type == "scanlines":
            self.apply_scanlines(intensity)
        elif effect_type == "glitch":
            self.apply_glitch(intensity)
        elif effect_type == "vhs":
            self.apply_vhs(intensity)
        elif effect_type == "neon":
            self.apply_neon(intensity)
    
    def apply_scanlines(self, intensity):
        """Aplica efecto de scanlines (VHS)"""
        height = 600
        for y in range(0, height, intensity * 2):
            self.draw.line((0, y, 800, y), fill=(0, 0, 0, 50))
    
    def apply_glitch(self, intensity):
        """Aplica efecto glitch vaporwave"""
        width, height = 800, 600
        for _ in range(intensity * 10):
            x = random.randint(0, width - 50)
            y = random.randint(0, height - 20)
            w = random.randint(10, 50)
            h = random.randint(1, 5)
            
            # Copiar una pequeña región y desplazarla
            region = self.img.crop((x, y, x + w, y + h))
            offset_x = random.randint(-intensity*3, intensity*3)
            self.img.paste(region, (x + offset_x, y))
    
    def apply_vhs(self, intensity):
        """Aplica efecto VHS característico del vaporwave"""
        # Crear ruido de color
        for _ in range(intensity * 100):
            x, y = random.randint(0, 799), random.randint(0, 599)
            color = random.choice(self.vapor_palette)
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            self.draw.point((x, y), fill=(r, g, b, 30))
        
        # Añadir bandas horizontales
        for i in range(intensity):
            band_height = random.randint(1, 3)
            y = random.randint(0, 599)
            color = random.choice(self.vapor_palette)
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            self.draw.rectangle((0, y, 800, y+band_height), fill=(r, g, b, 40))
    
    def apply_neon(self, intensity):
        """Aplica efecto neón vaporwave a los bordes"""
        # Convertir la imagen original a RGBA
        original_rgba = self.img.convert('RGBA')

        # Crear una capa de brillo en RGBA
        glow = Image.new('RGBA', original_rgba.size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)

        # Aplicar halos de neón
        width, height = original_rgba.size
        for _ in range(intensity * 50):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            r, g, b, a = original_rgba.getpixel((x, y))
            if r + g + b > 450:
                color = random.choice(self.vapor_palette)
                r_val, g_val, b_val = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
                glow_draw.ellipse((x-2, y-2, x+2, y+2), fill=(r_val, g_val, b_val, 30))

        # Combinar las capas
        self.img = Image.alpha_composite(original_rgba, glow)

    
    def process_elemento(self):
        self.advance()  # ELEMENTO
        elemento_type = self.current_token[1]  # ELEMENTO_TYPE
        self.advance()
        position = self.current_token[1]  # POS
        self.advance()
        
        # Parámetro opcional
        size = 100
        if self.current_token and self.current_token[0] == 'TAM':
            size = self.current_token[1]
            self.advance()
        
        # Dibujar elemento
        x, y = position
        
        if elemento_type == "busto":
            # Cabeza
            self.draw.ellipse((x-30, y-50, x+30, y), fill=(200, 200, 200, 180))
            # Hombros
            self.draw.rectangle((x-40, y, x+40, y+30), fill=(200, 200, 200, 180))
        
        elif elemento_type == "palmera":
            # Tronco
            self.draw.rectangle((x-10, y-100, x+10, y), fill=(101, 67, 33, 255))
            # Hojas
            for i in range(5):
                angle = math.radians(i * 72)
                end_x = x + int(100 * math.cos(angle))
                end_y = y - 100 + int(100 * math.sin(angle))
                self.draw.line((x, y-100, end_x, end_y), fill=(0, 200, 0, 200), width=15)
        
        elif elemento_type == "columnas":
            # Base
            self.draw.rectangle((x-20, y-150, x+20, y), fill=(200, 200, 180, 200))
            # Capiteles
            self.draw.rectangle((x-25, y-170, x+25, y-150), fill=(220, 220, 200, 200))
        
        elif elemento_type == "win95":
            # Fondo
            self.draw.rectangle((x-40, y-30, x+40, y+30), fill=(0, 0, 128, 200))
            # Cuadros de colores
            colors = [(0, 128, 0), (128, 0, 0), (255, 255, 0), (0, 128, 0)]
            positions = [(x-30, y-20), (x+5, y-20), (x-30, y+5), (x+5, y+5)]
            for (x_pos, y_pos), color in zip(positions, colors):
                self.draw.rectangle((x_pos, y_pos, x_pos+20, y_pos+20), fill=color)