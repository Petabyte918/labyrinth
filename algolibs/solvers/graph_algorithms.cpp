#include "graph_algorithms.h"

#include <limits>
#include <queue>
#include <unordered_map>

namespace labyrinth {
namespace reachable {

bool isReachable(const MazeGraph& graph, const Location& source, const Location& target) {
    std::queue<Location> q;
    std::vector<bool> visited(graph.getNumberOfNodes(), false);
    q.push(source);
    while (!q.empty()) {
        auto location = q.front();
        if (location == target) {
            return true;
        }
        q.pop();
        visited[graph.getNode(location).node_id] = true;
        for (auto neighbor_it = graph.neighbors(location); !neighbor_it.isAtEnd(); ++neighbor_it) {
            if (!visited[graph.getNode(*neighbor_it).node_id]) {
                q.push(*neighbor_it);
            }
        }
    }
    return false;
}

std::vector<Location> reachableLocations(const MazeGraph& graph, const Location& source) {
    std::queue<Location> q;
    std::vector<bool> visited(graph.getNumberOfNodes(), false);
    q.push(source);
    visited[graph.getNode(source).node_id] = true;
    std::vector<Location> result;
    result.reserve(graph.getNumberOfNodes());
    while (!q.empty()) {
        auto location = q.front();
        result.push_back(location);
        q.pop();
        visited[graph.getNode(location).node_id] = true;
        for (auto neighbor_it = graph.neighbors(location); !neighbor_it.isAtEnd(); ++neighbor_it) {
            if (!visited[graph.getNode(*neighbor_it).node_id]) {
                q.push(*neighbor_it);
            }
        }
    }
    return result;
}

std::vector<ReachableNode> multiSourceReachableLocations(const MazeGraph& graph, const std::vector<Location>& sources) {
    constexpr size_t no_parent = std::numeric_limits<size_t>::max();
    std::vector<ReachableNode> result;
    result.reserve(sources.size());
    std::vector<size_t> parent_indices(graph.getNumberOfNodes(), no_parent);
    std::queue<Location> q;
    for (size_t i = 0; i < sources.size(); ++i) {
        q.push(sources[i]);
        parent_indices[graph.getNode(sources[i]).node_id] = i;
        result.emplace_back(i, sources[i]);
    }
    while (!q.empty()) {
        auto location = q.front();
        auto parent_index = parent_indices[graph.getNode(location).node_id];
        q.pop();
        for (auto neighbor_it = graph.neighbors(location); !neighbor_it.isAtEnd(); ++neighbor_it) {
            if (no_parent == parent_indices[graph.getNode(*neighbor_it).node_id]) {
                parent_indices[graph.getNode(*neighbor_it).node_id] = parent_index;
                q.push(*neighbor_it);
                result.emplace_back(parent_index, *neighbor_it);
            }
        }
    }
    return result;
}

} // namespace reachable
} // namespace labyrinth
