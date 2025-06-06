from lexer import tokenize
from parser import VaporParser
import sys

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo.vapor> [salida.png]")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "salida.png"
    
    try:
        # Leer código fuente
        with open(input_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Fase léxica
        tokens = tokenize(code)
        print("Tokens generados:")
        for token in tokens:
            print(token)
        
        # Reiniciamos el generador para el parser
        tokens = tokenize(code)
        
        # Fase sintáctica
        parser = VaporParser(tokens)
        image = parser.parse()
        
        if image:
            image.save(output_file)
            print(f"Imagen generada: {output_file}")
            image.show()
    
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado - {input_file}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()