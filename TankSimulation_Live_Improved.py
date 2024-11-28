import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from datetime import datetime
import pyqtgraph as pg
import logging
import csv
import matplotlib.pyplot as plt



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

        self.start_flow_button = QPushButton("Start Water Flow")
        self.start_flow_button.clicked.connect(self.start_water_flow)
        button_layout.addWidget(self.start_flow_button)

        self.stop_flow_button = QPushButton("Stop Water Flow")
        self.stop_flow_button.clicked.connect(self.stop_water_flow)
        button_layout.addWidget(self.stop_flow_button)

        self.start_drain_button = QPushButton("Start Water Drain")
        self.start_drain_button.clicked.connect(self.start_water_drain)
        button_layout.addWidget(self.start_drain_button)

        self.stop_drain_button = QPushButton("Stop Water Drain")
        self.stop_drain_button.clicked.connect(self.stop_water_drain)
        button_layout.addWidget(self.stop_drain_button)

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
        self.setup_logger()
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger('TankSimulation')


    def setup_logger(self):
        self.logger = logging.getLogger('TankSimulation')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('tank_simulation.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

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
        self.water_flow = False
        self.water_drain = False
        self.setpoint1 = 50  # Desired level for tank 1
        self.setpoint2 = 50  # Desired level for tank 2
        self.Kp = 0.5  # Proportional gain
        self.Ki = 0.1  # Integral gain
        self.Kd = 0.05  # Derivative gain
        self.integral1 = 0
        self.integral2 = 0
        self.prev_error1 = 0
        self.prev_error2 = 0

    def pid_control(self, level, setpoint, integral, prev_error):
        error = setpoint - level
        integral += error * 0.1  # Assuming 0.1 second time step
        derivative = (error - prev_error) / 0.1
        output = self.Kp * error + self.Ki * integral + self.Kd * derivative
        return max(0, min(1, output)), integral, error

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

        if self.sensor_working:
            if self.water_flow:
                control1, self.integral1, self.prev_error1 = self.pid_control(self.level1, self.setpoint1, self.integral1, self.prev_error1)
                control2, self.integral2, self.prev_error2 = self.pid_control(self.level2, self.setpoint2, self.integral2, self.prev_error2)
                self.level1 = min(self.level1 + control1 * time_step, self.tank1_max)
                self.level2 = min(self.level2 + control2 * time_step, self.tank2_max)
            if self.water_drain:
                drain_rate1 = self.calculate_control(self.level1, 30, 80, 90, 95, is_draining=True)
                drain_rate2 = self.calculate_control(self.level2, 20, 80, 90, 95, is_draining=True)
                self.level1 = max(self.level1 - 0.5 * time_step, 0)  # Constant drain rate
                self.level2 = max(self.level2 - 0.5 * time_step, 0)
        else:
            self.status_label.setText("System Status: Sensor Failure")

        self.check_overflow()
        self.check_failsafe()
        self.play_alarms()

        self.times.append(self.time)
        self.levels1.append(self.level1)
        self.levels2.append(self.level2)

        self.curve1.setData(self.times, self.levels1)
        self.curve2.setData(self.times, self.levels2)

        if self.level1 >= 30 and self.prev_level1 < 30:
            self.logger.info("Tank 1 reached 30% level")
        if self.level2 >= 20 and self.prev_level2 < 20:
            self.logger.info("Tank 2 reached 20% level")
    
        if self.level1 >= 80 and self.prev_level1 < 80:
            self.logger.info("Tank 1 reached 80% level")
        if self.level2 >= 80 and self.prev_level2 < 80:
            self.logger.info("Tank 2 reached 80% level")
    
        if self.level1 >= 90 and self.prev_level1 < 90:
            self.logger.info("Tank 1 reached 90% level")
        if self.level2 >= 90 and self.prev_level2 < 90:
            self.logger.info("Tank 2 reached 90% level")
    
        if self.level1 >= 95 and self.prev_level1 < 95:
            self.logger.info("Tank 1 reached 95% level")
        if self.level2 >= 95 and self.prev_level2 < 95:
            self.logger.info("Tank 2 reached 95% level")
    
        self.prev_level1 = self.level1
        self.prev_level2 = self.level2

    def calculate_control(self, level, start_fill, slow_down1, slow_down2, stop_fill, is_draining=False):
        if is_draining:
            return 0.5  # Constant drain rate
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
    
    def set_pid_parameters(self, kp, ki, kd):
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd

    def set_setpoints(self, setpoint1, setpoint2):
        self.setpoint1 = setpoint1
        self.setpoint2 = setpoint2

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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"simulation_data_{timestamp}.csv"
        self.logger.info("Simulation stopped")
    
        # Save data as CSV
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'Tank1 Level', 'Tank2 Level'])
            for t, l1, l2 in zip(self.times, self.levels1, self.levels2):
                writer.writerow([t, l1, l2])
        
        self.status_label.setText(f"Simulation stopped. Data saved to {filename}")

        # Save plot as image
        plt.figure(figsize=(10, 6))
        plt.plot(self.times, self.levels1, label='Tank 1')
        plt.plot(self.times, self.levels2, label='Tank 2')
        plt.xlabel('Time (s)')
        plt.ylabel('Level (%)')
        plt.title('Tank Simulation Results')
        plt.legend()
        plt.savefig('simulation_results.png')
        self.close()

    def simulate_power_loss(self):
        self.power_on = not self.power_on
        if self.power_on:
            self.status_label.setText("System Status: Power Restored")
            self.logger.info("Power restored")

        else:
            self.status_label.setText("System Status: Power Loss")
            self.logger.warning("Power loss")

    def simulate_sensor_failure(self):
        self.sensor_working = not self.sensor_working
        if self.sensor_working:
            self.status_label.setText("System Status: Sensors Restored")
            self.logger.info("Sensors restored")

        else:
            self.status_label.setText("System Status: Sensor Failure")
            self.logger.warning("Sensor failure occurred")

    def start_water_flow(self):
        self.water_flow = True
        self.status_label.setText("System Status: Water Flow Started")
        self.logger.info("Water flow started")

    def stop_water_flow(self):
        self.water_flow = False
        self.status_label.setText("System Status: Water Flow Stopped")
        self.logger.info("Water flow stopped")


    def start_water_drain(self):
        self.water_drain = True
        self.status_label.setText("System Status: Water Drain Started")
        self.logger.info("Water drain started")


    def stop_water_drain(self):
        self.water_drain = False
        self.status_label.setText("System Status: Water Drain Stopped")
        self.logger.info("Water drain stopped")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    sim = TankSimulation()
    sim.show()
    sys.exit(app.exec_())
