# Схема Эль-Гамаля

## Описание и применение

При выполнении пользователь указывает:
1. n - длина простого числа
2. t - число, отображающее необходимую уверенность в простоте числа
3. имя файла с сообщением для зашифровки и расшифровки

Программа сгенерирует пару ключей (K1, K2) для расшифровки и зашфировки.
  
**K1** - это публичный ключ, содержащий три целых числа (p, g, h).

**p** - n-битное простое.  Вероятность его простоты: 1-(2^-t)

**g** - квадрат примитивного корня по модулю p

**h** = g^x mod p

**x** выбирается случайно, 1 <= x < p

**h** вычисляется через функцию _modexp_(base, exp, modulus).

**K2** закрытый ключ, содержащий описанные выше (p, g, x).

**K1** and **K2** are written to files named K1 and K2.

Next the program encodes the bytes of the message into integers z[i] < p.
The module for this is named encode() and is described further where it is implemented.

After the message has been encoded into integers, the integers are encrypted and written
to a file, Ciphertext.  The encryption procedure is implemented in encrypt().  It works
as follows:
      Each corresponds to a pair (c, d) that is written to Ciphertext.
      For each integer z[i]:
              c[i] = g^y (mod p).  d[i] = z[i]h^y (mod p)
              where y is chosen randomly, 0 <= y < p

The decryption module decrypt() reads each pair of integers from Ciphertext and converts
them back to encoded integers.  It is implemented as follows:
      s = c[i]^x (mod p)
      z[i] = d[i]*s^-1 (mod p)

The decode() module takes the integers produced from the decryption module and separates
them into the bytes received in the initial message.  These bytes are written to the file
Plaintext.

HURDLES CLEARED DURING IMPLEMENTATION

modular exponentiation
The first problem I encountered was in implementing the fast modular exponentiator, modexp().
At first it did not terminate when given a negative number.  I quickly figured out that when
performing integer division on negative numbers, the result is rounded down rather than toward
zero.

finding primitive roots
Understanding the definition of primitive roots was not enough to find one efficiently.  I had
search the web to understand how primitive roots can be found.  Wikipedia helped me understand
I needed to test potential primitive roots multiplicative order.  The algorithm found at
http://modular.math.washington.edu/edu/2007/spring/ent/ent-html/node31.html
is the one I implemented.

finding large prime numbers
After implementing the Solovay-Strassen primality test I found it was difficult to compute 100
bit primes even with probability 1/2.  I met with Professor Klapper to discuss this problem and he
suggested I quit running the program on UK's shared "multilab" and I speed up my Jacobi algorithm
by using branches to find powers of -1 rather than actually exponentiating them.  After doing this
I was able to find 500 bit primes in about 15 minutes.

finding prime numbers with confidence > 2
I found it took a long time to test primes with a large number of bits with confidence greater than
two.  I went to the web again to read over the description of the Solovay-Strassen primality test
and realized jacobi(a, n) should be congruent to modexp(a, (n-1)/2, n) mod n.  I had only been checking
that they were equal.  Before making this change I tried to find a 200 bit prime with confidence 100
and gave up after an hour and a half.  After this change I was able to succeed after a couple of minutes.

getting encoding and decoding to work
I knew that encoding and decoding were implemented correctly because I could encode and decode a message
and get the message I had started with.  But I did not receive the right message when I encrypted and
decrypted it, despite having checked my encrypt and decrypt modules many times.  I fixed this by raising
s to p-2 instead of -1 in the decryption function.