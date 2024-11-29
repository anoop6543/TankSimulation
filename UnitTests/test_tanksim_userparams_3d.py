import unittest
import numpy as np
from PyQt5.QtWidgets import QApplication
from TankSim_UserParams_3d import TankSimulation

class TestTankSimulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.sim = TankSimulation()

    def test_initialize_simulation(self):
        self.sim.initialize_simulation()
        self.assertEqual(self.sim.tank1_max, 100)
        self.assertEqual(self.sim.tank2_max, 100)
        self.assertEqual(self.sim.level1, 0)
        self.assertEqual(self.sim.level2, 0)
        self.assertEqual(self.sim.setpoint1, 50)
        self.assertEqual(self.sim.setpoint2, 50)
        self.assertEqual(self.sim.Kp, 0.5)
        self.assertEqual(self.sim.Ki, 0.1)
        self.assertEqual(self.sim.Kd, 0.05)

    def test_apply_parameters(self):
        self.sim.tank1_max_input.setValue(200)
        self.sim.tank2_max_input.setValue(200)
        self.sim.setpoint1_input.setValue(60)
        self.sim.setpoint2_input.setValue(60)
        self.sim.kp_input.setValue(1.0)
        self.sim.ki_input.setValue(0.2)
        self.sim.kd_input.setValue(0.1)
        self.sim.apply_parameters()
        self.assertEqual(self.sim.tank1_max, 200)
        self.assertEqual(self.sim.tank2_max, 200)
        self.assertEqual(self.sim.setpoint1, 60)
        self.assertEqual(self.sim.setpoint2, 60)
        self.assertEqual(self.sim.Kp, 1.0)
        self.assertEqual(self.sim.Ki, 0.2)
        self.assertEqual(self.sim.Kd, 0.1)

    def test_set_control_algorithm(self):
        self.sim.set_control_algorithm("MPC")
        self.assertEqual(self.sim.control_algorithm, "MPC")
        self.sim.set_control_algorithm("Fuzzy Logic")
        self.assertEqual(self.sim.control_algorithm, "Fuzzy Logic")

    def test_pid_control(self):
        output, integral, error = self.sim.pid_control(40, 50, 0, 0)
        self.assertGreaterEqual(output, 0)
        self.assertLessEqual(output, 1)
        self.assertNotEqual(integral, 0)
        self.assertNotEqual(error, 0)

    def test_mpc_control(self):
        control1, control2 = self.sim.mpc_control()
        self.assertGreaterEqual(control1, 0)
        self.assertLessEqual(control1, 1)
        self.assertGreaterEqual(control2, 0)
        self.assertLessEqual(control2, 1)

    def test_fuzzy_control(self):
        control1, control2 = self.sim.fuzzy_control()
        self.assertGreaterEqual(control1, 0)
        self.assertLessEqual(control1, 1)
        self.assertGreaterEqual(control2, 0)
        self.assertLessEqual(control2, 1)

    def test_calculate_control(self):
        control = self.sim.calculate_control(25, 30, 80, 90, 95)
        self.assertEqual(control, 1)
        control = self.sim.calculate_control(85, 30, 80, 90, 95)
        self.assertEqual(control, 0.5)
        control = self.sim.calculate_control(92, 30, 80, 90, 95)
        self.assertEqual(control, 0.25)
        control = self.sim.calculate_control(97, 30, 80, 90, 95)
        self.assertEqual(control, 0)

    def test_check_overflow(self):
        self.sim.level1 = 101
        self.sim.check_overflow()
        self.assertEqual(self.sim.status_label.text(), "WARNING: Tank overflow detected!")

    def test_check_failsafe(self):
        self.sim.level1 = 99
        self.sim.check_failsafe()
        self.assertEqual(self.sim.status_label.text(), "EMERGENCY: Critical level reached. Shutting down pumps.")

    def test_simulate_power_loss(self):
        self.sim.simulate_power_loss()
        self.assertFalse(self.sim.power_on)
        self.sim.simulate_power_loss()
        self.assertTrue(self.sim.power_on)

    def test_simulate_sensor_failure(self):
        self.sim.simulate_sensor_failure()
        self.assertFalse(self.sim.sensor_working)
        self.sim.simulate_sensor_failure()
        self.assertTrue(self.sim.sensor_working)

    def test_start_stop_water_flow(self):
        self.sim.start_water_flow()
        self.assertTrue(self.sim.water_flow)
        self.sim.stop_water_flow()
        self.assertFalse(self.sim.water_flow)

    def test_start_stop_water_drain(self):
        self.sim.start_water_drain()
        self.assertTrue(self.sim.water_drain)
        self.sim.stop_water_drain()
        self.assertFalse(self.sim.water_drain)

    def test_update_tank_water_level(self):
        self.sim.update_tank_water_level(self.sim.tank1, self.sim.tank1_vertices, 0.5)
        updated_vertices = self.sim.tank1_vertices.copy()
        updated_vertices[:, 2] = np.clip(updated_vertices[:, 2], 0, 0.5)
        self.assertTrue(np.array_equal(self.sim.tank1.meshData().vertexes(), updated_vertices))

if __name__ == '__main__':
    unittest.main()
