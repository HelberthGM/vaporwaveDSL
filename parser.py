from PIL import Image, ImageDraw, ImageFont
import math
import random

class VaporParser:
    def __init__(self, tokens):
        self.tokens = list(tokens)  # Convertimos a lista para indexación
        self.pos = 0
        self.img = Image.new('RGB', (800, 600), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.img, 'RGBA')
        self.current_color = "#FFFFFF"
        self.vapor_palette = [
            "#FF00FF", "#00FFFF", "#FF9900", "#290033", "#00A2FF",
            "#FF0066", "#33CCCC", "#663399", "#FF66CC", "#00FF99"
        ]
    
    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def consume(self, expected_type=None):
        if not self.current_token():
            raise SyntaxError("Fin inesperado del programa")
        
        token_type, token_value = self.current_token()
        
        if expected_type and token_type != expected_type:
            expected_str = ", ".join(expected_type) if isinstance(expected_type, tuple) else expected_type
            raise SyntaxError(
                f"Error en token {self.pos+1}: Esperaba {expected_str}, "
                f"obtuve {token_type} ('{token_value}')"
            )
        
        self.pos += 1
        return token_value
    
    def parse(self):
        try:
            while self.current_token():
                token_type, _ = self.current_token()
                
                if token_type == 'FONDO':
                    self.parse_background()
                elif token_type == 'FIGURA_TYPE':
                    self.parse_figure()
                elif token_type == 'TEXTO':
                    self.parse_text()
                elif token_type == 'EFECTO_TYPE':
                    self.parse_effect()
                # Nuevos comandos vaporwave
                elif token_type == 'JAPANESE_TEXT':
                    self.parse_japanese_text()
                elif token_type == 'VAPOR_EFFECT':
                    self.parse_vapor_effect()
                else:
                    raise SyntaxError(f"Comando inválido: {token_type}")
            
            return self.img
        except SyntaxError as e:
            print(f"Error de sintaxis: {e}")
            # Mostrar contexto del error
            start = max(0, self.pos - 2)
            end = min(len(self.tokens), self.pos + 3)
            context = " > ".join(f"{t[0]}({t[1]})" for t in self.tokens[start:end])
            print(f"Contexto: ...{context}...")
            return None
    
###
    def parse_background(self):
        self.consume('FONDO')
        color = self.consume('COLOR')
        if color.startswith('#'):
            self.img = Image.new('RGB', (800, 600), color)
        else:
            raise SyntaxError(f"Color de fondo inválido: {color}")
    
    def parse_figure(self):
        self.consume('FIGURA_TYPE')
        figure_type = self.consume('FIGURA')
        x = int(self.consume('NUMERO'))
        y = int(self.consume('NUMERO'))
        size = int(self.consume('NUMERO'))
        
        if figure_type == 'CIRCULO':
            self.draw.ellipse((x, y, x + size, y + size), fill=self.current_color)
        elif figure_type == 'CUADRADO':
            self.draw.rectangle((x, y, x + size, y + size), fill=self.current_color)
        else:
            raise SyntaxError(f"Tipo de figura desconocido: {figure_type}")
        
    def parse_text(self):  
        self.consume('TEXTO')
        text = self.consume('CADENA')
        x = int(self.consume('NUMERO'))
        y = int(self.consume('NUMERO'))
        font_size = int(self.consume('NUMERO'))
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        
        self.draw.text((x, y), text, fill=self.current_color, font=font)
    
    def parse_effect(self):
        self.consume('EFECTO_TYPE')
        effect_type = self.consume('EFECTO')
        
        if effect_type == 'VAPOR':
            self.apply_vapor_effect()
        else:
            raise SyntaxError(f"Efecto desconocido: {effect_type}")
    
    def apply_vapor_effect(self):
        width, height = self.img.size
        vapor_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(vapor_image)
        
        for _ in range(100):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(20, 100)
            color = random.choice(self.vapor_palette)
            draw.ellipse((x, y, x + size, y + size), fill=color + '80')
        vapor_image = vapor_image.filter(ImageFilter.GaussianBlur(radius=10))
        self.img = Image.alpha_composite(self.img.convert('RGBA'), vapor_image)
        self.img = self.img.convert('RGB')
        self.current_color = "#FFFFFF"
        self.draw = ImageDraw.Draw(self.img, 'RGBA')
        self.draw.text((10, 10), "Efecto Vapor aplicado", fill=self.current_color)
        self.draw.text((10, 30), "¡Disfruta de tu arte vaporwave!", fill=self.current_color)
  ### 
    def get_vapor_color(self, base_color=None):
        #Devuelve un color de la paleta vaporwave o modifica uno existente
        if base_color:
            # Convertir a HSV y ajustar para dar efecto neón
            r, g, b = int(base_color[1:3], 16), int(base_color[3:5], 16), int(base_color[5:7], 16)
            # Aumentar saturación
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            s = min(1.0, s * 1.8)  # Aumentar saturación
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            return f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}"
        return random.choice(self.vapor_palette)

    def draw_vapor_pyramid(self, pos, size, fill):
        """Pirámide con estilo vaporwave"""
        x, y = pos
        # Crear pirámide con gradiente
        for i in range(size, 0, -1):
            alpha = int(255 * (i/size))
            color = self.get_vapor_color(fill)
            self.draw.polygon([
                (x, y - i), 
                (x - i, y + i), 
                (x + i, y + i)
            ], fill=fill + hex(alpha)[2:])
    
    def draw_vapor_sun(self, pos, size, fill):
        """Sol con rayos distorsionados"""
        x, y = pos
        # Círculo central
        self.draw.ellipse(
            (x - size//2, y - size//2, x + size//2, y + size//2),
            fill=fill
        )
        
        # Rayos con efecto de distorsión
        for i in range(12):
            angle = math.radians(i * 30)
            # Variación aleatoria para efecto "glitch"
            offset = random.randint(-size//10, size//10)
            start_x = x + (size//2 + offset) * math.cos(angle)
            start_y = y + (size//2 + offset) * math.sin(angle)
            end_x = x + (size * 1.8) * math.cos(angle)
            end_y = y + (size * 1.8) * math.sin(angle)
            self.draw.line((start_x, start_y, end_x, end_y), fill=fill, width=3)
    
    def draw_japanese_text(self, text, pos, color):
        """Texto en japonés (característica vaporwave)"""
        # Solo para demostración - en una implementación real usaríamos una fuente japonesa
        self.draw.text(pos, "日本" * len(text), fill=color, font=self.get_vapor_font())

    def get_vapor_font(self, size=40):
        """Obtener fuente con estilo retro"""
        try:
            # Intentar cargar una fuente vaporwave
            return ImageFont.truetype("vcr_osd_mono.ttf", size)
        except:
            try:
                # Fuente alternativa
                return ImageFont.truetype("arial.ttf", size)
            except:
                # Fuente por defecto
                return ImageFont.load_default()
    
    def draw_vapor_text(self, text, pos, color):
        """Texto con estilo vaporwave"""
        x, y = pos
        font = self.get_vapor_font()
        
        # Sombra neón
        shadow_color = self.get_vapor_color(color)
        self.draw.text((x+3, y+3), text, fill=shadow_color + "80", font=font)
        
        # Texto principal
        self.draw.text(pos, text, fill=color, font=font)
        
        # Resplandor neón (simulado con múltiples líneas)
        for i in range(1, 4):
            alpha = hex(30 - i*10)[2:]  # Disminuir opacidad
            self.draw.text((x-i, y), text, fill=shadow_color + alpha, font=font)
            self.draw.text((x+i, y), text, fill=shadow_color + alpha, font=font)
            self.draw.text((x, y-i), text, fill=shadow_color + alpha, font=font)
            self.draw.text((x, y+i), text, fill=shadow_color + alpha, font=font)

    def parse_japanese_text(self):
        self.consume('JAPANESE_TEXT')
        content = self.consume('CADENA')
        position = self.consume('POS')
        color = self.current_color
        if self.current_token() and self.current_token()[0] == 'COLOR':
            self.consume('COLOR')
            color = self.consume('COLOR')
        
        self.draw_japanese_text(content, position, color)
    
    def parse_vapor_effect(self):
        self.consume('VAPOR_EFFECT')
        effect_type = self.consume('EFECTO_TYPE')
        
        if effect_type == "vhs":
            self.apply_vhs_distortion()
        elif effect_type == "neon":
            self.apply_neon_effect()
        else:
            raise SyntaxError(f"Efecto vaporwave desconocido: {effect_type}")
###
    def apply_vhs_distortion(self):
        """Simula un efecto VHS distorsionado"""
        width, height = self.img.size
        vhs_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(vhs_image)
        
        for y in range(height):
            offset = random.randint(-5, 5)
            for x in range(width):
                if random.random() < 0.05:
                    color = self.img.getpixel((x, y))
                    draw.point((x + offset, y), fill=color)
        vhs_image = vhs_image.filter(ImageFilter.GaussianBlur(radius=2))
        self.img = Image.alpha_composite(self.img.convert('RGBA'), vhs_image)
        self.img = self.img.convert('RGB')
  