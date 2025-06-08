from lexer import tokenize
from parser import VaporParser
import sys

def main():
    # Crear un programa VaporLang de ejemplo si no se proporciona archivo
    if len(sys.argv) < 2:
        print("Usando programa de ejemplo...")
        code = """
        fondo degradado #290033 -> #00A2FF
        figura piramide pos(400,300) tam 100 color #FF00FF alpha 0.7
        texto "DREAMNATION" pos(300,100) color #FFFFFF
        efecto scanlines grosor 2
        """
    else:
        try:
            with open(sys.argv[1], 'r') as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Error: Archivo no encontrado - {sys.argv[1]}")
            return
    
    # Fase léxica
    tokens = list(tokenize(code))
    print("\nTokens generados:")
    for i, (token_type, token_value) in enumerate(tokens):
        print(f"{i+1}: ({token_type}, {repr(token_value)})")
    
    # Fase sintáctica
    parser = VaporParser(tokens)
    image = parser.parse()
    
    if image:
        output_file = "vaporwave_output.png"
        image.save(output_file)
        print(f"\n¡Imagen generada con éxito! Guardada como: {output_file}")
        image.show()
    else:
        print("\nNo se pudo generar la imagen debido a errores")

if __name__ == "__main__":
    main()