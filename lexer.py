import re

TOKENS = [
    ('FONDO', r'fondo'),
    ('FIGURA_TYPE', r'(piramide|sol|grid)'),
    ('TEXTO', r'texto'),
    ('EFECTO_TYPE', r'(scanlines|glitch)'),
    ('COLOR', r'#[0-9a-fA-F]{6}'),
    ('POS', r'pos\(\d+,\d+\)'),
    ('TAM', r'tam\s+\d+'),
    ('CADENA', r'"[^"]*"'),
    ('DEGRADADO', r'degradado'),
    ('ALPHA', r'alpha\s+\d\.\d'),
    ('OPERADOR', r'->'),
    ('NUMERO', r'\d+'),
    ('IGNORAR', r'\s+'),
]

def tokenize(code):
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKENS)
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
        elif token_type == 'ALPHA':
            token_value = float(re.search(r'\d\.\d', token_value).group())
        elif token_type == 'CADENA':
            token_value = token_value[1:-1]  # Remover comillas
        
        yield (token_type, token_value)
# Ejemplo de uso
#code = """figura piramide pos(50,70) tam 40 texto "DREAM" pos(30,50) color #FFFFFF"""
#for token in tokenize(code): print(token)
