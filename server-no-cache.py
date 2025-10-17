#!/usr/bin/env python3

"""
Servidor HTTP local que respeta los headers de no-caché
Para desarrollo local sin problemas de caché
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Agregar headers para evitar caché
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def guess_type(self, path):
        # Asegurar tipos MIME correctos
        mimetype, encoding = super().guess_type(path)
        if path.endswith('.js'):
            return 'application/javascript'
        elif path.endswith('.css'):
            return 'text/css'
        elif path.endswith('.html'):
            return 'text/html'
        return mimetype

def main():
    PORT = 8080
    
    # Cambiar al directorio del script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print(f"🚀 Servidor EduCalc iniciado en http://localhost:{PORT}")
    print("💡 Sin problemas de caché - los cambios se ven inmediatamente")
    print("🛑 Presiona Ctrl+C para detener")
    print("-" * 50)
    
    try:
        with socketserver.TCPServer(("", PORT), NoCacheHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Puerto {PORT} ya está en uso")
            print("💡 Prueba: lsof -ti:8080 | xargs kill -9")
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
