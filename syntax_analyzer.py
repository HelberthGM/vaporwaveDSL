class SintacticAnalyzer:
    """Analizador sintáctico para VaporLang que solo verifica la sintaxis"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance()
    
    def advance(self):
        """Avanza al siguiente token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def parse(self):
        """Inicia el proceso de análisis sintáctico"""
        self.program()
        if self.current_token is not None:
            self.error("Fin del programa", self.current_token)
        else:
            print("✅ Análisis sintáctico completado con éxito. ¡No se encontraron errores!")
    
    def program(self):
        """<program> = { command }"""
        while self.current_token is not None:
            self.command()
    
    def command(self):
        """<command> = background | figure | text | effect | elemento"""
        if self.current_token is None:
            return
            
        token_type = self.current_token[0]
        
        if token_type == 'FONDO':
            self.background()
        elif token_type == 'FIGURA':
            self.figure()
        elif token_type == 'TEXTO':
            self.text()
        elif token_type == 'EFECTO':
            self.effect()
        elif token_type == 'ELEMENTO':
            self.elemento()
        else:
            self.error("Comando válido (FONDO, FIGURA, TEXTO, EFECTO, ELEMENTO)", token_type)
    
    def background(self):
        self.match('FONDO')
        self.match('DEGRADADO')
        self.color_value()
        self.match('OPERADOR')
        self.color_value()
    
    def figure(self):
        self.match('FIGURA')
        self.figure_type()
        self.position()
        
        while self.current_token is not None and self.current_token[0] in ['TAM', 'COLOR_KEYWORD', 'ALPHA']:
            token_type = self.current_token[0]
            
            if token_type == 'TAM':
                self.match('TAM')
            elif token_type == 'COLOR_KEYWORD':
                self.match('COLOR_KEYWORD')
                self.match('COLOR_VALUE')
            elif token_type == 'ALPHA':
                self.match('ALPHA')
    
    def figure_type(self):
        self.match('FIGURA_TYPE')
    
    def text(self):
        self.match('TEXTO')
        self.match('CADENA')
        self.position()
        
        while self.current_token is not None and self.current_token[0] in ['COLOR_KEYWORD', 'TAM']:
            token_type = self.current_token[0]
            
            if token_type == 'COLOR_KEYWORD':
                self.match('COLOR_KEYWORD')
                self.match('COLOR_VALUE')
            elif token_type == 'TAM':
                self.match('TAM')
    
    def effect(self):
        self.match('EFECTO')
        self.effect_type()
        
        if self.current_token is not None and self.current_token[0] in ['INTENSIDAD', 'GROSOR']:
            token_type = self.current_token[0]
            self.match(token_type)
            self.match('NUMERO')
    
    def effect_type(self):
        self.match('EFECTO_TYPE')
    
    def elemento(self):
        self.match('ELEMENTO')
        self.elemento_type()
        self.position()
        
        if self.current_token is not None and self.current_token[0] == 'TAM':
            self.match('TAM')
    
    def elemento_type(self):
        self.match('ELEMENTO_TYPE')
    
    def position(self):
        self.match('POS')
    
    def color_value(self):
        self.match('COLOR_VALUE')
    
    def match(self, expected_type):
        if self.current_token is None:
            self.error(expected_type, "Fin del programa")
            return
            
        token_type, token_value = self.current_token
        
        if token_type == expected_type:
            self.advance()
        else:
            self.error(expected_type, (token_type, token_value))
    
    def error(self, expected, found):
        if isinstance(found, tuple):
            found_type, found_value = found
            found_str = f"{found_type}({found_value})"
        else:
            found_str = found
        
        error_msg = f"❌ Error de sintaxis en la posición {self.pos}: Se esperaba {expected}, se encontró {found_str}"
        
        # Contexto
        start = max(0, self.pos - 2)
        end = min(len(self.tokens), self.pos + 3)
        context = " -> ".join(f"{t[0]}({t[1]})" for t in self.tokens[start:end])
        
        raise SyntaxError(f"{error_msg}\nContexto: ...{context}...")