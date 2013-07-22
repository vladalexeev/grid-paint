var sin30=Math.sin(Math.PI/6);
var sin60=Math.sin(60/180*Math.PI);
var cos30=Math.cos(30/180*Math.PI);
var cos60=Math.cos(60/180*Math.PI);
var tan30=Math.tan(30/180*Math.PI);
var tan60=Math.tan(60/180*Math.PI);

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
    this.items=[];
    
    // Set item cell to the artwork
    // The function returns artwork item
    // Example {shapeName:"flat", color:"#ff0000", element:[Object]}
    this.setItem=function (col, row, shapeName, color) {
        while (this.items.length<row) {
            this.items[this.items.length]=[];
        }

        var oldItem=this.items[row][col];
        if (oldItem && oldItem.shapeName==shapeName && oldItem.color==color) {
            return oldItem;
        } else {
            this.items[row][col]= {
                shapeName: shapeName,
                color: color
            }
            return this.items[row][col];
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
	
	this.getShapeRect=function() {
		return {w:this.cellSize, h:this.cellSize};
	}
	
	this.pointToCell=function(x,y) {
        var cellX=Math.floor(x/this.cellSize);
        var cellY=Math.floor(y/this.cellSize);	    
        return {col: cellX, row: cellY};
	}
	
	this.shapeCenterToBasePoint=function(x,y) {
		return {
			x: x-this.cellSize/2, 
			y: y-this.cellSize/2
			}
	}
	
	this.getCellPoint=function(row,col) {
	    return {
	        x: row*this.cellSize,
	        y: col*this.cellSize
	    }
	}
	
	this.shapes={
	    "empty": {
	       name: "empty",
	       parent: this,
	       paint: function(paper, point, color) {
	           var element=paper.rect(point.x,point.y,this.parent.cellSize,this.parent.cellSize);
	           element.attr({"stroke-colorfill":"#d0d0d0"});
	           return element;
	       }   
	    },
		"flat":{
			name: "flat",
			parent: this,
			paint: function(paper, point, color) {
				var element=paper.rect(point.x,point.y,this.parent.cellSize,this.parent.cellSize);
				element.attr({"fill":color, "stroke-width":0})
				return element;
			}
		},
		"diamond":{
			name: "diamond",
			parent: this,
			paint: function(paper, point, color) {
				var c=hexToHsl(color);
				cellSize=this.parent.cellSize;
				
				var c1=hslToHex(c.h, c.s, c.l+0.2);
				var e1=paper.path([
					"M ",point.x, point.y,
					"L",point.x+cellSize/2, point.y+cellSize/2,
					"L",point.x+cellSize, point.y,"Z"]);
				e1.attr({"fill":c1, "stroke-width":0});
				
				var c2=hslToHex(c.h, c.s, c.l+0.1);
				var e2=paper.path([
					"M",point.x, point.y,
					"L",point.x+cellSize/2, point.y+cellSize/2,
					"L",point.x, point.y+cellSize,"Z"])
				e2.attr({"fill":c2, "stroke-width":0});
				
				var c3=hslToHex(c.h, c.s, c.l-0.1);
				var e3=paper.path([
					"M",point.x, point.y+cellSize,
					"L",point.x+cellSize/2, point.y+cellSize/2,
					"L",point.x+cellSize, point.y+cellSize,"Z"]);
				e3.attr({"fill":c3, "stroke-width":0});
				
				var c4=hslToHex(c.h, c.s, c.l-0.15);
				var e4=paper.path([
					"M",point.x+cellSize, point.y,
					"L",point.x+cellSize/2, point.y+cellSize/2,
					"L",point.x+cellSize, point.y+cellSize,"Z"]);
				e4.attr({"fill":c4, "stroke-width":0});
			}			
		},
		"jewel": {
			name: "jewel",
			parent: this,
			paint: function(paper, point, color) {
				var c=hexToHsl(color);
				var cellSize=this.parent.cellSize;
				var facet=cellSize/6;
				
				var c1=hslToHex(c.h, c.s, c.l+0.2);
				var e1=paper.path([
					"M ",point.x, point.y,
					"L",point.x+facet, point.y+facet,
					"L",point.x+cellSize-facet, point.y+facet,
					"L",point.x+cellSize, point.y,"Z"]);
				e1.attr({"fill":c1, "stroke-width":0});
				
				var c2=hslToHex(c.h, c.s, c.l+0.1);
				var e2=paper.path([
					"M",point.x, point.y,
					"L",point.x+facet, point.y+facet,
					"L",point.x+facet, point.y+cellSize-facet,
					"L",point.x, point.y+cellSize,"Z"])
				e2.attr({"fill":c2, "stroke-width":0});
				
				var c3=hslToHex(c.h, c.s, c.l-0.1);
				var e3=paper.path([
					"M",point.x, point.y+cellSize,
					"L",point.x+facet, point.y+cellSize-facet,
					"L",point.x+cellSize-facet, point.y+cellSize-facet,
					"L",point.x+cellSize, point.y+cellSize,"Z"]);
				e3.attr({"fill":c3, "stroke-width":0});
				
				var c4=hslToHex(c.h, c.s, c.l-0.2);
				var e4=paper.path([
					"M",point.x+cellSize, point.y,
					"L",point.x+cellSize-facet, point.y+facet,
					"L",point.x+cellSize-facet, point.y+cellSize-facet,
					"L",point.x+cellSize, point.y+cellSize,"Z"]);
				e4.attr({"fill":c4, "stroke-width":0});
				
				var e5=paper.path([
					"M",point.x+facet, point.y+facet,
					"L",point.x+cellSize-facet, point.y+facet,
					"L",point.x+cellSize-facet, point.y+cellSize-facet,
					"L",point.x+facet, point.y+cellSize-facet,"Z"]);
				e5.attr({"fill":color, "stroke-width":0});
			}
		}
	}
}

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
		return pointToTriangleCoord(x,y,this.cellSize);
	}
	
	this.shapes=[];
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
