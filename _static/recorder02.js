function startChunkRecorder(roundNumber, chunkDurationSec = 10, pageDurationSec = 600, stopEarlySec = 30) {
    let mediaRecorder = null;
    let chunkIndex = 1;
    let totalRecordingSec = pageDurationSec - stopEarlySec; // z.B. 600 - 30 = 570

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = e => {
                if (e.data.size > 0) {
                    const reader = new FileReader();
                    reader.onloadend = function() {
                        // Info zu jedem Chunk im Browser (nicht im Server-Terminal!)
                        //console.log(
                        //    `[recorder02] Runde ${roundNumber}, Chunk ${chunkIndex} gesendet (${(chunkDurationSec)}s)`
                        //);
                        liveSend({
                            'audio': reader.result,
                            'round': roundNumber,
                            'chunk': chunkIndex
                        });
                        chunkIndex++;
                    };
                    reader.readAsDataURL(e.data);
                }
            };

            // Nimmt alle chunkDurationSec Sekunden einen Chunk auf
            mediaRecorder.start(chunkDurationSec * 1000);

            // Stoppe die Aufnahme frühzeitig (vor Pagewechsel)
            setTimeout(() => {
                if (mediaRecorder && mediaRecorder.state === "recording") {
                    mediaRecorder.stop();
                    console.log(
                        `[recorder02] Aufnahme nach ${totalRecordingSec} Sekunden gestoppt (${stopEarlySec}s vor Seitenwechsel)`
                    );
                }
            }, totalRecordingSec * 1000);
        })
        .catch(err => {
            console.error('Recorder-Fehler:', err);
        });
}
