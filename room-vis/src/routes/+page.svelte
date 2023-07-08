<script>
    import * as d3 from "d3";

    export let data;  // output of +page.js.load()
    
    let roomSizes = computeRoomSizes(data.rooms);

    // computes room sizes from origin middle and bottom left corner
    function computeRoomSizes(rooms) {
        let sizes = {};

        let roomNames = Object.keys(rooms.originMiddle);

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

    // create scales
    let totalHeightRooms = roomSizes["Bad Boll"].height + roomSizes["Potsdam"].height;
    let totalWidthRooms = roomSizes["Lüneburg"].width + roomSizes["Hermannsburg"].width + roomSizes["Potsdam"].width;
    
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
    <p>
        {JSON.stringify(roomSizes)};
    </p>
    <svg class="svg-layout" width={canvasWidth} height={canvasHeight}>
        <!-- Place rooms as rounded rects -->
        {#each Object.keys(roomSizes) as room}
            <rect x={xScale(data.rooms.originBottomLeftCorner[room][0])} y={canvasHeight - yScale(data.rooms.originBottomLeftCorner[room][1]) - yScale(roomSizes[room].height)} width={xScale(roomSizes[room].width)} height={yScale(roomSizes[room].height)} fill="grey" rx=10 stroke="black"></rect>
        {/each}
    </svg>
</div>




<style>
    .svg-layout {
        border: 1px black solid;
    }
</style>

