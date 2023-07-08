<script>
    import * as d3 from "d3";
    import PosterGlyph from "../components/PosterGlyph.svelte";
    import PosterLegendTable from "../components/PosterLegendTable.svelte";

    export let data;  // output of +page.js.load()

    let selectedTimeslot = "None";

    let dRooms = data.rooms;
    let dGraph = data.graph;
    
    let roomNames = Object.keys(dRooms.originMiddle);

    let roomSizes = computeRoomSizes(dRooms);
    let postersPerRoom = findPostersPerRoom(dGraph);

    function euclidean(a, b) {
        let sum = 0;

        if (a.length !== b.length) {
            throw Error("unequal sizes");
        }

        for (let i = 0; i < a.length; i++) {
            sum += Math.pow(a - b, 2);
        }

        return Math.sqrt(sum);
    }

    // returns a order of pairs to connect all points
    function getRoomOrderNextNeighbor(rooms) {
        let pairwiseDistances = [];

        for (let i = 0; i < rooms.length; i++) {
            let row = [];
            for (let j = 0; j < rooms.length; j++) {
                row.push(0);
            }
            pairwiseDistances.push(row);
        }

        for (let i = 0; i < rooms.length; i++) {
            for (let j = 0; j < i - 1; j++) {
                pairwiseDistances[i][j] = euclidean(rooms[i].doorPosition, rooms[j].doorPosition);
            }
        }

        // TOOD: continue
    }

    // computes room sizes from origin middle and bottom left corner
    function computeRoomSizes(rooms) {
        let sizes = {};

        for (let i = 0; i < roomNames.length; i++) {
            let roomName = roomNames[i];
            
            let width = 2 * (rooms.originMiddle[roomName][0] - rooms.originBottomLeftCorner[roomName][0]);
            let height = 2 * (rooms.originMiddle[roomName][1] - rooms.originBottomLeftCorner[roomName][1]);
            
            sizes[roomName] = {
                width: width,
                height: height
            };
        }

        return sizes;
    }

    // find all posters from rooms
    function findPostersPerRoom(graph) {
        let postersPerRoom = {};

        for (let i = 0; i < roomNames.length; i++) {
            postersPerRoom[roomNames[i]] = {
                roomInfo: undefined,
                posters: []
            };
        }

        graph.links.forEach(element => {
            let sourceRoom;
            let targetPoster;

            if (element.source.startsWith("room") && element.target.startsWith("poster")) {
                // find room object and poster object
                // find room if not yet available
                sourceRoom = graph.nodes.find((node) => {
                    return node.id === element.source;
                });

                targetPoster = graph.nodes.find((node) => {
                    return node.id === element.target;
                })

                if (!sourceRoom || !targetPoster) {
                    throw Error("couldn't find poster or room for link:", element);
                }

                postersPerRoom[sourceRoom.room_name].roomInfo = sourceRoom;
                postersPerRoom[sourceRoom.room_name].posters.push(targetPoster);
            } else {
                // ignore
                return
            }
        });

        return postersPerRoom;
    }

    // create scales
    let minXPos = d3.min(roomNames, (name) => dRooms.originBottomLeftCorner[name][0]);
    let maxXPos = d3.max(roomNames, (name) => dRooms.originBottomLeftCorner[name][0] + roomSizes[name].width);

    let minYPos = d3.min(roomNames, (name) => dRooms.originBottomLeftCorner[name][1]);
    let maxYPos = d3.max(roomNames, (name) => dRooms.originBottomLeftCorner[name][1] + roomSizes[name].height);

    let totalHeightRooms = maxYPos - minYPos;
    let totalWidthRooms = maxXPos - minXPos;
    
    let trueAspectRatio = totalHeightRooms / totalWidthRooms;

    let canvasWidth = 1000;
    let canvasHeight = canvasWidth * trueAspectRatio;

    /*
    let spacingX = 0.1;
    let spacingY = 0.05;

    totalHeightRooms = totalHeightRooms * spacingY + totalHeightRooms;
    totalWidthRooms = totalWidthRooms * spacingX + totalWidthRooms;

    let xPositionScale = d3.scaleLinear().domain([]).range([0, canvasWidth]);
    */

    let xScale = d3.scaleLinear().domain([0, totalWidthRooms]).range([0, canvasWidth]);
    let yScale = d3.scaleLinear().domain([0, totalHeightRooms]).range([0, canvasHeight]);
</script>

<div>
    <!--p>
        {JSON.stringify(dGraph)};
    </p-->
    <svg class="svg-layout" width={canvasWidth} height={canvasHeight}>
        <!-- Place rooms as rounded rects -->
        {#each Object.keys(roomSizes) as room}
            <rect x={xScale(dRooms.originBottomLeftCorner[room][0])} y={canvasHeight - yScale(dRooms.originBottomLeftCorner[room][1]) - yScale(roomSizes[room].height)} width={xScale(roomSizes[room].width)} height={yScale(roomSizes[room].height)} fill={d3.rgb(125, 125, 125, 0.3)} rx=10 stroke="black"></rect>
        
            <!-- Place posters in room -->
            <g transform="translate({xScale(dRooms.originBottomLeftCorner[room][0]) + 0.5 * xScale(roomSizes[room].width)} {canvasHeight - yScale(dRooms.originBottomLeftCorner[room][1]) - 0.5 * yScale(roomSizes[room].height)})">
                {#each postersPerRoom[room].posters.filter(p => p.timeslot === selectedTimeslot) as poster}
                    <PosterGlyph xpos={xScale(poster.pos[0])}, ypos={yScale(poster.pos[1])} keywords={[poster.kw_1, poster.kw_2]}></PosterGlyph>
                    <!--circle rx=0 ry=0 r=5 fill="black">

                    </circle-->
                {/each}
            </g>

            <!-- Place Door Knob -->
            <!--circle x={xScale(dRooms.doorknob[room].x)} y={yScale(dRooms.doorknob[room].y)} fill="green">
            </circle-->

            <!-- Connect Door Knobs -->

        {/each}
    </svg>

    <div class="poster-legend">
        <PosterLegendTable posters={postersPerRoom} timeslot={selectedTimeslot}></PosterLegendTable>
        <!--svg width=500 height=300></svg-->
    </div>
</div>

<style>
    .svg-layout {
        border: 1px black solid;
    }

    .poster-legend {
        position: absolute;
        left: 475px;
        top: 25px;
        background: black;
    }
</style>

