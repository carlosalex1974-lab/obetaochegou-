import http.server
import socketserver

PORT = 5500
Handler = http.server.SimpleHTTPRequestHandler

# Usando 127.0.0.1 explicitamente para evitar problemas de IPv6/localhost
with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
    print(f"Servidor rodando em http://127.0.0.1:{PORT}")
    httpd.serve_forever()
