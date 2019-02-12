# syleeMusicPlayer_backup
```
로컬 PC에서 동작하는 MP3 플레이어 앱에 대한 소스코드입니다. 
freezing python desktop application with pyinstaller
```
```
[설치 및 사용 가이드]
git clone https://github.com/sssssqew/syleeMusicPlayer_backup.git
syleeMusicPlayer(noDBVersion_window7_32_singlefile) 폴더로 이동
dist 폴더로 이동
syleeMusicPlayer 응용프로그램 실행
[Add]버튼으로 음원 추가
```

<center>
<img src="https://user-images.githubusercontent.com/9676553/52618132-4b752b00-2ee1-11e9-8e65-ede4f8bf829a.PNG" width="40%">
<img src="https://user-images.githubusercontent.com/9676553/52618134-4e701b80-2ee1-11e9-9ca2-752b5c1f9081.PNG" width="40%">
<center>
  
1. 파이썬 3 설치 (3.5.2) - easy_install, pip3 등은 자동설치 됨(확인)
```
python, vlc 경로를 환경변수 시스템변수에 등록하기 (window)
```
2. 프로젝트에 필요한 패키지나 모듈 설치 (pip3 requirments.txt 사용)
```
pip3 install pyinstaller
pip3 install pillow (PIL : Python Imaging Library)
pip3 install python-vlc (vlc media player 32비트/64비트 구분 설치)
pip3 install mutagen (mp3 metadata 추출)
```
3. 실행파일 생성하기 전에 python IDLE나 sublime등으로 잘 실행되는지 확인(디버깅)
4. pyinstaller spec 설정하기 (hiddenimports, pathex)
```
hiddenimports : 패키지나 모듈
pathex : python site-package 외부에 위치하는 패키지나 모듈 경로 추가
```
5. pyinstaller 실행하기
```
pyinstaller -w syleeMusicPlayer.spec (-w : GUI앱)
pyinstaller -w --noconsole syleeMusicPlayer.spec (--noconsole : 커맨드창 제거)
pyinstaller -w --noconsole --onefile syleeMusicPlayer.py (--onefile : 하나의 exe만 생성)
pyinstaller --debug syleeMusicPlayer (--debug : 커맨드창에서 실행하여 에러 확인)
```
6. dist, build 폴더 생성 확인
7. vlc 관련 폴더와 파일을 실행파일이 위치한 폴더 내에 추가하기 (window)
```
plugins
libvlc.dll
libvlc.dylib
libvlccore.dll
```
```
PS. 하나의 exe 파일을 생성하는 경우 window xp/7에서만 제대로 실행됨 
PS. 클릭으로 EXE를 실행하기 전에 Command창에서 미리 실행해서 오류 메세지 확인 
PS. 설치 패키지는 가능한 Virtual환경에서 pip3 requirements.txt로 관리하기
PS. 대부분의 패키지나 모듈은 site-packages 폴더 내에 존재함
PS. main libvlc error: No plugins found! Check your VLC installation (Linux)
sudo ln -s / /livefs.squashfs
export VLC_PLUGIN_PATH=/usr/lib/vlc/plugins/
PS. ImportError: No module named _tkinter_finder (Linux)
spec 파일 hidden_imports에 'PIL._tkinter_finder' 추가 
```

