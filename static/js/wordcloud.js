// Gets the width of text in pixels to create "impact boxes" around text in cloud to enable listening for user click events.
function getTextWidth(text, font) {
  var canvas = getTextWidth.canvas || (getTextWidth.canvas = document.createElement("canvas"));
  var context = canvas.getContext("2d");
  context.font = font;
  var metrics = context.measureText(text);
  return metrics.width;
}

//https://stackoverflow.com/questions/7128675/from-green-to-red-color-depend-on-percentage
// creates a green to red gradient (based on the Word Score of usage in positive conext vs pos/neg)
// function getGreenToRed(percent) {
//   r = percent < 50 ? 255 : Math.floor(255 - (percent * 2 - 100) * 255 / 100);
//   g = percent > 50 ? 255 : Math.floor((percent * 2) * 255 / 100);
//   return 'rgb(' + r + ',' + g + ',0)';
// }

function wordCloud(tag,quadrant,fontcolor) {
var wordSize = d3.scaleSqrt()
      .domain(d3.extent(quadrant.map(d => d.Counts)))
      .range([15, 30])
    // For testing. Create a list of possible colors for the words in the cloud.
    // var colorList = ["Blue",
    //   "Red",
    //   "Maroon",
    //   // "Yellow",
    //   "Olive",
    //   "Lime",
    //   "Green",
    //   "Aqua",
    //   "Teal",
    //   "Navy",
    //   "Fuchsia",
    //   "Purple",
    //   "lightgray",
    //   "Black",
    // ]

    // set the dimensions and margins of the graphic
    var margin = { top: 20, right: 10, bottom: 10, left: 10 },
      width = 285 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

    // // append the svg object to the body of the page
    var svg = d3.select(tag).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")")
      ;

    // // Constructs a new cloud layout instance. It runs an algorithm to find the position of words that suits requirements
    // // Wordcloud features that are different from one word to the other must be here
    var layout = d3.layout.cloud()
      .size([width- margin.right, height])
      .words(quadrant.map(function (d) {
        return {
          text: d.Adj,
          size: wordSize(d.Counts),
          wordCount: d.Counts,
          percent: d.Percent,
        };
      }))
      .padding(5)        //space between words
      .rotate(0)
      // .rotate(function () { return ~~(Math.random() * 2) * 90; })
      .fontSize(function (d) { return d.size; })      // font size of words
      .on("end", draw);
    layout.start();
      
    // // This function takes the output of 'layout' above and draw the words
    // // Wordcloud features that are THE SAME from one word to the other can be here
    function draw(words) {
      console.log(words)
      svg
        .append("g")
        .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
        .selectAll("text")
        .data(words)
        .enter().append("text")
        .style("font-size", function (d) { return d.size; })
        .style("fill", fontcolor)
        // .style("fill", function (d) { return getGreenToRed(d.Percent * 100) })
        .attr("stroke", "black")
        .attr("stroke-width", 1.5)
        .attr("text-anchor", "start")
        .attr("dominant-baseline", "hanging") // to get rectangles and text to rotate same
        .style("font-family", "Impact")
        .attr("transform", function (d) {
          return "translate(" + [d.x, d.y]
            + ")rotate(" + d.rotate + ")";
        })
        .text(function (d) { return d.text; })
      console.log(words)
      svg
        .append("g")
        .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
        .selectAll("dot")
        .data(words)
        .enter().append("rect")
        .attr("width", function (d) { return 0.8 * getTextWidth(d.text, d.size + "pt Impact") })
        .attr("height", function (d) { return d.size })
        .style("opacity", 0)
        .attr("transform", function (d) {
          return "translate(" + [d.x, d.y]
            + ")rotate(" + d.rotate + ")";
        })
        .on("click", function (d) {
          d3.select("#DataArea0").html(
            `Word: <strong>${d.text}</strong> <br>
            
            Observations: ${d.wordCount}<br>
            Observations vs Total Observers: ${(d.percent * 100).toFixed(0)}%`
            )})
          

      //     Object.entries(d.links).forEach(([key, value]) => {
      //       var option = d3.select("#wordcloud_news").append("ul");
      //       var item = option.append("li");
      //       item.html(`<${value[1]}>[${value[1]}] <a href="https://${value[0]}">${key}  </a>`);
      //     })
          
      //   })
      // d3.select("#wordcloud_sentiment").html("")
      // d3.select("#wordcloud_sentiment").html(
      //   `Overall Article Positivity: <strong>${(data[0].Pos_Neg * 100).toFixed(0)}%</strong>`)
    }

  }
function renderCloud() {
  // // Display text to let the user know dataset is being generated.
  // d3.select("#wordcloud_sentiment").html(
  //   `Collecting News from the Web...`)
  // //clear the visualization and the list if existing
  // d3.select("#wordcloud").html("")
  // d3.select("#wordcloud_news").html("")

  ///////////////////DATA VISUALIZATION/////////////////
  // Final
  d3.json('/get_cloud_data/').then(function (data) {
    // get data and create wordcloud
    // Promise Pending
    const dataPromise = d3.json('/get_cloud_data/');
    
    console.log("Data Promise: ", dataPromise);
    console.log(data)
    // Sort and use only the top 50 words
    var arenaData = data.Arena.sort((a, b) => b.Counts - a.Counts)
    var facadeData = data.Facade.sort((a, b) => b.Counts - a.Counts)
    var blindspotData = data.BlindSpot.sort((a, b) => b.Counts - a.Counts)
    var unknownData = data.Unknown.sort((a, b) => b.Counts - a.Counts)
    // create a linear scale to limit font size choices for the word cloud
    wordCloud("#Arena",arenaData,"green")
    wordCloud("#BlindSpot",facadeData,"yellow")
    wordCloud("#Facade",blindspotData,"orange")
    wordCloud("#Unknown",unknownData,"red")
  })
}

