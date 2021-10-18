// based on template at https://www.d3-graph-gallery.com/graph/lollipop_ordered.html

function JohariQuad(tag, quadrant, themeColor, num_obs, num_adj, winColor, title) {

    // set the dimensions and margins of the graph
    var margin = { top: 40, right: 30, bottom: 40, left: 100 }
    width = 400 - margin.left - margin.right,
    height = 550 - margin.top - margin.bottom;

    // append the svg object to the body of the page


    var svg = d3.select("#" + tag)
        .append("svg")
        // .attr("width", width + margin.left + margin.right)
        // .attr("height", height + margin.top + margin.bottom)
        .attr("viewBox", [0, 0, (width + margin.right + margin.left),
            (height + margin.top + margin.bottom)].join(' '))
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")")
        .attr("overflow", "visible")
    // .attr("border",1);

    // var borderPath = svg.append("rect")
    // .attr("x", 0)
    // .attr("y", 0)
    // .attr("height", 500)
    // .attr("width", 400)
    // .style("stroke", "black")
    // .style("fill", "none")
    // .style("stroke-width", 1);
    // Parse the Data
    // d3.json('/get_johari_data/').then(function (data) {
    //     const dataPromise = d3.json('/get_johari_data/');
    //     console.log("Data Promise: ", dataPromise);

    //     // console.log(data)


    // scale adjective font size labels
    var labelSize = d3.scaleLinear()
        .domain([56, 0])
        .range([8, 16]);
    // Add title
    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .attr("class", "h4")
        .text(title)
        ;
    //     // Add X axis
    var x = d3.scaleLinear()
        .domain([0, num_obs])
        .range([0, width]);

    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickFormat(function (e) {
            if (Math.floor(e) != e) {
                return;
            }

            return e;
        }))
        .selectAll("text")
        // .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

    // Y axis
    var y = d3.scaleBand()
        .range([0, height])
        .domain(quadrant.map(function (d) { return d.adj; }))
        .padding(1);
    svg.append("g")
        .call(d3.axisLeft(y))
        .style("font", labelSize(num_adj) + "px times")

    // Lines
    svg.selectAll("myline")
        .data(quadrant)
        .enter()
        .append("line")
        .attr("x1", function (d) { return x(d.obsCount); })
        .attr("x2", x(0))
        .attr("y1", function (d) { return y(d.adj); })
        .attr("y2", function (d) { return y(d.adj); })
        .attr("stroke", "grey")

    // Circles
    svg.selectAll("mycircle")
        .data(quadrant)
        .enter()
        .append("circle")
        .attr("cx", function (d) { return x(d.obsCount); })
        .attr("cy", function (d) { return y(d.adj); })
        .attr("r", "7")
        .style("fill", themeColor)
        .attr("stroke", "black")

    d3.select("#" + tag)
        .on('click', function () {
            // Get the d3js SVG element and save using saveSvgAsPng.js
            saveSvgAsPng(document.getElementById(tag).getElementsByTagName('svg')[0],
                "plot.png", { scale: 2, backgroundColor: winColor });
        }
        )
}

function renderQuad() {
    d3.json('/get_johari_data/').then(function (data) {
        // get data and create visualization
        // Promise Pending
        const dataPromise = d3.json('/get_johari_data/');

        console.log("Data Promise: ", dataPromise);
        //   console.log(data)
        // Sort 
        var arenaData = data.Arena.sort((a, b) => b.obsCount - a.obsCount)
        console.log(data.Blindspot)
        var blindspotData = data.Blindspot.sort((a, b) => b.obsCount - a.obsCount)
        var facadeData = data.Facade.sort((a, b) => b.obsCount - a.obsCount)
        var unknownData = data.Unknown.sort((a, b) => b.obsCount - a.obsCount)
        var num_obs = data.num_obs
        // create a linear scale to limit font size choices for the word cloud
        JohariQuad("Arena", arenaData, "green", num_obs, arenaData.length, "rgb(183, 198, 228)", "Arena (observed by self and by others)")
        JohariQuad("Blindspot", blindspotData, "yellow", num_obs, blindspotData.length, "rgb(241, 204, 177)", "Blind Spot (observed by others only)")
        JohariQuad("Facade", facadeData, "orange", num_obs, facadeData.length, "rgb(251, 230, 162)", "Facade (observed by self only)")
        JohariQuad("Unknown", unknownData, "red", num_obs, unknownData.length, "rgb(195, 195, 195)", "Unknown (not observed)")
    })
}

renderQuad()