from flask import Flask, render_template_string, send_file, make_response, request, Response, jsonify
import os
import json
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 80 * 1024 * 1024

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEXTS = [
    "Желаю тебе: счастья, здоровья, успеха и достичь многих высот в жизни 🥳",
    "Чтобы у тебя было много потрясающих эмоций,<br>где бы ты ни была 🙃",
    "Чтобы ты находила что-то хорошее<br>даже в самых ужасных вещах 😶",
    "🫵 Помни: у тебя есть те, кто тебе поможет —<br>друзья, родители и остальные",
    "Чтобы ты всегда оставалась красивой и умной 💅🧠",
    "Перед тем как что-то сделать, всегда подумай:<br>стоит ли это и к чему приведёт 🤔🧐",
    "И просто не забывай быть самой собой.<br>Конечно, слушайся родителей —<br>они плохого не скажут и не посоветуют 🤝",
    "🎉 А теперь включи эти треки, Соня! 🎵",
    "Спасибо, что ты есть! ❤️"
]

BACKGROUNDS = [
    "linear-gradient(135deg, rgba(255, 0, 127, 0.85), rgba(121, 40, 202, 0.85), rgba(184, 0, 255, 0.85))", 
    "linear-gradient(135deg, rgba(255, 78, 80, 0.85), rgba(249, 212, 35, 0.85), rgba(255, 140, 0, 0.85))", 
    "linear-gradient(135deg, rgba(0, 198, 255, 0.85), rgba(0, 114, 255, 0.85), rgba(122, 0, 255, 0.85))",          
    "linear-gradient(135deg, rgba(0, 255, 135, 0.85), rgba(96, 239, 255, 0.85), rgba(0, 97, 255, 0.85))",          
    "linear-gradient(135deg, rgba(255, 0, 85, 0.85), rgba(85, 0, 255, 0.85), rgba(0, 255, 170, 0.85))",          
    "linear-gradient(135deg, rgba(249, 212, 35, 0.85), rgba(255, 78, 80, 0.85), rgba(121, 40, 202, 0.85))",          
    "linear-gradient(135deg, rgba(0, 198, 255, 0.85), rgba(0, 255, 135, 0.85), rgba(184, 0, 255, 0.85))",
    "linear-gradient(135deg, rgba(255, 0, 85, 0.85), rgba(85, 0, 255, 0.85), rgba(0, 255, 170, 0.85))",
    "linear-gradient(135deg, rgba(255, 0, 127, 0.85), rgba(121, 40, 202, 0.85), rgba(0, 198, 255, 0.85))"
]

LETTER_TEXT = """<div style="font-family: 'Caveat', cursive; font-size: 1.8rem; color: #a84f68; margin-bottom: 20px;">это тебе, Соня</div>
<div style="font-family: 'Playfair Display', serif; font-style: italic; font-size: 1.05rem; color: #4a4a4a; line-height: 1.6; text-align: left;">
    <p>Соня, с днём рождения!</p>
    <p>Я безумно рад, что в моей жизни есть такой потрясающий, верный и крутой друг, как ты. Спасибо тебе за твой нескончаемый позитив, поддержку и за все наши общие безумные моменты, которые мы пережили.</p>
    <p>Ты человек с огромным сердцем. Помни, что бы ни случилось в жизни, у тебя есть друзья, готовые прийти на помощь в любую секунду и разделить с тобой как грусть, так и самый громкий смех.</p>
    <p>Ценю нашу дружбу и хочу, чтобы ты сегодня была самой счастливой. С праздником, Соня! Желаю тебе исполнения всех твоих самых смелых мечтаний!</p>
</div>"""

HTML_CODE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>С Днем Рождения, Соня!</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&family=Playfair+Display:ital,wght@0,400;1,400&display=swap" rel="stylesheet">
    <style>
        body, html {
            margin: 0; padding: 0; width: 100%; height: 100%;
            background-color: #050510;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
            touch-action: none;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
        }

        #global-stars { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; background-image: radial-gradient(1px 1px at 10% 20%, rgba(255,255,255,0.8), transparent), radial-gradient(1.5px 1.5px at 30% 40%, rgba(255,255,255,0.9), transparent), radial-gradient(1px 1px at 50% 10%, rgba(255,255,255,0.7), transparent), radial-gradient(1px 1px at 70% 30%, rgba(255,255,255,0.8), transparent), radial-gradient(1.5px 1.5px at 90% 60%, rgba(255,255,255,0.9), transparent); background-size: 200px 200px; opacity: 0.6; animation: twinkle 4s infinite alternate; }
        #intro-stars { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 2; pointer-events: none; background-image: radial-gradient(2px 2px at 20% 30%, rgba(255,255,255,1), transparent), radial-gradient(2.5px 2.5px at 40% 70%, rgba(255,255,255,0.9), transparent), radial-gradient(1.5px 1.5px at 60% 20%, rgba(255,255,255,1), transparent), radial-gradient(2px 2px at 80% 50%, rgba(255,255,255,0.8), transparent); background-size: 300px 300px; animation: twinkle 2s infinite alternate; }
        @keyframes twinkle { 0% { opacity: 0.5; } 100% { opacity: 1; } }
        
        .decorations-layer { position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; z-index: 3; overflow: hidden; }
        .bubble { position: absolute; bottom: -15%; opacity: 0; will-change: transform, opacity; transform: translate3d(0,0,0); animation-name: chaoticMove, flickerOpacity; animation-timing-function: linear, ease-in-out; animation-iteration-count: infinite, infinite; }
        @keyframes chaoticMove { 0% { transform: translate3d(0, 0, 0) translateX(0) rotate(0deg); } 20% { transform: translate3d(0, -25vh, 0) translateX(30px) rotate(45deg); } 40% { transform: translate3d(0, -50vh, 0) translateX(-40px) rotate(90deg); } 60% { transform: translate3d(0, -75vh, 0) translateX(25px) rotate(135deg); } 80% { transform: translate3d(0, -100vh, 0) translateX(-15px) rotate(180deg); } 100% { transform: translate3d(0, -125vh, 0) translateX(0) rotate(270deg); } }
        @keyframes flickerOpacity { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

        #intro-screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; background: radial-gradient(circle at center, rgba(26, 11, 46, 0.6) 0%, rgba(5, 5, 16, 0.8) 100%); z-index: 100; transition: 1.2s cubic-bezier(0.7, 0, 0.3, 1); transform-origin: center; overflow: hidden; }
        #intro-screen.zoom-out { transform: scale(0) rotate(10deg); opacity: 0; }
        .greeting-text { font-size: clamp(1.5rem, 5vw, 2.2rem); color: #FFD700; text-align: center; font-weight: 900; z-index: 10; text-shadow: 0 0 20px #FF8C00, 0 0 40px #FF3366; padding: 0 20px; animation: pulseText 2s infinite alternate; }
        @keyframes pulseText { from { transform: scale(0.98); } to { transform: scale(1.02); } }
        canvas#fireworks { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 5; pointer-events: none; }

        #portal-flash { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle, #ffffff 0%, #FFD700 50%, transparent 100%); opacity: 0; pointer-events: none; z-index: 150; transition: opacity 0.4s ease; }
        #portal-flash.active { opacity: 1; }

        #gallery-screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 80; transition: background 0.8s ease; overflow: hidden; }
        
        .slide { position: absolute; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; opacity: 0; pointer-events: none; padding: 20px; box-sizing: border-box; will-change: transform, opacity; }
        .slide img { max-width: 100%; max-height: 55vh; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.6); object-fit: contain; border: 2px solid rgba(255, 255, 255, 0.3); background-color: rgba(0, 0, 0, 0.4); pointer-events: none; content-visibility: auto; }
        .slide p { color: #fff; font-size: clamp(1rem, 3.5vw, 1.15rem); text-align: center; margin-top: 20px; line-height: 1.5; max-width: 90%; text-shadow: 0 2px 4px rgba(0,0,0,0.9); font-weight: 500; pointer-events: none; padding: 12px 20px; background: rgba(0, 0, 0, 0.7); border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.2); }

        #gallery-screen[data-anim="slide"] .slide { transform: translate3d(100%, 0, 0); transition: transform 0.35s cubic-bezier(0.2, 0.8, 0.2, 1), opacity 0.35s; }
        #gallery-screen[data-anim="slide"] .slide.active { transform: translate3d(0, 0, 0); opacity: 1; pointer-events: auto; z-index: 2; }
        #gallery-screen[data-anim="slide"] .slide.prev { transform: translate3d(-100%, 0, 0); opacity: 0; z-index: 1; }

        #gallery-screen[data-anim="vertical"] .slide { transform: translate3d(0, 100%, 0); transition: transform 0.35s cubic-bezier(0.2, 0.8, 0.2, 1), opacity 0.35s; }
        #gallery-screen[data-anim="vertical"] .slide.active { transform: translate3d(0, 0, 0); opacity: 1; pointer-events: auto; z-index: 2; }
        #gallery-screen[data-anim="vertical"] .slide.prev { transform: translate3d(0, -100%, 0); opacity: 0; z-index: 1; }

        #gallery-screen[data-anim="zoom"] .slide { transform: scale(0.7); transition: transform 0.35s ease-out, opacity 0.35s ease-out; }
        #gallery-screen[data-anim="zoom"] .slide.active { transform: scale(1); opacity: 1; pointer-events: auto; z-index: 2; }
        #gallery-screen[data-anim="zoom"] .slide.prev { transform: scale(1.3); opacity: 0; z-index: 1; }

        #gallery-screen[data-anim="fade"] .slide { transform: none; transition: opacity 0.4s ease-in-out; }
        #gallery-screen[data-anim="fade"] .slide.active { opacity: 1; pointer-events: auto; z-index: 2; }
        #gallery-screen[data-anim="fade"] .slide.prev { opacity: 0; z-index: 1; }

        .playlist-wrapper { display: flex; flex-direction: column; width: 100%; max-width: 400px; pointer-events: auto; height: 60vh; }
        .upload-btn-wrapper { display: none; }
        #upload-status { display: none; }
        .playlist-container { display: flex; flex-direction: column; gap: 15px; width: 100%; overflow-y: auto; padding-right: 5px; flex-grow: 1; touch-action: pan-y; }
        .song-card { display: flex; flex-direction: column; gap: 15px; background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 15px; border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .song-header { display: flex; align-items: center; justify-content: space-between; }
        .song-info { display: flex; flex-direction: column; text-align: left; max-width: 70%; }
        .song-title { font-weight: bold; color: #fff; font-size: 1.1rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .song-artist { color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .song-controls { display: flex; gap: 10px; }
        .ctrl-btn { width: 40px; height: 40px; border-radius: 50%; border: none; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; cursor: pointer; transition: transform 0.2s; color: white; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .ctrl-btn:active { transform: scale(0.9); }
        .btn-play { background: linear-gradient(135deg, #00c6ff, #0072ff); }
        .btn-stop { background: linear-gradient(135deg, #ff4e50, #f9d423); }

        .seek-container { display: none; align-items: center; gap: 10px; color: #fff; font-size: 0.85rem; font-family: monospace; width: 100%; }
        .seek-container.active { display: flex; }
        .seek-bar { flex-grow: 1; -webkit-appearance: none; height: 4px; background: rgba(255, 255, 255, 0.3); border-radius: 2px; outline: none; cursor: pointer; }
        .seek-bar::-webkit-slider-thumb { -webkit-appearance: none; appearance: none; width: 14px; height: 14px; border-radius: 50%; background: #00c6ff; cursor: pointer; box-shadow: 0 0 10px rgba(0, 198, 255, 0.8); }
        .song-card.playing { border-color: #00c6ff; box-shadow: 0 0 15px rgba(0, 198, 255, 0.5); background: rgba(0, 198, 255, 0.15); }

        .anim-controls { display: flex; gap: 10px; justify-content: center; margin-top: 15px; pointer-events: auto; flex-wrap: wrap; }
        .anim-btn { padding: 8px 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.1); color: white; font-size: 0.8rem; cursor: pointer; transition: 0.2s; }
        .anim-btn.active { background: #00c6ff; border-color: #00c6ff; }

        .timer-box { background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2); border-radius: 15px; padding: 20px; text-align: center; color: white; margin-top: 10px; width: 100%; max-width: 350px; cursor: pointer; transition: transform 0.1s; }
        .timer-box:active { transform: scale(0.98); }
        .timer-box h4 { margin: 0 0 10px 0; color: #00c6ff; font-size: 1.2rem; }
        .timer-box p { margin: 0; font-size: 1.3rem; font-weight: bold; color: #FFD700; }

        /* === СТИЛИ ДЛЯ КОНВЕРТА === */
        #envelope-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px);
            z-index: 20000; display: none; justify-content: center; align-items: center;
            flex-direction: column; perspective: 1200px;
        }
        #envelope-overlay.show { display: flex; }

        .envelope {
            position: relative; width: min(320px, 85vw); height: min(220px, 58vw);
            background: #fdf5e6; border-radius: 6px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.8), inset 0 0 20px rgba(0,0,0,0.05);
            transform: scale(0) rotate(-45deg); opacity: 0;
            transition: all 1.2s cubic-bezier(0.25, 1, 0.5, 1);
            transform-style: preserve-3d;
        }
        #envelope-overlay.show .envelope { transform: scale(1) rotate(0deg); opacity: 1; }
        
        .envelope::before {
            content: ''; position: absolute; inset: 0; border-radius: 6px;
            box-shadow: inset 0 0 40px rgba(139, 69, 19, 0.15); pointer-events: none;
        }

        .envelope-text {
            position: absolute; top: 55%; left: 0; width: 100%; text-align: center;
            font-family: 'Caveat', cursive; font-size: 1.8rem; color: #b05c72;
            pointer-events: none; z-index: 2;
        }

        .envelope-stamp {
            position: absolute; bottom: 10px; right: 10px; width: 60px; height: 60px;
            border: 2px dashed #888; border-radius: 50%; background: rgba(200, 200, 200, 0.2);
            cursor: pointer; z-index: 10; display: flex; justify-content: center; align-items: center;
            transition: transform 0.2s;
        }
        .envelope-stamp:active { transform: scale(0.9); }
        .envelope-stamp svg { width: 50px; height: 50px; opacity: 0.6; }

        .letter-paper {
            position: absolute; top: 10px; left: 50%; transform: translateX(-50%) translateY(0);
            width: 90%; height: 90%; background: #fffdf8; border-radius: 4px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); padding: 20px; box-sizing: border-box;
            opacity: 0; pointer-events: none; z-index: 1;
            transition: transform 1s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.6s;
            display: flex; flex-direction: column; justify-content: space-between; overflow-y: auto;
        }

        #envelope-overlay.open .envelope-stamp { opacity: 0; pointer-events: none; transition: opacity 0.3s; }
        #envelope-overlay.open .letter-paper {
            transform: translateX(-50%) translateY(-80%) scale(1.1);
            height: 120%; opacity: 1; pointer-events: auto; z-index: 15;
        }
        .close-letter-btn {
            margin-top: 15px; padding: 10px; background: #a84f68; color: white;
            border: none; border-radius: 10px; font-family: inherit; font-size: 1rem; cursor: pointer;
            align-self: center; transition: transform 0.2s;
        }
        .close-letter-btn:active { transform: scale(0.95); }

        /* Экран "Ничего не нажимай" */
        #wait-screen {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #000; z-index: 19000; display: none;
            justify-content: center; align-items: center;
        }
        #wait-screen.show { display: flex; }
        .wait-text {
            color: #fff; font-size: 1.5rem; font-family: 'Segoe UI', sans-serif;
            text-align: center; opacity: 0; animation: fadeInOut 3s forwards;
        }
        @keyframes fadeInOut {
            0% { opacity: 0; transform: scale(0.9); }
            20% { opacity: 1; transform: scale(1); }
            80% { opacity: 1; transform: scale(1); }
            100% { opacity: 0; transform: scale(1.1); }
        }
    </style>
</head>
<body>

    <div id="global-stars"></div>
    <div class="decorations-layer" id="decorations"></div>

    <div id="intro-screen">
        <div id="intro-stars"></div>
        <div class="greeting-text">🎉С ДНЕМ РОЖДЕНИЯ, СОНЯ!!! 😊 🎉</div>
        <canvas id="fireworks"></canvas>
    </div>

    <div id="portal-flash"></div>
    <div id="gallery-screen" data-anim="slide"></div>

    <div id="wait-screen">
        <div class="wait-text">Ничего не нажимай...<br>Смотри 👀</div>
    </div>

    <div id="envelope-overlay">
        <div class="envelope">
            <div class="envelope-text">открой, это тебе</div>
            <div class="letter-paper" id="letter-content">
                """ + LETTER_TEXT + """
                <button class="close-letter-btn" onclick="closeEnvelope()">Закрыть конверт</button>
            </div>
            <div class="envelope-stamp" onclick="openEnvelope()">
                <svg viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
            </div>
        </div>
    </div>

    <audio id="bg-audio" preload="none"></audio>

    <script>
        const songs = [
            { title: "Космос", artist: "Три Дня Дождя & Лапи", url: "/song1.mp3" },
            { title: "Выдыхай", artist: "Три Дня Дождя feat. Zivert", url: "/song2.mp3" },
            { title: "Выше", artist: "Авдейка", url: "/song3.mp3" }
        ];

        const texts = {{ texts | safe }};
        const backgrounds = {{ backgrounds | safe }};
        
        let currentAnimType = 'slide';
        let isSeeking = false;

        localStorage.removeItem('envelopeFinished');

        const audio = document.getElementById('bg-audio');
        
        function renderSongs() {
            const container = document.getElementById('playlist-container');
            if(!container) return;
            container.innerHTML = '';
            
            songs.forEach((song, index) => {
                let card = document.createElement('div');
                card.className = 'song-card';
                card.id = `card-${index}`;
                
                card.innerHTML = `
                    <div class="song-header">
                        <div class="song-info">
                            <div class="song-title">${song.title}</div>
                            <div class="song-artist">${song.artist}</div>
                        </div>
                        <div class="song-controls">
                            <button class="ctrl-btn btn-play" id="play-btn-${index}" onclick="playSong(${index})">▶</button>
                            <button class="ctrl-btn btn-stop" onclick="stopSong()">⏹</button>
                        </div>
                    </div>
                    <div class="seek-container" id="seek-container-${index}">
                        <span id="curr-time-${index}">0:00</span>
                        <input type="range" class="seek-bar" id="seek-bar-${index}" value="0" min="0" max="100" step="0.1">
                        <span id="dur-time-${index}">0:00</span>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        function formatTime(seconds) {
            if (isNaN(seconds) || seconds === Infinity) return "0:00";
            const m = Math.floor(seconds / 60);
            const s = Math.floor(seconds % 60);
            return `${m}:${s < 10 ? '0' : ''}${s}`;
        }

        window.playSong = function(index) {
            const btn = document.getElementById(`play-btn-${index}`);
            const card = document.getElementById(`card-${index}`);
            const seekContainer = document.getElementById(`seek-container-${index}`);
            const songSrc = songs[index].url;

            if (audio.src.endsWith(songSrc) && !audio.paused) {
                audio.pause(); btn.innerHTML = "▶"; card.classList.remove('playing'); return;
            }

            audio.pause();
            document.querySelectorAll('.song-card').forEach(c => c.classList.remove('playing'));
            document.querySelectorAll('.btn-play').forEach(b => b.innerHTML = "▶");
            
            audio.src = songSrc;
            audio.load();
            audio.play();
            
            btn.innerHTML = "⏸";
            card.classList.add('playing');
            seekContainer.classList.add('active');

            audio.onloadedmetadata = function() {
                const dur = document.getElementById(`dur-time-${index}`);
                const seekBar = document.getElementById(`seek-bar-${index}`);
                if (dur) dur.textContent = formatTime(audio.duration);
                if (seekBar) { seekBar.max = audio.duration; seekBar.value = 0; }
            };
        }

        window.stopSong = function() {
            audio.pause();
            audio.currentTime = 0;
            document.querySelectorAll('.song-card').forEach(c => c.classList.remove('playing'));
            document.querySelectorAll('.btn-play').forEach(b => b.innerHTML = "▶");
            document.querySelectorAll('.seek-bar').forEach(s => s.value = 0);
            document.querySelectorAll('.seek-container span[id^="curr-time"]').forEach(s => s.textContent = "0:00");
        }

        audio.addEventListener('timeupdate', function() {
            if (isSeeking) return; 
            const playingCard = document.querySelector('.song-card.playing');
            if (playingCard) {
                const index = playingCard.id.split('-').pop();
                const seekBar = document.getElementById(`seek-bar-${index}`);
                const currTime = document.getElementById(`curr-time-${index}`);
                if (seekBar && currTime) {
                    seekBar.value = audio.currentTime;
                    currTime.textContent = formatTime(audio.currentTime);
                }
            }
        });

        document.addEventListener('input', function(e) {
            if (e.target.classList.contains('seek-bar')) {
                isSeeking = true;
                const playingCard = document.querySelector('.song-card.playing');
                if(playingCard) {
                    const index = playingCard.id.split('-').pop();
                    const currTime = document.getElementById(`curr-time-${index}`);
                    if (currTime) currTime.textContent = formatTime(e.target.value);
                }
            }
        });

        document.addEventListener('change', function(e) {
            if (e.target.classList.contains('seek-bar')) {
                audio.currentTime = parseFloat(e.target.value);
                isSeeking = false;
            }
        });
        
        document.addEventListener('mouseup', function(e) { if(e.target.classList.contains('seek-bar')) isSeeking = false; });
        document.addEventListener('touchend', function(e) { if(e.target.classList.contains('seek-bar')) isSeeking = false; });

        const startDate = new Date('2023-12-15T00:00:00'); 
        function updateTimer() {
            const now = new Date();
            const diff = now - startDate;
            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
            const mins = Math.floor((diff / 1000 / 60) % 60);
            const secs = Math.floor((diff / 1000) % 60);
            const timerEl = document.getElementById('friend-timer');
            if (timerEl) {
                timerEl.innerText = `${days} дн. ${hours} ч. ${mins} мин. ${secs} сек.`;
            }
        }
        setInterval(updateTimer, 1000);

        let timerClicks = 0;
        window.handleTimerClick = function() {
            if (localStorage.getItem('envelopeFinished')) {
                alert("Увидев однажды — не увидишь дважды. (Но если перезапустить сайт, можно попробовать снова 😉)");
                return;
            }
            timerClicks++;
            if (timerClicks >= 5) {
                timerClicks = 0;
                const waitScreen = document.getElementById('wait-screen');
                waitScreen.classList.add('show');
                setTimeout(() => {
                    waitScreen.classList.remove('show');
                    document.getElementById('envelope-overlay').classList.add('show');
                }, 3000);
            }
        }

        window.openEnvelope = function() { document.getElementById('envelope-overlay').classList.add('open'); }
        window.closeEnvelope = function() {
            const overlay = document.getElementById('envelope-overlay');
            overlay.classList.remove('open');
            setTimeout(() => { 
                overlay.classList.remove('show'); 
                localStorage.setItem('envelopeFinished', 'true');
            }, 500);
        }

        function handleTilt(e) {
            const slide = document.querySelector('.slide.active');
            if (!slide) return;
            const img = slide.querySelector('img');
            const p = slide.querySelector('p');
            if (!img) return;

            let xAxis, yAxis;
            if (e.type === 'deviceorientation') {
                xAxis = e.beta / 30;
                yAxis = e.gamma / 30;
            } else {
                const centerX = window.innerWidth / 2;
                const centerY = window.innerHeight / 2;
                xAxis = (e.clientY - centerY) / 20;
                yAxis = (centerX - e.clientX) / 20;
            }
            xAxis = Math.max(-10, Math.min(10, xAxis));
            yAxis = Math.max(-10, Math.min(10, yAxis));
            img.style.transform = `rotateX(${xAxis}deg) rotateY(${yAxis}deg) scale(1.02)`;
            if (p) p.style.transform = `translateX(${yAxis * -1.5}px)`;
        }
        if (window.DeviceOrientationEvent) { window.addEventListener('deviceorientation', handleTilt); }
        document.addEventListener('mousemove', handleTilt);

        function createDecorations() {
            const container = document.getElementById('decorations');
            const emojis = ['✨', '⭐', '🎈', '🎉', '💖', '👑', '🌸', '🦄', '🎂', '🥳', '🎁'];
            const totalElements = 25;
            for (let i = 0; i < totalElements; i++) {
                const bubble = document.createElement('div');
                bubble.classList.add('bubble');
                bubble.innerText = emojis[Math.floor(Math.random() * emojis.length)];
                bubble.style.left = `${Math.random() * 100}%`;
                bubble.style.fontSize = `${Math.random() * 20 + 25}px`;
                bubble.style.animationDelay = `${Math.random() * 5}s, ${Math.random() * 2}s`;
                bubble.style.animationDuration = `${Math.random() * 6 + 8}s, ${Math.random() * 2 + 1}s`;
                container.appendChild(bubble);
            }
        }
        createDecorations();

        const canvas = document.getElementById('fireworks');
        const ctx = canvas.getContext('2d');
        let particles = [];
        function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
        window.addEventListener('resize', resizeCanvas); resizeCanvas();

        class Particle {
            constructor(x, y, color) { this.x = x; this.y = y; this.vx = (Math.random() - 0.5) * 12; this.vy = (Math.random() - 0.5) * 12; this.life = 1; this.color = color; }
            update() { this.x += this.vx; this.y += this.vy; this.vy += 0.15; this.life -= 0.02; }
            draw() { ctx.globalAlpha = Math.max(0, this.life); ctx.fillStyle = this.color; ctx.beginPath(); ctx.arc(this.x, this.y, 2.5, 0, Math.PI * 2); ctx.fill(); }
        }
        function createFirework(x, y) {
            const colors = ['#FFD700', '#FF3366', '#00FFFF', '#FF8C00', '#FFFFFF'];
            const color = colors[Math.floor(Math.random() * colors.length)];
            for (let i = 0; i < 70; i++) { particles.push(new Particle(x, y, color)); }
        }
        function animateFireworks() {
            ctx.fillStyle = 'rgba(5, 5, 16, 0.2)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            if (Math.random() < 0.08) { createFirework(Math.random() * canvas.width, canvas.height - (Math.random() * 150)); }
            for (let i = particles.length - 1; i >= 0; i--) {
                particles[i].update(); particles[i].draw(); if (particles[i].life <= 0) { particles.splice(i, 1); }
            }
            requestAnimationFrame(animateFireworks);
        }
        animateFireworks();

        setTimeout(() => {
            const intro = document.getElementById('intro-screen');
            const flash = document.getElementById('portal-flash');
            if(intro) intro.classList.add('zoom-out');
            setTimeout(() => {
                if(flash) flash.classList.add('active');
                setTimeout(() => {
                    if(intro) intro.style.display = 'none';
                    initGallery();
                    if(flash) flash.classList.remove('active');
                }, 400);
            }, 600);
        }, 8000); 

        let currentSlide = 0;
        const galleryScreen = document.getElementById('gallery-screen');
        let startX = 0, startY = 0, isDragging = false;

        function initGallery() {
            galleryScreen.style.background = backgrounds[0];

            for (let i = 0; i < 9; i++) {
                let div = document.createElement('div');
                div.className = 'slide';
                if (i === 0) div.classList.add('active');
                
                if (i < 7) {
                    div.innerHTML = `<img src="/${i + 1}.jpg" alt="фото ${i+1}" loading="${i===0?'eager':'lazy'}" fetchpriority="${i===0?'high':'low'}"><p>${texts[i]}</p>`;
                } else if (i === 7) {
                    div.innerHTML = `
                        <div class="playlist-wrapper">
                            <div class="playlist-container" id="playlist-container"></div>
                            <div class="anim-controls">
                                <button class="anim-btn active" id="btn-slide" onclick="setAnim('slide')">↔ Слайд</button>
                                <button class="anim-btn" id="btn-vertical" onclick="setAnim('vertical')">↕ Вертикально</button>
                                <button class="anim-btn" id="btn-zoom" onclick="setAnim('zoom')">🔍 Масштаб</button>
                                <button class="anim-btn" id="btn-fade" onclick="setAnim('fade')">✨ Затухание</button>
                            </div>
                        </div>
                        <p style="margin-top: 15px;">${texts[i]}</p>
                    `;
                    renderSongs();
                } else if (i === 8) {
                    div.innerHTML = `
                        <div class="timer-box" onclick="handleTimerClick()">
                            <h4>Мы дружим уже:</h4>
                            <p id="friend-timer">Загрузка...</p>
                        </div>
                        <p style="margin-top: 20px;">${texts[i]}</p>
                    `;
                    updateTimer();
                }
                galleryScreen.appendChild(div);
            }
            galleryScreen.style.display = 'flex';
            setupSwipe(galleryScreen);
            setupKeyboard();
        }

        function setupKeyboard() {
            window.addEventListener('keydown', (e) => {
                if (e.target && /INPUT|TEXTAREA/.test(e.target.tagName)) return;
                const next = currentAnimType === 'vertical' ? ['ArrowDown', ' '] : ['ArrowRight', ' '];
                const prev = currentAnimType === 'vertical' ? ['ArrowUp'] : ['ArrowLeft'];
                if (next.indexOf(e.key) >= 0) changeSlide(currentSlide + 1);
                else if (prev.indexOf(e.key) >= 0) changeSlide(currentSlide - 1);
            });
        }

        function setAnim(type) {
            currentAnimType = type;
            document.querySelectorAll('.anim-btn').forEach(b => b.classList.remove('active'));
            const btn = document.getElementById(`btn-${type}`);
            if (btn) btn.classList.add('active');
            galleryScreen.setAttribute('data-anim', type);
        }

        function setupSwipe(element) {
            element.addEventListener('touchstart', e => {
                if (e.target.tagName === 'BUTTON' || e.target.tagName === 'INPUT' || e.target.tagName === 'LABEL' || e.target.classList.contains('seek-bar') || e.target.closest('.playlist-container') || e.target.closest('.timer-box')) return;
                startX = e.touches[0].clientX;
                startY = e.touches[0].clientY;
                isDragging = true;
                const slides = document.querySelectorAll('.slide');
                slides[currentSlide].style.transition = 'none';
            }, {passive: true});

            element.addEventListener('touchmove', e => {
                if (!isDragging) return;
                const diffX = e.touches[0].clientX - startX;
                const diffY = e.touches[0].clientY - startY;
                const slides = document.querySelectorAll('.slide');
                
                if (currentAnimType === 'vertical') { slides[currentSlide].style.transform = `translate3d(0, ${diffY}px, 0)`; }
                else if (currentAnimType === 'zoom') { slides[currentSlide].style.transform = `scale(${Math.max(0.7, 1 - Math.abs(diffX) / window.innerWidth)})`; }
                else if (currentAnimType === 'fade') { }
                else { slides[currentSlide].style.transform = `translate3d(${diffX}px, 0, 0)`; }
            }, {passive: true});

            element.addEventListener('touchend', e => {
                if (!isDragging) return;
                isDragging = false;
                const endX = e.changedTouches[0].clientX;
                const endY = e.changedTouches[0].clientY;
                const diffX = endX - startX;
                const diffY = endY - startY;
                const slides = document.querySelectorAll('.slide');
                slides[currentSlide].style.transition = '';
                slides[currentSlide].style.transform = '';

                if (currentAnimType === 'fade') return;

                if (currentAnimType === 'vertical') {
                    if (diffY > 80) changeSlide(currentSlide - 1);
                    else if (diffY < -80) changeSlide(currentSlide + 1);
                } else {
                    if (diffX > 80) changeSlide(currentSlide - 1);
                    else if (diffX < -80) changeSlide(currentSlide + 1);
                }
            }, {passive: true});
        }

        function changeSlide(newIndex) {
            const slides = document.querySelectorAll('.slide');
            if (newIndex >= 0 && newIndex < slides.length) {
                galleryScreen.style.background = backgrounds[newIndex];
                const oldSlide = slides[currentSlide];
                oldSlide.classList.remove('active');
                oldSlide.classList.add('prev');
                
                currentSlide = newIndex;
                const newSlide = slides[currentSlide];
                newSlide.classList.remove('prev');
                newSlide.classList.add('active');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    try:
        return render_template_string(
            HTML_CODE, 
            texts=json.dumps(TEXTS, ensure_ascii=False), 
            backgrounds=json.dumps(BACKGROUNDS, ensure_ascii=False)
        )
    except Exception as e:
        print(f"ОШИБКА В INDEX: {e}")
        return f"<h1>Ошибка сервера:</h1><p>{e}</p>"

# --- РОУТЫ ДЛЯ КАРТИНОК И ПЕСЕН ИЗ КОРНЯ ---
@app.route('/<int:num>.jpg')
def serve_image(num):
    filepath = os.path.join(BASE_DIR, f"{num}.jpg")
    if not os.path.exists(filepath): 
        return f"Файл {num}.jpg не найден", 404
    response = make_response(send_file(filepath, mimetype='image/jpeg'))
    response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    return response

@app.route('/song1.mp3')
def serve_song1():
    filepath = os.path.join(BASE_DIR, 'song1.mp3')
    if not os.path.exists(filepath): return "Файл не найден", 404
    return send_file(filepath, mimetype='audio/mpeg')

@app.route('/song2.mp3')
def serve_song2():
    filepath = os.path.join(BASE_DIR, 'song2.mp3')
    if not os.path.exists(filepath): return "Файл не найден", 404
    return send_file(filepath, mimetype='audio/mpeg')

@app.route('/song3.mp3')
def serve_song3():
    filepath = os.path.join(BASE_DIR, 'song3.mp3')
    if not os.path.exists(filepath): return "Файл не найден", 404
    return send_file(filepath, mimetype='audio/mpeg')
