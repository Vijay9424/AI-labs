#include <bits/stdc++.h>

using namespace std;
typedef tuple<int, int, int> triplet;





typedef struct nodes{
    triplet state;
    nodes* parent;
    pair<int, int> action;
} nodes;

triplet initState(3, 3, 0);

triplet goalState(0, 0, 1);

map<triplet, bool> explored;
queue<nodes*> frontier;
map<triplet, int> frontStates;

vector<nodes> getChildren(nodes* currNode) {
    vector<nodes>  children;
    int sz = 0;
    int m = get<0>(currNode->state);
    int c = get<1>(currNode->state);
    if(get<2>(currNode->state) == 0) {
        triplet childState(0, 0, 1);
        for(int i=0; i<=m; i++){
            for(int j=0; j<=c; j++){
                if(i + j >= 1 && i + j <= 2) {
                    int remM = m - i;
                    int remC = c - j;
                    if((remM == 0) || (remM >= remC)) {
                        get<0>(childState) = remM;
                        get<1>(childState) = remC;
                        children.push_back(nodes());
                        children[sz].state = childState;
                        children[sz].parent = currNode;
                        children[sz].action = make_pair(i, j);
                        
                        sz++;
                    }
                }
            }
        }
    }
    else {
        triplet childState(0, 0, 0);
        int rightM = 3 - m;
        int rightC = 3 - c;
        for(int i=0; i<=rightM; i++){
            for(int j=0; j<=rightC; j++){
                if(i + j >= 1 && i + j <= 2) {
                    int remM = rightM - i;
                    int remC = rightC - j;
                    if((remM == 0) || (remM >= remC)) {
                        get<0>(childState) = m + i;
                        get<1>(childState) = c + j;
                        children.push_back(nodes());
                        children[sz].state = childState;
                        children[sz].parent = currNode;
                        children[sz].action = make_pair(i, j);
                        
                        sz++;
                    }
                }
            }
        }
    }
    return children;
}

int main() {
    
    ios_base::sync_with_stdio(false), cin.tie(0), cout.tie(0);

    
    nodes* root = new nodes();

    
    vector< pair< triplet , pair<int, int> > > moves;

    
    root->state = initState;
    root->parent = NULL;
    root->action = make_pair(0, 0);

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
                    moves.insert(moves.begin(), make_pair(goalState, node->action));
                    while(temp != NULL) {
                        moves.insert(moves.begin(), make_pair(temp->state, temp->action));
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
        cout<<"Total States Visited:\t"<<count<<endl;
        
        cout<<"Moves are:"<<endl;
        cout<<"| LEFT || Boat DIR || RIGHT |"<<endl;
        cout<<"| M  C || M  C DIR || M  C  |"<<endl;
        cout<<"| 3  3 || 0  0     || 0  0  |"<<endl;
        for(int i=0; i<moves.size()-1; i++){
            int lm = get<0>(moves[i].first);
            int lc = get<1>(moves[i].first);
            int bm = moves[(i+1) % moves.size()].second.first;
            int bc = moves[(i+1) % moves.size()].second.second;
            int b = get<2>(moves[i].first);
            string dir = "";
            if(b == 0) {
                dir = "L-R";
                lm -= bm;
                lc -= bc;
            }
            else {
                dir = "R-L";

            }
            int rl = 3 - (bm + lm);
            int rc = 3 - (bc + lc);
            cout<<"| "<<lm<<"  "<<lc<<" || "<<bm<<"  "<<bc<<" "<<dir<<" || "<<rl<<"  "<<rc<<"  |"<<endl;
        }
        cout<<"| "<<0<<"  "<<0<<" || "<<0<<"  "<<0<<"     || "<<3<<"  "<<3<<"  |"<<endl;
        cout<<"Total moves taken:\t"<<moves.size() + 1<<endl;
    }
    return 0;
}