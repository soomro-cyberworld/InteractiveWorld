import random
import sqlite3
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

DB_FILE = "cyber_world.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            username TEXT PRIMARY KEY,
            level INTEGER DEFAULT 1,
            score INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

def generate_dynamic_hardcore_puzzle(level_num):
    if level_num <= 3:
        puzzles = [
            {"title": f"LEVEL {level_num}: MAIN PROTOCOL BREACH", "description": f"Mainframe routing key lock active. Convert decimal number '{100 + level_num * 12}' into 8-bit Binary code.", "correct_answer": bin(100 + level_num * 12)[2:]},
            {"title": f"LEVEL {level_num}: PORT SCANNING OVERRIDE", "description": "Security layers are active. Enter the standard port number used for unencrypted normal web traffic (HTTP).", "correct_answer": "80"},
            {"title": f"LEVEL {level_num}: CRYPTO SHIFT CIPHER", "description": "Decrypted data packets captured. Convert the standard decimal number '15' into Hexadecimal format.", "correct_answer": "f"}
        ]
        return random.choice(puzzles)
    elif 4 <= level_num <= 10:
        multiplier = level_num * 3
        puzzles = [
            {"title": f"LEVEL {level_num}: CYBER INVENTORY CRASH", "description": f"Evaluate this memory matrix loop: x = 10; x += {multiplier}; x -= 5. Enter the final value of x to overflow the stack.", "correct_answer": str(10 + multiplier - 5)},
            {"title": f"LEVEL {level_num}: STRING MANIPULATION ATTACK", "description": f"A malicious script uses: print('ROOT' + str({level_num})). Enter the exact output string.", "correct_answer": f"root{level_num}"},
            {"title": f"LEVEL {level_num}: LINUX KERNEL COMMAND", "description": "Linux terminal is locked. Type the exact shorthand terminal command used to display the current working directory path.", "correct_answer": "pwd"}
        ]
        return random.choice(puzzles)
    else:
        target_val = level_num * 7
        return {
            "title": f"LEVEL {level_num}: QUANTUM FIREWALL ENCRYPTION",
            "description": f"Warning! High-level security active. System demands a dynamic bypass token value. Calculate and enter the exact numerical value of: ({target_val} * 2) - {level_num}.",
            "correct_answer": str((target_val * 2) - level_num)
        }

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Interactive Learning World - Login</title>
    <style>
        body { background-color: #05050a; color: #00ffcc; font-family: 'Courier New', monospace; text-align: center; padding-top: 150px; margin: 0; }
        .login-card { max-width: 400px; margin: 0 auto; background: #0d0d1f; padding: 40px; border: 2px solid #00ffcc; border-radius: 8px; box-shadow: 0 0 20px #00ffcc; }
        input { background: transparent; border: none; border-bottom: 2px solid #00ffcc; color: white; padding: 10px; width: 80%; font-size: 18px; text-align: center; outline: none; margin-bottom: 20px; }
        button { background: #00ffcc; color: black; border: none; padding: 10px 30px; font-size: 16px; font-weight: bold; cursor: pointer; border-radius: 4px; }
        button:hover { box-shadow: 0 0 15px #00ffcc; }
    </style>
</head>
<body>
    <div class="login-card">
        <h2>[ CYBER INITIALIZATION NETWORK ]</h2>
        <p>Enter Agent ID to Access Permanent Vault:</p>
        <form action="/login" method="POST">
            <input type="text" name="agent_name" placeholder="AGENT_NAME" autocomplete="off" required><br>
            <button type="submit">BREACH GATEWAY</button>
        </form>
    </div>
</body>
</html>
"""

ROOM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ level_title }}</title>
    <style>
        body { background-color: #05050a; color: #00ffcc; font-family: 'Courier New', monospace; display: flex; flex-direction: column; align-items: center; padding-top: 50px; margin: 0; }
        .main-container { display: flex; flex-direction: row; gap: 30px; max-width: 1100px; width: 90%; justify-content: center; align-items: flex-start; }
        .room-box { flex: 2; background: #080815; padding: 40px; border: 2px dashed #ff0055; border-radius: 10px; box-shadow: 0px 0px 25px rgba(255, 0, 85, 0.4); text-align: center; }
        .leaderboard-box { flex: 1; background: #070714; padding: 25px; border: 2px solid #00ffcc; border-radius: 10px; box-shadow: 0px 0px 20px rgba(0, 255, 204, 0.2); width: 350px; }
        h1 { font-size: 24px; color: #ff0055; text-shadow: 0 0 10px #ff0055; margin-top: 0; }
        h2 { font-size: 20px; color: #00ffcc; text-shadow: 0 0 10px #00ffcc; margin-top: 0; text-align: center; }
        p { color: #ffffff; font-size: 15px; line-height: 1.6; }
        .input-box { background: transparent; border: 1px solid #333; border-bottom: 2px solid #00ffcc; color: #fff; padding: 10px; width: 70%; font-size: 18px; text-align: center; outline: none; margin-bottom: 20px; }
        .btn { background: transparent; color: #00ffcc; border: 2px solid #00ffcc; padding: 10px 30px; font-size: 16px; cursor: pointer; font-weight: bold; border-radius: 4px; }
        .btn:hover { background: #00ffcc; color: black; box-shadow: 0 0 15px #00ffcc; }
        .error-msg { color: #ff3333; margin-top: 15px; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #222; }
        th { color: #00ffcc; border-bottom: 2px solid #00ffcc; }
        td { color: #fff; }
        .highlight-row { background: rgba(0, 255, 204, 0.2); color: #00ffcc; font-weight: bold; }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="room-box">
            <p style="color: #888;">Authenticated Vault Profile: <strong style="color: #00ffcc;">{{ agent_name }}</strong> | SECURE SCORE: <strong style="color: #ffff00;">{{ score }}</strong></p>
            <h1>{{ level_title }}</h1>
            <hr style="border-color: #ff0055;">
            <br>
            <p>{{ level_desc }}</p>
            <br>
            <form action="/submit_action/{{ agent_name }}" method="POST">
                <input type="text" name="user_answer" class="input-box" placeholder="EXECUTE OVERRIDE PAYLOAD" autocomplete="off" required><br>
                <input type="hidden" name="correct_ans" value="{{ correct_answer }}">
                <input type="hidden" name="current_level" value="{{ current_level }}">
                <input type="hidden" name="current_score" value="{{ score }}">
                <button type="submit" class="btn">INJECT DECRYPTION</button>
            </form>
            {% if error_msg %}
                <div class="error-msg">❌ {{ error_msg }}</div>
            {% endif %}
            <br>
            <a href="/" style="color: #888; text-decoration: none; font-size: 12px;">[ DISCONNECT SESSION ]</a>
        </div>
        <div class="leaderboard-box">
            <h2>🌍 GLOBAL RANK</h2>
            <table>
                <thead>
                    <tr>
                        <th>Agent</th>
                        <th>Lvl</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in leaderboard_data %}
                    <tr class="{% if row[0] == agent_name %}highlight-row{% endif %}">
                        <td>{{ row[0] }}</td>
                        <td>{{ row[1] }}</td>
                        <td>{{ row[2] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(LOGIN_HTML)

@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('agent_name').strip().lower()
    if name:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT level, score FROM players WHERE username = ?", (name,))
        player_record = cursor.fetchone()
        if player_record:
            p_level, p_score = player_record
        else:
            cursor.execute("INSERT INTO players (username, level, score) VALUES (?, 1, 0)", (name,))
            conn.commit()
            p_level, p_score = 1, 0
        conn.close()
        return redirect(url_for('game_room', agent_name=name, level=p_level, score=p_score))
    return redirect(url_for('home'))

@app.route('/room/<agent_name>')
def game_room(agent_name):
    p_level = int(request.args.get('level', 1))
    p_score = int(request.args.get('score', 0))
    error = request.args.get('error', '')
    puzzle = generate_dynamic_hardcore_puzzle(p_level)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT username, level, score FROM players ORDER BY score DESC LIMIT 10")
    leaderboard = cursor.fetchall()
    conn.close()
    return render_template_string(
        ROOM_HTML, 
        agent_name=agent_name,
        score=p_score,
        current_level=p_level,
        level_title=puzzle["title"],
        level_desc=puzzle["description"],
        correct_answer=puzzle["correct_answer"],
        error_msg=error,
        leaderboard_data=leaderboard
    )

@app.route('/submit_action/<agent_name>', methods=['POST'])
def submit_action(agent_name):
    user_ans = request.form.get('user_answer').strip().lower()
    correct_ans = request.form.get('correct_ans').strip().lower()
    current_lvl = int(request.form.get('current_level'))
    current_scr = int(request.form.get('current_score'))
    if user_ans == correct_ans:
        new_score = current_scr + 1000
        new_level = current_lvl + 1
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE players SET level = ?, score = ? WHERE username = ?", (new_level, new_score, agent_name))
        conn.commit()
        conn.close()
        
        return redirect(url_for('game_room', agent_name=agent_name, level=new_level, score=new_score))
    else:
        return redirect(url_for('game_room', agent_name=agent_name, level=current_lvl, score=current_scr, error="ACCESS DENIED: Payload Corrupted! Try again."))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
