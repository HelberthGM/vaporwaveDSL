import re

def tokenize(code):
    tokens = [
        ('FONDO', r'fondo'),
        ('FIGURA', r'figura'),
        ('FIGURA_TYPE', r'(piramide|sol|grid)'),
        ('TEXTO', r'texto'),
        ('EFECTO', r'efecto'),
        ('EFECTO_TYPE', r'(scanlines|glitch|vhs|neon)'),
        ('ELEMENTO', r'elemento'),
        ('ELEMENTO_TYPE', r'(busto|palmera|columnas|win95)'),
        ('COLOR_VALUE', r'#[0-9a-fA-F]{6}'),
        ('POS', r'pos\(\d+,\d+\)'),
        ('TAM', r'tam\s+(\d+)'),  
        ('CADENA', r'"[^"]*"'),
        ('DEGRADADO', r'degradado'),
        ('ALPHA', r'alpha\s+\d\.\d+'),
        ('OPERADOR', r'->'),
        ('NUMERO', r'\d+'),
        ('FLOAT', r'\d+\.\d+'),
        ('COLOR_KEYWORD', r'color'),
        ('INTENSIDAD', r'intensidad'),
        ('GROSOR', r'grosor'),
        ('IGNORAR', r'\s+'),
    ]
    
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in tokens)
    
    for match in re.finditer(token_regex, code):
        token_type = match.lastgroup
        token_value = match.group()
        
        if token_type == 'IGNORAR':
            continue
        elif token_type == 'POS':
            x, y = re.findall(r'\d+', token_value)
            token_value = (int(x), int(y))
        elif token_type == 'TAM':
            token_value = int(re.search(r'\d+', token_value).group())
        elif token_type == 'NUMERO':
            token_value = int(token_value)
        elif token_type == 'FLOAT':
            token_value = float(token_value)
        elif token_type == 'ALPHA':
            token_value = float(re.search(r'\d\.\d+', token_value).group())
        elif token_type == 'CADENA':
            token_value = token_value[1:-1]
        
        yield (token_type, token_value)
