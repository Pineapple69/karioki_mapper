class InputManager:
    @staticmethod
    def get_audio_file_path():
        print('Please provide audio file path.')
        return input()

    @staticmethod
    def get_lyrics_file_path():
        print('Please provide lyrics file path.')
        return input()

    @staticmethod
    def get_title():
        print("Please provide song title.")
        return input()

    @staticmethod
    def get_artist():
        print('Please provide artist.')
        return input()

    @staticmethod
    def get_bpm():
        print('Please provide BPM (optional).')
        return input()
