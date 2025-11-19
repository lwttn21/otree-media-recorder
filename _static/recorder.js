// _static/recorder.js
function initializeRecorder(playerName, roundNumber) {
    const status = document.getElementById('status');
    const timerDisplay = document.getElementById('timer');
    let mediaRecorder = null;
    let chunks = [];
    let uploadTriggered = false;

    const TOTAL_SECONDS = 30;
    const UPLOAD_BEFORE_END = 5;
    let remainingSeconds = TOTAL_SECONDS;

    function updateTimer() {
        const minutes = Math.floor(remainingSeconds / 60);
        const seconds = remainingSeconds % 60;
        timerDisplay.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;

        if (remainingSeconds === UPLOAD_BEFORE_END && !uploadTriggered) {
            uploadTriggered = true;
            stopAndUpload();
        }

        if (remainingSeconds > 0) {
            remainingSeconds--;
            setTimeout(updateTimer, 1000);
        }
    }

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then((stream) => {
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.start();
                status.textContent = `🔴 Aufnahme läuft... (${playerName})`;
                console.log(`${playerName}: Aufnahme gestartet (Runde ${roundNumber})`);

                updateTimer();

                mediaRecorder.ondataavailable = (e) => {
                    chunks.push(e.data);
                };

                mediaRecorder.onstop = (e) => {
                    const blob = new Blob(chunks, { type: 'audio/webm' });
                    console.log(`${playerName}: Blob erstellt, Größe:`, blob.size, 'bytes');
                    status.textContent = '⏳ Speichere Aufnahme...';

                    const reader = new FileReader();
                    reader.onloadend = function() {
                        liveSend({'audio': reader.result});
                    };
                    reader.readAsDataURL(blob);
                };
            })
            .catch((err) => {
                console.error(`getUserMedia error: ${err}`);
                status.textContent = 'Fehler: Mikrofon-Zugriff verweigert';
            });
    } else {
        status.textContent = 'Fehler: getUserMedia wird nicht unterstützt';
    }

    function stopAndUpload() {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            console.log(`${playerName}: Stoppe Aufnahme für Upload...`);
            mediaRecorder.stop();
        }
    }

    function liveRecv(data) {
        if (data.status === 'saved') {
            status.textContent = `✅ Aufnahme gespeichert! (${playerName})`;
            console.log(`${playerName}: Upload erfolgreich:`, data.filename);
        }
    }
    window.liveRecv = liveRecv;
}