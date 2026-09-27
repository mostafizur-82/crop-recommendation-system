from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import pickle


# Load trained Random Forest model
with open("crop_model.pkl", "rb") as file:
    model = pickle.load(file)


class CropRecommendationServer(BaseHTTPRequestHandler):

    # -----------------------------
    # GET REQUEST
    # -----------------------------
    def do_GET(self):

        if self.path == "/":
            self.send_file("index.html", "text/html")

        elif self.path == "/style.css":
            self.send_file("style.css", "text/css")

        elif self.path == "/script.js":
            self.send_file("script.js", "application/javascript")

        else:
            self.send_response(404)
            self.end_headers()


    # -----------------------------
    # SEND FILE
    # -----------------------------
    def send_file(self, filename, content_type):

        try:

            with open(filename, "rb") as file:
                content = file.read()

            self.send_response(200)

            self.send_header(
                "Content-Type",
                content_type
            )

            self.send_header(
                "Content-Length",
                str(len(content))
            )

            self.end_headers()

            self.wfile.write(content)

        except FileNotFoundError:

            self.send_response(404)
            self.end_headers()


    # -----------------------------
    # POST REQUEST
    # -----------------------------
    def do_POST(self):

        if self.path == "/predict":

            content_length = int(
                self.headers["Content-Length"]
            )

            body = self.rfile.read(content_length)

            data = json.loads(body)


            # Get input values
            N = float(data["N"])
            P = float(data["P"])
            K = float(data["K"])

            temperature = float(
                data["temperature"]
            )

            humidity = float(
                data["humidity"]
            )

            ph = float(
                data["ph"]
            )

            rainfall = float(
                data["rainfall"]
            )


            # Prepare input for Random Forest
            features = [[
                N,
                P,
                K,
                temperature,
                humidity,
                ph,
                rainfall
            ]]


            # Predict crop
            prediction = model.predict(features)

            crop = prediction[0]


            # Create response
            response = {
                "crop": crop
            }

            response_data = json.dumps(
                response
            ).encode()


            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/json"
            )

            self.send_header(
                "Content-Length",
                str(len(response_data))
            )

            self.end_headers()

            self.wfile.write(response_data)

        else:

            self.send_response(404)
            self.end_headers()


# -----------------------------
# START SERVER
# -----------------------------

server = HTTPServer(
    ("localhost", 8000),
    CropRecommendationServer
)

print("Server started...")
print("Open: http://localhost:8000")

server.serve_forever()