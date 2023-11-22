# monitoring 메시지를 구독
# monitoring 메시지를 구독토픽 DSChos/Clinicalsymptoms/+
# 임상증상에 따라 회진시 도움을 줄수 있도록 함 
import paho.mqtt.client as mqtt
import re

def split_payload_etc(payload):
    sentence = ""

    # 한글 문장 추출
    sentence_match = re.search(r"[\uac00-\ud7a3]+", payload)
    if sentence_match:
        sentence = sentence_match.group()

    return sentence


def f_numbers(string): #payload 호실 정보 추출 함수 
    numbers = re.findall(r'\d+', string)
    if len(numbers) > 0:
        return numbers[0]
    else:
        return None
    
def extract_letters(string): #payload 이름 정보 추출 함수 
    name = re.findall(r'[a-zA-Z]+', string)
    name_string = ' '.join(name)
    return name_string

def extract_numbers(payload):  # payload 임상증상 추출 
    numbers = []
    parts = payload.split(',')
    for part in parts:
        part = part.strip() 
        
        if part.isdigit():  
            numbers.append(part)  
    
    numbers_string = ','.join(numbers)  
    return numbers_string


Clinicalsymptoms=["기침", "오한", "두통", "후각/미각손실", "식욕감소", "어지러움", "호흡곤란", "근육통", "인후통", "피로", "가래", "설사", "콧물/코막힘", "기타"];
check=[];
cl=[];
def on_connect(client, userdata, flags, re):
    print("Connected with result code " + str(re));
    subClient.subscribe("DSChos/Clinicalsymptoms/+" );
    subClient.subscribe("DSChos/Clinicalsymptomse/+" );

def on_message(client, userdata, msg):
    global check
    global cl
    
    print(msg.topic + msg.payload.decode("utf-8"));
    
    if(msg.topic.startswith("DSChos/Clinicalsymptoms/")): # 그외 선택시 
        Clinicalsymptoms_payload = str(msg.payload.decode("utf-8"));
        
        cl_room = f_numbers(Clinicalsymptoms_payload);
        cl_name = extract_letters(Clinicalsymptoms_payload);
        cl = extract_numbers(Clinicalsymptoms_payload);
        
        print(cl_room + "호실 " + cl_name + " 회진시 임상증상확인바람.");
        print("임상증상 : ");
        check = [int(item) for item in cl.split(',')];
        for i in check:
            print(Clinicalsymptoms[i]);
        
    if(msg.topic.startswith("DSChos/Clinicalsymptomse/")):# 13번 선택시
        etc_payload = str(msg.payload.decode("utf-8"));
        
        etc_room = str(f_numbers(etc_payload));
        etc_name = str(extract_letters(etc_payload));
        etc_etc = split_payload_etc(etc_payload)
        
        print(etc_room + "호실 " + etc_name + " 회진시 임상증상확인바람.");
        print("임상증상(기타) : " + etc_etc);


        
#구독관련
subClient = mqtt.Client();
subClient.on_connect = on_connect;
subClient.on_message = on_message;
subClient.connect("localhost");


try:
    subClient.loop_forever();
except KeyboardInterrupt:
    print("Finished!");
    subClient.unsubscribe(['DSChos/Clinicalsymptoms/+','DSChos/Clinicalsymptomse/+']);
    subClient.disconnect();
                  

