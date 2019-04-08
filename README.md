# pwnable.tw_tcache-tear
#tcache #unsorted bin fake chunk->leak libc

### 다시 풀어보기  

먼저, tcache에서는 check과정이 없기 때문에 double free를 쉽게 할 수 있다.  
이를 통해 원하는 주소에 malloc 할당이 가능하다.  

힙문제에서 libc leak을 하기 위해 unsorted bin에 들어갈 수 있는 fake chunk를 사용할 수 있다. 
unsorted bin에 들어갈때 fd, bk에 main_arena+88주소가 들어가기 때문에 이를 출력해내면 libc leak이 가능하다.  

tcache에서는 0x420보다 크기가 클 경우, unsorted bin에 해당하는 chunk가 된다.  
따라서 이를 위해 fake chunk를 만들어준다. 또한 만들어준 fake chunk가 top chunk가 되지 않기 위해 해당 청크 다음 fake chunk도 만들어준다!  

libc leak이 성공했다면 free_hook을 이용해서 쉘을 딸 수 있다.  
free_hook에는 원래 아무 값이 들어가있지 않은데, 특정 주소를 주면 free과정에서 실행하게 된다.

*p &__free_hook*  
이렇게 찾은 hook에 overwrite를 하게되면 free()함수를 호출하면 overwrite된 가젯을 실행시킨다.  

Full Relro가 걸려있을 때 유용하게 사용할 수 있다.  
ps. malloc_hook, realloc_hook도 사용가능하니 참고하자.
