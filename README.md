## MQTT Tester


### 1) 2021.11.03 09:01
   - 첫 번째 푸쉬
   - 대략적인 MQTT 연결 기능 구현

### 2) 2021.11.05 16:31
   - 두 번째 푸쉬
   - Payload 프린트 기능 구현
   - MQTT.fx를 사용하면서 불편하다 생각이 들어서 그냥 만든 테스터임
   - 최소한의 기본적인 기능만 구현
   - Qos 부분은 아직 없음
   - 현재 기능이 여기까지 업데이트는 본인이 필요하다 싶으면 할 생각

### 3) 2021.11.09 11:01
   - 버그가 많다
   - Hex 형식이 맞지 않는 msg를 전송하는 경우 예외처리
   - Subscribe 목록에 중복되는 부분 수정
   - Disconnect flags가 1일때는 데이터 유지 (유저가 직접 끊는 것이 아닌 오류로 인한 잠깐에 끊김)
   - Subscribe clear 기능 추가
   - Unsubscribe 기능 추가
   - UI 변경

### 기능
   - 나중에... 별거 없음... 아래 영상 한번 보면 이해될 듯
   - Config/config copy.ini 파일 -> Config/config.ini 파일명 변경해야함
   - 아래 영상은 변경 예정

   <img width="70%" src="https://user-images.githubusercontent.com/38420069/140478811-d32bb0a5-a6f1-4ea0-a06d-c3d5a2ba21f1.gif"/>