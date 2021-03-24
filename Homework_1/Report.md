



## Exercise 1

 `strassen_matrix_mult` function was implemented in the file matrix.py

## Exercise 2

The generalization of the `strassen_matrix_mult` function was implemented in the file matrix.py with the name `strassen_matrix_mult_non_power`. Taking two matrices A and B, the function check if they can be multiplied. It find the smallest power of 2 larger than the largest dimension of A and B, and it resize them to   squares of that value adding the adequate number of lines and columns of zeros. It then carries out the multiplication using the `strassen_matrix_mult` function, and eventually it trims out the unnecessary dimensions. 

Lets call n=m+c the dimension of the new resized matrix, where m is the smaller dimension of the input matrix considered. In this way, when comparing it to the classic square matrix case, we are overestimating the time complexity. We can then carry out the same calculation as for the square dimension case (where n is a power of 2)
$$
\begin{align*}
    T(n)& = \sum^{\log_2 n}_{i=0} 7^i \cdot c \cdot \frac{n}{n^i}^2  \\
    & = c \cdot n^2 \cdot  \sum^{\log_2 n}_{i=0} (\frac{7}{4})^i \\
    & = c \cdot n^2 \cdot \frac{((\frac{7}{4})^{ \log_2 n+1}-1)}{\frac{7}{4}-1}\\
    & =c' \cdot n^2 \cdot ((\frac{7}{4})^{ \log_2 n+1}-1)\ \  \text{ for }\ \  c'=\frac{4}{3}c\\
    & = c'' \cdot n^2 \cdot (\frac{7}{4})^{\log_2 n} - \frac{4}{7} \\
    & = c'' \cdot 4^{\log_2 n} \cdot (\frac{7}{4})^{\log_2 n} - c'\cdot n^2 \\
    & = c'' \cdot 7^{\log_2 n} - c'\cdot n^2 \\
    & = c'' \cdot n^{\log_2 7}- c' \cdot n^2 \in \Theta (n^{\log_2 7})
\end{align*}
$$
Making the substitution
$$
\begin{align*}
    T(n)& =T (m +c) \in \Theta (n^{\log_2 7}) = \Theta ((m+c)^{\log_2 7})= \Theta (a(m)^{\log_2 7})=\Theta (m^{\log_2 7})
\end{align*}
$$
So the asymptotic complexity is the same.

## Exercise 3

The function `strassen_matrix_mult_memory_efficent` implement the strassen matrix multiplication using only 2 S matrices. In order to study the execution time of the code, a memory efficient implementation of the `strassen_matrix_mult_non_power` function was also implemented, in order tho increase the batch size of the matrices computable on a personal computer. It was called `strassen_matrix_mult_non_power_memory`.

The following plot shows the execution time for increasing matrices size for the Gauss algorithm, the Naive Strassen algorithm, and the memory efficient Strassen algorithm.

![](/home/showreally/Desktop/Algorithmic_Design/Homework_1/Plot1.png)

The plot shows a clear distinction between time required by the Gauss algorithm (in blue), and the two implementation of the Strassen algorithm (in green and orange). Between the second two, although a slight difference is notable, being the memory efficient version of the algorithm a bit faster, it can be considered reasonably within the time fluctuations normally present in the execution of a program. This can be caused by the nature of Python language itself, whose data management doesn't provide the tool to assure that an overwriting is actually happening. 

## Exercise 4

First of all, I will only consider the S an P matrices as auxiliary matrices.  In addiction to this, as my implementation of the Strassen Algorithm for rectangular matrix rescale them to the nearest square matrix whose dimension is a power of two, I will take in consideration only this latter case to asses the space required by the algorithm. 

For the computation of the C matrices, one can step by step evaluate the required P, update the C matrices, and then evaluate the following P on the space one allocated by the previous  P.  Even thought  S an P matrices have the same dimensions, one cannot overwrite the data of the P matrix evaluated at a given time on the memory space used just before by the S required to calculate the P itself. As P is the result of a matrix multiplication, an update of the values of one of the input matrices at runtime will lead to an error in the evaluation  of the output of the next entries on the same line of the output matrix. Furthermore, directly updating in place the values of the C matrix would require for some C , as every C matrix is different, to repeat more than once the calculation required to evaluate the P (ideally augmenting the number of auxiliary matrix calculated, and the complexity of the algorithm through them), and data updated on one cannot be retrieved and use to update another.   

Also, some P require the knowing of two S matrices at the same time, so the lower bound on the space required by the auxiliary matrices is the sum of the memory allocated for this three matrices at each iteration of the recursion i  i.e. `3*n/2*n/2` entries, or `n*3/4 ` float, where n is the dimension of the matrix. So, as the recursion is carried on until the input matrices as a dimension lower than a given threshold (after which the Gauss algorithm is used, which does not require auxiliary matrices) , n=32 in our cases , and as the next recursion of the strassen algorithm will also require the aforementioned auxiliary matrices, the lower bound on the space used by the auxiliary matrices in the algorithm altogether is

  
$$
Memory = 3 \cdot \frac{n}{2}\cdot \frac{n}{2} + 3 \cdot \Big(\frac{1}{2} \cdot  \frac{n}{2} \Big) \cdot \Big(\frac{1}{2} \cdot  \frac{n}{2} \Big) + 3 \cdot \Big[ \frac{1}{2} \cdot \Big(\frac{1}{2} \cdot  \frac{n}{2} \Big) \Big]\cdot \Big[ \frac{1}{2} \cdot \Big(\frac{1}{2} \cdot  \frac{n}{2} \Big) \Big] ... = 3 \cdot \sum_{i=1}^{\frac{1}{2}\log_2 n -2} \frac{n^2}{2^{2i}}
$$
Where the upper bound on the sum is given by the threshold.  

If Gauss algorithm is never used, the upper bound is `1/2* log_2(n)`