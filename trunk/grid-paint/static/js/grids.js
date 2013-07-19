var sin30=Math.sin(Math.PI/6);
var sin60=Math.sin(60/180*Math.PI);
var cos30=Math.cos(30/180*Math.PI);
var cos60=Math.cos(60/180*Math.PI);
var tan30=Math.tan(30/180*Math.PI);
var tan60=Math.tan(60/180*Math.PI);

/*
 * Interface of Grid
 *   function paintGrid(paper) - paints grid on a paper 
 * 
 *   function pointToCell(x,y) - convert mouse coordinates to cell indices.
 *     example of returning object: {col:10, row:15} 
 * 
 *   Yet unimplemented 
 * -------------------
 *   function cellCenterPoint(column, row) - convert cell coordinate
 *     to coordinate of a center point of cell
 */


function GridSquare() {
	this.cellSize=24;
	
	this._createGridLine=function(paper, pathArray) {
		var path=paper.path(pathArray);
        path.attr({
            "stroke":"#d0d0d0",
        })
	}
	
	this.paintGrid=function (paper) {
		for (var y=0; y<paper.height; y+=this.cellSize) {
			this._createGridLine(paper,["M",0,y,"L",paper.width,y]);
		}
		
		for (var x=0; x<paper.width; x+=this.cellSize) {
			this._createGridLine(paper,["M",x,0,"L",x,paper.height]);
		}			
		
	}
	
	this.pointToCell=function(x,y) {
        var cellX=Math.floor(x/this.cellSize);
        var cellY=Math.floor(y/this.cellSize);	    
        return {col: cellX, row: cellY};
	}
}

function GridTriangle () {
	this.cellSize=24;
	this._rowHeight=this.cellSize*sin60;
	
	this._createGridLine=function(paper, pathArray) {
		var path=paper.path(pathArray);
        path.attr({
            "stroke":"#d0d0d0",
        })
	}
		
	this.paintGrid=function (paper) {
		var trianglesBehind=Math.floor(paper.height/this.cellSize)
				
		for (var y=0; y<paper.height; y+=2*this._rowHeight) {
			this._createGridLine(paper,["M",this.cellSize*sin30,y,"H",paper.width]);
		}
		
		for (var y=this._rowHeight; y<paper.height; y+=2*this._rowHeight) {
			this._createGridLine(paper,["M",0,y,"H",paper.width]);
		}
		
		for (var x=this.cellSize/2-trianglesBehind*this.cellSize; x<paper.width; x+=this.cellSize) {
			this._createGridLine(paper,["M",x,0,"L",x+paper.height*tan30,paper.height]);
		}
		
		for (var x=this.cellSize/2; x<paper.width+trianglesBehind*this.cellSize; x+=this.cellSize) {
			this._createGridLine(paper,["M",x,0,"L",x-paper.height*tan30,paper.height]);
		}
	}
	
	this.pointToCell=function(x,y) {
	    var cellY=Math.floor(y/this._rowHeight);
	    
	    var relativeY;
	    if (cellY % 2 == 0) {
	        relativeY=y-cellY*this._rowHeight;
	    } else {
	        relativeY=y-(cellY-1)*this._rowHeight
	    }
	    	    
	    var A1=-tan60;
	    var B1=-1;
	    var C1=-this.cellSize*sin60;
	    var dist1=Math.abs(A1*x+B1*relativeY+C1)/Math.sqrt(A1*A1+B1*B1);
	    var d1=Math.floor(dist1/this._rowHeight)-1;
	    
        var A2=-tan60;
        var B2=1;
        var C2=-3*this.cellSize*sin60;
        var dist2=Math.abs(A2*x+B2*relativeY+C2)/Math.sqrt(A2*A2+B2*B2);
        var d2=Math.floor(dist2/this._rowHeight)-1;
        
        $("#test").append("rowHeight="+this._rowHeight+"<br>");
        $("#test").append("dist1="+dist1+" dist2="+dist2+"<br>");
        $("#test").append("d1="+d1+" d2="+d2+"<br>");	    
	    
	    return {col:d1+d2, row:cellY}
	}
}

function GridHex() {
	this.cellSize=24;
	this._sideLength=this.cellSize/2;
	this._stroke_dash_array=this._sideLength+","+this.cellSize;
	
	this._createGridLine=function(paper, pathArray) {
		var path=paper.path(pathArray);
        path.attr({
            "stroke":"#d0d0d0",
        })
        path.node.setAttribute("stroke-dasharray",this._stroke_dash_array);
	}
	
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
		    this._createGridLine(paper,["M ",dx,y,"H",paper.width]);
		}
		
		for (y=halfHeight; y<paper.height; y+=halfHeight*2) {
		    this._createGridLine(paper,["M",2*dx+sideLength,y,"H",paper.width]);
		}
		
		var slantedLinesStep=2*dx+2*sideLength;
		var hexBehind=Math.floor(paperHeight/slantedLinesStep);
		
		for (x=dx+sideLength-hexBehind*slantedLinesStep; x<paper.width; x+=slantedLinesStep) {
		    this._createGridLine(paper,["M",x,0,"L",x+paperHeight*tan30,paperHeight]);
		}
		
		for (x=0-hexBehind*slantedLinesStep; x<paper.width; x+=slantedLinesStep) {
            this._createGridLine(paper,["M",x,halfHeight,"L",x+paperHeight*tan30,halfHeight+paperHeight]);
        }
        
        for (x=dx+sideLength-hexBehind*slantedLinesStep; x<paper.width; x+=slantedLinesStep) {
            this._createGridLine(paper,["M",x,halfHeight*2,"L",x+paperHeight*tan30,halfHeight*2+paperHeight]);
        }
        
		
		for (x=dx; x<paper.width+hexBehind*slantedLinesStep; x+=slantedLinesStep) {
            this._createGridLine(paper,["M",x,0,"L",x-paperHeight*tan30,paperHeight]);
        }
        
        for (x=2*dx+sideLength; x<paper.width+hexBehind*slantedLinesStep; x+=slantedLinesStep) {
            this._createGridLine(paper,["M",x,halfHeight,"L",x-paperHeight*tan30,halfHeight+paperHeight]);
        }
        
        for (x=dx; x<paper.width+hexBehind*slantedLinesStep; x+=slantedLinesStep) {
            this._createGridLine(paper,["M",x,2*halfHeight,"L",x-paperHeight*tan30,2*halfHeight+paperHeight]);
        }
	}
}
