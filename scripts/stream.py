import vlc
import time

url = 'http://streaming.enantena.com:8000/radiovoltrega128.mp3'
#define VLC instance
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

#Define VLC player
player=instance.media_player_new()

#Define VLC media
media=instance.media_new(url)

#Set player media
player.set_media(media)

#Play the media
player.play()


#Sleep for 5 sec for VLC to complete retries.
time.sleep(5)
#Get current state.
state = str(player.get_state())

#Find out if stream is working.
if state == "vlc.State.Error" or state == "State.Error":
    print 'Error al streaming'
    player.stop()
else:
    print 'Streaming correcte'
    player.stop()
