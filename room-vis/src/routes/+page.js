export async function load() {
    return {
        rooms: await fetch("data/roomlayout.json").then(data => data.json()),
    };
}

// graph: await d3.load("static/data/graph-layout.json")
