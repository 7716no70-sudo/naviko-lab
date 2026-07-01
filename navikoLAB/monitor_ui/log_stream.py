# log_stream.py

import tkinter as tk


class LogStream:

    def stream(self, data):

        print("\n[LOG STREAM]")

        for k, v in data.items():
            print(f"{k}: {v}")