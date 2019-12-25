/*
 * Square grid
 */

function GridSquare_ShapeEmpty(parent) {
	this.name="empty";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		x=col*parent.cellSize+dx;
		y=row*parent.cellSize+dy;
	    var element=paper.rect(x,y,this.parent.cellSize,this.parent.cellSize);
	    element.attr({"stroke":"#808080"});
	    return element;
	};   
}

function GridSquare_BasicShapeFlat(parent) {
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		x=col*parent.cellSize+dx;
		y=row*parent.cellSize+dy;
		var cellSize=this.parent.cellSize;
        var facet=this.getFacet();		
		var element=paper.rect(
			x+facet,
			y+facet,
			cellSize-facet*2,
			cellSize-facet*2);
		element.attr({"fill":color, "stroke-width":0});
		return element;
	};
}

function GridSquare_ShapeFlat(parent) {
	this.super=GridSquare_BasicShapeFlat;
	this.super(parent);
	this.name='flat';
	this.getFacet=function() {
		return 0;
	};
}

function GridSquare_ShapeFlat1(parent) {
	this.super=GridSquare_BasicShapeFlat;
	this.super(parent);
	
	this.name="flat1";
	this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/6;	    
	};
}

function GridSquare_ShapeFlat2(parent) {
    this.super=GridSquare_BasicShapeFlat;
    this.super(parent);
    
    this.name="flat2";
    this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/4;      
    };
}

function GridSquare_ShapeFlat3(parent) {
    this.super=GridSquare_BasicShapeFlat;
    this.super(parent);
    
    this.name="flat3";
    this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/3;      
    };
}

function GridSquare_BasicShapeCircle(parent) {
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		x=col*parent.cellSize+dx;
		y=row*parent.cellSize+dy;
		var cellSize=this.parent.cellSize;
        var facet=this.getFacet();		
		var element=paper.circle(
			x+cellSize/2,
			y+cellSize/2,
			cellSize/2-facet);
		element.attr({"fill":color, "stroke-width":0});
		return element;
	};
}

function GridSquare_ShapeCircle(parent) {
	this.super=GridSquare_BasicShapeCircle;
	this.super(parent);
	this.name='circle';
	this.getFacet=function() {
		return 0;
	};
}

function GridSquare_ShapeCircle1(parent) {
	this.super=GridSquare_BasicShapeCircle;
	this.super(parent);
	
	this.name="circle1";
	this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/6;	    
	};
}

function GridSquare_ShapeCircle2(parent) {
    this.super=GridSquare_BasicShapeCircle;
    this.super(parent);
    
    this.name="circle2";
    this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/4;      
    };
}

function GridSquare_ShapeCircle3(parent) {
    this.super=GridSquare_BasicShapeCircle;
    this.super(parent);
    
    this.name="circle3";
    this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/3;      
    };
}


function GridSquare_ShapeSelected(parent) {
	this.name="selected";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		x=col*parent.cellSize+dx;
		y=row*parent.cellSize+dy;		
		var element=paper.rect(x,y,this.parent.cellSize,this.parent.cellSize);
		element.attr({
			"fill":"url('/img/selection-hatch.png')", 
			"fill-opacity": 0.5,
			"stroke-width":0})
		return element;
	}	
}

function GridSquare_ShapeDiamond(parent) {
	this.name="diamond";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		x=col*parent.cellSize+dx;
		y=row*parent.cellSize+dy;
		var c=hexToHsl(color);
		cellSize=this.parent.cellSize;
				
		paper.setStart();
				
		var c1=hslToHex(c.h, c.s, c.l+0.2);
		var e1=paper.path([
			"M ",x, y,
			"L",x+cellSize/2, y+cellSize/2,
			"L",x+cellSize, y,"Z"]);
		e1.attr({"fill":c1, "stroke-width":0});
				
		var c2=hslToHex(c.h, c.s, c.l+0.1);
		var e2=paper.path([
			"M",x, y,
			"L",x+cellSize/2, y+cellSize/2,
			"L",x, y+cellSize,"Z"])
		e2.attr({"fill":c2, "stroke-width":0});
				
		var c3=hslToHex(c.h, c.s, c.l-0.1);
		var e3=paper.path([
			"M",x, y+cellSize,
			"L",x+cellSize/2, y+cellSize/2,
			"L",x+cellSize, y+cellSize,"Z"]);
		e3.attr({"fill":c3, "stroke-width":0});
				
		var c4=hslToHex(c.h, c.s, c.l-0.2);
		var e4=paper.path([
			"M",x+cellSize, y,
			"L",x+cellSize/2, y+cellSize/2,
			"L",x+cellSize, y+cellSize,"Z"]);
		e4.attr({"fill":c4, "stroke-width":0});
		return paper.setFinish();
	}			
}

function GridSquare_BasicShapeJewel(parent) {
    this.parent=parent;
    this.paint=function(paper, col, row, color, dx, dy) {
		x=col*parent.cellSize+dx;
		y=row*parent.cellSize+dy;    	
        var c=hexToHsl(color);
        var cellSize=this.parent.cellSize;
        var facet=this.getFacet();
                
        paper.setStart();
        var c1=hslToHex(c.h, c.s, c.l+0.2);
        var e1=paper.path([
            "M ",x, y,
            "L",x+facet, y+facet,
            "L",x+cellSize-facet, y+facet,
            "L",x+cellSize, y,"Z"]);
        e1.attr({"fill":c1, "stroke-width":0});
                
        var c2=hslToHex(c.h, c.s, c.l+0.1);
        var e2=paper.path([
            "M",x, y,
            "L",x+facet, y+facet,
            "L",x+facet, y+cellSize-facet,
            "L",x, y+cellSize,"Z"])
        e2.attr({"fill":c2, "stroke-width":0});
                
        var c3=hslToHex(c.h, c.s, c.l-0.1);
        var e3=paper.path([
            "M",x, y+cellSize,
            "L",x+facet, y+cellSize-facet,
            "L",x+cellSize-facet, y+cellSize-facet,
            "L",x+cellSize, y+cellSize,"Z"]);
        e3.attr({"fill":c3, "stroke-width":0});
                
        var c4=hslToHex(c.h, c.s, c.l-0.2);
        var e4=paper.path([
            "M",x+cellSize, y,
            "L",x+cellSize-facet, y+facet,
            "L",x+cellSize-facet, y+cellSize-facet,
            "L",x+cellSize, y+cellSize,"Z"]);
        e4.attr({"fill":c4, "stroke-width":0});
                
        var e5=paper.path([
            "M",x+facet, y+facet,
            "L",x+cellSize-facet, y+facet,
            "L",x+cellSize-facet, y+cellSize-facet,
            "L",x+facet, y+cellSize-facet,"Z"]);
        e5.attr({"fill":color, "stroke-width":0});
        return paper.setFinish();
    }    
}

function GridSquare_ShapeJewel(parent) {
	this.super=GridSquare_BasicShapeJewel;
	this.super(parent);
	
	this.name="jewel";
	this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/6;	    
	}
}

function GridSquare_ShapeJewel2(parent) {
    this.super=GridSquare_BasicShapeJewel;
    this.super(parent);
    
    this.name="jewel2";
    this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/4;      
    }
}

function GridSquare_ShapeJewel3(parent) {
    this.super=GridSquare_BasicShapeJewel;
    this.super(parent);
    
    this.name="jewel3";
    this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/3;      
    }
}

function GridSquare_BasicShapeFramed(parent) {
    this.parent=parent;
    this.frameLight = 0;
    this.frameWidth = 0
    this.paint=function(paper, col, row, color, dx, dy) {
		x=col*parent.cellSize+dx;
		y=row*parent.cellSize+dy;
        var c=hexToHsl(color);
        var cellSize=this.parent.cellSize;
        var facet=this.parent.cellSize * this.frameWidth;
        var frameColor = hslToHex(c.h, c.s, c.l+this.frameLight);

        paper.setStart();
        var e1=paper.rect(
			x,
			y,
			cellSize,
			cellSize);
		e1.attr({"fill":frameColor, "stroke-width":0});


        var e2=paper.rect(
			x + facet,
			y + facet,
			cellSize - facet * 2,
			cellSize - facet * 2);
		e2.attr({"fill": color, "stroke-width":0});

        return paper.setFinish();
    }
}

function GridSquare_ShapeFramed5Dark(parent) {
    this.super = GridSquare_BasicShapeFramed;
    this.super(parent)
    this.frameLight = -0.15;
    this.frameWidth = 0.05;
}

function GridSquare_ShapeFramed10Dark(parent) {
    this.super = GridSquare_BasicShapeFramed;
    this.super(parent)
    this.frameLight = -0.15;
    this.frameWidth = 0.10;
}

function GridSquare_ShapeFramed5Light(parent) {
    this.super = GridSquare_BasicShapeFramed;
    this.super(parent)
    this.frameLight = 0.15;
    this.frameWidth = 0.05;
}

function GridSquare_ShapeFramed10Light(parent) {
    this.super = GridSquare_BasicShapeFramed;
    this.super(parent)
    this.frameLight = 0.15;
    this.frameWidth = 0.10;
}

function GridSquare_ToolLine() {
	/*
		A draw tool should contain:
			properties:
				- title
				- iconUrl
			methods: 
				- calculateCells(startCell, endCell) - to calculate cell coordinates to be drawn
				- adjustEndCell(startCell, endCell) - to adjust end point to predefined rulers

	*/

	this.title = 'Draw line';
	this.iconUrl = '/img/buttons/line.png';

	this.basicLineAngles = [
		0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330		
	];

	this.adjustEndCell = function(startCell, endCell) {
		var vectorCol = endCell.col - startCell.col;
		var vectorRow = endCell.row - startCell.row;
		var vectorLength = Math.sqrt(vectorCol * vectorCol + vectorRow * vectorRow);
		if (vectorLength == 0) {
			return endCell;
		}

		var angleCos = Math.abs(vectorCol) / vectorLength;
		var angle;
		if (angleCos == 0 ) {
			angle = Math.PI / 2;
		} else {
			angle = Math.acos(angleCos);
		}
		if (vectorCol >=0 && vectorRow >= 0) {
			// pass
		} else if (vectorCol < 0 && vectorRow >=0) {
			angle = Math.PI - angle;
		} else if (vectorCol < 0 && vectorRow < 0) {
			angle = Math.PI + angle;
		} else { // vectorCol >=0 && vectorRow < 0
			angle = 2 * Math.PI - angle;
		}
		var angleGrad = angle * 180 / Math.PI;
		var minAngleDiff = 100;
		var chosenAngleGrad = 0;
		for (var i=0; i < this.basicLineAngles.length; i++) {
			var diff = Math.abs(angleGrad - this.basicLineAngles[i]);
			if (diff < minAngleDiff) {
				minAngleDiff = diff;
				chosenAngleGrad = this.basicLineAngles[i]
			}
		}

		var chosenAngle = chosenAngleGrad * Math.PI / 180;
		return {
			col: startCell.col + Math.round(vectorLength * Math.cos(chosenAngle)),
			row: startCell.row + Math.round(vectorLength * Math.sin(chosenAngle))
		}
	}

	this.plotLineLow = function(x0, y0, x1, y1) {
        var result = [];
        var dx = x1 - x0;
        var dy = y1 - y0;
        var yi = 1;
        if (dy < 0) {
            yi = -1;
            dy = -dy;
        }
        var D = 2 * dy - dx;
        var y = y0;

        for (var x = x0; x <= x1; x++) {
            result.push({
                col: x,
                row: y
            });
            if (D > 0) {
                y = y + yi;
                D = D - 2 * dx;
            }
            D = D + 2 * dy;
        }
        return result;
    }

    this.plotLineHigh = function(x0, y0, x1, y1) {
        var result = [];
        var dx = x1 - x0;
        var dy = y1 - y0;
        var xi = 1;
        if (dx < 0) {
            xi = -1;
            dx = -dx;
        }
        var D = 2*dx - dy;
        var x = x0;

        for (var y = y0; y <= y1; y++) {
            result.push({
                col: x,
                row: y
            });
            if (D > 0) {
                x = x + xi;
                D = D - 2*dy;
            }
            D = D + 2*dx;
        }
        return result;
    }

	this.plotLine = function(col0, row0, col1, row1) {
	    var x0 = col0;
	    var y0 = row0;
	    var x1 = col1;
	    var y1 = row1;
        if (Math.abs(y1 - y0) < Math.abs(x1 - x0)) {
            if (x0 > x1) {
                return this.plotLineLow(x1, y1, x0, y0)
            } else {
                return this.plotLineLow(x0, y0, x1, y1)
            }
        } else {
            if (y0 > y1) {
                return this.plotLineHigh(x1, y1, x0, y0)
            } else {
                return this.plotLineHigh(x0, y0, x1, y1)
            }
        }
	}

	this.calculateCells = function(startCell, endCell) {
		return this.plotLine(startCell.col, startCell.row, endCell.col, endCell.row);
	}
}


function GridSquare_ToolRectangle() {
	this.title = 'Draw rectangle';
	this.iconUrl = '/img/buttons/rectangle.png';

	this.calculateCells = function(startCell, endCell) {
		var result = [];
		var top = startCell.row;
		var left = startCell.col;
		var bottom = endCell.row;
		var right = endCell.col;

		if (top == bottom && left == right) {
			return result;
		}

		if (top > bottom) {
			var tmp = top;
			top = bottom;
			bottom = tmp;
		}

		if (left > right) {
			var tmp = left;
			left = right;
			right = tmp;
		}

		for (var col = left; col <= right; col++) {
			result.push({
				col: col, 
				row: top
			})
		}

		for (var row = top + 1; row <= bottom; row++) {
			result.push({
				col: right,
				row: row
			})
		}

		if (bottom > top) {
			for (var col = left; col < right; col++) {
				result.push({
					col: col,
					row: bottom
				})
			}
		}	

		if (right > left) {
			for (var row = top + 1; row < bottom; row++) {
				result.push({
					col: left,
					row: row
				})
			}
		}

		return result;
	}

	this.adjustEndCell = function(startCell, endCell) {
		var width = Math.abs(startCell.col - endCell.col);
		var height = Math.abs(startCell.row - endCell.row);
		var size;
		if (width < height) {
			size = width;
		} else {
			size = height;
		}

		var newEndCellCol = startCell.col + size;
		var newEndCellRow = startCell.row + size;
		if (endCell.col < startCell.col) {
			newEndCellCol = startCell.col - size;
		}
		if (endCell.row < startCell.row) {
			newEndCellRow = startCell.row - size;
		}

		return {
			col: newEndCellCol,
			row: newEndCellRow
		}
	}
}



function GridSquare_ToolEllipse() {
	this.title = 'Draw ellipse';
	this.iconUrl = '/img/buttons/ellipse.png';

	this.calculateCells = function(startCell, endCell) {
		var result = [];
		var top = startCell.row;
		var left = startCell.col;
		var bottom = endCell.row;
		var right = endCell.col;
		if (top > bottom) {
			var tmp = top;
			top = bottom;
			bottom = tmp;
		}

		if (top == bottom && left == right) {
			return result;
		}

		if (left > right) {
			var tmp = left;
			left = right;
			right = tmp;
		}

		// TODO calculate ellipse

		var cx = (left + right) / 2;
		var cy = (top + bottom) / 2;
		var a = Math.round((right - left) / 2);
		var b = Math.round((bottom - top) / 2);

		var addPoint = function(x, y) {
			result.push({
				col: Math.round(cx + x),
				row: Math.round(cy + y)
			});
			result.push({
				col: Math.round(cx - x),
				row: Math.round(cy + y)
			});
			result.push({
				col: Math.round(cx + x),
				row: Math.round(cy - y)
			});
			result.push({
				col: Math.round(cx - x),
				row: Math.round(cy - y)
			});
		}


		var a2 = a*a, b2 = b*b;
		var x = 0, y = b; //Starting point

		var incSW = b2*2 + a2*2;

		var deltaW = b2*(-2*x + 3); //deduced from incremental algorithm with the second-order logic
		var deltaS = a2*(-2*y + 3);
		var deltaSW = deltaW + deltaS;

		var d1 = b2 - a2*b + a2/4; //dp starting value in the first region
		var d2 = b2*(x - 0.5)*(x - 0.5) + a2*(y - 1)*(y - 1) - a2*b2; //dp starting value in the second region

		//First region
		while(a2*(y-0.5) >= b2*(-x-1)) {
			addPoint(x, y);
			// DrawPixel(g,-x+xc, -y+yc); // 1st case
			// DrawPixel(g,-x+xc, y+yc); // 2nd case
			// DrawPixel(g,x+xc, y+yc); // 3rd case
			// DrawPixel(g,x+xc, -y+yc); // 4th case
			if(d1>0) {
				d1+=deltaSW;
				deltaW+=b2*2;
				deltaSW+=incSW;
				y--;
			}
			else {
				d1+=deltaW;
				deltaW+=2*b2;
				deltaSW+=2*b2;
			}
			x--;
		}

		deltaSW = b2*(2 - 2*x) + a2*(-2*y + 3);

		//Second region
		while(y>=0) {
			// DrawPixel(g,-x+xc, -y+yc); // 1st case
			// DrawPixel(g,-x+xc, y+yc); // 2nd case
			// DrawPixel(g,x+xc, y+yc); // 3rd case
			// DrawPixel(g,x+xc, -y+yc); // 4th case
			addPoint(x,y);
			if(d2>0) {
				d2+=deltaS;
				deltaS+=a2*2;
				deltaSW+=a2*2;
			}
			else {
				d2+=deltaSW;
				deltaSW+=incSW;
				deltaS+=a2*2;
				x--;
			}
			y--;
		}

		console.log(result);

		return result;
	}

	this.adjustEndCell = function(startCell, endCell) {
		var width = Math.abs(startCell.col - endCell.col);
		var height = Math.abs(startCell.row - endCell.row);
		var size;
		if (width < height) {
			size = width;
		} else {
			size = height;
		}

		var newEndCellCol = startCell.col + size;
		var newEndCellRow = startCell.row + size;
		if (endCell.col < startCell.col) {
			newEndCellCol = startCell.col - size;
		}
		if (endCell.row < startCell.row) {
			newEndCellRow = startCell.row - size;
		}

		return {
			col: newEndCellCol,
			row: newEndCellRow
		}
	}
}


function GridSquare() {
	this.cellSize=24;
	this.name="square";
	
	this._createGridLine=function(paper, pathArray) {
		var path=paper.path(pathArray);
        path.attr({
            "stroke":gridLineColor,
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
	
	this.getCellRect=function(col, row) {
	    return {
	        left: col*this.cellSize,
	        top: row*this.cellSize,
	        width: this.cellSize,
	        height: this.cellSize
	    }
	}
	
	this.nearestSameCell=function(col, row, nearCol, nearRow) {
		return {
			col: nearCol,
			row: nearRow
		};
	}
	
	this.getAdjacentCells = function(col, row) {
		return [
			{
				col: col - 1,
				row: row
			},
			{
				col: col,
				row: row - 1
			},
			{
				col: col + 1,
				row: row
			},
			{
				col: col,
				row: row + 1
			}
		]
	}
	
	this.isCellInsideWorkspace = function(col, row) {
		var colCount=this.workspaceWidth/this.cellSize;
		var rowCount=this.workspaceHeight/this.cellSize;
		return col>=0 && col<colCount && row>=0 && row<rowCount;
	}
	
	this.shapes={
	    "empty": new GridSquare_ShapeEmpty(this),
		"flat": new GridSquare_ShapeFlat(this),
		"flat1": new GridSquare_ShapeFlat1(this),
		"flat2": new GridSquare_ShapeFlat2(this),
		"flat3": new GridSquare_ShapeFlat3(this),
		'circle': new GridSquare_ShapeCircle(this),
		'circle1': new GridSquare_ShapeCircle1(this),
		'circle2': new GridSquare_ShapeCircle2(this),
		'circle3': new GridSquare_ShapeCircle3(this),
		"jewel": new GridSquare_ShapeJewel(this),
		"jewel2": new GridSquare_ShapeJewel2(this),
		"jewel3": new GridSquare_ShapeJewel3(this),
		"diamond": new GridSquare_ShapeDiamond(this),
		"frame5d": new GridSquare_ShapeFramed5Dark(this),
		"frame10d": new GridSquare_ShapeFramed10Dark(this),
		"frame5u": new GridSquare_ShapeFramed5Light(this),
		"frame10u": new GridSquare_ShapeFramed10Light(this)
	};
	
	this.internalShapes={
	    "selected": new GridSquare_ShapeSelected(this)
	}
	
	this.shiftLeft={
	    cell_dx:-1,
	    cell_dy:0,
	    dx: -this.cellSize,
	    dy: 0
	}
	
	this.shiftRight={
	    cell_dx:1,
	    cell_dy:0,
	    dx: this.cellSize,
	    dy: 0
	}
	
	this.shiftUp={
	    cell_dx:0,
	    cell_dy:-1,
	    dx: 0,
	    dy: -this.cellSize
	}
	
	this.shiftDown={
	    cell_dx:0,
	    cell_dy:1,
	    dx:0,
	    dy: this.cellSize
	}

	this.drawTools = {
		'line': new GridSquare_ToolLine(),
		'rectangle': new GridSquare_ToolRectangle(),
		'ellipse': new GridSquare_ToolEllipse()
	}
}

// Register grid
gridFactory["square"]=function() {
	return new GridSquare();
}

