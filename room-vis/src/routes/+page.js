export async function load() {
    return {
        rooms: await fetch("data/roomlayout.json").then(data => data.json()),
        graph: await fetch("data/graph_with_random_poster_assignment.json").then(data => data.json())
    };
}
