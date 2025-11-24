from otree.api import *
import base64
import os

doc = """
Audio Chunk Recording Experiment: Jede Runde wird beim Player chunkweise aufgenommen und hochgeladen.
"""

class C(BaseConstants):
    NAME_IN_URL = 'App02demo'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 3

    TIMEOUT_SECONDS = 120

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    """
    Wird für JEDE Runde einmal ausgeführt.
    Erstellt für alle Spieler in Runde 1 die komplette Ordnerstruktur inkl. round_N.
    """
    if subsession.round_number == 1:
        session_code = subsession.session.code
        # create main recordings directory
        for group in subsession.get_groups():
            # create player directories
            for player in group.get_players():
                participant_code = player.participant.code
                player_id = player.id_in_group
                player_dir = os.path.join(
                    'recordings',
                    f'session_{session_code}',
                    f'player_{player_id}_{participant_code}'
                )

                # TODO: nur zum Debugggen - entfernen später
                print(f"Order für Session erstellt: recordings/session_{session_code}/")
                print(f"✓ Ordner erstellt: {player_dir}")

                os.makedirs(player_dir, exist_ok=True)

                # create round directories within player directory
                for r in range(1, C.NUM_ROUNDS + 1):
                    round_dir = os.path.join(player_dir, f'round_{r}')
                    os.makedirs(round_dir, exist_ok=True)

    # maintain group structure across rounds
    if subsession.round_number > 1:
        subsession.group_like_round(1)


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass

def save_audio_chunk(player, data):
    """Speichert einen Audio-Chunk im passenden Runde-Unterordner."""
    if 'audio' not in data or 'round' not in data or 'chunk' not in data:
        return None

    session_code = player.session.code
    participant_code = player.participant.code
    player_id = player.id_in_group
    round_num = data['round']
    chunk_index = data['chunk']

    base_dir = os.path.join(
        'recordings',
        f'session_{session_code}',
        f'player_{player_id}_{participant_code}',
        f'round_{round_num}'
    )
    os.makedirs(base_dir, exist_ok=True)
    filename = f'chunk_{chunk_index:02d}.webm'
    filepath = os.path.join(base_dir, filename)

    audio_base64 = data['audio']
    audio_data = base64.b64decode(audio_base64.split(',')[1])
    with open(filepath, 'wb') as f:
        f.write(audio_data)

    #TODO: nur zum Debugggen - entfernen später
    print(f"✓ Audio-Chunk gespeichert: {filepath} (Runde {round_num}, Chunk {chunk_index})")

    return None

class StartPage(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class WaitForGroup(WaitPage):
    pass


class RecorderPage01(Page):
    form_model = 'player'
    timeout_seconds = C.TIMEOUT_SECONDS

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

    @staticmethod
    def live_method(player, data):
        return save_audio_chunk(player, data)


class RecorderPage02(Page):
    form_model = 'player'
    timeout_seconds = C.TIMEOUT_SECONDS

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2

    @staticmethod
    def live_method(player, data):
        return save_audio_chunk(player, data)


class RecorderPage03(Page):
    form_model = 'player'
    timeout_seconds = C.TIMEOUT_SECONDS

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 3

    @staticmethod
    def live_method(player, data):
        return save_audio_chunk(player, data)


class WaitAfterRecording(WaitPage):
    pass


class BreakPage(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number < C.NUM_ROUNDS


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
