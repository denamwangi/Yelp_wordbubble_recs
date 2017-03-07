var width = 500,
    height = 500,
    padding = 8, // separation between same-color nodes
    clusterPadding = 6, // separation between different-color nodes
    maxRadius = 10;

var color = d3.scale.ordinal()
      .range([ "#d9534f", "#E4002B",  "#7A99AC"]);


// Loop through the array of keyword items (each is a string) and 
// These will need to be pulled from each business object eventually


function multiD3(data, div_assign) {
    d3.text(data, function(error, text) {

      data.forEach(function(d) {
                        console.log(d);
                        d.size = +d.size;
      });

    // debugger;
    //unique cluster/group id's
    var cs = [];
    data.forEach(function(d){
            if(!cs.contains(d.group)) {
                cs.push(d.group);
                // cs.push(1);
            }
    });

    var n = data.length, // total number of nodes.              Add number of keywords
        m = cs.length; // number of distinct clusters           Keep this to 1
        // m=1
    //create clusters and nodes
    var clusters = new Array(m);
    var nodes = [];
    for (var i = 0; i<n; i++){
        nodes.push(create_nodes(data,i));
    }

    var force = d3.layout.force()
        .nodes(nodes)
        .size([width, height])
        .gravity(0.02)
        .charge(0)
        .on("tick", tick)
        .start();

    var svg = d3.select("#"+div_assign).append("svg")
        .attr("width", width)
        .attr("height", height);


    var node = svg.selectAll("circle")
        .data(nodes)
        .enter().append("g").call(force.drag);


    node.append("circle")
        .style("fill", function (d) {
        return color(d.cluster);                       // make color constant
        })
        .attr("r", function(d){return d.radius;});     //Radius is clculated below
        

    node.append("text")
          .attr("dy", ".3em")
          .style("text-anchor", "middle")
          .style('fill', 'black')
          .text(function(d) {
            var splitText= d.text.split(" ", 2);
            if (splitText[1]) {
                // return splitText[0] + "\n"+splitText[1];
                return splitText[0] +' '+splitText[1];
            } else {
                return splitText[0];
            }


            });
          // .text(function(d) { return d.text.substring(0, d.radius / 3); });   //dynamically pull # of chars. Change this to ensure we get the whole thing. Dynamically change the text size? 


    function create_nodes(data,node_counter) {
        var unscaled_radius=parseInt(data[node_counter].size);
        var scale_radius= parseInt(data[node_counter].size);
        if (unscaled_radius>1000){
            console.log("Before:",scale_radius);
            scale_radius=unscaled_radius/50;
            console.log("After:",scale_radius)
         }
        if (unscaled_radius<=20){

            scale_radius=data[node_counter].size*2;
         }
        if (unscaled_radius>20 && unscaled_radius<1000 ){

            scale_radius=unscaled_radius/5;
         }
         console.log(scale_radius)
          var i = cs.indexOf(data[node_counter].group),
          r = Math.sqrt((i + 1) / m * -Math.log(Math.random())) * maxRadius,
          

          d = {
            cluster: i,
            // radius: data[node_counter].size*1.5,
            radius: scale_radius,
            text: data[node_counter].text,
            x: Math.cos(i / m * 2 * Math.PI) * 200 + width / 2 + Math.random(),
            y: Math.sin(i / m * 2 * Math.PI) * 200 + height / 2 + Math.random()
          };
      if (!clusters[i] || (r > clusters[i].radius)) clusters[i] = d;
      return d;
    }



    function tick(e) {
        node.each(cluster(10 * e.alpha * e.alpha))
            .each(collide(0.5))
        .attr("transform", function (d) {
            var k = "translate(" + d.x + "," + d.y + ")";
            return k;
        });
    }

    // Move d to be adjacent to the cluster node.
    function cluster(alpha) {
        return function (d) {
            var cluster = clusters[d.cluster];
            if (cluster === d) return;
            var x = d.x - cluster.x,
                y = d.y - cluster.y,
                l = Math.sqrt(x * x + y * y),
                r = d.radius + cluster.radius;
            if (l != r) {
                l = (l - r) / l * alpha;
                d.x -= x *= l;
                d.y -= y *= l;
                cluster.x += x;
                cluster.y += y;
            }
        };
    }

    // Resolves collisions between d and all other circles.
    function collide(alpha) {
        var quadtree = d3.geom.quadtree(nodes);
        return function (d) {
            var r = d.radius + maxRadius + Math.max(padding, clusterPadding),
                nx1 = d.x - r,
                nx2 = d.x + r,
                ny1 = d.y - r,
                ny2 = d.y + r;
            quadtree.visit(function (quad, x1, y1, x2, y2) {
                if (quad.point && (quad.point !== d)) {
                    var x = d.x - quad.point.x,
                        y = d.y - quad.point.y,
                        l = Math.sqrt(x * x + y * y),
                        r = d.radius + quad.point.radius + (d.cluster === quad.point.cluster ? padding : clusterPadding);
                    if (l < r) {
                        l = (l - r) / l * alpha;
                        d.x -= x *= l;
                        d.y -= y *= l;
                        quad.point.x += x;
                        quad.point.y += y;
                    }
                }
                return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
            });
        };
    }

    });

    Array.prototype.contains = function(v) {
        for(var i = 0; i < this.length; i++) {
            if(this[i] === v) return true;
        }
        return false;
    };
}
