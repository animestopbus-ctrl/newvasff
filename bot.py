import telebot
import os
import requests
import json
from flask import Flask, request

# Import your custom modules
from LastPerson07.start import register_start_handlers
from LastPerson07.handler import register_github_handlers

# Fetch environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL") # e.g., https://newvasff.onrender.com

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Register your commands
register_start_handlers(bot)
register_github_handlers(bot)

# 1. Health check route
@app.route('/')
def index():
    # Hardcoded Anime Scenery for the initial load (Nekosia API)
    bg_api = "https://api.nekosia.cat/v1/get/image/neko"
    try:
        bg_url = requests.get(bg_api).json()['image']['url']['original']
    except:
        bg_url = "https://i.postimg.cc/sggGrLhn/18.png"

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GitPuller • GitHub in Telegram</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Space+Grotesk:wght@600;700&amp;display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root {{ --accent: #00f5ff; --glass: rgba(20,20,28,0.92); }}
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        
        /* FIX: Changed overflow from hidden to auto to allow scrolling */
        body {{ 
            font-family:'Inter',sans-serif; 
            background:#000; 
            color:#fff; 
            min-height:100vh; 
            overflow-y: auto !important; 
            overflow-x: hidden;
        }}

        /* WALLPAPER - FIXED LAYERING */
        .wall {{ position:fixed; inset:0; background-size:cover; background-position:center; transition:opacity 3.5s ease; opacity:0; z-index:1; filter:brightness(0.68) contrast(1.18); }}
        .wall.active {{ opacity:1; }}
        .overlay {{ position:fixed; inset:0; z-index:2; background:linear-gradient(180deg, rgba(0,0,0,0.38) 0%, rgba(0,0,0,0.94) 78%); }}

        /* FIX: Ensure the app container allows its children to expand and scroll */
        .app {{ 
            position:relative; 
            z-index:10; 
            display:flex; 
            flex-direction:column;
            min-height: 100vh;
        }}

        .header {{
            padding:16px 5%; background:rgba(10,10,15,0.95); backdrop-filter:blur(20px);
            display:flex; align-items:center; justify-content:space-between; position:sticky; top:0; z-index:100;
        }}
        .logo {{ font-family:'Space Grotesk'; font-size:28px; font-weight:700; letter-spacing:-2px; background:linear-gradient(90deg,#fff,var(--accent)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}

        .tab-content {{ display:none; flex:1; padding:20px 5% 120px; max-width:720px; margin:0 auto; width:100%; }}
        .tab-content.active {{ display:block; animation:fadeIn 0.4s ease; }}
        @keyframes fadeIn {{ from {{ opacity:0; transform:translateY(20px); }} to {{ opacity:1; transform:none; }} }}

        .bottom-nav {{
            position:fixed; bottom:0; left:0; right:0; z-index:100;
            background:rgba(10,10,15,0.95); backdrop-filter:blur(20px);
            display:flex; border-top:1px solid rgba(255,255,255,0.1);
        }}
        .nav-item {{ flex:1; text-align:center; padding:10px 0 6px; color:rgba(255,255,255,0.65); font-size:12px; transition:0.3s; cursor:pointer; }}
        .nav-item.active {{ color:var(--accent); }}
        .nav-item i {{ font-size:23px; display:block; margin-bottom:3px; }}

        /* SEARCH TAB */
        .search-box {{ background:rgba(255,255,255,0.09); border:1px solid rgba(255,255,255,0.18); border-radius:9999px; padding:8px 12px; display:flex; align-items:center; box-shadow:0 12px 35px rgba(0,0,0,0.5); }}
        .search-box input {{ flex:1; background:transparent; border:none; outline:none; color:white; font-size:18px; padding:14px 18px; }}
        .search-btn {{ width:56px; height:56px; background:var(--accent); color:#000; border:none; border-radius:9999px; font-size:24px; cursor:pointer; }}

        .chips, .recent {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:26px; justify-content:center; }}
        .chip, .recent-item {{ background:rgba(255,255,255,0.1); padding:10px 20px; border-radius:9999px; font-size:14.5px; cursor:pointer; transition:0.3s; }}
        .chip:active, .recent-item:active {{ background:var(--accent); color:#000; transform:scale(0.95); }}

        /* RESULT */
        .result-card {{ background:var(--glass); border-radius:24px; overflow:hidden; margin-top:30px; border:1px solid rgba(255,255,255,0.1); }}
        .profile-header {{ padding:28px; display:flex; gap:20px; align-items:center; background:linear-gradient(135deg,rgba(0,245,255,0.12),transparent); }}
        .profile-header img {{ width:96px; height:96px; border-radius:20px; border:4px solid var(--accent); }}
        .stats {{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; padding:20px 28px; }}
        .stat {{ text-align:center; }}
        .stat span {{ font-size:23px; font-weight:700; color:var(--accent); display:block; }}
        .action-btn {{ margin:20px 28px 28px; padding:17px; background:var(--accent); color:#000; font-weight:700; border:none; border-radius:18px; width:calc(100% - 56px); cursor:pointer; }}

        /* SAVED PROFILES */
        .saved-item {{ background:rgba(255,255,255,0.07); padding:14px; border-radius:16px; display:flex; align-items:center; gap:16px; margin-bottom:12px; cursor:pointer; }}
        .saved-item img {{ width:52px; height:52px; border-radius:12px; border:2px solid var(--accent); }}

        /* DEVS */
        .dev-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:16px; }}
        .dev-card {{ background:var(--glass); border-radius:20px; padding:18px; text-align:center; cursor:pointer; transition:0.3s; }}
        .dev-card:hover {{ transform:translateY(-8px); background:rgba(0,245,255,0.12); }}
        .dev-card img {{ width:78px; height:78px; border-radius:50%; border:3px solid var(--accent); margin-bottom:12px; }}

        /* ABOUT PAGE */
        .about-section {{ margin-bottom:50px; }}
        .about-section h2 {{ margin-bottom:20px; font-size:26px; }}
        .feature-list {{ display:flex; flex-direction:column; gap:24px; }}
        .feature {{ display:flex; gap:18px; }}
        .feature i {{ font-size:32px; color:var(--accent); flex-shrink:0; margin-top:4px; }}

        .stats-row {{ display:flex; justify-content:space-around; background:rgba(255,255,255,0.06); padding:30px 20px; border-radius:20px; margin:40px 0; }}
        .stat-big span {{ font-size:36px; font-weight:700; color:var(--accent); display:block; }}

        .spinner {{ width:42px; height:42px; border:5px solid rgba(255,255,255,0.2); border-top-color:var(--accent); border-radius:50%; animation:spin 0.9s linear infinite; margin:60px auto; }}
        @keyframes spin {{ to {{ transform:rotate(360deg); }} }}
    </style>
</head>
<body>

    <div id="wall1" class="wall active" style="background-image:url('{bg_url}')"></div>
    <div id="wall2" class="wall"></div>
    <div class="overlay"></div>

    <div class="app">
        <div class="header">
            <div class="logo">GitPuller</div>
            <div id="tg-user" style="display:flex;align-items:center;gap:10px;font-size:14px;"></div>
        </div>

        <div id="search-tab" class="tab-content active">
            <div class="search-box">
                <input type="text" id="username" placeholder="GitHub username..." autocomplete="off">
                <button class="search-btn" onclick="pullProfile()">→</button>
            </div>
            
            <div style="margin-top:30px;">
                <small style="opacity:0.6;margin-left:10px;">QUICK PULL</small>
                <div class="chips" id="chips"></div>
            </div>

            <div style="margin-top:40px;">
                <small style="opacity:0.6;margin-left:10px;">RECENT SEARCHES</small>
                <div class="recent" id="recent-searches"></div>
            </div>

            <div id="search-result"></div>
        </div>

        <div id="profile-tab" class="tab-content">
            <div class="result-card" id="tg-profile" style="margin-bottom:30px;"></div>
            
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                <h3 style="opacity:0.8;">Saved Profiles</h3>
                <button onclick="exportSaved()" style="background:transparent;border:1px solid var(--accent);color:var(--accent);padding:6px 14px;border-radius:999px;font-size:13px;cursor:pointer;">Export All</button>
            </div>
            <div id="saved-list"></div>
        </div>

        <div id="devs-tab" class="tab-content">
            <h2 style="margin-bottom:24px;">Community Developers</h2>
            <div class="dev-grid" id="dev-grid"></div>
        </div>

        <div id="page-tab" class="tab-content">
            <h1 style="font-size:46px;line-height:1.05;margin-bottom:12px;">GitPuller</h1>
            <p style="font-size:19px;opacity:0.85;margin-bottom:50px;">The fastest way to pull GitHub intelligence inside Telegram</p>

            <div class="about-section">
                <h2>Why GitPuller?</h2>
                <div class="feature-list">
                    <div class="feature"><i class="fas fa-bolt"></i><div><strong>Lightning Fast</strong><br>0.4s average response using GitHub API</div></div>
                    <div class="feature"><i class="fas fa-save"></i><div><strong>Save Forever</strong><br>Local storage — never lose a developer</div></div>
                    <div class="feature"><i class="fas fa-users"></i><div><strong>Discover Talent</strong><br>Curated list of top open-source devs</div></div>
                    <div class="feature"><i class="fas fa-share-alt"></i><div><strong>One-Tap Share</strong><br>Send any profile directly to chat</div></div>
                </div>
            </div>

            <div class="stats-row">
                <div class="stat-big"><span id="stat-profiles">12400</span><small>Profiles pulled</small></div>
                <div class="stat-big"><span id="stat-countries">47</span><small>Countries</small></div>
                <div class="stat-big"><span id="stat-repos">89000</span><small>Repos scanned</small></div>
            </div>

            <div style="text-align:center;margin-top:60px;opacity:0.6;font-size:14px;">
                Made for recruiters, researchers &amp; developers<br>
                Version 2.4 • February 2026
            </div>
        </div>

        <div class="bottom-nav">
            <div class="nav-item active" onclick="switchTab(0)"><i class="fas fa-search"></i><div>Search</div></div>
            <div class="nav-item" onclick="switchTab(1)"><i class="fas fa-user"></i><div>Profile</div></div>
            <div class="nav-item" onclick="switchTab(2)"><i class="fas fa-users"></i><div>Devs</div></div>
            <div class="nav-item" onclick="switchTab(3)"><i class="fas fa-info-circle"></i><div>About</div></div>
        </div>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand(); tg.ready();

        // ================== WALLPAPER ==================
        const wallpapers = [
            'https://i.postimg.cc/1tNwGVxC/5.png',
            'https://i.postimg.cc/kX9tjGXP/16.png',
            'https://i.postimg.cc/cC7txyhz/15.png',
            'https://i.postimg.cc/gcNtrv0m/2.png'
        ];
        let currentWall = 0;
        function startWallpaper() {{
            document.getElementById('wall1').style.backgroundImage = `url(${{wallpapers[0]}})`;
            document.getElementById('wall2').style.backgroundImage = `url(${{wallpapers[1]}})`;
            setInterval(() => {{
                currentWall = (currentWall + 1) % wallpapers.length;
                const next = document.getElementById('wall2');
                next.style.backgroundImage = `url(${{wallpapers[currentWall]}})`;
                next.classList.add('active');
                setTimeout(() => {{
                    document.getElementById('wall1').style.backgroundImage = `url(${{wallpapers[currentWall]}})`;
                    next.classList.remove('active');
                }}, 3500);
            }}, 15000);
        }}

        // ================== TAB SYSTEM ==================
        function switchTab(n) {{
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            document.getElementById(['search-tab','profile-tab','devs-tab','page-tab'][n]).classList.add('active');
            document.querySelectorAll('.nav-item')[n].classList.add('active');
        }}

        // ================== TELEGRAM USER ==================
        function showUser() {{
            if (tg.initDataUnsafe.user) {{
                const u = tg.initDataUnsafe.user;
                document.getElementById('tg-user').innerHTML = `<img src="${{u.photo_url||''}}" style="width:34px;height:34px;border-radius:50%;border:2px solid var(--accent);" onerror="this.style.display='none'"><span>${{u.first_name}}</span>`;
                document.getElementById('tg-profile').innerHTML = `<div style="padding:28px;display:flex;gap:20px;align-items:center;"><img src="${{u.photo_url||''}}" style="width:82px;height:82px;border-radius:20px;border:4px solid var(--accent);"><div><h2>${{u.first_name}} ${{u.last_name||''}}</h2><p style="color:var(--accent);">@${{u.username||'user'}}</p></div></div>`;
            }}
        }}

        // ================== QUICK CHIPS ==================
        const popular = ['torvalds','octocat','freeCodeCamp','sindresorhus','gaearon','midudev','kentcdodds','dan-abramov','tj','addyosmani','yyx990803','rauchg'];
        function renderChips() {{
            const container = document.getElementById('chips');
            popular.forEach(name => {{
                const chip = document.createElement('div');
                chip.className = 'chip';
                chip.textContent = '@' + name;
                chip.onclick = () => {{ document.getElementById('username').value = name; pullProfile(); }};
                container.appendChild(chip);
            }});
        }}

        // ================== RECENT SEARCHES ==================
        function addToRecent(username) {{
            let recent = JSON.parse(localStorage.getItem('recentSearches') || '[]');
            recent = recent.filter(u => u !== username);
            recent.unshift(username);
            if (recent.length > 8) recent.pop();
            localStorage.setItem('recentSearches', JSON.stringify(recent));
            renderRecent();
        }}
        function renderRecent() {{
            const container = document.getElementById('recent-searches');
            container.innerHTML = '';
            const recent = JSON.parse(localStorage.getItem('recentSearches') || '[]');
            recent.forEach(name => {{
                const el = document.createElement('div');
                el.className = 'recent-item';
                el.textContent = '@' + name;
                el.onclick = () => {{ document.getElementById('username').value = name; pullProfile(); }};
                container.appendChild(el);
            }});
        }}

        // ================== DEVS TAB ==================
        const devs = [
            {{login:"torvalds", name:"Linus Torvalds", avatar:"https://avatars.githubusercontent.com/u/1024025?v=4"}},
            {{login:"octocat", name:"GitHub", avatar:"https://avatars.githubusercontent.com/u/583231?v=4"}},
            {{login:"freeCodeCamp", name:"freeCodeCamp", avatar:"https://avatars.githubusercontent.com/u/9892522?v=4"}},
            {{login:"sindresorhus", name:"Sindre Sorhus", avatar:"https://avatars.githubusercontent.com/u/170270?v=4"}},
            {{login:"gaearon", name:"Dan Abramov", avatar:"https://avatars.githubusercontent.com/u/810438?v=4"}},
            {{login:"midudev", name:"Miguel Ángel Durán", avatar:"https://avatars.githubusercontent.com/u/1561955?v=4"}},
            {{login:"kentcdodds", name:"Kent C. Dodds", avatar:"https://avatars.githubusercontent.com/u/1500684?v=4"}},
            {{login:"tj", name:"TJ Holowaychuk", avatar:"https://avatars.githubusercontent.com/u/25254?v=4"}},
            {{login:"addyosmani", name:"Addy Osmani", avatar:"https://avatars.githubusercontent.com/u/110953?v=4"}},
            {{login:"yyx990803", name:"Evan You", avatar:"https://avatars.githubusercontent.com/u/499550?v=4"}},
            {{login:"rauchg", name:"Guillermo Rauch", avatar:"https://avatars.githubusercontent.com/u/13041?v=4"}},
            {{login:"vercel", name:"Vercel", avatar:"https://avatars.githubusercontent.com/u/14985020?v=4"}}
        ];
        function renderDevs() {{
            const grid = document.getElementById('dev-grid');
            devs.forEach(d => {{
                const card = document.createElement('div');
                card.className = 'dev-card';
                card.innerHTML = `<img src="${{d.avatar}}"><h4>${{d.name}}</h4><p style="font-size:13px;opacity:0.7;">@${{d.login}}</p>`;
                card.onclick = () => {{ document.getElementById('username').value = d.login; switchTab(0); pullProfile(); }};
                grid.appendChild(card);
            }});
        }}

        // ================== PULL PROFILE ==================
        async function pullProfile() {{
            const username = document.getElementById('username').value.trim();
            if (!username) return;

            const resultDiv = document.getElementById('search-result');
            resultDiv.innerHTML = `<div style="text-align:center;padding:80px;"><div class="spinner"></div><p style="margin-top:20px;opacity:0.7;">Pulling from GitHub...</p></div>`;

            try {{
                const userRes = await fetch(`https://api.github.com/users/${{username}}`);
                if (!userRes.ok) throw new Error("User not found");
                const user = await userRes.json();

                const repoRes = await fetch(`https://api.github.com/users/${{username}}/repos?sort=stars&per_page=3`);
                const repos = await repoRes.json();

                let html = `<div class="result-card"><div class="profile-header"><img src="${{user.avatar_url}}"><div><h2>${{user.name || user.login}}</h2><p style="color:var(--accent);font-family:monospace;font-size:17px;">@${{user.login}}</p>${{user.bio ? `<p style="margin-top:14px;opacity:0.9;">${{user.bio}}</p>` : ''}}</div></div><div class="stats"><div class="stat"><span>${{user.public_repos}}</span><small>Repos</small></div><div class="stat"><span>${{user.followers}}</span><small>Followers</small></div><div class="stat"><span>${{user.following}}</span><small>Following</small></div></div><div style="padding:0 28px 20px;"><small style="opacity:0.6;">TOP REPOS</small>`;

                repos.forEach(r => {{
                    html += `<div style="margin:10px 0;padding:14px;background:rgba(255,255,255,0.06);border-radius:14px;display:flex;justify-content:space-between;align-items:center;"><a href="${{r.html_url}}" target="_blank" style="color:white;text-decoration:none;">${{r.name}}</a><span style="color:var(--accent)">★ ${{r.stargazers_count}}</span></div>`;
                }});

                html += `</div><div style="display:flex;gap:12px;margin:0 28px 28px;"><button onclick="saveProfile(${{JSON.stringify(user).replace(/"/g,'&quot;')}});" class="action-btn" style="flex:1;"><i class="fas fa-bookmark"></i> Save</button><button onclick="shareProfile(${{JSON.stringify(user).replace(/"/g,'&quot;')}});" style="flex:1;background:rgba(255,255,255,0.1);color:white;border:none;border-radius:18px;font-weight:600;">Share</button></div></div>`;

                resultDiv.innerHTML = html;
                addToRecent(username);
            }} catch (e) {{
                resultDiv.innerHTML = `<div style="padding:80px;text-align:center;color:#ff5555;font-size:18px;">❌ ${{e.message}}</div>`;
            }}
        }}

        function shareProfile(user) {{
            tg.share({{
                url: user.html_url,
                title: `${{user.name || user.login}} on GitHub`,
                message: `Check out this awesome developer: @${{user.login}}`
            }});
        }}

        // ================== SAVE & EXPORT ==================
        function saveProfile(user) {{
            let saved = JSON.parse(localStorage.getItem('savedGitProfiles') || '[]');
            if (!saved.find(u => u.login === user.login)) {{
                saved.unshift(user);
                if (saved.length > 15) saved.pop();
                localStorage.setItem('savedGitProfiles', JSON.stringify(saved));
            }}
            switchTab(1);
            loadSaved();
        }}

        function loadSaved() {{
            const container = document.getElementById('saved-list');
            container.innerHTML = '';
            const saved = JSON.parse(localStorage.getItem('savedGitProfiles') || '[]');
            if (saved.length === 0) {{
                container.innerHTML = `<p style="text-align:center;padding:60px 20px;opacity:0.5;">No saved profiles yet.<br>Save some from Search tab.</p>`;
                return;
            }}
            saved.forEach(user => {{
                const div = document.createElement('div');
                div.className = 'saved-item';
                div.innerHTML = `<img src="${{user.avatar_url}}"><div style="flex:1;"><div style="font-weight:600;">${{user.name || user.login}}</div><div style="color:var(--accent);font-size:13px;">@${{user.login}}</div></div>`;
                div.onclick = () => {{ switchTab(0); document.getElementById('username').value = user.login; pullProfile(); }};
                container.appendChild(div);
            }});
        }}

        function exportSaved() {{
            const saved = JSON.parse(localStorage.getItem('savedGitProfiles') || '[]');
            if (saved.length === 0) return alert("Nothing to export");
            const data = JSON.stringify(saved, null, 2);
            const blob = new Blob([data], {{type: 'application/json'}});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'gitpuller_saved_profiles.json';
            a.click();
        }}

        // ================== INIT ==================
        window.onload = () => {{
            startWallpaper();
            showUser();
            renderChips();
            renderRecent();
            renderDevs();
            loadSaved();
            document.getElementById('username').focus();
        }};
    </script>
</body>
</html>
    """
    return html_content, 200

# ==========================================
# 🤖 2. THE WEBHOOK ENDPOINTS
# ==========================================
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Forbidden', 403

@app.route('/set_webhook')
def set_webhook():
    if not WEBHOOK_URL:
        return "❌ Error: WEBHOOK_URL is missing.", 400
    bot.remove_webhook()
    success = bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    return "✅ Webhook Connected!" if success else "❌ Failed!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
