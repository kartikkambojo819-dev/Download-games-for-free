import cloudscraper
from bs4 import BeautifulSoup
from flask import Flask, Response, request

app = Flask(__name__)

scraper = cloudscraper.create_scraper()
TARGET_URL = 'https://ankergames.to'
NEW_TITLE = 'Download Games For Piracy'

STYLE_CSS = r"""
*{box-sizing:border-box}
html{background:#03040c !important;}
html, body {
    width: 100%;
    max-width: 100%;
    overflow-x: hidden;
    color: #eef1ff;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
}
/* body aur main wrappers transparent taaki galaxy dikhe */
body, body > div, body > main, #app, #root, #__next, main, .wrap,
[class*="min-h-screen"] {
    background: transparent !important;
    background-color: transparent !important;
    background-image: none !important;
}
#bg {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: -1 !important;
    pointer-events: none !important;
    display: block !important;
}
nav img, header img, [class*="logo"] img {
    display: none !important;
}
.custom-brand-text {
    color: #ffffff !important;
    font-size: 17px !important;
    font-weight: 900 !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.9);
    text-decoration: none !important;
    margin-left: 6px;
    white-space: nowrap;
}
"""

GALAXY_JS = r"""
(function () {
    if (window.__galaxyProxyLoaded) return;
    window.__galaxyProxyLoaded = true;

    function gauss() { return (Math.random() + Math.random() + Math.random() - 1.5) / 1.5; }

    function startGalaxy() {
        if (document.getElementById('bg')) return;

        var canvas = document.createElement('canvas');
        canvas.id = 'bg';
        document.body.prepend(canvas);
        var ctx = canvas.getContext('2d');

        var W = 0, H = 0, dpr = 1;
        var ARMS = 4, N_ARM = 4200, N_BULGE = 900, N_FAR = 320, RADIUS = 900;
        var stars = [], far = [];
        var angle = 0, tiltBase = 1.08;
        var tx = 0, ty = 0, mx = 0, my = 0;
        var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
        var running = true;

        function resize() {
            dpr = Math.min(window.devicePixelRatio || 1, 2);
            W = window.innerWidth;
            H = window.innerHeight;
            canvas.width = Math.floor(W * dpr);
            canvas.height = Math.floor(H * dpr);
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        }

        // radius ke hisaab se rang: core garam, beech neela/purple, bahar pink
        function colorAt(t) {
            var h, s, l;
            if (t < 0.18) { h = 38 + t * 60; s = 95; l = 82 - t * 40; }
            else if (t < 0.55) { h = 215 + (t - 0.18) * 160; s = 90; l = 72; }
            else { h = 275 + (t - 0.55) * 120; s = 85; l = 70; }
            return 'hsl(' + h.toFixed(0) + ',' + s + '%,' + l.toFixed(0) + '%)';
        }

        function build() {
            stars = []; far = [];
            var i, r, t, th, a, sc, thick;

            // spiral arms
            for (i = 0; i < N_ARM; i++) {
                r = Math.pow(Math.random(), 1.35) * RADIUS + 25;
                t = r / RADIUS;
                a = i % ARMS;
                th = a * (Math.PI * 2 / ARMS) + r * 0.0072;
                sc = 0.16 + t * 0.42;
                th += gauss() * sc;
                thick = 46 * Math.exp(-r / 260) + 9;
                stars.push({
                    x: Math.cos(th) * r,
                    z: Math.sin(th) * r,
                    y: gauss() * thick,
                    c: colorAt(t),
                    s: Math.random() * 1.5 + 0.6,
                    al: 0.5 + Math.random() * 0.5,
                    ph: Math.random() * 6.28,
                    tw: Math.random() < 0.35
                });
            }
            // central bulge
            for (i = 0; i < N_BULGE; i++) {
                r = Math.abs(gauss()) * 170 + 6;
                var u = Math.random() * 6.283, v = Math.acos(2 * Math.random() - 1);
                stars.push({
                    x: r * Math.sin(v) * Math.cos(u),
                    z: r * Math.sin(v) * Math.sin(u),
                    y: r * Math.cos(v) * 0.6,
                    c: colorAt(Math.random() * 0.15),
                    s: Math.random() * 1.3 + 0.5,
                    al: 0.55 + Math.random() * 0.45,
                    ph: Math.random() * 6.28,
                    tw: false
                });
            }
            // door ke fixed taare
            for (i = 0; i < N_FAR; i++) {
                far.push({
                    x: Math.random(), y: Math.random(),
                    s: Math.random() * 1.4 + 0.3,
                    ph: Math.random() * 6.28,
                    sp: 500 + Math.random() * 900
                });
            }
        }

        function frame(t) {
            if (!running) return;
            mx += (tx - mx) * 0.04;
            my += (ty - my) * 0.04;

            ctx.globalCompositeOperation = 'source-over';
            ctx.globalAlpha = 1;
            ctx.fillStyle = '#03040c';
            ctx.fillRect(0, 0, W, H);

            var cx = W / 2 + mx * 26, cy = H / 2 + my * 18;
            var i, p;

            // nebula glow (peeche halka rang)
            var big = Math.max(W, H);
            var g1 = ctx.createRadialGradient(cx, cy, 0, cx, cy, big * 0.62);
            g1.addColorStop(0, 'rgba(90,60,200,0.20)');
            g1.addColorStop(0.5, 'rgba(40,50,140,0.09)');
            g1.addColorStop(1, 'rgba(3,4,12,0)');
            ctx.fillStyle = g1;
            ctx.fillRect(0, 0, W, H);

            // door ke twinkling taare
            for (i = 0; i < far.length; i++) {
                p = far[i];
                ctx.globalAlpha = 0.25 + 0.55 * (0.5 + 0.5 * Math.sin(t / p.sp + p.ph));
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(p.x * W, p.y * H, p.s, p.s);
            }

            // galaxy stars (additive blending = chamak)
            ctx.globalCompositeOperation = 'lighter';
            var fov = big * 0.85, D = 1700;
            var a = angle + mx * 0.35;
            var tilt = tiltBase + my * 0.18;
            var ca = Math.cos(a), sa = Math.sin(a), ct = Math.cos(tilt), st = Math.sin(tilt);

            for (i = 0; i < stars.length; i++) {
                p = stars[i];
                var x1 = p.x * ca - p.z * sa;
                var z1 = p.x * sa + p.z * ca;
                var y2 = p.y * ct - z1 * st;
                var z2 = p.y * st + z1 * ct;
                var dp = z2 + D;
                if (dp < 200) continue;
                var k = fov / dp;
                var px = cx + x1 * k, py = cy + y2 * k;
                if (px < -4 || px > W + 4 || py < -4 || py > H + 4) continue;
                var al = p.al;
                if (p.tw) al *= 0.7 + 0.3 * Math.sin(t / 600 + p.ph);
                ctx.globalAlpha = Math.min(1, al);
                ctx.fillStyle = p.c;
                var sz = Math.max(0.7, p.s * k * 1.25);
                ctx.fillRect(px - sz / 2, py - sz / 2, sz, sz);
            }

            // core ki tez roshni
            ctx.globalAlpha = 1;
            var g2 = ctx.createRadialGradient(cx, cy, 0, cx, cy, big * 0.17);
            g2.addColorStop(0, 'rgba(255,236,190,0.60)');
            g2.addColorStop(0.35, 'rgba(255,190,110,0.24)');
            g2.addColorStop(1, 'rgba(255,170,90,0)');
            ctx.fillStyle = g2;
            ctx.fillRect(cx - big * 0.2, cy - big * 0.2, big * 0.4, big * 0.4);

            ctx.globalCompositeOperation = 'source-over';
            if (!reduce) {
                angle += 0.0016;
                requestAnimationFrame(frame);
            }
        }

        window.addEventListener('mousemove', function (e) {
            tx = (e.clientX / W - 0.5) * 2;
            ty = (e.clientY / H - 0.5) * 2;
        });
        window.addEventListener('touchmove', function (e) {
            var t = e.touches[0];
            tx = (t.clientX / W - 0.5) * 2;
            ty = (t.clientY / H - 0.5) * 2;
        }, { passive: true });
        window.addEventListener('resize', function () { resize(); if (reduce) frame(0); });
        document.addEventListener('visibilitychange', function () {
            if (document.hidden) { running = false; }
            else if (!running) { running = true; if (!reduce) requestAnimationFrame(frame); }
        });

        resize();
        build();
        requestAnimationFrame(frame);
    }

    function setupBrandAndCleanup() {
        var navBrand = document.querySelector('nav a, header a, [class*="logo"]');
        if (navBrand && !document.getElementById('fixed-brand-name')) {
            navBrand.innerHTML = '<span id="fixed-brand-name" class="custom-brand-text">Download Games For Piracy</span>';
        }
        var keywords = ['Discord', 'Reddit', 'Nebulo', 'Donations'];
        document.querySelectorAll('div, a, button').forEach(function (el) {
            var text = el.textContent.trim();
            if (keywords.indexOf(text) !== -1 && el.children.length <= 4) {
                var box = el.closest('div.grid, div.flex, div') || el;
                box.style.display = 'none';
            }
        });
    }

    function boot() {
        startGalaxy();
        setupBrandAndCleanup();
        // SPA sites ke liye dobara check
        setTimeout(setupBrandAndCleanup, 1500);
        setTimeout(setupBrandAndCleanup, 4000);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
"""


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    url = f"{TARGET_URL}/{path}"
    if request.query_string:
        url += f"?{request.query_string.decode('utf-8')}"

    try:
        headers_dict = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': TARGET_URL
        }

        if request.method == 'POST':
            if request.content_type:
                headers_dict['Content-Type'] = request.content_type
            resp = scraper.post(url, headers=headers_dict, data=request.get_data(),
                                allow_redirects=True, cookies=request.cookies)
        else:
            resp = scraper.get(url, headers=headers_dict,
                               allow_redirects=True, cookies=request.cookies)

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        resp_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                        if name.lower() not in excluded_headers]

        content_type = resp.headers.get('Content-Type', '')

        if 'text/html' in content_type:
            soup = BeautifulSoup(resp.text, 'html.parser')
            base = f"{request.scheme}://{request.host}"

            # Internal links, scripts, images ko local proxy par route karna
            for tag in soup.find_all(['a', 'link', 'script', 'img', 'form']):
                for attr in ['href', 'src', 'action']:
                    val = tag.get(attr)
                    if val:
                        if 'ankergames.to' in val:
                            tag[attr] = (val.replace('https://ankergames.to', base)
                                            .replace('http://ankergames.to', base))
                        elif val.startswith('/') and not val.startswith('//'):
                            tag[attr] = f'{base}{val}'

            # Browser title
            if soup.title:
                soup.title.string = NEW_TITLE

            # CSS
            style_tag = soup.new_tag('style')
            style_tag.string = STYLE_CSS
            if soup.head:
                soup.head.append(style_tag)

            # Galaxy JS
            script_tag = soup.new_tag('script')
            script_tag.string = GALAXY_JS
            if soup.body:
                soup.body.append(script_tag)

            return Response(str(soup), resp.status_code, resp_headers)

        return Response(resp.content, resp.status_code, resp_headers)

    except Exception as e:
        return f"Proxy Error: {str(e)}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
