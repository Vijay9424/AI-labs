

#include <bits/stdc++.h>

using namespace std;

typedef struct nodes{
    string state;
    nodes* parent;
    int action;
} nodes;

string initState = "LLL-RRR";
string goalState = "RRR-LLL";


map<string, bool> explored;


queue<nodes*> frontier;
map<string, int> frontStates;

string swapChar(string child, int i, int j) {
    string ans = child;
    ans[i] = child[j];
    ans[j] = child[i];
    return ans;
}

vector<nodes> getChildren(nodes* currNode) {
    int blankPos = 0;
    int n = currNode->state.length();
    for(int i=0; i<currNode->state.length(); i++){
        if(currNode->state[i] == '-'){
            blankPos = i;
            break;
        }
    }
    vector<nodes>  children;
    int j = 0;

    if (blankPos - 1 >= 0 && (currNode->state[blankPos - 1] - 'L') == 0) {
        string childState = swapChar(currNode->state, blankPos, blankPos - 1);
        children.push_back(nodes());
        children[j].state = childState;
        children[j].parent = currNode;
        children[j].action = -1;
        j++;
    }
    if (blankPos - 2 >= 0 && (currNode->state[blankPos - 2] - 'L') == 0) {
        string childState = swapChar(currNode->state, blankPos, blankPos - 2);
        children.push_back(nodes());
        children[j].state = childState;
        children[j].parent = currNode;
        children[j].action = -2;
        j++;
    }
    if (blankPos + 1 < n && (currNode->state[blankPos + 1] - 'R') == 0) {
        string childState = swapChar(currNode->state, blankPos, blankPos + 1);
        children.push_back(nodes());
        children[j].state = childState;
        children[j].parent = currNode;
        children[j].action = 1;
        j++;
    }
    if (blankPos + 2 < n && (currNode->state[blankPos + 2] - 'R') == 0) {
        string childState = swapChar(currNode->state, blankPos, blankPos + 2);
        children.push_back(nodes());
        children[j].state = childState;
        children[j].parent = currNode;
        children[j].action = 2;
        j++;
    }
    return children;
}

int main() {
    nodes* root = new nodes();

    vector<string> moves;

    root->state = initState;
    root->parent = NULL;
    root->action = 0;

    int count = 0;

    frontStates[initState]++;
    frontier.push(root);
    explored[initState] = true;

    bool completed = false;

    while(!frontier.empty()) {
        nodes* node = frontier.front();
        if(node->state == goalState) {
            completed = true;
            break;
        }

        frontier.pop();
        frontStates.erase(node->state);

        vector<nodes> children = getChildren(node);
        for (auto child : children) {
            if(explored.find(child.state) == explored.end() && frontStates.find(child.state) == frontStates.end()){
                count++;
                if(child.state == goalState){
                    completed = true;
                    nodes* temp = node;
                    moves.insert(moves.begin(), goalState);
                    while(temp != NULL) {
                        moves.insert(moves.begin(), temp->state);
                        temp = temp->parent;
                    }
                    break;
                }
                frontStates[child.state]++;
                nodes* c = new nodes();
                c->state = child.state;
                c->parent = child.parent;
                c->action = child.action;
                frontier.push(c);
                explored[child.state] = true;
            }
        }

        if(completed) {
            break;
        }
    }
    
    if(completed) {
        cout<<"total states:\t"<<count<<endl;
        cout<<"total moves:\t"<<moves.size() - 1<<endl;
        cout<<"Moves: \t"<<flush;
        for(int i=0; i<moves.size(); i++){
            cout<<moves[i]<<"\t";
        }
        cout<<endl;
    }
    return 0;
}