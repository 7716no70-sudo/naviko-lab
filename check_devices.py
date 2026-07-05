import pyaudio

print("=== 利用可能なオーディオデバイス一覧 ===\n")

pa = pyaudio.PyAudio()

for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    name = info['name']
    max_input = info['maxInputChannels']
    
    # 入力デバイスのみ表示
    if max_input > 0:
        print(f"{i}: {name} (入力チャンネル:{max_input})")

pa.terminate()

print("\n=== Bluetoothデバイス検索 ===")
print("上記の一覧から 'Bluetooth' または 'ハンズフリー' を含むデバイスを探してください。")
