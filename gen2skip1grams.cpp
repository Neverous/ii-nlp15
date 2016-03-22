#include <algorithm>
#include <cstdio>
#include <map>
#include <string>
#include <unordered_map>
#include <vector>

char first[1048576];
char second[1048576];
long long int weight;
std::unordered_map<std::string, int> hash;
std::vector<int> sortme;
std::vector<long long int> weights;
std::vector<std::string> map;

bool compareWeights(const int a, const int b)
{
    return weights[a] > weights[b];
}

int main(void)
{
    while(scanf("%lld %s %*s %s ", &weight, first, second) != -1)
    {
        std::string key = first;
        key += " ";
        key += second;

        if(!hash.count(key))
        {
            hash[key] = map.size();
            sortme.push_back(map.size());
            map.push_back(key);
            weights.push_back(weight);
        }

        else
            weights[hash[key]] += weight;
    }

    std::sort(begin(sortme), end(sortme), compareWeights);
    for(const auto &idx: sortme)
        printf("%lld %s\n", weights[idx], map[idx].c_str());

    return 0;
}
