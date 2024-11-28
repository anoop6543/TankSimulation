# You're right, improving the visualization and adding more interactive features will enhance the simulation. Here's an updated version of the program with larger text, additional buttons for power loss and sensor failure scenarios, and buzzer sounds for different tank levels:


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
import pyqtgraph as pg


class TankSimulation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Two-Tank System Simulation")
        self.setGeometry(100, 100, 1000, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)

        self.plot_widget = pg.PlotWidget()
        main_layout.addWidget(self.plot_widget)

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        self.stop_button = QPushButton("Stop Simulation")
        self.stop_button.clicked.connect(self.stop_simulation)
        button_layout.addWidget(self.stop_button)

        self.power_loss_button = QPushButton("Simulate Power Loss")
        self.power_loss_button.clicked.connect(self.simulate_power_loss)
        button_layout.addWidget(self.power_loss_button)

        self.sensor_failure_button = QPushButton("Simulate Sensor Failure")
        self.sensor_failure_button.clicked.connect(self.simulate_sensor_failure)
        button_layout.addWidget(self.sensor_failure_button)

        self.status_label = QLabel("System Status: Normal")
        main_layout.addWidget(self.status_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(100)  # Update every 100 ms

        self.player_90 = QMediaPlayer()
        self.player_95 = QMediaPlayer()
        self.player_100 = QMediaPlayer()

        self.initialize_simulation()
        self.setup_plot()
        self.setup_sounds()

    def initialize_simulation(self):
        self.tank1_max = 100
        self.tank2_max = 100
        self.level1 = 0
        self.level2 = 0
        self.time = 0
        self.times = []
        self.levels1 = []
        self.levels2 = []
        self.power_on = True
        self.sensor_working = True

    def setup_plot(self):
        self.plot_widget.setBackground('w')
        self.plot_widget.setLabel('left', 'Level (%)', **{'font-size': '16pt'})
        self.plot_widget.setLabel('bottom', 'Time (s)', **{'font-size': '16pt'})
        self.plot_widget.addLegend(size=(160, 80), offset=(20, 20))
        self.plot_widget.getAxis('left').setTickFont(pg.QtGui.QFont('Arial', 12))
        self.plot_widget.getAxis('bottom').setTickFont(pg.QtGui.QFont('Arial', 12))

        self.curve1 = self.plot_widget.plot(pen=pg.mkPen('b', width=3), name='Tank 1')
        self.curve2 = self.plot_widget.plot(pen=pg.mkPen('r', width=3), name='Tank 2')

        self.plot_widget.addLine(y=30, pen=pg.mkPen('b', width=2, style=pg.QtCore.Qt.DashLine))
        self.plot_widget.addLine(y=20, pen=pg.mkPen('r', width=2, style=pg.QtCore.Qt.DashLine))
        self.plot_widget.addLine(y=80, pen=pg.mkPen('g', width=2, style=pg.QtCore.Qt.DashLine))
        self.plot_widget.addLine(y=90, pen=pg.mkPen('y', width=2, style=pg.QtCore.Qt.DashLine))
        self.plot_widget.addLine(y=95, pen=pg.mkPen('m', width=2, style=pg.QtCore.Qt.DashLine))

    def setup_sounds(self):
        self.sound_90 = QSound("sound_90.wav")
        self.sound_95 = QSound("sound_95.wav")
        self.sound_100 = QSound("sound_100.wav")
        self.player_90.setMedia(QMediaContent(QUrl.fromLocalFile("./sound_90.wav")))
        self.player_95.setMedia(QMediaContent(QUrl.fromLocalFile("./sound_95.wav")))
        self.player_100.setMedia(QMediaContent(QUrl.fromLocalFile("./sound_100.wav")))

    def update_simulation(self):
        if not self.power_on:
            self.status_label.setText("System Status: Power Off")
            return

        time_step = 0.1
        self.time += time_step

        control1 = self.calculate_control(self.level1, 30, 80, 90, 95)
        control2 = self.calculate_control(self.level2, 20, 80, 90, 95)

        if self.sensor_working:
            self.level1 = min(self.level1 + control1 * time_step, self.tank1_max)
            self.level2 = min(self.level2 + control2 * time_step, self.tank2_max)
        else:
            # Simulate sensor failure by not updating levels
            self.status_label.setText("System Status: Sensor Failure")

        self.check_overflow()
        self.check_failsafe()
        self.play_alarms()

        self.times.append(self.time)
        self.levels1.append(self.level1)
        self.levels2.append(self.level2)

        self.curve1.setData(self.times, self.levels1)
        self.curve2.setData(self.times, self.levels2)

    def calculate_control(self, level, start_fill, slow_down1, slow_down2, stop_fill):
        if level < start_fill:
            return 1
        elif start_fill <= level < slow_down1:
            return 1
        elif slow_down1 <= level < slow_down2:
            return 0.5
        elif slow_down2 <= level < stop_fill:
            return 0.25
        else:
            return 0

    def check_overflow(self):
        if self.level1 >= self.tank1_max or self.level2 >= self.tank2_max:
            self.status_label.setText("WARNING: Tank overflow detected!")

    def check_failsafe(self):
        if self.level1 >= 98 or self.level2 >= 98:
            self.status_label.setText("EMERGENCY: Critical level reached. Shutting down pumps.")

    def play_alarms(self):
        if self.level1 >= 100 or self.level2 >= 100:
            self.player_100.play()
        elif self.level1 >= 95 or self.level2 >= 95:
            self.player_95.play()
        elif self.level1 >= 90 or self.level2 >= 90:
            self.player_90.play()

    def stop_simulation(self):
        self.timer.stop()
        self.close()

    def simulate_power_loss(self):
        self.power_on = not self.power_on
        if self.power_on:
            self.status_label.setText("System Status: Power Restored")
        else:
            self.status_label.setText("System Status: Power Loss")

    def simulate_sensor_failure(self):
        self.sensor_working = not self.sensor_working
        if self.sensor_working:
            self.status_label.setText("System Status: Sensors Restored")
        else:
            self.status_label.setText("System Status: Sensor Failure")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sim = TankSimulation()
    sim.show()
    sys.exit(app.exec_())

# This updated version includes the following improvements:

# 1. **Larger Text**: The plot labels and axis ticks now use larger fonts for better visibility.

# 2. **Additional Buttons**: New buttons for simulating power loss and sensor failure have been added.

# 3. **Power Loss Simulation**: The `simulate_power_loss()` method toggles the power state, affecting the simulation.

# 4. **Sensor Failure Simulation**: The `simulate_sensor_failure()` method simulates a sensor malfunction by stopping level updates.

# 5. **Status Label**: A status label has been added to display system conditions and warnings.

# 6. **Buzzer Sounds**: The `setup_sounds()` method initializes different sounds for various tank levels. The `play_alarms()` method triggers these sounds at appropriate levels.

# 7. **Improved Visualization**: The plot lines are now thicker for better visibility.

# To use this updated version:

# 1. Replace your existing `two_tank_simulation.py` file with this new code.
# 2. Ensure you have sound files named `sound_90.wav`, `sound_95.wav`, and `sound_100.wav` in the same directory as your script. These will be used for the alarm sounds.
# 3. Run the script as before in Visual Studio 2022.

# This enhanced simulation provides a more interactive and realistic representation of a two-tank system, with improved visibility and additional features to simulate real-world scenarios.