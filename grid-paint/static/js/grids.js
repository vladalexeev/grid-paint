var gridAttrs={
	"fill":"#f0f0f0",
	"stroke": "#808080"
}

var sin30=Math.sin(Math.PI/6);
var sin60=Math.sin(60/180*Math.PI);
var cos30=Math.cos(30/180*Math.PI);
var cos60=Math.cos(60/180*Math.PI);
var tan30=Math.tan(30/180*Math.PI);
var tan60=Math.tan(60/180*Math.PI);


function GridSquare() {
	this.cellSize=24;
	this.paintGrid=function (paper) {
		for (var y=0; y<=(paper.height-this.cellSize); y+=this.cellSize) {
			for (var x=0; x<=(paper.width-this.cellSize); x+=this.cellSize) {
				var r=paper.rect(x, y, this.cellSize, this.cellSize);
				r.attr(gridAttrs);
			}			
		}
	}
}

function GridTriangle () {
	this.cellSize=24;
	this.paintGrid=function (paper) {
		var rowHeight=this.cellSize*Math.sin(60/180*Math.PI);
		var rowIndex=0;
		for (var y=0; y<(paper.height-rowHeight); y+=rowHeight, rowIndex++) {
			for (var x=0; x<(paper.width-this.cellSize*1.5); x+=this.cellSize) {
				if (rowIndex % 2 == 0) {
					var path1=paper.path(
						"M "+x+" "+(y+rowHeight)+" L "+(x+this.cellSize/2)+" "+y+
						" L "+(x+this.cellSize)+" "+(y+rowHeight)+" Z");
					path1.attr(gridAttrs);
					
					var path2=paper.path(
						"M "+(x+this.cellSize/2)+" "+y+" L "+(x+this.cellSize)+" "+(y+rowHeight)+
						" L "+(x+this.cellSize*1.5)+" "+y+" Z");
					path2.attr(gridAttrs);
				} else {
					var path1=paper.path(
						"M "+x+" "+y+" L "+(x+this.cellSize/2)+" "+(y+rowHeight)+
						" L "+(x+this.cellSize)+" "+y+" Z");
					path1.attr(gridAttrs);
					
					var path2=paper.path(
						"M "+(x+this.cellSize/2)+" "+(y+rowHeight)+" L "+(x+this.cellSize)+" "+y+
						" L "+(x+this.cellSize*1.5)+" "+(y+rowHeight)+" Z");
					path2.attr(gridAttrs);
				}
			}
		}
	}
}

function GridHex() {
	this.cellSize=24;
	this.paintGrid=function(paper) {
	    var paperHeight=paper.height;
	    var paperWidth=paper.width;
		var sideLength=this.cellSize/2;
		var halfHeight=sideLength*sin60;
		var dx=sideLength*cos60;
				/*
		var rowIndex=0;
		for (y=0; y<=(paper.height-2*halfHeight); y+=halfHeight) {
			var x=0;
			if (rowIndex % 2 >0) {
				x=dx+sideLength;
			}
			while (x<=(paper.width-sideLength-2*dx)) {
				var path=paper.path(
					"M "+x+" "+(y+halfHeight)+
					" L "+(x+dx)+" "+y+
					" L "+(x+dx+sideLength)+" "+y+
					" L "+(x+2*dx+sideLength)+" "+(y+halfHeight)+
					" L "+(x+dx+sideLength)+" "+(y+2*halfHeight)+
					" L "+(x+dx)+" "+(y+2*halfHeight)+
					" Z")
				path.attr(gridAttrs);
				x+=2*sideLength+2*dx;
			}
			
			rowIndex++
		}*/

		for (y=0; y<paper.height; y+=halfHeight*2) {
		    var path=paper.path(["M ",dx,y,"H",paper.width]);
		    path.attr({
		        "stroke":"#ff0000",
		    })
		    path.node.setAttribute("stroke-dasharray","12,24");
		}
		
		for (y=halfHeight; y<paper.height; y+=halfHeight*2) {
		    var path=paper.path(["M",2*dx+sideLength,y,"H",paper.width]);
		    path.attr({
                "stroke":"#ff0000",
            })
            path.node.setAttribute("stroke-dasharray","12,24");
		}
		
		var slantedLinesStep=2*dx+2*sideLength;
		var hexBehind=Math.floor(paperHeight/slantedLinesStep);
		
		for (x=dx+sideLength-hexBehind*slantedLinesStep; x<paper.width; x+=slantedLinesStep) {
		    var path=paper.path(["M",x,0,"L",x+paperHeight*tan30,paperHeight]);
            path.attr({
                "stroke":"#ff0000",
            })
            path.node.setAttribute("stroke-dasharray","12,24");
		}
		
		for (x=0-hexBehind*slantedLinesStep; x<paper.width; x+=slantedLinesStep) {
            var path=paper.path(["M",x,halfHeight,"L",x+paperHeight*tan30,halfHeight+paperHeight]);
            path.attr({
                "stroke":"#ff0000",
            })
            path.node.setAttribute("stroke-dasharray","12,24");
        }
        
        for (x=dx+sideLength-hexBehind*slantedLinesStep; x<paper.width; x+=slantedLinesStep) {
            var path=paper.path(["M",x,halfHeight*2,"L",x+paperHeight*tan30,halfHeight*2+paperHeight]);
            path.attr({
                "stroke":"#ff0000",
            })
            path.node.setAttribute("stroke-dasharray","12,24");
        }
        
		
		for (x=dx; x<paper.width+hexBehind*slantedLinesStep; x+=slantedLinesStep) {
            var path=paper.path(["M",x,0,"L",x-paperHeight*tan30,paperHeight]);
            path.attr({
                "stroke":"#ff0000",
            })
            path.node.setAttribute("stroke-dasharray","12,24");
        }
        
        for (x=2*dx+sideLength; x<paper.width+hexBehind*slantedLinesStep; x+=slantedLinesStep) {
            var path=paper.path(["M",x,halfHeight,"L",x-paperHeight*tan30,halfHeight+paperHeight]);
            path.attr({
                "stroke":"#ff0000",
            })
            path.node.setAttribute("stroke-dasharray","12,24");
        }
        
        for (x=dx; x<paper.width+hexBehind*slantedLinesStep; x+=slantedLinesStep) {
            var path=paper.path(["M",x,2*halfHeight,"L",x-paperHeight*tan30,2*halfHeight+paperHeight]);
            path.attr({
                "stroke":"#ff0000",
            })
            path.node.setAttribute("stroke-dasharray","12,24");
        }
	}
}
