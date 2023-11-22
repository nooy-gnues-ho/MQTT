# 환자의 건강정보를 자동으로 감지 할수 없으므로 사용자가 입력으로 대신함
# 입력받는 부분은 탈착 입력전까지 계속하여 반복함
# 센서탈착, 비상호출 ,환자ID 중 입력받음 (건강정보 입력 1,  비상호출 2,  임상증상 3 : ") 
# 환자ID 선택시 환자호실과 이름 출력함
# 환자ID 선택후 심전도, 혈압, 산소포화도 각각 입력 
# 입력받은 건강정보 데이터를 발행하는 MQTT 클라언트 기능 구현
# 건강정보 발행 토픽 DSChos/electrocardiogram/환자ID
# 건강정보 발행 토픽 DSChos/Bloodpressur/환자ID
# 건강정보 발행 토픽 DSChos/oxygensaturation/환자ID
# 비상호출 발행 토픽 DSChos/Emergency/환자
# 
import paho.mqtt.client as mqtt

ID=["101HongGilDong", "202LimKkeokJeong", "403OhSeungYun", "505ParkJiHye", "610YuJinChoe"]; #환자 정보 저장 변수
Clinicalsymptoms=["기침", "오한", "두통", "후각/미각손실", "식욕감소", "어지러움", "호흡곤란", "근육통", "인후통", "피로", "가래", "설사", "콧물/코막힘", "기타"]; #임상증상 목록
EPerID=[]; # 긴급상황버튼 클릭시 환자정보 저장 변수 
PerID=0; # 환자선택변수 
etc=[]; # 기타입력저장 변수 
mqttc = mqtt.Client();
mqttc.connect("localhost");
mqttc.loop_start();

try:
    while True:
        print("---------------------------------------------");
        com = int(input("센서탈착(종료) 0, 환자ID 1 : "));
        print("---------------------------------------------");
        if com == 0:
            print("센서탈착(종료)");
            break;
        elif com == 1:#건강정보 입력 
            print("---------------------------------------------");
            print(ID);
            print("---------------------------------------------");
            PerID = int(input("환자 선택 : "));
            comm = int(input("건강정보 입력 1,  비상호출 2,  임상증상 3 : "));
            
            if comm == 1: #건강정보 입력
                while 1:
                    electrocardiogram = str(input("심박수 입력 : "));
                    if electrocardiogram == 'x':
                        break;
                    bloodpressur = str(input("혈압 입력 : "));
                    oxygensaturation = str(input("산소포화도 입력 : "));
                    
                    eid_eh=str(ID[PerID])+electrocardiogram
                    bid_eh=str(ID[PerID])+bloodpressur
                    oid_eh=str(ID[PerID])+oxygensaturation
                    
                    infot = mqttc.publish("DSChos/electrocardiogram/",eid_eh);
                    infot.wait_for_publish();
                    infot = mqttc.publish("DSChos/bloodpressur/",bid_eh);
                    infot.wait_for_publish();
                    infot = mqttc.publish("DSChos/oxygensaturation/",oid_eh);
                    infot.wait_for_publish();
                                                      
            elif comm == 2:  #비상호출 처리
                EPerID = ID[PerID];
                infot = mqttc.publish("DSChos/Emergency/",str(EPerID));
                infot.wait_for_publish();
            elif comm == 3:
                print("\n-------------------------");
                print("\n-------, 부터 입력-------");
                for i in range(14):
                    print(i," : ",Clinicalsymptoms[i]);
                print("\n-------------------------");
                CS=str(input("0 ~ 13번 중 해당되는 증상 모두 체크해 주세요 : "));

                
                if CS=='13':
                    print("\n-------띄어쓰기 없이  입력-------");
                    etc=str(input("기타사항을 입력해주시기 바랍니다 : "));
                    CS_etc=str(ID[PerID])+etc;
                    infot = mqttc.publish("DSChos/Clinicalsymptomse/",CS_etc);
                    infot.wait_for_publish();
                    CS=0;
                else:
                    CS_eh=str(ID[PerID])+CS
                    infot = mqttc.publish("DSChos/Clinicalsymptoms/",CS_eh);
                    infot.wait_for_publish();                    
            
        else: 
            print("옵션을 다시 선택해주세요.");
            continue;



except KeyboardInterrupt:
    print("강제 종료");
    mqttc.loop_stop();
    mqttc.disconnect();
