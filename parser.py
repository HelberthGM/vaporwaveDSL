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
    
    #def parse_background(self):
        # Implementación completa como en el ejemplo anterior
        # ...
    
    #def parse_figure(self):
        # Implementación completa como en el ejemplo anterior
        # ...
    
    # ... otros métodos del parser ...