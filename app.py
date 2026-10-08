from flask import Flask, Response, render_template_string, request
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template_string(
        """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title id="page-title">chasyprox ⚡</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root {
                --bg: #030712;
                --surface: #111827;
                --surface-hover: #1f2937;
                --accent: #6366f1;
                --accent-glow: rgba(99, 102, 241, 0.3);
                --text: #f3f4f6;
                --text-muted: #9ca3af;
                --border: rgba(255, 255, 255, 0.08);
            }
            body {
                background: var(--bg);
                color: var(--text);
                font-family: 'Inter', system-ui, sans-serif;
                margin: 0;
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }
            .container {
                width: 90%;
                max-width: 650px;
                padding: 20px;
                box-sizing: border-box;
            }
            .card {
                background: var(--surface);
                border: 1px solid var(--border);
                border-radius: 24px;
                padding: 40px;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
                text-align: center;
            }
            .brand {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 12px;
                margin-bottom: 8px;
            }
            .brand i {
                font-size: 30px;
                color: #818cf8;
                filter: drop-shadow(0 0 12px var(--accent-glow));
            }
            h1 {
                font-size: 34px;
                font-weight: 800;
                margin: 0;
                background: linear-gradient(135deg, #fff 20%, #818cf8 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            p.desc {
                color: var(--text-muted);
                font-size: 14px;
                margin-bottom: 30px;
            }
            .search-bar {
                display: flex;
                align-items: center;
                background: #090d16;
                border: 2px solid var(--border);
                border-radius: 16px;
                padding: 6px 6px 6px 18px;
                transition: all 0.25s ease;
            }
            .search-bar:focus-within {
                border-color: var(--accent);
                box-shadow: 0 0 25px var(--accent-glow);
            }
            .search-bar input {
                flex: 1;
                background: transparent;
                border: none;
                color: var(--text);
                font-size: 16px;
                outline: none;
            }
            .search-bar input::placeholder {
                color: #4b5563;
            }
            .search-bar button {
                background: var(--accent);
                color: white;
                border: none;
                padding: 14px 26px;
                border-radius: 12px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.1s, opacity 0.2s;
            }
            .search-bar button:hover {
                opacity: 0.9;
            }
            .search-bar button:active {
                transform: scale(0.97);
            }
            .chips {
                display: flex;
                justify-content: center;
                gap: 10px;
                margin-top: 20px;
                flex-wrap: wrap;
            }
            .chip {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid var(--border);
                padding: 8px 14px;
                border-radius: 20px;
                font-size: 13px;
                color: var(--text-muted);
                cursor: pointer;
                transition: all 0.2s;
            }
            .chip:hover {
                background: var(--surface-hover);
                color: var(--text);
                border-color: rgba(255, 255, 255, 0.2);
            }
            .footer {
                margin-top: 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 12px;
                color: #4b5563;
                border-top: 1px solid var(--border);
                padding-top: 15px;
            }
            .cloak-btn {
                background: none;
                border: none;
                color: var(--text-muted);
                cursor: pointer;
                font-size: 12px;
            }
            .cloak-btn:hover {
                color: var(--accent);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <div class="brand">
                    <i class="fa-solid fa-bolt-lightning"></i>
                    <h1>chasyprox</h1>
                </div>
                <p class="desc">Railway Unblocked Core v8.0</p>

                <form action="/fetch" method="GET">
                    <div class="search-bar">
                        <input type="text" name="url" placeholder="Enter URL (e.g. tiktok.com)" autocomplete="off" required>
                        <button type="submit">Launch</button>
                    </div>
                </form>

                <div class="chips">
                    <span class="chip" onclick="fill('https://tiktok.com')">TikTok</span>
                    <span class="chip" onclick="fill('https://discord.com')">Discord</span>
                    <span class="chip" onclick="fill('https://wikipedia.org')">Wikipedia</span>
                </div>

                <div class="footer">
                    <span>chasyprox • Railway Node</span>
                    <button class="cloak-btn" onclick="toggleCloak()"><i class="fa-solid fa-user-secret"></i> Cloak Tab</button>
                </div>
            </div>
        </div>

        <script>
            function fill(url) {
                document.querySelector('input[name="url"]').value = url;
            }

            let cloaked = false;
            function toggleCloak() {
                const title = document.getElementById('page-title');
                if (!cloaked) {
                    title.innerText = "Google Classroom";
                    alert("Tab cloaked as Google Classroom!");
                    cloaked = true;
                } else {
                    title.innerText = "chasyprox ⚡";
                    alert("Tab uncloaked.");
                    cloaked = false;
                }
            }
        </script>
    </body>
    </html>
    """
    )


@app.route("/fetch")
def fetch_proxy():
    target_url = request.args.get("url", "").strip()
    if not target_url:
        return "Error: No URL provided.", 400

    if not target_url.startswith("http://") and not target_url.startswith(
        "https://"
    ):
        target_url = "https://" + target_url

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        response = requests.get(target_url, headers=headers, timeout=12)

        excluded_headers = [
            "content-encoding",
            "content-length",
            "transfer-encoding",
            "connection",
            "x-frame-options",
            "content-security-policy",
        ]
        clean_headers = [
            (name, value)
            for name, value in response.raw.headers.items()
            if name.lower() not in excluded_headers
        ]

        return Response(response.content, response.status_code, clean_headers)

    except Exception as e:
        return f"Fetch Error: {str(e)}", 500


if __name__ == "__main__":
    app.run()
