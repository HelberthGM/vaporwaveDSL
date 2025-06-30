# vaporwaveDSL

## Gramatica
```
S = { command } | λ;
command = background | figure | text | effect | elemento | command ;

background      = "fondo" "degradado" {color_value} "->" {color_value} ;

figure          = "figura" {figure_type} {position} | "figura" {figure_type} {position} {size_param} | "figura" {figure_type} {position} {color_param} | "figura" {figure_type} {position} {alpha_param} ;
figure_type     = "piramide" | "sol" | "grid" ;

text            = "texto" {string} {position} | "texto" {string} {position} {color_param} |"texto" {string} {position} {size_param} ;

effect          = "efecto" {effect_type} {intensity_param} ;
effect_type     = "scanlines" | "glitch" | "vhs" | "neon" ;

elemento        = "elemento" {elemento_type} {position} {size_param} ;
elemento_type   = "busto" | "palmera" | "columnas" | "win95" ;

position        = "pos" "(" {number} "," {number} ")" ;
size_param      = "tam" {number} ;
color_param     = "color" {color_value} ;
alpha_param     = "alpha" {float} ;
intensity_param = "intensidad" {number} | "grosor" {number} ;

color_value     = "#" hex_digit {6} ;
number          = digit { digit } ;
float           = number "." number ;
string          = '"' { character } '"' ;
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