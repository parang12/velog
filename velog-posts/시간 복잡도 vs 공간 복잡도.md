<h3 id="시간복잡도란">시간복잡도란</h3>
<ul>
<li><p><strong>알고리즘이 문제를 해결하는데 걸리는 시간</strong>이 시간복잡도라고 한다.</p>
</li>
<li><p><strong>입력데이터의 크기(n)에 따라</strong> 연산회수가 얼마나 <strong>증가</strong>하는지를 나타내는 척도다.</p>
</li>
</ul>
<p>주로 빅오(Big-O)표기법을 통해서 나타내게 된다.</p>
<p><em>ex)</em></p>
<pre><code>python
#리스트를 하나씩 순회하여 arr에 x값이 있는지 확인.

arr = [1,2,3,4,5,6,7,8,9]
x = 8 
for n in arr:
    if n == x:
        print(&quot;find number&quot;)</code></pre><p>_
최선의 경우에는 O(1)
최악의 경우 O(n)
_</p>
<blockquote>
<p>Tip. 시간복잡도를 표기할때는 최악의 경우를 표기함</p>
</blockquote>
<h3 id="공간복잡도란">공간복잡도란</h3>
<ul>
<li><strong>알고리즘이 문제를 해결하는데 필요한 메모리 공간의 양</strong>을 나타내는 지표이다.</li>
<li><strong>입력크기(n)</strong>에 따라 메모리 공간이 얼마나 증가하는지를 측정</li>
</ul>
<pre><code>python
#기존 리스트를 하나씩 복사하는 코드.
arr = [1,2,3,4,5,6,7,8,9]
new_arr = arr.copy()</code></pre><p><em><code>arr</code> 크기 만큼 새 배열 <code>new_arr</code>생성 
<code>arr</code> 크기가 n이라면 공간이 O(n)필요하다</em></p>
<blockquote>
<p>Tip.
파이썬의 모든 것은 객체이기 때문에 
<code>new_arr</code> =<code>arr</code>라고 표기할시 <code>new_arr</code>과 <code>arr</code>은 
같은 객체(같은 메모리 주소)를 가리킨다.
<code>arr</code> 변경시 <code>new_arr</code>도 변경됨</p>
</blockquote>
<h3 id="시간복잡도-vs-공간복잡도">시간복잡도 vs 공간복잡도</h3>
<ul>
<li>시간복잡도랑 공간복잡도를 우선시해야 되는 경우는 각각 다르다.</li>
</ul>
<h4 id="시간우선">시간우선</h4>
<p><strong>웹 서비스</strong>: 사용자가 요청을 보내면 거의 실시간으로 응답해야 하기 때문에 지연시간 준수가 최우선</p>
<p><strong>알고리즘 문제 / CS 과제</strong>: 보통의 문제는 실행 시간 제한이 존재 한다. 
<em>몇몇 문제는 메모리 제한이 나오기도함</em></p>
<h4 id="공간우선">공간우선</h4>
<p><strong>배치/데이터 파이프라인(대용량)</strong>: 처리할 데이터가 수십~수백 GB 이상으로 메모리에 한 번에 올리기가 어렵기 때문에 메모리 사용을 최소화화고, 디스크/스트리밍 기반으로 처리해야 안정적으로 수행이 가능하기 때문</p>
<p><strong>IoT / 임베디드</strong>: IoT나 임베디드 경우에는 해당 장치의 RAM이 제한적인 경우가 많다 (메모리 MB단위)</p>
<h3 id="결론">결론</h3>
<blockquote>
<p><strong>업무 성격과 수행할 동작에 따라 시간복잡도와 공간복잡도의 우선순위가 달라지므로, 상황을 잘 파악하고 그때그때 적절히 조율하는 것이 가장 현실적이다.</strong></p>
</blockquote>