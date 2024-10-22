import os
import librosa
import pandas as pd
import matplotlib.pyplot as plt



def time_to_seconds( hour, minute, second):
    return int(hour)*3600 + int(minute)*60 + int(second)

def get_thermal_audio_faults():
    looking_folder_path = '/home/skglab/Desktop/projects/AUDIO_TERMICO/backup_files'
    save_folder_path = '/home/skglab/Desktop/projects/AUDIO_TERMICO/inspection_files'
    excel_path = '/home/skglab/Desktop/projects/AUDIO_TERMICO/data/Inspeccion_CT138_Izquierdo.xlsx'
    buffer_time = 3 
    i = 0

    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)

    data = pd.read_excel(excel_path)

    for fault in data.iterrows():
        print(fault)
        if fault[1]['fault_type'] == 'Thermal':

            i+=1

            day = fault[1]['day']
            if len(str(day)) == 1:
                day = '0'+str(day)
            month = fault[1]['month']
            if len(str(month)) == 1:
                month = '0'+str(month)
            year = fault[1]['year']
            hour = fault[1]['hour']
            if len(str(hour)) == 1:
                hour = '0'+str(hour)
            minute = fault[1]['minute']
            if len(str(minute)) == 1:
                minute = '0'+str(minute)
            second = fault[1]['second']
            if len(str(second)) == 1:
                second = '0'+str(second)

            audio_path = str(fault[1]['belt_name'])+'_'+str(fault[1]['belt_name'][-1])+'_'+str(fault[1]['table'])+'_'+str(fault[1]['station'])+'_'+str(month)+str(day)+str(year)+'_'+str(hour)+str(minute)+str(second)+'_thermal_audio.wav'
            print('------------------->',audio_path)
            belt_bame = fault[1]['belt_name']
            belt_side = fault[1]['belt_name'][-1]
            table = fault[1]['table']
            station = fault[1]['station']
            
            fault_time = time_to_seconds(hour, minute, second)
            file_list = os.listdir(looking_folder_path)
            file_list.sort()

            for file in file_list:
                try:
                    if file.endswith('.wav'):
                        initial_hour = int(file.split('_')[2][0:2])
                        initial_minute = int(file.split('_')[2][2:4])
                        initial_second = int(file.split('_')[2][4:6])
                        final_hour = int(file.split('_')[3][0:2])
                        final_minute = int(file.split('_')[3][2:4])
                        final_second = int(file.split('_')[3][4:6])
                        initial_time = time_to_seconds(initial_hour, initial_minute, initial_second)
                        final_time = time_to_seconds(final_hour, final_minute, final_second)

                        if fault_time >= initial_time and fault_time <= final_time:
                            audio_path = os.path.join(looking_folder_path, file)
                            wav_file_name = f'{belt_bame}_{belt_side}_{table}_{station}_{month}{day}{year}_{hour}{minute}{second}_thermal_audio.wav'
                            wav_path = os.path.join(save_folder_path, wav_file_name)

                            initial_wav_time = fault_time - initial_time
                            os.system(f'ffmpeg -i {audio_path} -ss {initial_wav_time - buffer_time} -to {initial_wav_time + buffer_time} {wav_path}')

                            nfft = 2048
                            hop_length = 512
                            audio_data, sample_rate = librosa.load(wav_path, sr=None)
                            spectogram = librosa.stft(y=audio_data, n_fft=nfft, hop_length=hop_length)
                            spectogram_db = librosa.amplitude_to_db(abs(spectogram))
                            plt.figure(figsize=(8, 6))
                            librosa.display.specshow(spectogram_db, sr=sample_rate, x_axis='time', y_axis='mel', cmap='inferno')
                            plt.colorbar(format='%+2.0f dB')
                            plt.title('Espectrograma')
                            plt.tight_layout()
                            plt.savefig(wav_path.replace(f'_thermal_audio.wav', f'_thermal_mel.jpg'))

                except:
                    pass
            
            print('total thermal records', i)

get_thermal_audio_faults()