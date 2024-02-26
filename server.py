import http.server
import socketserver
import os

# Define the port number to run the server on
PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/deleteJson':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Delete Json file</h1><p>This route delete json file.</p>")
            if os.path.exists("data.json"):
              # Delete the file
              os.remove("data.json")
              print("File deleted successfully.")
        else:
            # If the path is not '/about', let the parent class handle it
            super().do_GET()

# Create a simple HTTP server with the custom request handler
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print("Server running at port", PORT)
    # Start the server
    httpd.serve_forever()
