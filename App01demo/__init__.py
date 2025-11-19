from otree.api import *
import base64
import os
from datetime import datetime

doc = """
Audio Recording Experiment mit 3 Spielern pro Gruppe und 3 Runden
"""


class C(BaseConstants):
    NAME_IN_URL = 'App01demo'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 3  # ← WICHTIG: 3 Runden!

    PLAYER1_ROLE = 'Player1'
    PLAYER2_ROLE = 'Player2'
    PLAYER3_ROLE = 'Player3'


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    """
    Wird für JEDE Runde einmal ausgeführt.
    Erstellt Ordnerstruktur nur in Runde 1.
    """
    if subsession.round_number == 1:
        # Session-Code für eindeutige Identifikation
        session_code = subsession.session.code

        # Hauptordner erstellen
        os.makedirs('recordings', exist_ok=True)

        # Session-Ordner erstellen
        session_dir = os.path.join('recordings', f'session_{session_code}')
        os.makedirs(session_dir, exist_ok=True)

        # Für jede Gruppe
        for group in subsession.get_groups():
            # Für jeden Player direkt im Session-Ordner
            for player in group.get_players():
                participant_code = player.participant.code
                player_id = player.id_in_group

                # Ordner: recordings/session_XXX/player_Y_CODE/
                player_dir = os.path.join(session_dir, f'player_{player_id}_{participant_code}')
                os.makedirs(player_dir, exist_ok=True)

                print(f"✓ Ordner erstellt: {player_dir}")

    # Gruppen-Struktur beibehalten über alle Runden
    if subsession.round_number > 1:
        subsession.group_like_round(1)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class StartPage(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class WaitForGroup(WaitPage):
    pass


class RecorderPage01(Page):
    """Aufnahmeseite für Player 1 - in allen 3 Runden"""
    form_model = 'player'
    timeout_seconds = 30

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

    @staticmethod
    def live_method(player, data):
        if 'audio' in data:
            audio_base64 = data['audio']
            audio_data = base64.b64decode(audio_base64.split(',')[1])

            session_code = player.session.code
            participant_code = player.participant.code
            player_id = player.id_in_group
            round_num = player.round_number  # ← WICHTIG: Runden-Nummer!

            recording_dir = os.path.join('recordings', f'session_{session_code}',
                                         f'player_{player_id}_{participant_code}')

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"round_{round_num}_recording_{timestamp}.webm"  # ← Mit Runden-Nummer!
            filepath = os.path.join(recording_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(audio_data)

            print(f"✓ Audio gespeichert: {filepath} (Runde {round_num})")

            return {player.id_in_group: {
                'status': 'saved',
                'filename': filename,
                'participant': participant_code,
                'session': session_code,
                'player_id': player_id,
                'round': round_num,
                'role': 'Player 1'
            }}


class RecorderPage02(Page):
    """Aufnahmeseite für Player 2 - in allen 3 Runden"""
    form_model = 'player'
    timeout_seconds = 30

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2

    @staticmethod
    def live_method(player, data):
        if 'audio' in data:
            audio_base64 = data['audio']
            audio_data = base64.b64decode(audio_base64.split(',')[1])

            session_code = player.session.code
            participant_code = player.participant.code
            player_id = player.id_in_group
            round_num = player.round_number

            recording_dir = os.path.join('recordings', f'session_{session_code}',
                                         f'player_{player_id}_{participant_code}')

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"round_{round_num}_recording_{timestamp}.webm"
            filepath = os.path.join(recording_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(audio_data)

            print(f"✓ Audio gespeichert: {filepath} (Runde {round_num})")

            return {player.id_in_group: {
                'status': 'saved',
                'filename': filename,
                'participant': participant_code,
                'session': session_code,
                'player_id': player_id,
                'round': round_num,
                'role': 'Player 2'
            }}

class RecorderPage03(Page):
    """Aufnahmeseite für Player 3 - in allen 3 Runden"""
    form_model = 'player'
    timeout_seconds = 30

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 3

    @staticmethod
    def live_method(player, data):
        if 'audio' in data:
            audio_base64 = data['audio']
            audio_data = base64.b64decode(audio_base64.split(',')[1])

            session_code = player.session.code
            participant_code = player.participant.code
            player_id = player.id_in_group
            round_num = player.round_number

            recording_dir = os.path.join('recordings', f'session_{session_code}',
                                         f'player_{player_id}_{participant_code}')

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"round_{round_num}_recording_{timestamp}.webm"
            filepath = os.path.join(recording_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(audio_data)

            print(f"✓ Audio gespeichert: {filepath} (Runde {round_num})")

            return {player.id_in_group: {
                'status': 'saved',
                'filename': filename,
                'participant': participant_code,
                'session': session_code,
                'player_id': player_id,
                'round': round_num,
                'role': 'Player 3'
            }}


class BreakPage(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number < C.NUM_ROUNDS

class WaitAfterRecording(WaitPage):
    pass

class EndPage(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
    StartPage,
    WaitForGroup,
    RecorderPage01,
    RecorderPage02,
    RecorderPage03,
    WaitAfterRecording,
    BreakPage,
    EndPage
]
