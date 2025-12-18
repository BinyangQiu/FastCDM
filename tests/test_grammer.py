from fastcdm.core import preprocess

def test_preprocess():
    latex_string = r"\begin{bmatrix}(\mathbf{I}-\mathbf{A}^{\mathsf{DD}})&-\mathbf{A}^{\mathsf{DP }}&-\mathbf{A}^{\mathsf{DN}}\\ 0&\mathbf{I}&0\\ -\mathbf{A}^{\mathsf{ND}}&-\mathbf{A}^{\mathsf{NP}}&(\mathbf{I}-\mathbf{A}^{ \mathsf{NN}})\end{bmatrix}^{-1}=\begin{bmatrix}\mathbf{B}^{\mathsf{DD}}& \mathbf{B}^{\mathsf{DP}}&\mathbf{B}^{\mathsf{DN}}\\ \mathbf{B}^{\mathsf{PD}}&\mathbf{B}^{\mathsf{PP}}&\mathbf{B}^{\mathsf{PN}}\\ \mathbf{B}^{\mathsf{ND}}&\mathbf{B}^{\mathsf{NP}}&\mathbf{B}^{\mathsf{NN}} \end{bmatrix}"
    processed, _ = preprocess(latex_string)
    print(processed)

test_preprocess()
