# monitoring 메시지를 구독
# monitoring 메시지를 구독토픽 DSChos/electrocardiogram/환자ID
# monitoring 메시지를 구독토픽 DSChos/Bloodpressur/환자ID
# monitoring 메시지를 구독토픽 DSChos/oxygensaturation/환자ID
# monitoring 메시지를 구독토픽 DSChos/Emergency/환자ID
# monitoring 메시지를 발행토픽 "DSChos/electrocardiogram/danger/심전도
# monitoring 메시지를 발행토픽 DSChos/환자ID/electrocardiogram/혈압
# monitoring 메시지를 발행토픽  DSChos/환자ID/electrocardiogram/산소포화도
# 제어메시지에 따라 각 건강정보를 출력하여 긴급상황임을 알려줌 
import paho.mqtt.client as mqtt
import re
counte=0;
countb=0;
counto=0;
oxy_name_s="a";
ele_name_s="a";
blo_name_s="a";

#발행관련 
pubClient = mqtt.Client();
pubClient.connect("localhost");
pubClient.loop_start();



def b_numbers(string): #payload 건강정보값 추출 함수 
    numbers = ""
    found_alpha = False
    for char in string:
        if char.isalpha():
            found_alpha = True
        elif found_alpha and char.isdigit():
            numbers += char
        elif found_alpha and not char.isdigit():
            break
    return int(numbers) if numbers else 0

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
    subClient.subscribe("DSChos/electrocardiogram/+" );
    subClient.subscribe("DSChos/bloodpressur/+");
    subClient.subscribe("DSChos/oxygensaturation/+" );
    subClient.subscribe("DSChos/Emergency/+" );

def on_message(client, userdata, msg):
    global counte
    global countb
    global counto
    global ele_name_s
    global blo_name_s
    global oxy_name_s
    
    
    if(msg.topic.startswith("DSChos/electrocardiogram/")):
        ele_payload = str(msg.payload.decode('utf-8'));
        ele_h = b_numbers(ele_payload);
        ele_name = extract_letters(ele_payload);
        ele_room = f_numbers(ele_payload);
       
        if((ele_h <= 60) | (ele_h >= 160)):
            if(ele_name != ele_name_s):
                counte=0;
            counte+=1;
            ele_name_s=ele_name;
            if(counte > 5):
                print(ele_room + "호실 " + ele_name + " 심전도 문제 발생 확인바람.");
                infot = pubClient.publish("DSChos/electrocardiogram/danger/", ele_payload);
                infot.wait_for_publish();
                counte = 0;
                                
    if msg.topic.startswith("DSChos/bloodpressur/"):
        blo_payload = str(msg.payload.decode('utf-8'));
        blo_h = b_numbers(blo_payload);
        blo_name = extract_letters(blo_payload);
        blo_room = f_numbers(blo_payload);
        
        if((blo_h <= 80) | (blo_h >= 120)):
            if(blo_name != blo_name_s):
                countb=0;
            countb+=1;
            blo_name_s=blo_name;
            if(countb > 5):
                print(blo_room + "호실 " + blo_name + " 혈압 문제 발생 확인바람.");
                infot = pubClient.publish("DSChos/bloodpressur/danger/", blo_payload);
                infot.wait_for_publish();
                countb = 0;
                                
    if(msg.topic.startswith("DSChos/oxygensaturation/")):
        oxy_payload = str(msg.payload.decode('utf-8'));
        oxy_h = b_numbers(oxy_payload);
        oxy_name = extract_letters(oxy_payload);
        oxy_room = f_numbers(oxy_payload);
        
        if(oxy_h < 95) | (oxy_h > 100):
            if(oxy_name != oxy_name_s):
                countb=0;
            counto+=1;
            oxy_name_s=oxy_name;
            if(counto > 5):
                print(oxy_room + "호실 " + oxy_name + " 산소포화도 문제 발생 확인바람.");
                infot = pubClient.publish("DSChos/oxygensaturation/danger/", oxy_payload);
                infot.wait_for_publish();
                counto = 0;
                                
    if msg.topic.startswith("DSChos/Emergency/"):
        emr = str(msg.payload.decode('utf-8'));
        if len(emr) >= 1:
            room = f_numbers(emr);
            name = extract_letters(emr);
            print(room + "호실 " + name + " 환자 긴급상황입니다.");        
#구독관련
subClient = mqtt.Client();
subClient.on_connect = on_connect;
subClient.on_message = on_message;
subClient.connect("localhost");


try:
    subClient.loop_forever();
except KeyboardInterrupt:
    print("Finished!");
    subClient.unsubscribe(['DSChos/electrocardiogram/+', 'DSChos/bloodpressur/+', 'DSChos/oxygensaturation/+', 'DSChos/Emergency/+']);
    subClient.disconnect();
    
    pubClient.loop_stop();
    pubClient.disconnect();
                  

