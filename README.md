<H1>codeMarble


<H3>codeMarble 이란?
<H6>소프트웨어(알고리즘) 학습 방법에는 여러 가지 방법이 있습니다. 가장 대표적인 방법은 알고리즘 채점 사이트로 학생이 제출한 코드에 대한 실행 시간, 사용 메모리 등의 정보를 제공합니다. 하지만 이러한 방법은 학생들이 스스로 자기의 코드를 판단하기 어려우며, 단순한 문제풀이로 전락할 수 있습니다. 
<H6>그래서 codeMarble은 단순 알고리즘 문제가 아닌 보드게임을 해결하기 위한 알고리즘을 설계, 구현하고 다른 사람과의 알고리즘과 대결하는 방식을 통해 승/패라는 보다 직관적인 결과를 학생들에 제공합니다. 
<H6>또한 게임을 통해 보다 재밌게 알고리즘 학습에 접근하고 지루하지 않게 학습을 진행할 수 있습니다.



<H3>사용 전 유의사항


<H3>제약 사항


<H3>사용방법
<H4>1. 설치방법 및 실행
<H6> 1. codeMarble_Web clone
<H6> 2. Redis 설치/실행
<H6> 3. installs.sh 파일 실행
<H6> 4. backendCelery에서 celery실행 (celery -A celeryFile worker --loglevel=info)
<H6> 5. python runserver.py (관리자 권한)
<H6> * 추후 docker 이미지 지원 예정 (문제 발생 시 DB와 properties파일 설정을 확인)

<H4>2. 관리자 사용방법
<H6> 1. 초기 ID/Password는 master이다.
<H6> 2. .../admin을 쳐서 페이지에 접근한다.
<H6> 3. 부관리자 등록은 ID로 등록해야 하며, 부관리자의 모든 사용자의 코드를 확인할 수 있는 권한을 가진다.

<H4>3. 일반 사용자 사용방법
<H6>세부 사용방법은 웹사이트에 About탭에서 추후 제공.


<H3>권장 시스템 사양
<H4>1. 운영체제
<H6>centOS를 비롯한 모든 리눅스OS, Windows에서는 Docker를 사용하면 가능합니다.
<H7>(현재 installs파일은 redhat계열만 지원합니다.)

<H4>2. 최소사양
<H6>CPU 3core, RAM 2GB, HDD 8GB

<H4>3. 권장사양
<H6>CPU 4core, RAM 3GB, HDD 10GB 이상
