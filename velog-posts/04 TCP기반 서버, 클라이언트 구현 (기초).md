<p>※본 내용은 열혈 TCP/IP 내용을 참고 하였으며, 리눅스 환경 기반으로 테스트를 진행하였습니다.</p>
<h2 id="tcpip-프로토콜">TCP/IP 프로토콜</h2>
<p>일단 우리가 TCP와 IP를 알아보기 전에 네트워크 계층에서 각각 어디에 위치해 있는지 살펴보자
<img alt="" src="https://velog.velcdn.com/images/parang12/post/103bb950-dab7-47b3-8223-f9bad085b8c3/image.png" /></p>
<p>위의 사진이 ISO7계층이라고 부르며, 우리가 인터넷을 할때 정보가 이렇게 이동한다고 생각하면 된다.</p>
<p>그 중 IP는 네트워크 계층에 TCP, UDP는 전송 계층에 속해 있다고 보면 된다.</p>
<p>짧게 설명하자면 네트워크 계층에서는 여러 네트워크를 공유하여 목적지 까지 전달하는 기능을 하고, 전송계층에서는 응용프로그램에서 응용프로그램까지 전달한다고 보면된다. </p>
<pre><code>e.g. 
택배로 예시를 들자면 기사님(네트워크계층)이 택배상자를 우리집까지 배달해 주면 내가(전송계층) 내 방까지 가져오는 일이라고 생각하면 쉽다</code></pre><p>TCP와 UDP에 대해서 더욱 자세히 알고 싶다면 전전 포스팅인 소케의 타입 및 프로토콜에 자세히 설명을 해놨으니 참고하면 이해가 더욱 쉽다.</p>
<hr />
<h2 id="tcp-기반-서버-클라이언트-구현">TCP 기반 서버, 클라이언트 구현</h2>
<p>TCP 기반 서버에서 기본적인 함수 호출 순서를 알아보자</p>
<table>
<thead>
<tr>
<th><strong>순서</strong></th>
<th><strong>서버 (Server / 맛집)</strong></th>
<th><strong>클라이언트 (Client / 손님)</strong></th>
<th><strong>설명</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>1</strong></td>
<td><strong>socket()</strong></td>
<td><strong>socket()</strong></td>
<td><strong>소켓 생성</strong>: 통신을 위한 도구(전화기) 마련</td>
</tr>
<tr>
<td><strong>2</strong></td>
<td><strong>bind()</strong></td>
<td>-</td>
<td><strong>주소 할당</strong>: 서버의 IP와 Port 번호 설정</td>
</tr>
<tr>
<td><strong>3</strong></td>
<td><strong>listen()</strong></td>
<td>-</td>
<td><strong>대기 상태</strong>: 손님을 받을 수 있는 상태로 전환</td>
</tr>
<tr>
<td><strong>4</strong></td>
<td>-</td>
<td><strong>connect()</strong></td>
<td><strong>연결 요청</strong>: 서버 주소로 전화를 걸음 (3-Way Handshake)</td>
</tr>
<tr>
<td><strong>5</strong></td>
<td><strong>accept()</strong></td>
<td>-</td>
<td><strong>연결 허용</strong>: 대기 중인 요청을 수락 (실제 통신용 소켓 생성)</td>
</tr>
<tr>
<td><strong>6</strong></td>
<td><strong>read() / write()</strong></td>
<td><strong>write() / read()</strong></td>
<td><strong>데이터 송수신</strong>: 서로 대화를 주고받음</td>
</tr>
<tr>
<td><strong>7</strong></td>
<td><strong>close()</strong></td>
<td><strong>close()</strong></td>
<td><strong>연결 종료</strong>: 통신을 마치고 소켓 자원 반납</td>
</tr>
</tbody></table>
<p>이제 우리가 처음시간에 봤던 <code>Hello world.c</code>프로그램으로 어떻게 되는지 한번 봐보자</p>
<h3 id="서버-코드">서버 코드</h3>
<pre><code class="language-c">int main(int argc, char **argv) {
    int serv_sock; 
    int clnt_sock; 

    struct sockaddr_in serv_addr; 
    struct sockaddr_in clnt_addr; 
    socklen_t clnt_addr_size; 

    char message[] = &quot;Hello World!\n&quot;;

    if (argc != 2) { 
        printf(&quot;Usage: %s &lt;port&gt;\n&quot;, argv[0]);
        exit(1);
    }


    // [STEP 1] 소켓 생성 (Socket Creation)
    serv_sock = socket(PF_INET, SOCK_STREAM, 0);
    if (serv_sock == -1) 
        error_handling(&quot;socket() error&quot;);


    //[STEP 2] 주소 및 포트 설정 (Address Setting)
    memset(&amp;serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY); 
    serv_addr.sin_port = htons(atoi(argv[1]));     


     //[STEP 3] 소켓 주소 할당 (Bind)
    if (bind(serv_sock, (struct sockaddr*)&amp;serv_addr,//형변환
     sizeof(serv_addr)) == -1) 
        error_handling(&quot;bind() error&quot;);
//-------------------------------------------------------------------
// int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
// sockfd: 주소를 할당할 파일 디스크립터
// struct sockaddr *addr: 소켓 주소 포인터, 이곳에서는 serv_addr(IPv4)타입을 강제로 공용 소켓 주소 포인터로 형변환을 사용해서 넣어줌 (함수 원형의 규격을 맞추기 위해서)
//sizeof: 소켓 구조체의 전체크기 (오류를 방직하기 위해서)
//--------------------------------------------------------------------
    //[STEP 4] 연결 요청 대기 (Listen)
    if (listen(serv_sock, 5) == -1)
        error_handling(&quot;listen() error&quot;);
//-----------------------------------------------------
// int listen(int sockfd, int backlog)
// sockfd: 파일 디스크립터 
// backlog: 연결 요청 대기 큐의 크기, 서버가 너무 바빠서 아직 accept()를 못할때 튕기지 않고 대기 해주게 할 수 있음
//---------------------------------------

     //[STEP 5] 연결 수락 및 통신 소켓 생성 (Accept)
    clnt_addr_size = sizeof(clnt_addr);
    clnt_sock = accept(serv_sock, (struct sockaddr*)&amp;clnt_addr, &amp;clnt_addr_size);
    if (clnt_sock == -1)
        error_handling(&quot;accept() error&quot;);
//-----------------------------------------------------------------
//int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
// sockfd: 파일 디스크립터
// struct sockaddr *addr: 아까는 나의 주소였다면, 지금에서는 Client(손님)의 주소정보
// *addrlen: 구조체 크기가 담긴 변수의 주소(accept는 값을 써넣야 해서 포인터 사용)
//------------------------------------------------------------------

    //[STEP 6] 데이터 송수신 (Write/Read)
    write(clnt_sock, message, sizeof(message));

    //[STEP 7] 소켓 폐쇄 (Close)
    close(clnt_sock);
    close(serv_sock); 

    return 0;
}
</code></pre>
<h3 id="클라이언트쪽-코드">클라이언트쪽 코드</h3>
<pre><code class="language-c">// [STEP 1] 소켓 생성 (Socket)
sock = socket(PF_INET, SOCK_STREAM, 0);
if (sock == -1)
    error_handling(&quot;socket() error&quot;);

// [STEP 2] 대상 서버 주소 설정 (Addressing)
memset(&amp;serv_addr, 0, sizeof(serv_addr));
serv_addr.sin_family = AF_INET;
serv_addr.sin_addr.s_addr = inet_addr(argv[1]);
serv_addr.sin_port = htons(atoi(argv[2]));

// [STEP 3] 연결 요청 (Connect)
if(connect(sock, (struct sockaddr*)&amp;serv_addr, sizeof(serv_addr)) == -1)
    error_handling(&quot;connect() error!&quot;);

// int connect(int sockfd, const struct sockaddr *serv_addr, socklen_t addrlen);
// sockfd: 서버로 전화를 걸 내 소켓의 파일 디스크립터
// struct sockaddr *serv_addr: 찾아갈 서버(맛집)의 주소 정보 포인터, 형변환 필수!
// addrlen: 서버 주소 구조체의 전체 크기 (커널이 어디까지 읽을지 알려주는 오류 방지용)
// ------------------------------------------------------------------

// [STEP 4] 데이터 수신 (Read)
str_len = read(sock, message, sizeof(message) - 1);
if(str_len == -1)
    error_handling(&quot;read() error!&quot;);

// read(int fd, void *buf, size_t nbytes);
// fd: 데이터를 읽어올 소켓의 파일 디스크립터
// buf: 읽어온 데이터를 저장할 버퍼의 주소
// nbytes: 읽어올 데이터의 최대 바이트 수
// ------------------------------------------------------------------

// [STEP 5] 소켓 폐쇄 (Close)
printf(&quot;Message from server : %s\n&quot;, message);
close(sock);</code></pre>
<hr />
<h2 id="lterative-서버의-구현">lterative 서버의 구현</h2>
<p>lterative 서버를 구현하기 위해서는 lterative가 뭔지 알아야 한다 </p>
<p>-&gt;이전의 코드는 클라이언트와 단 한 번의 데이터 송수신(Single Transaction) 후 종료되었으나, lterative  서버는 while 루프를 통해 한 클라이언트와 세션을 지속적으로 유지한다. 또한, 해당 클라이언트와 연결이 종료되더라도 서버가 꺼지지 않고 다음 대기 중인 클라이언트를 반복해서 수락하는 구조를 가진다</p>
<p><img alt="" src="https://velog.velcdn.com/images/parang12/post/56e90872-b746-44de-bd55-0d8d9e775694/image.png" /></p>
<p>이제 lterative서버 예시를 보자</p>
<h3 id="echo_serverc">echo_server.c</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;string.h&gt;
#include &lt;unistd.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;arpa/inet.h&gt;
#include &lt;sys/socket.h&gt;

#define BUF_SIZE 1024
void error_handling(char *message);

int main(int argc, char *argv[])
{
    int serv_sock, clnt_sock;
    char message[BUF_SIZE];
    int str_len, i;
    struct sockaddr_in serv_adr, clnt_adr;
    socklen_t clnt_adr_sz;

    if(argc != 2) {
        printf(&quot;Usage : %s &lt;port&gt;\n&quot;, argv[0]);
        exit(1);
    }

    serv_sock = socket(PF_INET, SOCK_STREAM, 0);
    if(serv_sock == -1)
        error_handling(&quot;socket() error&quot;);

    memset(&amp;serv_adr, 0, sizeof(serv_adr));
    serv_adr.sin_family = AF_INET;
    serv_adr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_adr.sin_port = htons(atoi(argv[1]));

    if(bind(serv_sock, (struct sockaddr*)&amp;serv_adr, sizeof(serv_adr)) == -1)
        error_handling(&quot;bind() error&quot;);

    if(listen(serv_sock, 5) == -1)
        error_handling(&quot;listen() error&quot;);

    clnt_adr_sz = sizeof(clnt_adr);

    for(i=0; i&lt;5; i++) // 최대 5개의 클라이언트 접속 허용 (연결 -&gt; 데이터 송수신 -&gt; 연결 종료 -&gt; 연결 ... 5번 반복)
    {
        clnt_sock = accept(serv_sock, (struct sockaddr*)&amp;clnt_adr, &amp;clnt_adr_sz);
        if(clnt_sock == -1)
            error_handling(&quot;accept() error&quot;);
        else
            printf(&quot;Connected client %d \n&quot;, i+1);

        while((str_len = read(clnt_sock, message, BUF_SIZE)) != 0)
            write(clnt_sock, message, str_len);

        close(clnt_sock);
    }

    close(serv_sock);
    return 0;
}

void error_handling(char *message)
{
    fputs(message, stderr);
    fputc('\n', stderr);
    exit(1);
}</code></pre>
<h3 id="echo_clientc">echo_client.c</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;
#include &lt;unistd.h&gt;
#include &lt;arpa/inet.h&gt;
#include &lt;sys/socket.h&gt;

#define BUF_SIZE 1024
void error_handling(char *message);

int main(int argc, char *argv[])
{
    int sock;
    char message[BUF_SIZE];
    int str_len;
    struct sockaddr_in serv_adr;

    if(argc != 3) {
        printf(&quot;Usage : %s &lt;IP&gt; &lt;port&gt;\n&quot;, argv[0]);
        exit(1);
    }

    sock = socket(PF_INET, SOCK_STREAM, 0);
    if(sock == -1)
        error_handling(&quot;socket() error&quot;);

    memset(&amp;serv_adr, 0, sizeof(serv_adr));
    serv_adr.sin_family = AF_INET;
    serv_adr.sin_addr.s_addr = inet_addr(argv[1]);
    serv_adr.sin_port = htons(atoi(argv[2]));

    if(connect(sock, (struct sockaddr*)&amp;serv_adr, sizeof(serv_adr)) == -1)
        error_handling(&quot;connect() error&quot;);
    else
        printf(&quot;Connected........... \n&quot;); // 연결 성공 메시지

    while(1) // 무한 루프를 사용하여 메시지를 계속해서 입력받고 서버로 전송
    {
        fputs(&quot;Input message(Q to quit): &quot;, stdout);  // 사용자에게 메시지 입력을 요청하는 프롬프트 출력
        fgets(message, BUF_SIZE, stdin);

        if(!strcmp(message,&quot;q\n&quot;) || !strcmp(message,&quot;Q\n&quot;)) // 사용자가 'q' 또는 'Q'를 입력하면 루프를 종료
            break;

        write(sock, message, strlen(message)); // 입력된 메시지를 서버로 전송
        str_len = read(sock, message, BUF_SIZE-1); 
        message[str_len] = 0;
        printf(&quot;Message from server: %s&quot;, message);
    }

    close(sock);
    return 0;
}

void error_handling(char *message)
{
    fputs(message, stderr);
    fputc('\n', stderr);
    exit(1);
}</code></pre>
<hr />
<h2 id="요약">요약</h2>
<h3 id="tcpip-프로토콜-계층">TCP/IP 프로토콜 계층</h3>
<ul>
<li><strong>IP (네트워크 계층):</strong>  여러 네트워크를 공유하여 목적지 까지 경로 부착</li>
<li><strong>TCP/UDP (전송 계층):</strong> 응용프로그램에서 응용프로그램까지 전달하는 경로 부착</li>
</ul>
<blockquote>
<p><strong>e.g. 택배 예시:</strong> 기사님(IP)이 집 앞까지 배달하면, 내가(TCP) 방으로 가져옴!</p>
</blockquote>
<h3 id="tcp-서버클라이언트-함수-호출-순서">TCP 서버/클라이언트 함수 호출 순서</h3>
<table>
<thead>
<tr>
<th><strong>순서</strong></th>
<th><strong>서버 (맛집)</strong></th>
<th><strong>클라이언트 (손님)</strong></th>
<th><strong>설명</strong></th>
</tr>
</thead>
<tbody><tr>
<td>1</td>
<td><strong>socket()</strong></td>
<td><strong>socket()</strong></td>
<td>전화기 마련 (소켓 생성)</td>
</tr>
<tr>
<td>2</td>
<td><strong>bind()</strong></td>
<td>-</td>
<td>주소 설정 (IP/Port)</td>
</tr>
<tr>
<td>3</td>
<td><strong>listen()</strong></td>
<td>-</td>
<td>벨소리 대기 (대기 상태)</td>
</tr>
<tr>
<td>4</td>
<td>-</td>
<td><strong>connect()</strong></td>
<td>전화 걸기 (연결 요청)</td>
</tr>
<tr>
<td>5</td>
<td><strong>accept()</strong></td>
<td>-</td>
<td>손님 입장 (연결 허용)</td>
</tr>
<tr>
<td>6</td>
<td><strong>read/write</strong></td>
<td><strong>write/read</strong></td>
<td>대화 나누기 (데이터 송수신)</td>
</tr>
<tr>
<td>7</td>
<td><strong>close()</strong></td>
<td><strong>close()</strong></td>
<td>영업 종료 (소켓 폐쇄)</td>
</tr>
</tbody></table>
<h3 id="iterative-서버-핵심-요약">Iterative 서버 핵심 요약</h3>
<p><strong>&quot;한 번에 한 명씩, 하지만 죽지 않고 반복해서 받는 서버&quot;</strong></p>
<ul>
<li><strong>기존 코드:</strong> 단 한 번의 데이터 송수신(Single Transaction) 후 바로 종료.</li>
<li><strong>Iterative 서버:</strong> <code>while</code> 루프를 통해 한 클라이언트와 <strong>세션을 지속적으로 유지</strong>.</li>
<li><strong>반복 구조:</strong> 해당 클라이언트가 나가도 서버가 꺼지지 않고, <strong>다음 대기자를 반복해서 수락(accept)</strong>함.</li>
</ul>