# emergency 메시지를 구독
# monitoring 메시지를 구독토픽 "DSChos/electrocardiogram/danger/심전도
# monitoring 메시지를 구독토픽 DSChos/환자ID/electrocardiogram/혈압
# monitoring 메시지를 구독토픽  DSChos/환자ID/electrocardiogram/산소포화도
# monitoring 메시지를 구독토픽  DSChos/환자ID/electrocardiogram/Emergency
# 제어메시지에 따라 문제가 있는 건강정보에 따라서 조치사항을 출력하여 보여줌 

import paho.mqtt.client as mqtt
import re
def f_numbers(string): #payload 호실 정보 추출 함수 
    numbers = re.findall(r'\d+', string)
    if len(numbers) > 0:
        return numbers[0]
    else:
        return None
    
def extract_letters(string): #payload 이름 정보 추출 함수 
    letters = ""
    for char in string:
        if char.isalpha():
            letters += char
    return letters


def on_connect(client, userdata, flags, re):
    print("Connected with result code " + str(re));
    subClient.subscribe("DSChos/electrocardiogram/danger/+" );
    subClient.subscribe("DSChos/bloodpressur/danger/+");
    subClient.subscribe("DSChos/oxygensaturation/danger/+" );

def on_message(client, userdata, msg):
    print(msg.topic + msg.payload.decode("utf-8"));
    
    if(msg.topic.startswith("DSChos/electrocardiogram/danger/")):
        ele_payload = str(msg.payload.decode('utf-8'));
        
        ele_name = extract_letters(ele_payload);
        ele_room = f_numbers(ele_payload);
        
        print(ele_room + "호실 " + ele_name + "환자 심전도 문제로 아래 조치사항을 따르십시오\n");
        print("심전도 이상 발생 CPR 및 자동제세동기 실시\n조치후 의료진 도착전까지 대기");
        
    if(msg.topic.startswith("DSChos/bloodpressur/danger/")):
        blo_payload = str(msg.payload.decode('utf-8'));
        
        blo_name = extract_letters(blo_payload);
        blo_room = f_numbers(blo_payload);
        
        print(blo_room + "호실 " + blo_name + "환자 혈압 문제로 아래 조치사항을 따르십시오\n");
        print("혈압약 복용 \n조치후 의료진 도착전까지 대기");
        
    if(msg.topic.startswith("DSChos/oxygensaturation/danger/")):
        oxy_payload = str(msg.payload.decode('utf-8'));
        
        oxy_name = extract_letters(oxy_payload);
        oxy_room = f_numbers(oxy_payload);
        
        print(oxy_room + "호실 " + oxy_name + "환자 혈압 문제로 아래 조치사항을 따르십시오\n");
        print("응급 산소 투여 \n조치후 의료진 도착전까지 대기");



subClient = mqtt.Client();
subClient.on_connect = on_connect;
subClient.on_message = on_message;
subClient.connect("localhost");


try:
    subClient.loop_forever();
except KeyboardInterrupt:
    print("Finished!");
    subClient.unsubscribe(['DSChos/electrocardiogram/danger/+', 'DSChos/bloodpressur/danger/+', 'DSChos/oxygensaturation/danger/+']);
    subClient.disconnect();
    
