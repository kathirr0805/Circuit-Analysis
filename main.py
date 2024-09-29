import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

# Import necessary libraries for calculations
import numpy as np
from sympy import symbols, Eq, solve

class CircuitAnalyzer(QMainWindow):
    def __init__(self):
        super(CircuitAnalyzer, self).__init__()
        uic.loadUi('circuit_analyzer.ui', self)

        # Connect signals
        self.analysisTypeComboBox.currentIndexChanged.connect(self.show_formula)
        self.calculateButton.clicked.connect(self.calculate_result)

    def show_formula(self):
        # Get selected analysis type
        analysis_type = self.analysisTypeComboBox.currentText()
        
        # Display corresponding formula
        if analysis_type == "Ohm's Law":
            self.formulaText.setText("V = I * R\nWhere:\nV: Voltage\nI: Current\nR: Resistance")
            self.show_input_fields("Voltage (V)", "Current (I)", "Resistance (R)")
        
        elif analysis_type == "Kirchhoff's Voltage Law":
            self.formulaText.setText("ΣV around a loop = 0\nEnter voltages for each component.")
            self.show_input_fields("Voltage 1", "Voltage 2", "Voltage 3")
        
        elif analysis_type == "Thevenin's Theorem":
            self.formulaText.setText("V_th = (R2 / (R1 + R2)) * V_in\nEnter R1, R2, and V_in.")
            self.show_input_fields("R1", "R2", "V_in")
        
        elif analysis_type == "Maximum Power Transfer":
            self.formulaText.setText("R_L = R_th\nMaximum power transfer occurs when load resistance equals Thevenin resistance.")
            self.show_input_fields("R_th")
        
        elif analysis_type == "Resonance":
            self.formulaText.setText("f_res = 1 / (2 * π * √(L * C))\nEnter L (Inductance) and C (Capacitance).")
            self.show_input_fields("Inductance (L)", "Capacitance (C)")

    def show_input_fields(self, *args):
        # Clear all input fields
        self.input1.clear()
        self.input2.clear()
        self.input3.clear()

        # Show labels and text boxes for the necessary inputs
        self.label1.setText(args[0] if len(args) > 0 else "")
        self.label2.setText(args[1] if len(args) > 1 else "")
        self.label3.setText(args[2] if len(args) > 2 else "")
        
        # Hide unused fields
        self.label1.setVisible(len(args) > 0)
        self.input1.setVisible(len(args) > 0)
        self.label2.setVisible(len(args) > 1)
        self.input2.setVisible(len(args) > 1)
        self.label3.setVisible(len(args) > 2)
        self.input3.setVisible(len(args) > 2)

    def calculate_result(self):
        # Get selected analysis type
        analysis_type = self.analysisTypeComboBox.currentText()
        
        # Perform calculation based on selected analysis
        if analysis_type == "Ohm's Law":
            try:
                # Fetch values from input
                voltage = float(self.input1.text())
                current = float(self.input2.text())
                resistance = voltage / current if current != 0 else 0
                self.resultLabel.setText(f"Resistance: {resistance:.2f} Ohms")
            except ValueError:
                self.resultLabel.setText("Please enter valid numbers.")

        elif analysis_type == "Kirchhoff's Voltage Law":
            try:
                # Fetch voltage values
                v1 = float(self.input1.text())
                v2 = float(self.input2.text())
                v3 = float(self.input3.text())
                total_voltage = v1 + v2 + v3
                self.resultLabel.setText(f"ΣV = {total_voltage:.2f} V")
            except ValueError:
                self.resultLabel.setText("Please enter valid numbers.")

        elif analysis_type == "Thevenin's Theorem":
            try:
                r1 = float(self.input1.text())
                r2 = float(self.input2.text())
                vin = float(self.input3.text())
                vth = (r2 / (r1 + r2)) * vin
                self.resultLabel.setText(f"Thevenin Voltage: {vth:.2f} V")
            except ValueError:
                self.resultLabel.setText("Please enter valid numbers.")
        
        elif analysis_type == "Maximum Power Transfer":
            try:
                rth = float(self.input1.text())
                self.resultLabel.setText(f"Load Resistance (for max power transfer): {rth:.2f} Ohms")
            except ValueError:
                self.resultLabel.setText("Please enter a valid number.")
        
        elif analysis_type == "Resonance":
            try:
                l = float(self.input1.text())
                c = float(self.input2.text())
                fres = 1 / (2 * np.pi * np.sqrt(l * c))
                self.resultLabel.setText(f"Resonance Frequency: {fres:.2f} Hz")
            except ValueError:
                self.resultLabel.setText("Please enter valid numbers.")

# Main function to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CircuitAnalyzer()
    window.show()
    sys.exit(app.exec_())
