import re

tokens = [
  ('FONDO', r'fondo'),    
  ('FIGURA', r'(piramide|sol|grid)'),    
  ('TEXTO', r'texto'),    
  ('EFECTO', r'(scanlines|glitch)'),    
  ('COLOR', r'#[0-9a-fA-F]{6}'),    
  ('POS', r'pos\(\d+,\d+\)'),    
  ('TAM', r'tam \d+'),    
  ('CADENA', r'"[^"]*"'),    
  ('DEGRADADO', r'degradado'),    
  ('ALPHA', r'alpha \d\.\d'),    
  ('OPERADOR', r'->'),    
  ('NUMERO', r'\d+'),    
  ('IGNORAR', r'\s+')]

def tokenize(code):    
  token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in tokens)    
  for match in re.finditer(token_regex, code):        
    token_type = match.lastgroup        
    token_value = match.group()                
    if token_type == 'IGNORAR':            
      continue        
    elif token_type == 'POS':            
      # Extraer coordenadas: pos(50,70) → (50, 70)            
      x, y = re.findall(r'\d+', token_value)            
      token_value = (int(x), int(y))        
    elif token_type == 'TAM':            
      # Extraer número: tam 30 → 30            
      token_value = int(re.search(r'\d+', token_value).group())                
      yield (token_type, token_value)
# Ejemplo de usocode = """figura piramide pos(50,70) tam 40texto "DREAM" pos(30,50) color #FFFFFF"""for token in tokenize(code):    print(token)
