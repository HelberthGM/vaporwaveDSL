# VaporLang User Manual
VaporLang is a DSL (Domain-Specific Language) for creating images with vaporwave aesthetics. This document explains how to use the language and its features.

## Installation 🔧
### Clone the repository:

```
git clone https://github.com/your-username/vaporlang.git
cd vaporlang
```

### Install dependencies:
```
pip install Pillow
```
## Basic Syntax 📝
### General structure
```
[COMMAND] [PARAMETERS] [MODIFIERS]
```
### Comments
```
// This is a comment
```
## Available Commands 🖼️
1. Gradient Background
```
fondo degradado #290033 -> #00A2FF
```
2. Geometric Shapes
Available shapes: sol (sun), piramide (pyramid), grid
```
figura sol pos(400,300) tam 100 color #e89d33 alpha 0.8
figura piramide pos(200,200) tam 80 color #FF00FF
figura grid pos(500,400) tam 50
```

3. Styled Text
```
texto "VAPORWAVE" pos(300,100) tam 60 color #FFFFFF
```
4. Visual Effects
Available effects: scanlines, glitch, vhs, neon
```
efecto scanlines grosor 2
efecto glitch intensidad 3
efecto vhs intensidad 4
efecto neon intensidad 2
```

5. Decorative Elements
Available elements: busto (bust), palmera (palm tree), columnas (columns), win95
```
elemento busto pos(200,400) tam 80
elemento palmera pos(600,500) tam 120
elemento columnas pos(400,450)
elemento win95 pos(100,350) tam 90
```

## Parameters ⚙️
| Parameter | Description | Example |
|:---:|:---:|:---:|
| ```pos(x,y)```	|Position on the image	| ```pos(300,200)``` |
| ```tam <value>``` | Size (integer)	| ```tam 100 ```|
| ```color #RRGGBB``` | Color in hexadecimal	| ```color #FF00FF``` |
| ```alpha <value>```	| Transparency (0.0 to 1.0)	| ```alpha 0.7``` |
| ```grosor <value> ```| Thickness for effects (integer)	| ```grosor 3``` |
| ```intensidad <value> ```| Intensity for effects (integer) | ```intensidad 4 ```|

## Complete Example ✨
VaporLang sample program
```
fondo degradado #290033 -> #00A2FF
figura sol pos(400,300) tam 100 color #e89d33 alpha 0.9
texto "VAPORWAVE" pos(300,100) tam 60 color #FFFFFF
efecto scanlines grosor 2
efecto neon intensidad 3
elemento busto pos(200,400) tam 80
elemento palmera pos(600,500) tam 120
```
## Execution ▶️
### Run with input file:
```
python main.py my_program.vapor
``` 
### Or to specify output file name:
```
python main.py my_program.vapor output.png
```
### Use sample program:
```
python main.py
```
##  Pro Tips 💡
### Custom Fonts:

1. Place ```.ttf``` fonts in the ```fonts/``` directory

The program will automatically look for fonts like:

- ```VCR_OSD_MONO.ttf```
- ```GreelMythology.ttf```
- ```ExtraBlur.ttf```

2. Vaporwave Color Palette:

```
#FF00FF  // Bright magenta
#00FFFF  // Cyan
#FF9900  // Electric orange
#290033  // Dark purple
#00A2FF  // Bright blue
```
3. Transparency Effects:

- Use alpha to create overlay effects

Example: ```alpha 0.5``` for 50% transparency

4. Effect Combinations:

- You can apply multiple effects in sequence

Example: ```efecto scanlines``` followed by ```efecto neon```

## Generative Grammar 📜​
```
S = <command>  ;
<command> = <background> | <figure> | <text> | <effect> | <elemento> | <command>;

<background>      = "fondo" "degradado" {color_value} "->" {color_value} ;

<figure>          = "figura" <figure_type> <position> | "figura" <figure_type> <position> <size_param> | "figura" <figure_type> <position> <color_param> | "figura" <figure_type> {position} {alpha_param} ;
<figure_type>     = "piramide" | "sol" | "grid" ;

<text>            = "texto" <string> <position> | "texto" <string> <position> <color_param> |"texto" <string> <position> <size_param> ;

<effect>          = "efecto" <effect_type> <intensity_param> ;
<effect_type>     = "scanlines" | "glitch" | "vhs" | "neon" ;

<elemento>        = "elemento" <elemento_type> <position> <size_param> ;
<elemento_type>   = "busto" | "palmera" | "columnas" | "win95" ;

<position>        = "pos" "(" <number> "," <number> ")" ;
<size_param>      = "tam" <number> ;
<color_param>     = "color" <color_value> ;
<alpha_param>     = "alpha" <float> ;
<intensity_param> = "intensidad" <number> | "grosor" <number> ;

<color_value>     = "#" <hex_digit> ;
<hex_color> ::= "#" <hex_digit> <hex_digit> <hex_digit> <hex_digit> <hex_digit> <hex_digit>
<hex_digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "a" | "b" | "c" |"d" | "e" | "f" | "A" | "B" | "C" | "D" | "E" | "F"
<float>           = number "." number ;
<string>          = '"' <character> '"' ;
<character>       = "a"|"b"|"c"|"d"|"e"|"f"|"g"|"h"|"i"|"j"|"k"|"l"|"m"|"n"|"i"|"o"|"p"|"q"|"r"|"s"|"t"|"u"|"v"|"x"|"y"|"z"
<number>          = 1|2|3|4|5|6|7|8|9|0
```