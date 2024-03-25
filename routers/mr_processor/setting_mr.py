import os
import shutil
import zipfile 
import subprocess
from pydub import AudioSegment


class mr:
    def __init__(self, mr_dir):
        self.mr_dir = mr_dir

    def separating(self, stems, file):

        path = os.path.join(self.mr_dir)

        file.filename = file.filename.replace(" ", "_")
        file_path = os.path.join(path, file.filename)
        print(file_path)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        name, _ = os.path.splitext(file.filename)

        for song in os.listdir(path):
            if song == file.filename:
                # 사용자로 부터 받은 mp3형태의 노래 파일을 stems 값에 따라 분리
                spl = r'spleeter separate -p spleeter:' + \
                str(stems) + r'stems -o ' + os.path.join(path) + ' ' + os.path.join(path, name) + '.mp3'
                flag = subprocess.run(spl, shell=True)
                os.remove(os.path.join(path, file.filename))
        
        zip_name = f'{stems}_{name}'
        zip_path = os.path.join(path, name)
        send_path = os.path.join(path,name)

        # # mp3파일을 MR 분리 후 사용자에게 zip형태로 반환
        # with zipfile.ZipFile(zip_path, 'w') as zipf:
        #     result_path = os.path.join(self.mr_dir, self.mr_id, name)
        #     for files in os.listdir(result_path):
        #         if files.lower().endswith('.wav'):
        #             result = os.path.join(result_path, files)
        #             zipf.write(result, os.path.basename(result))

        # print(zip_path, name)
        # for file in os.listdir(zip_path):
        #     print(file)
        
        shutil.make_archive(zip_path,'zip',zip_path)

        delete_path = os.path.join(path)

        
        return zip_path, zip_name, delete_path

        
    
    # 음원 합성
    def mix(self, zip_file):

        path = os.path.join(self.mr_dir, self.mr_id)
        os.makedirs(path, exist_ok=True) 

        copy_path = os.path.join(path, zip_file.filename)

        with open(copy_path, "wb") as f:
            shutil.copyfileobj(zip_file.file, f)

        shutil.unpack_archive(copy_path, path, "zip")
        os.remove(copy_path)

        mrs = []
        for wavs in os.listdir(path):
            wavs = os.path.join(path, wavs)
            mrs.append(AudioSegment.from_wav(wavs))
            
        result_audio = mrs[0]
        for audio in mrs[1:]:
            result_audio = result_audio.overlay(audio)

        answer_file_name = "mixed_file.mp3"
        result_path = os.path.join(path,answer_file_name)
        result_audio.export(result_path, format="mp3")

        return result_path, path
