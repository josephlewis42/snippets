#pragma once

#include<map>
#include<set>


class SparseVector : public std::map<int, double> {
	public:
		SparseVector();
		void normalize();
		double cosineSimilarity(SparseVector& other);
		double dotProduct(SparseVector& other);
		std::set<int> getKeys();
		double getMagnitude();
		void insert(int key, double value);
		double get(int key);
	private:
		std::map<int, double> data;
};


