#include "extern.h"
#include "exhsearch.h"

labyrinth::Location mapLocation(const struct CLocation & location) noexcept {
    return labyrinth::Location{location.row, location.column};
}

labyrinth::MazeGraph::InputNode mapNode(const struct CNode & node) noexcept {
    return labyrinth::MazeGraph::InputNode{node.node_id, node.out_paths, node.rotation};
}

labyrinth::MazeGraph mapGraph(struct CGraph graph) {
    const auto num_nodes = graph.extent * graph.extent + 1;
    std::vector<labyrinth::MazeGraph::InputNode> input_nodes;
    input_nodes.reserve(num_nodes);
    for (size_t i = 0; i < num_nodes; ++i) {
        input_nodes.push_back(mapNode(graph.nodes[i]));
    }
    labyrinth::MazeGraph maze_graph{graph.extent, input_nodes};
    for (auto pos = 1; pos < graph.extent; pos += 2) {
        maze_graph.addShiftLocation(labyrinth::Location{0, pos});
        maze_graph.addShiftLocation(labyrinth::Location{graph.extent - 1, pos});
        maze_graph.addShiftLocation(labyrinth::Location{pos, 0});
        maze_graph.addShiftLocation(labyrinth::Location{pos, graph.extent - 1});
    }
    return maze_graph;
}

struct CLocation locationToCLocation(const labyrinth::Location & location) noexcept {
    struct CLocation c_location = {location.getRow(), location.getColumn()};
    return c_location;
}

struct CAction actionToCAction(const labyrinth::exhsearch::PlayerAction & action) {
    struct CAction c_action = {locationToCLocation(action.shift.location), action.shift.rotation, locationToCLocation(action.move_location)};
    return c_action;
}

__declspec(dllexport) struct CAction find_action(struct CGraph cgraph, struct CLocation c_player_location, unsigned int objective_id,
                                                 struct CLocation c_previous_shift_location) {
    std::cout << "Sanity check.." << std::endl;
    std::cout << "cgraph.nodes[0].node_id: " << cgraph.nodes[0].node_id << std::endl;
    std::cout << "cgraph.nodes[0].out_paths: " << +cgraph.nodes[0].out_paths << std::endl;
    std::cout << "cgraph.nodes[0].rotation: " << cgraph.nodes[0].rotation << std::endl;
    auto graph = mapGraph(cgraph);
    auto player_location = mapLocation(c_player_location);
    auto previous_shift_location = mapLocation(c_previous_shift_location);
    auto best_actions = labyrinth::exhsearch::findBestActions(
        graph,
        player_location,
        objective_id,
        previous_shift_location);
    auto best_action = best_actions[0];
    struct CAction action = actionToCAction(best_actions[0]);
    return action;
}
