public class Matching {
	/**
	* Assumption. 
	*  1. Event representation: for each event data, a category set is used.
	*      If a category is assigned to an event, the corresponding bit of the set is 1; otherwise, it is 0.
	*  2. Argument format: each data is divided by " ... ".
	*  3. Data arrange: a category set of the present is located at last.
	*/
	public static void main(String[] args){
		Matching m = new Matching();
		m.invoke(args[0], Integer.parseInt(args[1]));
	}

	/**
	* @param cats: categories of all past events and one present event.
	* @param k: number of return value.
	*/
	private void invoke(String cats, int k){
		// Make a matrix for the input data.
		Double[][] mat = makeMatrix(cats);
		
		// Determine similarity between events.
		Double[][] mulResult = multiplyByTransposedMatrix(mat);
		
		// Get a row corresponding the present issue without an element representing that how many categories the present issue has. 
		Double[] modernIssue = mulResult[mat.length-1];
		
		modernIssue[modernIssue.length-1] = -Double.MAX_VALUE;

		outputResult(k, modernIssue);
	}

    /**
	* From input string, this method makes a matrix.
	*/
	private Double[][] makeMatrix(String args){
		String[] data = args.split(" ... ");
		String[] firstDataCategories = data[0].split(", ");
		Double[][] mat = new Double[data.length][firstDataCategories.length];
		mat[0] = str2doubleForCategory(firstDataCategories);
		for(int i=1;i<data.length;i++){
			mat[i] = str2doubleForCategory(data[i].split(", "));
		}
		
		return mat;
	}

	/**
	* This method changes types from string to double.
	* @param cdata: category data
	*/
	private Double[] str2doubleForCategory(String[] cdata){
		Double[] result = new Double[cdata.length];
		for(int i=0;i<cdata.length;i++){
			result[i] = Double.parseDouble(cdata[i]);
		}
		return result;
	}
	
	/**
	 * Print top k historical events similar to the modern issue.
	 * @param k: number of printing results.
	 * @param vec: a result of matrix multiplication.
	 */
	private void outputResult(int k, Double[] vec){
		if (vec ==null || vec.length==0) return;
		int[] event_index = new int[vec.length];
		for(int i=0;i<event_index.length;i++) event_index[i] = i;
		quicksort(0, vec.length-1, vec, event_index);

		String topk = "" + (event_index[event_index.length-1]+1);
		if(k>event_index.length) k = event_index.length;
		for(int i=1;i<k;i++){
		    topk += " <br> " + (event_index[event_index.length-i-1]+1);
		}
		System.out.println(topk);
	}

	/**
	* This method just sorts values by simple quicksort with arranging corresponding indexes.  
	*/
	private void quicksort(int low, int high, Double[] vec, int[] index) {
		int i = low;
		int j = high;
		double mid = vec[low + (high-low)/2];
		
		while (i <= j) {
			while (vec[i] < mid) i++;
			while (vec[j] > mid) j--;
			if (i <= j) {
				double tmp = vec[i];
				vec[i] = vec[j];
				vec[j] = tmp;
				int tindex = index[i];
				index[i] = index[j];
				index[j] = tindex;
				i++;
				j--;
			}
		}
		
		if (low < j) quicksort(low, j, vec, index);
		if (i < high) quicksort(i, high, vec, index);
	}
	
	
	/**
	 * This method multiplies a matrix by its transposed matrix. 
	 * We manually optimize this algorithm for effectively using cache memories. 
	 * First, this method calculates values only corresponding to an upper triangular matrix of a result because the result matrix is a symmetric matrix.
	 * Then, scalar replacement, loop unrolling, and global load instruction aggregation (GLIA) are applied.
	 * 
	 * If you want to know GLIA in detail, see the following research paper.
	 * Yasunobu Sumikawa and Munehiro Takimoto, 
	 * "Global Load Instruction Aggregation Based on Dimensions of Arrays", 
	 * Computers and Electrical Engineering, Elsevier, in press.
	 * @param mat
	 * @return a matrix
	 */
	private Double[][] multiplyByTransposedMatrix(Double[][] mat){ 
		int col = mat.length;
		int row = mat[0].length;
		
		Double[][] result = new Double[col][col];

		/* Calculating diagonal elements */
		for(int i=col-1;i>=0;i--){
			double sum = 0;
			for(int j=row-1;j>=0;j--){
				double a1 = mat[i][j];
				sum += a1*a1;
			}
			result[i][i] = sum;
		}
		
		for(int i=0;i<col;i++){
			int j=i+1;
			/* Unrolling one iteration */
			for(;j+1<col;){
				double sum1 = 0;
				double sum2 = 0;
				/* Unrolling five iterations */
				for(int k=0;k<row;){
					if(k+6<row){
						/* Loop unrolling for j-loop discover redundant load statements. We eliminates them. */
						double a1 = mat[i][k];
						double a2 = mat[i][k+1];
						double a3 = mat[i][k+2];
						double a4 = mat[i][k+3];
						double a5 = mat[i][k+4];
						double a6 = mat[i][k+5];
						
						/* After loop unrolling for k-loop, arranging load statements improves utilization of cache memory as follows. */
						double b11 = mat[j][k];
						double b12 = mat[j][k+1];
						double b13 = mat[j][k+2];
						double b14 = mat[j][k+3];
						double b15 = mat[j][k+4];
						double b16 = mat[j][k+5];
						
						sum1 += a1*b11+a2*b12+a3*b13+a4*b14+a5*b15+a6*b16;
						
						double b21 = mat[j+1][k];
						double b22 = mat[j+1][k+1];
						double b23 = mat[j+1][k+2];
						double b24 = mat[j+1][k+3];
						double b25 = mat[j+1][k+4];
						double b26 = mat[j+1][k+5];
						
						sum2 += a1*b21+a2*b22+a3*b23+a4*b24+a5*b25+a6*b26;
						
						k+=6;
					}
					else{
						sum1 += mat[i][k] * mat[j][k];
						sum2 += mat[i][k] * mat[j+1][k];
						k++;
					}
				}
				
				result[i][j] = sum1;
				result[j][i] = sum1;
				
				result[i][j+1] = sum2;
				result[j+1][i] = sum2;
				
				j+=2;
			}
			if(j<col){
				double sum = 0;
				for(int k=0;k<row;k++){
					sum += mat[i][k] * mat[j][k];
				}
				result[i][j] = sum;
				result[j][i] = sum;
			}
		}
		
		return result;
	}

	/**
	* For debug. This method prints an input matrix.
	*/
    void printMatrix(Double[][] mat){
	    for(int i=0;i<mat.length;i++){
		    for(int j=0;j<mat[0].length;j++){
		        System.out.print(mat[i][j] + ", ");
    		}
	    	System.out.println("<br>");
	    }
    }
}
