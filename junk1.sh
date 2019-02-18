ffmpeg -loglevel verbose -i http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/uk/sbr_high/ak/bbc_radio_three.m3u8 -t 00:00:10.0 -c copy -bsf:a aac_adtstoasc /home/user1/radiotext_TD/output/audio_45s_segments/UK_BBC_Radio_4_FM/b/a41.mp4 2>&1 |grep ".ts"
sleep 10
ffmpeg -loglevel verbose -i http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/uk/sbr_high/ak/bbc_radio_three.m3u8 -t 00:00:10.0 -c copy -bsf:a aac_adtstoasc /home/user1/radiotext_TD/output/audio_45s_segments/UK_BBC_Radio_4_FM/b/a51.mp4 2>&1 |grep ".ts"
sleep 10
ffmpeg -loglevel verbose -i http://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/uk/sbr_high/ak/bbc_radio_three.m3u8 -t 00:00:10.0 -c copy -bsf:a aac_adtstoasc /home/user1/radiotext_TD/output/audio_45s_segments/UK_BBC_Radio_4_FM/b/a61.mp4 2>&1 |grep ".ts"
