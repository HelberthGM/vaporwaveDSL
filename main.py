from lexer import tokenize
from syntax_analyzer import SintacticAnalyzer
from image_generator import ImageGenerator
import sys
import os

def main():
    # Manejar argumentos de línea de comandos
    if len(sys.argv) < 2:
        print("Usando programa de ejemplo...")
        code = """
        fondo degradado #290033 -> #00A2FF
        figura sol pos(400,300) tam 100 color #e89d33 
        texto "VAPORWAVE" pos(300,100) color #FFFFFF
        efecto scanlines grosor 2
        """
        output_file = "vaporwave_output.png"  # Extensión garantizada
    else:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Determinar archivo de salida con extensión válida
            if len(sys.argv) > 2:
                output_file = ensure_image_extension(sys.argv[2])
            else:
                # Usar mismo nombre con extensión .png
                base_name = os.path.splitext(sys.argv[1])[0]
                output_file = f"{base_name}.png"
                
        except FileNotFoundError:
            print(f"Error: Archivo no encontrado - {sys.argv[1]}")
            return
    
    # Fase léxica
    try:
        tokens = list(tokenize(code))
        """" 
        print("\nTokens generados:")
        for i, (token_type, token_value) in enumerate(tokens):
            print = (f"{i+1}: ({token_type}, {repr(token_value)})")
        """
    except Exception as e:
        print(f"Error en análisis léxico: {e}")
        return
    
    # Fase sintáctica
    try:
        analyzer = SintacticAnalyzer(tokens)
        analyzer.parse()
        print("✅ ¡El código es sintácticamente válido!")
    except SyntaxError as e:
        print(e)
        return
    
    # Fase de generación de imágenes
    try:
        generator = ImageGenerator(tokens)
        image = generator.generate()

        if image:
            if image.mode == 'RGBA':
                image = image.convert('RGB')  # Convertir a RGB para formatos como JPG
            # Guardar con formato basado en extensión
            image.save(output_file, format=get_image_format(output_file))
            print(f"\n🎨 ¡Imagen generada con éxito! Guardada como: {output_file}")
            image.show()
        else:
            print("\n❌ No se pudo generar la imagen debido a errores")
    except Exception as e:
        print(f"\n❌ Error generando imagen: {e}")

def ensure_image_extension(filename):
    """Asegura que el archivo tenga una extensión de imagen válida"""
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    name, ext = os.path.splitext(filename)
    
    if not ext or ext.lower() not in valid_extensions:
        # Añadir extensión PNG por defecto
        return f"{name}.png"
    return filename

def get_image_format(filename):
    """Obtiene el formato de imagen basado en la extensión del archivo"""
    ext = os.path.splitext(filename)[1].lower()
    
    if ext in ['.jpg', '.jpeg']:
        return 'JPEG'
    elif ext == '.gif':
        return 'GIF'
    elif ext == '.bmp':
        return 'BMP'
    else:  # .png y cualquier otro caso
        return 'PNG'

def print_tokens(tokens):
    """Imprime los tokens con información detallada"""
    print("\nLista completa de tokens:")
    print("Pos | Tipo               | Valor")
    print("-" * 40)
    for i, (token_type, token_value) in enumerate(tokens):
        print(f"{i:3} | {token_type:<18} | {repr(token_value)}")

if __name__ == "__main__":
    main()