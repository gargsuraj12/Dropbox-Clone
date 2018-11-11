#include <iostream>
#include <cmath>
#include <algorithm>
#define MAX_SIZE 100000000
#define kIndex  100000
using namespace std;

long long numArray[MAX_SIZE];

void swap(long long *ar, long long i, long long j){
	long long temp  = ar[i];
	ar[i] = ar[j];
	ar[j] = temp;
}

long long kthMin(long long *ar, long long lb, long long ub, long long k){
	srand(time(0)); 
	long long pivPos = rand()%(ub-lb+1) + lb;
	long long pivot = ar[pivPos];
	swap(ar, pivPos, ub);
	long long i=lb-1, j = lb;
	while(j<=ub){
		if(ar[j] < pivot){
			//i++;
			swap(ar, ++i, j);
		}
		j++;
	}
	swap(ar, ++i, ub);
	if(i == k){
		return pivot;
	}else{
		if(i<k){
			return kthMin(ar, i+1, ub, k);
		}else{
			return kthMin(ar, lb, i-1, k);
		}
	}
}

int main(){
	/*cout<<"Enter the size of thr array: "<<endl;
	long long n, k;
	cin>>n;
	long long ar[n];
	cout<<"Enter the values of the array (seperated by space):"<<endl;
	for(long long i=0; i<n; i++){
		cin>>ar[i];
	}
	cout<<"Enter the value of k for kth minimum element in the array: "<<endl;
	cin>>k;
	cout<<k<<"th minimum value of the array is: "<<kthMin(ar, 0, n-1, k-1)<<endl;	//k-1th position because 0 based indexing
	*/
	
	
	srand((unsigned)time(0)); 
	 
	for(long long i=0; i<MAX_SIZE; i++){ 
	    numArray[i] = (rand()%MAX_SIZE)+1; 
	} 

	clock_t currTime; 
    double timeInterval;

////////////my fuction for nth smallest/////////////////////////////

    currTime = clock(); 

    cout<<kthMin(numArray, 0,MAX_SIZE-1, kIndex-1)<<"\n";

    timeInterval = (double)(clock() - currTime)/CLOCKS_PER_SEC; 
    
    cout<<"My fuction: "<<timeInterval<<"\n"; 

///////////////////////////// stl ////////////////////////////////////////

    currTime = clock(); 

    nth_element(numArray, numArray+kIndex-1, numArray+MAX_SIZE);
    
    cout<<numArray[kIndex-1]<<"\n";

    timeInterval = (double)(clock() - currTime)/CLOCKS_PER_SEC; 
    
    cout<<"stl: "<<timeInterval<<"\n";
	return 0;
}