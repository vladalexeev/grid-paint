

/**
 * Return array of 6 points of shape in array with
 * indices from 0 to 5, and element with index=6 
 * with coordinate of center of shape 
 * @param {Object} col
 * @param {Object} row
 * @param {Object} sideLength
 */
function getHexCellPoints(col, row, sideLength) {
	var x=(sideLength+sideLength*cos60)*col;
	var y=2*sideLength*sin60*row;
	var halfHeight=sideLength*sin60;
	var dx=sideLength*cos60;
	if (col % 2 == 1) {
		y+=sideLength*sin60;
	}
	
	return [
		{x: x, y: y+halfHeight},
		{x: x+dx, y: y},
		{x: x+dx+sideLength, y: y},
		{x: x+2*dx+sideLength, y: y+halfHeight},
		{x: x+dx+sideLength, y: y+2*halfHeight},
		{x: x+dx, y: y+2*halfHeight},
		{x: x+dx+sideLength/2, y: y+halfHeight}
	]
}


function GridHex_ShapeEmpty(parent) {
	this.name="empty";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=getHexCellPoints(col, row, parent.cellSize/2);
	    var element=paper.path([
	    		"M",pp[0].x+dx, pp[0].y+dy,
	    		"L",pp[1].x+dx, pp[1].y+dy,
	    		"L",pp[2].x+dx, pp[2].y+dy,
	    		"L",pp[3].x+dx, pp[3].y+dy,
	    		"L",pp[4].x+dx, pp[4].y+dy,
	    		"L",pp[5].x+dx, pp[5].y+dy,"Z"]);
	    element.attr({"stroke":"#808080"});
	    return element;
	}   
}

function GridHex_ShapeFlat(parent) {
	this.name="flat";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=getHexCellPoints(col, row, parent.cellSize/2);
	    var element=paper.path([
	    		"M",pp[0].x+dx, pp[0].y+dy,
	    		"L",pp[1].x+dx, pp[1].y+dy,
	    		"L",pp[2].x+dx, pp[2].y+dy,
	    		"L",pp[3].x+dx, pp[3].y+dy,
	    		"L",pp[4].x+dx, pp[4].y+dy,
	    		"L",pp[5].x+dx, pp[5].y+dy,"Z"]);
	    element.attr({"fill":color, "stroke-width":0});
	    return element;
	}   
}

function GridHex_ShapeSelected(parent) {
	this.name="selected";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=getHexCellPoints(col, row, parent.cellSize/2);
	    var element=paper.path([
	    		"M",pp[0].x+dx, pp[0].y+dy,
	    		"L",pp[1].x+dx, pp[1].y+dy,
	    		"L",pp[2].x+dx, pp[2].y+dy,
	    		"L",pp[3].x+dx, pp[3].y+dy,
	    		"L",pp[4].x+dx, pp[4].y+dy,
	    		"L",pp[5].x+dx, pp[5].y+dy,"Z"]);
	    element.attr({
			"fill":"url('/img/selection-hatch.png')", 
			"fill-opacity": 0.5,
			"stroke-width":0});
	    return element;
	}   
}

function GridHex_ShapeDiamond(parent) {
	this.name="diamond";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=getHexCellPoints(col, row, parent.cellSize/2);
		var c=hexToHsl(color);
		paper.setStart();
		cx=pp[6].x
		cy=pp[6].y
		
		var c0=hslToHex(c.h, c.s, c.l+0.2);
	    var e0=paper.path([
	    		"M",pp[0].x+dx, pp[0].y+dy,
	    		"L",pp[1].x+dx, pp[1].y+dy,
	    		"L",cx+dx, cy+dy,"Z"]);
	    e0.attr({"fill":c0, "stroke-width":0});
	    
   		var c1=hslToHex(c.h, c.s, c.l+0.1);
	    var e1=paper.path([
	    		"M",pp[1].x+dx, pp[1].y+dy,
	    		"L",pp[2].x+dx, pp[2].y+dy,
	    		"L",cx+dx, cy+dy,"Z"]);
	    e1.attr({"fill":c1, "stroke-width":0});

   		var c2=hslToHex(c.h, c.s, c.l-0.1);	    
   	    var e2=paper.path([
	    		"M",pp[2].x+dx, pp[2].y+dy,
	    		"L",pp[3].x+dx, pp[3].y+dy,
	    		"L",cx+dx, cy+dy,"Z"]);
	    e2.attr({"fill":c2, "stroke-width":0});

   		var c3=hslToHex(c.h, c.s, c.l-0.2);	    
   	    var e3=paper.path([
	    		"M",pp[3].x+dx, pp[3].y+dy,
	    		"L",pp[4].x+dx, pp[4].y+dy,
	    		"L",cx+dx, cy+dy,"Z"]);
	    e3.attr({"fill":c3, "stroke-width":0});

   		var c4=c2;	    
   	    var e4=paper.path([
	    		"M",pp[4].x+dx, pp[4].y+dy,
	    		"L",pp[5].x+dx, pp[5].y+dy,
	    		"L",cx+dx, cy+dy,"Z"]);
	    e4.attr({"fill":c4, "stroke-width":0});

		var c5=c1
	    var e5=paper.path([
	    		"M",pp[5].x+dx, pp[5].y+dy,
	    		"L",pp[0].x+dx, pp[0].y+dy,
	    		"L",cx+dx, cy+dy,"Z"]);
	    e5.attr({"fill":c5, "stroke-width":0});
	    
	    return paper.setFinish();;
	}   	
}

function GridHex_ShapeJewel(parent) {
	this.name="diamond";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=getHexCellPoints(col, row, parent.cellSize/2);
		var c=hexToHsl(color);
		
		cx=pp[6].x;
		cy=pp[6].y;
		
		paper.setStart();
		
		var c0=hslToHex(c.h, c.s, c.l+0.2);
	    var e0=paper.path([
	    		"M",pp[0].x+dx, pp[0].y+dy,
	    		"L",pp[1].x+dx, pp[1].y+dy,
	    		"L",pp[1].x+dx+(cx-pp[1].x)/2, pp[1].y+dy+(cy-pp[1].y)/2,
	    		"L",pp[0].x+dx+(cx-pp[0].x)/2, pp[0].y+dy+(cy-pp[0].y)/2,"Z"]);
	    e0.attr({"fill":c0, "stroke-width":0});
	    
   		var c1=hslToHex(c.h, c.s, c.l+0.1);
	    var e1=paper.path([
	    		"M",pp[1].x+dx, pp[1].y+dy,
	    		"L",pp[2].x+dx, pp[2].y+dy,
	    		"L",pp[2].x+dx+(cx-pp[2].x)/2, pp[2].y+dy+(cy-pp[2].y)/2,
	    		"L",pp[1].x+dx+(cx-pp[1].x)/2, pp[1].y+dy+(cy-pp[1].y)/2,"Z"]);
	    e1.attr({"fill":c1, "stroke-width":0});

   		var c2=hslToHex(c.h, c.s, c.l-0.1);	    
   	    var e2=paper.path([
	    		"M",pp[2].x+dx, pp[2].y+dy,
	    		"L",pp[3].x+dx, pp[3].y+dy,
	    		"L",pp[3].x+dx+(cx-pp[3].x)/2, pp[3].y+dy+(cy-pp[3].y)/2,
	    		"L",pp[2].x+dx+(cx-pp[2].x)/2, pp[2].y+dy+(cy-pp[2].y)/2,"Z"]);
	    e2.attr({"fill":c2, "stroke-width":0});

   		var c3=hslToHex(c.h, c.s, c.l-0.2);	    
   	    var e3=paper.path([
	    		"M",pp[3].x+dx, pp[3].y+dy,
	    		"L",pp[4].x+dx, pp[4].y+dy,
	    		"L",pp[4].x+dx+(cx-pp[4].x)/2, pp[4].y+dy+(cy-pp[4].y)/2,
	    		"L",pp[3].x+dx+(cx-pp[3].x)/2, pp[3].y+dy+(cy-pp[3].y)/2,"Z"]);
	    e3.attr({"fill":c3, "stroke-width":0});

   		var c4=c2;	    
   	    var e4=paper.path([
	    		"M",pp[4].x+dx, pp[4].y+dy,
	    		"L",pp[5].x+dx, pp[5].y+dy,
	    		"L",pp[5].x+dx+(cx-pp[5].x)/2, pp[5].y+dy+(cy-pp[5].y)/2,
	    		"L",pp[4].x+dx+(cx-pp[4].x)/2, pp[4].y+dy+(cy-pp[4].y)/2,"Z"]);
	    e4.attr({"fill":c4, "stroke-width":0});

		var c5=c1
	    var e5=paper.path([
	    		"M",pp[5].x+dx, pp[5].y+dy,
	    		"L",pp[0].x+dx, pp[0].y+dy,
	    		"L",pp[0].x+dx+(cx-pp[0].x)/2, pp[0].y+dy+(cy-pp[0].y)/2,
	    		"L",pp[5].x+dx+(cx-pp[5].x)/2, pp[5].y+dy+(cy-pp[5].y)/2,"Z"]);
	    e5.attr({"fill":c5, "stroke-width":0});
	    
	    var e6=paper.path([
	    		"M",pp[0].x+dx+(cx-pp[0].x)/2, pp[0].y+dy+(cy-pp[0].y)/2,
	    		"L",pp[1].x+dx+(cx-pp[1].x)/2, pp[1].y+dy+(cy-pp[1].y)/2,
	    		"L",pp[2].x+dx+(cx-pp[2].x)/2, pp[2].y+dy+(cy-pp[2].y)/2,
	    		"L",pp[3].x+dx+(cx-pp[3].x)/2, pp[3].y+dy+(cy-pp[3].y)/2,
	    		"L",pp[4].x+dx+(cx-pp[4].x)/2, pp[4].y+dy+(cy-pp[4].y)/2,
	    		"L",pp[5].x+dx+(cx-pp[5].x)/2, pp[5].y+dy+(cy-pp[5].y)/2,"Z"]);
	    e6.attr({"fill":color, "stroke-width":0});
	    
	    return paper.setFinish();;
	}   	
}

function GridHex_ShapeCube(parent) {
    this.name="diamond";
    this.parent=parent;
    this.paint=function(paper, col, row, color, dx, dy) {
        var pp=getHexCellPoints(col, row, parent.cellSize/2);
        var c=hexToHsl(color);
        paper.setStart();
        cx=pp[6].x
        cy=pp[6].y
        
        var c0=hslToHex(c.h, c.s, c.l+0.2);
        var e0=paper.path([
                "M",pp[0].x+dx, pp[0].y+dy,
                "L",pp[1].x+dx, pp[1].y+dy,
                "L",pp[2].x+dx, pp[2].y+dy,
                "L",cx+dx, cy+dy,"Z"]);
        e0.attr({"fill":c0, "stroke-width":0});
        
        var c1=c;
        var e1=paper.path([
                "M",pp[2].x+dx, pp[2].y+dy,
                "L",pp[3].x+dx, pp[3].y+dy,
                "L",pp[4].x+dx, pp[4].y+dy,
                "L",cx+dx, cy+dy,"Z"]);
        e1.attr({"fill":c1, "stroke-width":0});

        var c2=hslToHex(c.h, c.s, c.l-0.2);     
        var e2=paper.path([
                "M",pp[4].x+dx, pp[4].y+dy,
                "L",pp[5].x+dx, pp[5].y+dy,
                "L",pp[0].x+dx, pp[0].y+dy,
                "L",cx+dx, cy+dy,"Z"]);
        e2.attr({"fill":c2, "stroke-width":0});
        
        return paper.setFinish();;
    }       
}




function GridHex() {
	this.cellSize=24;
	this.name="hex";
	
	this._createGridLine=function(paper, pathArray, stroke_dash_array) {
		var path=paper.path(pathArray);
        path.attr({
            "stroke":"#d0d0d0",
        })
        path.node.setAttribute("stroke-dasharray",stroke_dash_array);
	}
	
	this.paintGrid=function(paper) {
	    var paperHeight=paper.height;
	    var paperWidth=paper.width;
		var sideLength=this.cellSize/2;
		var halfHeight=sideLength*sin60;
		var dx=sideLength*cos60;
		
		stroke_dash_array=sideLength+","+this.cellSize;

		for (y=0; y<paper.height; y+=halfHeight*2) {
		    this._createGridLine(
		    	paper,
		    	["M ",dx,y,"H",paper.width],
		    	stroke_dash_array);
		}
		
		for (y=halfHeight; y<paper.height; y+=halfHeight*2) {
		    this._createGridLine(
		    	paper,
		    	["M",2*dx+sideLength,y,"H",paper.width],
		    	stroke_dash_array);
		}
		
		var slantedLinesStep=2*dx+2*sideLength;
		var hexBehind=Math.floor(paperHeight/slantedLinesStep);
		
		for (x=dx+sideLength-hexBehind*slantedLinesStep; x<paper.width; x+=slantedLinesStep) {
		    this._createGridLine(
		    	paper,
		    	["M",x,0,"L",x+paperHeight*tan30,paperHeight],
		    	stroke_dash_array);
		}
		
		for (x=0-hexBehind*slantedLinesStep; x<paper.width; x+=slantedLinesStep) {
            this._createGridLine(
            	paper,
            	["M",x,halfHeight,"L",x+paperHeight*tan30,halfHeight+paperHeight],
            	stroke_dash_array);
        }
        
        for (x=dx+sideLength-hexBehind*slantedLinesStep; x<paper.width; x+=slantedLinesStep) {
            this._createGridLine(
            	paper,
            	["M",x,halfHeight*2,"L",x+paperHeight*tan30,halfHeight*2+paperHeight],
            	stroke_dash_array);
        }
        
		
		for (x=dx; x<paper.width+hexBehind*slantedLinesStep; x+=slantedLinesStep) {
            this._createGridLine(
            	paper,
            	["M",x,0,"L",x-paperHeight*tan30,paperHeight],
            	stroke_dash_array);
        }
        
        for (x=2*dx+sideLength; x<paper.width+hexBehind*slantedLinesStep; x+=slantedLinesStep) {
            this._createGridLine(
            	paper,
            	["M",x,halfHeight,"L",x-paperHeight*tan30,halfHeight+paperHeight],
            	stroke_dash_array);
        }
        
        for (x=dx; x<paper.width+hexBehind*slantedLinesStep; x+=slantedLinesStep) {
            this._createGridLine(
            	paper,["M",x,2*halfHeight,"L",x-paperHeight*tan30,2*halfHeight+paperHeight],
            	stroke_dash_array);
        }
	}
	
	this.pointToCell=function(x,y) {
		sideLength=this.cellSize/2;
		var triangleCell=pointToTriangleCoord(x,y,sideLength);
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
	
	this.getCellRect=function(col, row) {
		sideLength=this.cellSize/2;
		return {
			left: (sideLength+sideLength*cos60)*col,
			top: row*2*sideLength*sin60+(col % 2 == 0 ? 0 : sideLength*sin60),
			width: sideLength+2*sideLength*cos60,
			height: 2*sideLength*sin60
		}
	}
	
	this.nearestSameCell=function(col, row, nearCol, nearRow) {
		return {
			col: nearCol,
			row: nearRow
		};
	}
	
	this.specialPasteShift=function(cells, baseCol, baseRow, pasteCol, pasteRow) {
		var shiftCol=pasteCol-baseCol;
		var shiftRow=pasteRow-baseRow;
		var result=[];
		
		var baseCellTop=(baseCol % 2) == 0;
		var pasteCellTop=(pasteCol % 2) == 0;
		var rowAddition=0;
		if (baseCellTop && !pasteCellTop) {
			rowAddition=1;
		} else if (!baseCellTop && pasteCellTop) {
			rowAddition=-1;
		}
		
		for (var i=0; i<cells.length; i++) {
			var cc=cells[i];
			
			var shiftedCol=cc.col+shiftCol;
			var shiftedRow=cc.row+shiftRow+((cc.col+shiftCol-pasteCol)%2)*rowAddition;
			if (shiftedRow>=0) {
				result.push({
					col: shiftedCol,
					row: shiftedRow,
					shapeName: cc.shapeName,
					color: cc.color
				})
			}
		}
		
		return result;
	}
	
	this.shapes={
		"empty": new GridHex_ShapeEmpty(this),
		"flat": new GridHex_ShapeFlat(this),
		"diamond": new GridHex_ShapeDiamond(this),
		"jewel": new GridHex_ShapeJewel(this),
		"cube": new GridHex_ShapeCube(this)
	};
	
	this.internalShapes={
	    "selected": new GridHex_ShapeSelected(this)
	}
	
	this.shiftLeft={
	    cell_dx:-2,
	    cell_dy:0,
	    dx: -this.cellSize-this.cellSize*cos60,
	    dy: 0
	}
	
	this.shiftRight={
	    cell_dx:2,
	    cell_dy:0,
	    dx: this.cellSize+this.cellSize*cos60,
	    dy: 0
	}
	
	this.shiftUp={
	    cell_dx:0,
	    cell_dy:-1,
	    dx: 0,
	    dy: -this.cellSize*sin60
	}
	
	this.shiftDown={
	    cell_dx:0,
	    cell_dy:1,
	    dx:0,
	    dy: this.cellSize*sin60
	}
}

// Register grid
gridFactory["hex"]=function() {
	return new GridHex();
}

