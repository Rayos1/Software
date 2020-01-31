#ifndef BINARY_SEARCH_TREE_H
#define BINARY_SEARCH_TREE_H

#include "Binary_Tree.h"

template<typename Item_Type>
class Binary_Search_Tree : public Binary_Tree<Item_Type>
{
public:
	// Constructor
	Binary_Search_Tree() : Binary_Tree<Item_Type>() { root->data = "root"; }

	// Public Member Functions
	virtual bool insert(const Item_Type& encoding, const Item_Type& decoding);

	virtual bool erase(const Item_Type& item);

	const Item_Type* min() const;

	const Item_Type* min(BTNode<Item_Type>* local_root) const;

	const Item_Type* max() const;

	const Item_Type* max(BTNode<Item_Type>* local_root) const;

	const Item_Type* find(const Item_Type& target) const;
private:

	// Private Member Functions
	virtual bool insert(BTNode<Item_Type>*& local_root, const Item_Type& encoding, const Item_Type& decoding);

	virtual bool erase(BTNode<Item_Type>*& local_root,
		const Item_Type& item);

	const Item_Type* find(BTNode<Item_Type>* local_root,
		const Item_Type& target) const;

	virtual void replace_parent(
		BTNode<Item_Type>*& old_root,
		BTNode<Item_Type>*& local_root);

}; // End binary search tree

template<typename Item_Type>
const Item_Type* Binary_Search_Tree<Item_Type>::min() const {
	return min(this->root);

}

template<typename Item_Type>
const Item_Type* Binary_Search_Tree<Item_Type>::min(BTNode<Item_Type>* local_root) const {
	if (local_root == NULL)
		return NULL;

	if (local_root->left == NULL)
		return &(local_root->data);
	return min(local_root->left);
}

template<typename Item_Type>
const Item_Type* Binary_Search_Tree<Item_Type>::max() const {
	return max(this->root);

}

template<typename Item_Type>
const Item_Type* Binary_Search_Tree<Item_Type>::max(BTNode<Item_Type>* local_root) const {
	if (local_root == NULL)
		return NULL;

	if (local_root->right == NULL)
		return &(local_root->data);
	return max(local_root->right);
}

template<typename Item_Type>
const Item_Type* Binary_Search_Tree<Item_Type>::find(
	const Item_Type& item) const {
	return find(this->root, item);
}

template<typename Item_Type>
const Item_Type* Binary_Search_Tree<Item_Type>::find(BTNode<Item_Type>* local_root,
	const Item_Type& target) const {
	if (local_root == NULL)
		return NULL;	//FIXME: THIS SHOULD MAYBE BE AN ERROR MESSAGE INSTEAD?
	else {
		//iteratively traverse BST
		for (int i = 0; i < target.size(); i++) {
			if (target[i] == '.') {
				local_root = local_root->left;
			}
			else if (target[i] == '_') {
				local_root = local_root->right;
			}

			//if the last character of the morse code letter is reached return the data of the current node
			if (i == target.size() - 1) {
				return &(local_root->data);
			}
		}
	}
}

template<typename Item_Type>
bool Binary_Search_Tree<Item_Type>::insert(const Item_Type& encoding, const Item_Type& decoding) {
	return insert(this->root, encoding, decoding);
}

template<typename Item_Type>
bool Binary_Search_Tree<Item_Type>::insert(BTNode<Item_Type>*& local_root, const Item_Type& encoding, const Item_Type& decoding) {
	
	if (local_root == NULL) {
		// create new node from first index of encoding
		local_root = new BTNode<Item_Type>(encoding.substr(0, 1));
	}
	if (encoding.size() > 1) {

		std::string remainder = encoding.substr(1, encoding.size());
		std::string next = encoding.substr(1, 1);

		if (next == ".")
			return insert(local_root->left, remainder, decoding);
		else if (next == "_")
			return insert(local_root->right, remainder, decoding);
		else
			return false;
	}
	else
		local_root->decoding = decoding;
		return true;
}

template<typename Item_Type>
bool Binary_Search_Tree<Item_Type>::erase(const Item_Type& item) {
	return erase(this->root, item);
}

template<typename Item_Type>
bool Binary_Search_Tree<Item_Type>::erase(BTNode<Item_Type>*& local_root, const Item_Type& item) {
	if (local_root == NULL) {
		return false;
	}
	else {
		if (item < local_root->data)
			return erase(local_root->left, item);
		else if (local_root->data < item)
			return erase(local_root->right, item);
		else {
			BTNode<Item_Type>* old_root = local_root;
			if (local_root->left == NULL) {
				local_root = local_root->right;
			}
			else if (local_root->right == NULL) {
				local_root = local_root->left;
			}
			else {
				replace_parent(old_root, old_root->left);
			}
			delete old_root;
			return true;
		}
	}
}

template<typename Item_Type>
void Binary_Search_Tree<Item_Type>::replace_parent(BTNode<Item_Type>*& old_root, BTNode<Item_Type>*& local_root) {
	if (local_root->right != NULL) {
		replace_parent(old_root, local_root->right);
	}
	else {
		old_root->data = local_root->data;
		old_root = local_root;
		local_root = local_root->left;
	}
}

#endif
