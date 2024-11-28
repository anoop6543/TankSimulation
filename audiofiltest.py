# # from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
# # from PyQt5.QtCore import QUrl

# # self.player = QMediaPlayer()
# # self.player.setMedia(QMediaContent(QUrl.fromLocalFile("./sound_90.wav")))
# # self.player.play()

# To implement these suggestions, you'll need to modify the `setup_sounds()` method and the `play_alarms()` method in your `TankSimulation` class. Here's how you can update these methods:

# ```python
# from PyQt5.QtCore import QUrl
# from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

# class TankSimulation(QMainWindow):
#     # ... (other parts of the class remain the same)

#     def setup_sounds(self):
#         self.player_90 = QMediaPlayer()
#         self.player_95 = QMediaPlayer()
#         self.player_100 = QMediaPlayer()

#         self.player_90.setMedia(QMediaContent(QUrl.fromLocalFile("./sound_90.wav")))
#         self.player_95.setMedia(QMediaContent(QUrl.fromLocalFile("./sound_95.wav")))
#         self.player_100.setMedia(QMediaContent(QUrl.fromLocalFile("./sound_100.wav")))

#     def play_alarms(self):
#         if self.level1 >= 100 or self.level2 >= 100:
#             self.player_100.play()
#         elif self.level1 >= 95 or self.level2 >= 95:
#             self.player_95.play()
#         elif self.level1 >= 90 or self.level2 >= 90:
#             self.player_90.play()

#     # ... (rest of the class remains the same)
# ```

# These changes do the following:

# 1. We import `QUrl`, `QMediaPlayer`, and `QMediaContent` from PyQt5.
# 2. In `setup_sounds()`, we create three `QMediaPlayer` objects instead of using `QSound`.
# 3. We use `QUrl.fromLocalFile()` to specify the file paths, assuming the sound files are in the same directory as the script.
# 4. In `play_alarms()`, we use the `play()` method of the `QMediaPlayer` objects to play the sounds.

# Make sure to replace the existing `setup_sounds()` and `play_alarms()` methods in your code with these updated versions. Also, ensure that the sound files (`sound_90.wav`, `sound_95.wav`, and `sound_100.wav`) are in the same directory as your Python script.

# These changes should resolve the "Error decoding source file" issues you were experiencing.


def setup_sounds(self):
    self.player_90.setMedia(QMediaContent(QUrl.fromLocalFile("./sound_90.wav")))
    self.player_95.setMedia(QMediaContent(QUrl.fromLocalFile("./sound_95.wav")))
    self.player_100.setMedia(QMediaContent(QUrl.fromLocalFile("./sound_100.wav")))