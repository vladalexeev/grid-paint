var sin30=Math.sin(Math.PI/6);
var sin60=Math.sin(60/180*Math.PI);
var cos30=Math.cos(30/180*Math.PI);
var cos60=Math.cos(60/180*Math.PI);
var tan30=Math.tan(30/180*Math.PI);
var tan60=Math.tan(60/180*Math.PI);

var gridLineColor="#d0d0d0";

var gridFactory=[];

function hexToHsl(hex) {
	return Raphael.color(hex);
}

function hslToHex(h,s,l) {
	if (h<0) {
		h=0;
	}
	if (h>1) {
		h=1;
	}
	if (s<0) {
		s=0;
	}
	if (s>1) {
		s=1;
	}
	if (l<0) {
		l=0;
	}
	if (l>1) {
		l=1;
	}
	
	return Raphael.hsl(h,s,l);
}

function GridArtwork() {
    this.cells=[];
    
    // Set item cell to the artwork
    // The function returns artwork item
    // Example {shapeName:"flat", color:"#ff0000", element:[Object]}
    this.setCell=function (col, row, shapeName, color) {
        while (this.cells.length<=row) {
            this.cells[this.cells.length]=[];
        }

        while (this.cells[row].length<=col) {
            this.cells[row][this.cells[row].length]=null;
        }
        
        var oldCell=this.cells[row][col];
        
        
        if (oldCell && oldCell.shapeName==shapeName && oldCell.color==color) {
            return oldCell;
        } else {
        	if (oldCell && oldCell.element) {
        		oldCell.element.remove();
        	}
        	
            this.cells[row][col]= {
                shapeName: shapeName,
                color: color
            }
            return this.cells[row][col];
        }        
    }
}

/*
 * Interface of Grid
 *   function paintGrid(paper) - paints grid on a paper 
 * 
 *   function pointToCell(x,y) - convert mouse coordinates to cell indices.
 *     example of returning object: {col:10, row:15}
 * 
 *   function getShapeRect() - bounding rectangle {w:24, h:24}
 *  
 *   function shapeCenterToBasePoint(x, y) - convert cell center coordinate
 *     to coordinate of base point of cell
 *     example {x:20, y:30}
 * 
 *   function getCellPoint(col, row) - get cell base point by it's column and row
 *     example {x:20, y:30}
 * 
 * 
 *  Interface of Shape
 *   function paint(paper, point{x,y}, color)
 */



function pointToTriangleCoord(x,y,sideLength) {
	var rowHeight=sideLength*sin60;
	var cellY=Math.floor(y/rowHeight);
	    
    var relativeY;
    if (cellY % 2 == 0) {
        relativeY=y-cellY*rowHeight;
    } else {
        relativeY=y-(cellY-1)*rowHeight
    }
	    	    
    var A1=-tan60;
    var B1=-1;
    var C1=-sideLength*sin60;
    var dist1=Math.abs(A1*x+B1*relativeY+C1)/Math.sqrt(A1*A1+B1*B1);
    var d1=Math.floor(dist1/rowHeight)-1;
	    
    var A2=-tan60;
    var B2=1;
    var C2=-3*sideLength*sin60;
    var dist2=Math.abs(A2*x+B2*relativeY+C2)/Math.sqrt(A2*A2+B2*B2);
    var d2=Math.floor(dist2/rowHeight)-1;
        
    return {col:d1+d2, row:cellY}
}

/**
 * get path and center point of triangle by it's cell coordinates 
 * @param {Object} col
 * @param {Object} row
 * @param {Object} sideLength
 * @return array of four points: points [0,1,2] - corners, point[3] - center point
 */
function trianglePath(col, row, sideLength) {
	rowHeight=sideLength*sin60
	x=col*sideLength/2
	y=row*rowHeight;
	if (row % 2 == 0) {
		if (col % 2 == 0) {
			return [
				{x:x, y:y+rowHeight},
				{x:x+sideLength/2, y:y},
				{x:x+sideLength, y:y+rowHeight},
				{x:x+sideLength/2, y:y+rowHeight*2/3}
				]
		} else {
			return [
				{x:x, y:y},
				{x:x+sideLength, y:y},
				{x:x+sideLength/2, y:y+rowHeight},
				{x:x+sideLength/2, y:y+rowHeight/3}
				]
		}
	} else {
		if (col % 2 == 0) {
			return [
				{x:x, y:y},
				{x:x+sideLength, y:y},
				{x:x+sideLength/2, y:y+rowHeight},
				{x:x+sideLength/2, y:y+rowHeight/3}
				]
		} else {
			return [
				{x:x, y:y+rowHeight},
				{x:x+sideLength/2, y:y},
				{x:x+sideLength, y:y+rowHeight},
				{x:x+sideLength/2, y:y+rowHeight*2/3}
				]
		}
	}
}


function GridHex() {
	this.cellSize=24;
	this.name="hex";
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
	
	this.pointToCell=function(x,y) {
		var triangleCell=pointToTriangleCoord(x,y,this._sideLength);
		if (triangleCell.col<0) {
			return {col:-1, row:-1};
		}
		
		if (triangleCell.row % 2 == 0) {
			var triada=Math.floor(triangleCell.col/3);
			if (triada % 2 == 0) {
				return {col:triada, row: Math.floor(triangleCell.row / 2)}
			} else {
				return {col: triada, row: Math.floor(triangleCell.row / 2) - 1}
			}
		} else {
			var triada=Math.floor(triangleCell.col/3);
			if (triada % 2 == 0) {
				return {col: triada, row: Math.floor(triangleCell.row/2)}
			} else {
				return {col: triada, row: Math.floor(triangleCell.row/2)}
			}
		}
	}
	
	this.shapes=[];
}

// Register grid
gridFactory["hex"]=function() {
	return new GridHex();
}

