// based on template at https://www.d3-graph-gallery.com/graph/lollipop_ordered.html

function JohariQuad(tag, quadrant, themeColor) {

    // set the dimensions and margins of the graph
    var margin = { top: 10, right: 30, bottom: 40, left: 100 },
        width = 460 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select(tag)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // Parse the Data
    d3.json(, function (data) {

        // sort data
        data.sort(function (b, a) {
            return a.Value - b.Value;
        });

        // Add X axis
        var x = d3.scaleLinear()
            .domain([0, 13000])
            .range([0, width]);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))
            .selectAll("text")
            .attr("transform", "translate(-10,0)rotate(-45)")
            .style("text-anchor", "end");

        // Y axis
        var y = d3.scaleBand()
            .range([0, height])
            .domain(data.map(function (d) { return d.Country; }))
            .padding(1);
        svg.append("g")
            .call(d3.axisLeft(y))

        // Lines
        svg.selectAll("myline")
            .data(data)
            .enter()
            .append("line")
            .attr("x1", function (d) { return x(d.Value); })
            .attr("x2", x(0))
            .attr("y1", function (d) { return y(d.Country); })
            .attr("y2", function (d) { return y(d.Country); })
            .attr("stroke", "grey")

        // Circles
        svg.selectAll("mycircle")
            .data(data)
            .enter()
            .append("circle")
            .attr("cx", function (d) { return x(d.Value); })
            .attr("cy", function (d) { return y(d.Country); })
            .attr("r", "7")
            .style("fill", "#69b3a2")
            .attr("stroke", "black")
    })
}

function renderQuad() {
       d3.json('/get_johari_data/').then(function (data) {
      // get data and create visualization
      // Promise Pending
      const dataPromise = d3.json('/get_johari_data/');
      
      console.log("Data Promise: ", dataPromise);
      console.log(data)
      // Sort 
      var arenaData = data.Arena.sort((a, b) => b.Counts - a.Counts)
      var facadeData = data.Facade.sort((a, b) => b.Counts - a.Counts)
      var blindspotData = data.BlindSpot.sort((a, b) => b.Counts - a.Counts)
      var unknownData = data.Unknown.sort((a, b) => b.Counts - a.Counts)
      // create a linear scale to limit font size choices for the word cloud
      JohariQuad("#Arena",arenaData,"green")
      JohariQuad("#BlindSpot",blindspotData,"yellow")
      JohariQuad("#Facade",facadeData,"orange")
      JohariQuad("#Unknown",unknownData,"red")
    })
  }