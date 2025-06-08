from PIL import Image, ImageDraw, ImageFont
import random
import math

class VaporParser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
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
            # Crear un mensaje de error más descriptivo
            line_start = max(0, self.pos - 3)
            line_end = min(len(self.tokens), self.pos + 4)
            context = " ".join(str(t[1]) for t in self.tokens[line_start:line_end])
            
            error_msg = (f"Error de sintaxis en la posición {self.pos}:\n"
                        f"Se esperaba: {expected_type}\n"
                        f"Se encontró: {token_type} ({token_value})\n"
                        f"Contexto: ...{context}...")
            raise SyntaxError(error_msg)
        
        self.pos += 1
        return token_value
    
    def parse(self):
        try:
            while self.current_token():
                token_type, token_value = self.current_token()

                if token_type == 'FONDO':
                    self.parse_background()
                elif token_type == 'FIGURA_TYPE':
                    self.parse_figure()
                elif token_type == 'TEXTO':
                    self.parse_text()
                elif token_type == 'EFECTO_TYPE':
                    self.parse_effect()
                else:
                    # Manejar comandos inesperados
                    raise SyntaxError(f"Comando inválido o fuera de lugar: {token_type}")

            return self.img
        except SyntaxError as e:
            print(f"Error de sintaxis: {e}")
            # Mostrar contexto del error
            start = max(0, self.pos - 2)
            end = min(len(self.tokens), self.pos + 3)
            context = " > ".join(f"{t[0]}({t[1]})" for t in self.tokens[start:end])
            print(f"Contexto: ...{context}...")
            return None
    
    def parse_background(self):
        self.consume('FONDO')
        self.consume('DEGRADADO')

        # Manejar diferentes formatos de color
        color1 = self.get_color_value()
        self.consume('OPERADOR')
        color2 = self.get_color_value()

        # Crear fondo degradado
        for y in range(600):
            r = int(int(color1[1:3], 16) * (1 - y/600) + int(color2[1:3], 16) * (y/600))
            g = int(int(color1[3:5], 16) * (1 - y/600) + int(color2[3:5], 16) * (y/600))
            b = int(int(color1[5:7], 16) * (1 - y/600) + int(color2[5:7], 16) * (y/600))
            self.draw.line((0, y, 800, y), fill=(r, g, b))


    
    def parse_figure(self):
        figure_type = self.consume('FIGURA_TYPE')
        position = self.consume('POS')

        # Parámetros opcionales
        size = 50
        alpha = 1.0
        color = self.current_color

        while self.current_token() and self.current_token()[0] in ['TAM', 'COLOR_KEYWORD', 'ALPHA']:
            token_type, token_value = self.current_token()

            if token_type == 'TAM':
                self.consume('TAM')
                size = token_value

            elif token_type == 'COLOR_KEYWORD':
                self.consume('COLOR_KEYWORD')  # Consume la palabra "color"
                color_value = self.consume('COLOR_VALUE')  # Consume el valor del color
                color = color_value
                self.current_color = color

            elif token_type == 'ALPHA':
                self.consume('ALPHA')
                alpha = token_value

        # Convertir color a RGBA
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        fill = (r, g, b, int(alpha * 255))

        # Dibujar la figura
        if figure_type == "piramide":
            self.draw_pyramid(position, size, fill)
        elif figure_type == "sol":
            self.draw_sun(position, size, fill)

    def draw_pyramid(self, pos, size, fill):
        x, y = pos
        self.draw.polygon([
            (x, y - size),         # Vértice superior
            (x - size, y + size),  # Esquina inferior izquierda
            (x + size, y + size)   # Esquina inferior derecha
        ], fill=fill)
    
    def draw_sun(self, pos, size, fill):
        x, y = pos
        # Círculo central
        self.draw.ellipse(
            (x - size//2, y - size//2, x + size//2, y + size//2),
            fill=fill
        )
        
        # Rayos
        for i in range(8):
            angle = math.radians(i * 45)
            end_x = x + (size * 1.5) * math.cos(angle)
            end_y = y + (size * 1.5) * math.sin(angle)
            self.draw.line((x, y, end_x, end_y), fill=fill, width=3)
    
    def parse_text(self):
        self.consume('TEXTO')
        content = self.consume('CADENA')
        position = self.consume('POS')
        
        # Manejar color opcional
        color = self.current_color
        if self.current_token() and self.current_token()[0] == 'COLOR_KEYWORD':
            self.consume('COLOR_KEYWORD')  # Consume la palabra "color"
            color = self.consume('COLOR_VALUE')  # Consume el valor del color
            self.current_color = color
        
        # Dibujar texto
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        font = ImageFont.load_default()
        
        # Texto principal
        self.draw.text(position, content, fill=(r, g, b), font=font)
        
        # Sombra para efecto neon
        self.draw.text((position[0]+2, position[1]+2), content, fill=(0, 0, 0, 128), font=font)
    
    def parse_effect(self):
        effect_type = self.consume('EFECTO_TYPE')
        
        # Parámetros opcionales
        intensity = 2
        if self.current_token() and self.current_token()[0] == 'GROSOR':
            self.consume('GROSOR')
            intensity = self.consume('NUMERO')
        
        if effect_type == "scanlines":
            self.apply_scanlines(intensity)
        elif effect_type == "glitch":
            self.apply_glitch(intensity)
    
    def apply_scanlines(self, intensity):
        """Aplica efecto de scanlines"""
        for y in range(0, 600, intensity * 2):
            self.draw.line((0, y, 800, y), fill=(0, 0, 0, 50))
    
    def apply_glitch(self, intensity):
        """Aplica efecto glitch simple"""
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
    
    def get_color_value(self):
        # Obtiene un valor de color, manejando diferentes formatos
        if self.current_token()[0] == 'COLOR_KEYWORD':
            self.consume('COLOR_KEYWORD')
            return self.consume('COLOR_VALUE')
        elif self.current_token()[0] == 'COLOR_VALUE':
            return self.consume('COLOR_VALUE')
        else:
            raise SyntaxError(f"Se esperaba un valor de color, se encontró {self.current_token()[0]}")