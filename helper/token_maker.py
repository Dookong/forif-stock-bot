import commons
import msg_sender
import time

time_info = time.gmtime()
m_hour = time_info.tm_hour
    

commons.make_new_token("r")
commons.make_new_token("v")

#8시가 맞으면 메세지 전송
if m_hour == 23:
    msg_sender.send_msg("토큰 발급 완료!")
    
# msg_sender.send_msg("yolo")