#include "sparsevector.hpp"

#include<map>
#include<iterator>
#include<cmath>
#include<set>
#include<algorithm>
#include<cassert>


SparseVector::SparseVector(){
}

void SparseVector::insert(int key, double value){
	data[key] = value;
}

double SparseVector::get(int key) {
	return data.find(key)->second;
}


void SparseVector::normalize() {
	double magnitude = getMagnitude();
	
	for(auto key : getKeys()) {
		data[key] = data.find(key)->second / magnitude;
	}
}

double SparseVector::cosineSimilarity(SparseVector& other) {
    
    auto product = dotProduct(other);
    auto denom   = sqrt(getMagnitude()) *  sqrt(other.getMagnitude());

    return product / denom;
}

double SparseVector::dotProduct(SparseVector& other) {
	auto myElements 	= getKeys();
	auto otherElements 	= other.getKeys();

	std::set<int> intersect;
	set_intersection(	myElements.begin(), myElements.end(),
						otherElements.begin(), otherElements.end(),
                  		std::inserter(intersect,intersect.begin()));
    
    
    double product = 0;
    for(auto key : intersect) {
    	product += get(key) * other.get(key);
    }
    
    return product;
}

std::set<int> SparseVector::getKeys() {
	auto keys = std::set<int>();
	
	for(auto element : data) {
		keys.insert(element.first);
	}
	
	return keys;
}

double SparseVector::getMagnitude() {
	double magnitude = 0;
	
	for(auto i : data) {
		magnitude += i.second * i.second;
	}
	
	return sqrt(magnitude);
}


void test() {
	{
		SparseVector s;
	
		s.insert(0,3);
		s.insert(1,1);
		s.insert(2,2);	
		//printf("%f\n", s.getMagnitude());
		assert(abs(s.getMagnitude() - 3.742) < 0.000001);
		
		s.normalize();
		assert(abs(s.get(0) - 0.802) < 0.000001);
		assert(abs(s.get(1) - 0.267) < 0.000001);
		assert(abs(s.get(2) - 0.534) < 0.000001);
	}
	
	{
	
		SparseVector s;
		s.insert(0,3);
		s.insert(1,1);
		s.insert(2,2);
		s.normalize();
		assert(s.getKeys().size() == 3);
		
		SparseVector t;
		t.insert(0,3);
		t.insert(1,1);
		t.insert(2,2);
		t.normalize();
		assert(t.getKeys().size() == 3);
		assert(abs(s.cosineSimilarity(t) - 1.0) < 0.000001);
	}
}
