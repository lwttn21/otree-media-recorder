from otree.api import *
import base64
import os
from datetime import datetime


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'App01demo'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


class RecorderPage(Page):
    form_model = 'player'

    @staticmethod
    def live_method(player, data):
        """
        Empfängt und speichert Audio-Daten vom Client
        """
        if 'audio' in data:
            # Base64-String empfangen und dekodieren
            audio_base64 = data['audio']
            audio_data = base64.b64decode(audio_base64.split(',')[1])

            # Eindeutigen Dateinamen erstellen
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            participant_code = player.participant.code
            filename = f"participant_{participant_code}_{timestamp}.webm"
            filepath = os.path.join('recordings', filename)

            # Datei speichern
            with open(filepath, 'wb') as f:
                f.write(audio_data)

            print(f"✓ Audio gespeichert: {filepath}")
            return {player.id_in_group: {'status': 'saved', 'filename': filename}}

class StartPage(Page):
    pass

class EndPage(Page):
    pass

page_sequence = [StartPage, RecorderPage, EndPage]
