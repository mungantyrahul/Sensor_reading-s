from flask import Flask, request, render_template_string

app = Flask(__name__)
latest_temp = 0   # store the last received temperature

# HTML template with a simple gauge
html_template = """
<!DOCTYPE html>
<html>
<head>
  <title>Temperature Meter</title>
  <style>
    body { text-align: center; font-family: Arial; margin-top: 50px; }
    #gauge {
      width: 300px;
      height: 150px;
    }
    .temp {
      font-size: 24px;
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <h1>🌡️ Temperature Gauge</h1>
  <canvas id="gauge"></canvas>
  <div class="temp">Current Temp: {{temp}} °C</div>

  <script>
    let temp = {{temp}};
    let canvas = document.getElementById("gauge");
    let ctx = canvas.getContext("2d");

    function drawGauge(temp) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      let startAngle = Math.PI;
      let endAngle = 0;
      let currentAngle = Math.PI - (temp / 150) * Math.PI;

      // Background arc
      ctx.beginPath();
      ctx.arc(150, 150, 100, startAngle, endAngle, false);
      ctx.lineWidth = 20;
      ctx.strokeStyle = "#eee";
      ctx.stroke();

      // Filled arc
      ctx.beginPath();
      ctx.arc(150, 150, 100, startAngle, currentAngle, true);
      ctx.lineWidth = 20;
      ctx.strokeStyle = "red";
      ctx.stroke();

      // Needle
      ctx.beginPath();
      ctx.moveTo(150, 150);
      ctx.lineTo(150 - 100 * Math.cos(currentAngle), 150 - 100 * Math.sin(currentAngle));
      ctx.lineWidth = 4;
      ctx.strokeStyle = "black";
      ctx.stroke();
    }

    drawGauge(temp);
  </script>
</body>
</html>
"""

@app.route("/update", methods=["GET", "POST"])
def update():
    global latest_temp
    if request.method == "GET":
        temp = request.args.get("temp")
    else:
        data = request.get_json(force=True)
        temp = data.get("temp")
    latest_temp = float(temp)
    return {"status": "success", "temperature": latest_temp}

@app.route("/", methods=["GET"])
def home():
    return render_template_string(html_template, temp=latest_temp)
