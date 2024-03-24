# Experiments with Z3 and FHE

This repo contains some experiments on Z3 and FHE from the Hack Day at the 2024 [HACS Workshop](https://www.hacs-workshop.org/) in Toronto.
Thanks to @alex-ozdemir for doing virtually all of the work here! 

## Matrix-Vector Product (MVP) with FHE
In most FHE schemes, ciphertexts encrypt large vectors of integers (e.g., n=1024 or n=65536 elements) 
on which we can perform elementwise additions (virtually "free") and multiplications operations (costly) 
giving rise to a Single Instruction Multiple Data (SIMD) programming paradigm.
In addition, we can rotate the elements in a ciphertext in a cyclic fashion (approx. as costly as a multiplication).

This gives rise to a variety of unusual approaches to realizing common linear algebra functions, such as the "diagonal method" by Halevi and Shoup [1]
which visualized on Slide 24 from Hao Chen's talk on [Techniques in PPML](https://github.com/WeiDaiWD/Private-AI-Bootcamp-Materials/blob/master/4_Hao_Techniques_in_PPML.pdf) 
at the [Microsoft Research Private AI Bootcamp](https://www.microsoft.com/en-us/research/video/private-ai-bootcamp-techniques-in-ppml/).

## Verifying "Diagonal" MVP with Z3
In order to explore how feasible it is to use SMT solvers to verify the correcntess of (potentially more complex) FHE transformations,
we want to show that the diagonal method is equivalent to the traditional formulation of the matrix-vector product.
This repository contains several snapshots (as different commits, so please refer to the commit history) of our journey towards this, 
(currently) ending with the inability to express sums of vectors efficiently.


[1] Halevi, S. and Shoup, V. 2014. Algorithms in HElib. Advances in Cryptology – CRYPTO 2014 (2014), 554–571.
