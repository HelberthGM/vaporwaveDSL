# vaporwaveDSL

## Gramatica
```
program     = { command } ;
command     = background | figure | text | effect ;
background  = "fondo" "degradado" color "->" color ;
figure      = "figura" figure_type position [ size ] [ color ] [ alpha ] ;
figure_type = "piramide" | "sol" | "grid" ;
text        = "texto" string position [ color ] ;
effect      = "efecto" effect_type [ intensity ] ;
effect_type = "scanlines" | "glitch" ;
position    = "pos" "(" number "," number ")" ;
size        = "tam" number ;
color       = "color" hex_color ;
alpha       = "alpha" float ;
intensity   = "grosor" number ;
hex_color   = "#" hex_digit {6} ;
number      = digit { digit } ;
float       = number "." number ;
string      = '"' { character } '"' ;
```
## Ejemplos de uso

## Fondos degradados:
```
Púrpura (#6A0DAD) → Rosa (#FF00FF)

Azul oscuro (#003366) → Cian (#00FFFF)
```

## Figuras básicas:

### Pirámide simplificada (triángulo)
```
draw.polygon([(x, y-tam), (x-tam, y+tam), (x+tam, y+tam)])
```

### Sol (círculo + líneas radiales)
```
draw.ellipse((x-tam, y-tam, x+tam, y+tam))
for i in range(8):
    angle = i * 45
    draw.line((x, y, x+tam*1.5*cos(angle), y+tam*1.5*sin(angle)))
```

## Efectos rápidos:

### Scanlines (líneas horizontales)
```
for y in range(0, height, 4):
    draw.line((0, y, width, y), fill=(0,0,0,50))
```

### Glitch (desplazamiento aleatorio)
```
offset_x = random.randint(-5, 5)
cropped = img.crop((50, 0, width-50, height))
img.paste(cropped, (50+offset_x, 0))
```