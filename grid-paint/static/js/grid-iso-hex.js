

/**
 * Return array of 6 points of shape in array with
 * indices from 0 to 5, and element with index=6
 * with coordinate of center of shape
 * @param {Object} col
 * @param {Object} row
 * @param {Object} sideLength
 */
function getIsoHexCellPoints(col, row, sideLength) {  // ISO
	var y=(sideLength+sideLength*cos60)*row;
	var x=2*sideLength*sin60*col;
	var halfWidth=sideLength*sin60;
	var dy=sideLength*cos60;
	if (row % 2 == 1) {
		x+=sideLength*sin60;
	}

	return [
		{y: y, x: x+halfWidth},
		{y: y+dy, x: x},
		{y: y+dy+sideLength, x: x},
		{y: y+2*dy+sideLength, x: x+halfWidth},
		{y: y+dy+sideLength, x: x+2*halfWidth},
		{y: y+dy, x: x+2*halfWidth},
		{y: y+dy+sideLength/2, x: x+halfWidth}
	]
}


function GridIsoHex_ShapeEmpty(parent) {
	this.name="empty";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=getIsoHexCellPoints(col, row, parent.cellSize/2);
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

function GridIsoHex_ShapeFlat(parent) {
	this.name="flat";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=getIsoHexCellPoints(col, row, parent.cellSize/2);
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

function GridIsoHex_ShapeSelected(parent) {
	this.name="selected";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=getIsoHexCellPoints(col, row, parent.cellSize/2);
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

function GridIsoHex_ShapeDiamond(parent) {
	this.name="diamond";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=getIsoHexCellPoints(col, row, parent.cellSize/2);
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

	    return paper.setFinish();
	}
}

function GridIsoHex_ShapeJewel(parent) {
	this.name="diamond";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=getIsoHexCellPoints(col, row, parent.cellSize/2);
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

	    return paper.setFinish();
	}
}

function GridIsoHex_ShapeCube(parent) {
    this.name="diamond";
    this.parent=parent;
    this.paint=function(paper, col, row, color, dx, dy) {
        var pp=getIsoHexCellPoints(col, row, parent.cellSize/2);
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

        return paper.setFinish();
    }
}


function GridIsoHex_BasicShapeFramed(parent) {
	this.parent=parent;
	this.frameLight = 0;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=getIsoHexCellPoints(col, row, parent.cellSize/2);
		var c=hexToHsl(color);

		cx=pp[6].x;
		cy=pp[6].y;

		paper.setStart();

		var c0=hslToHex(c.h, c.s, c.l+this.frameLight);
	    var e0=paper.path([
	    		"M",pp[0].x+dx, pp[0].y+dy,
	    		"L",pp[1].x+dx, pp[1].y+dy,
	    		"L",pp[2].x+dx, pp[2].y+dy,
	    		"L",pp[3].x+dx, pp[3].y+dy,
	    		"L",pp[4].x+dx, pp[4].y+dy,
	    		"L",pp[5].x+dx, pp[5].y+dy,"Z"]);
	    e0.attr({"fill":c0, "stroke-width":0});

	    var e6=paper.path([
	    		"M",pp[0].x+dx+(cx-pp[0].x)/4, pp[0].y+dy+(cy-pp[0].y)/4,
	    		"L",pp[1].x+dx+(cx-pp[1].x)/4, pp[1].y+dy+(cy-pp[1].y)/4,
	    		"L",pp[2].x+dx+(cx-pp[2].x)/4, pp[2].y+dy+(cy-pp[2].y)/4,
	    		"L",pp[3].x+dx+(cx-pp[3].x)/4, pp[3].y+dy+(cy-pp[3].y)/4,
	    		"L",pp[4].x+dx+(cx-pp[4].x)/4, pp[4].y+dy+(cy-pp[4].y)/4,
	    		"L",pp[5].x+dx+(cx-pp[5].x)/4, pp[5].y+dy+(cy-pp[5].y)/4,"Z"]);
	    e6.attr({"fill":color, "stroke-width":0});

	    return paper.setFinish();
	}
}


function GridIsoHex_ShapeFramedLight(parent) {
    this.super = GridIsoHex_BasicShapeFramed;
    this.super(parent);
    this.frameLight = 0.15;
}


function GridIsoHex_ShapeFramedDark(parent) {
    this.super = GridIsoHex_BasicShapeFramed;
    this.super(parent);
    this.frameLight = -0.15;
}


function GridIsoHex() {
	this.cellSize=24;
	this.gridThickness=1;
	this.gridColor=gridLineColor;
	this.name="iso-hex";

	this._createGridLine=function(paper, pathArray, stroke_dash_array) {
		var path=paper.path(pathArray);
        path.attr({
            "stroke":this.gridColor,
			"stroke-width": this.gridThickness
        })
        path.node.setAttribute("stroke-dasharray",stroke_dash_array);
	}

	this.paintGrid=function(paper) {  // ISO
	    var paperHeight=paper.height;
	    var paperWidth=paper.width;
		var sideLength=this.cellSize/2;
		var halfWidth=sideLength*sin60;
		var dy=sideLength*cos60;

		stroke_dash_array=sideLength+","+this.cellSize;

		for (x=0; x<paper.width; x+=halfWidth*2) {
		    this._createGridLine(
		    	paper,
		    	["M ",x, dy,"V",paper.height],
		    	stroke_dash_array);
		}

		for (x=halfWidth; x<paper.width; x+=halfWidth*2) {
		    this._createGridLine(
		    	paper,
		    	["M",x, 2*dy+sideLength,"V",paper.width],
		    	stroke_dash_array);
		}

		var slantedLinesStep=2*dy+2*sideLength;
		var hexBehind=Math.floor(paperWidth/slantedLinesStep);

		for (y=dy+sideLength-hexBehind*slantedLinesStep; y<paper.height; y+=slantedLinesStep) {
		    this._createGridLine(
		    	paper,
		    	["M",0, y,"L",paperWidth, y+paperHeight*tan30],
		    	stroke_dash_array);
		}

		for (y=0-hexBehind*slantedLinesStep; y<paper.height; y+=slantedLinesStep) {
            this._createGridLine(
            	paper,
            	["M",halfWidth, y,"L", halfWidth+paperWidth, y+paperWidth*tan30],
            	stroke_dash_array);
        }

        for (y=dy+sideLength-hexBehind*slantedLinesStep; y<paper.height; y+=slantedLinesStep) {
            this._createGridLine(
            	paper,
            	["M",halfWidth*2, y,"L",halfWidth*2+paperWidth, y+paperWidth*tan30,],
            	stroke_dash_array);
        }


		for (y=dy; y<paper.height+hexBehind*slantedLinesStep; y+=slantedLinesStep) {
            this._createGridLine(
            	paper,
            	["M",0, y, "L", paperWidth, y-paperWidth*tan30],
            	stroke_dash_array);
        }

        for (y=2*dy+sideLength; y<paper.height+hexBehind*slantedLinesStep; y+=slantedLinesStep) {
            this._createGridLine(
            	paper,
            	["M",halfWidth, y, "L", halfWidth+paperWidth, y-paperWidth*tan30],
            	stroke_dash_array);
        }

        for (y=dy; y<paper.height+hexBehind*slantedLinesStep; y+=slantedLinesStep) {
            this._createGridLine(
            	paper,["M",2*halfWidth, y, "L", 2*halfWidth+paperWidth, y-paperWidth*tan30],
            	stroke_dash_array);
        }
	}

	this.pointToCell=function(x,y) {  // ISO
		sideLength=this.cellSize/2;
		var triangleCell=pointToIsoTriangleCoord(x,y,sideLength);
		if (triangleCell.col<0) {
			return {col:-1, row:-1};
		}

		if (triangleCell.col % 2 == 0) {
			var triada=Math.floor(triangleCell.row/3);
			if (triada % 2 == 0) {
				return {row:triada, col: Math.floor(triangleCell.col / 2)}
			} else {
				return {row: triada, col: Math.floor(triangleCell.col / 2) - 1}
			}
		} else {
			var triada=Math.floor(triangleCell.row/3);
			if (triada % 2 == 0) {
				return {row: triada, col: Math.floor(triangleCell.col/2)}
			} else {
				return {row: triada, col: Math.floor(triangleCell.col/2)}
			}
		}
	}

	this.getCellRect=function(col, row) {  // ISO
		sideLength=this.cellSize/2;
		return {
			top: (sideLength+sideLength*cos60)*row,
			left: col*2*sideLength*sin60+(row % 2 == 0 ? 0 : sideLength*sin60),
			height: sideLength+2*sideLength*cos60,
			width: 2*sideLength*sin60
		}
	}

	this.nearestSameCell=function(col, row, nearCol, nearRow) {
		return {
			col: nearCol,
			row: nearRow
		};
	}

	this.getAdjacentCells = function(col, row) {  // ISO
		if (row % 2 == 0) {
			return [
				{row: row - 1, col: col - 1},
				{row: row, col: col - 1},
				{row: row + 1, col: col - 1},
				{row: row - 1, col: col},
				{row: row + 1, col: col},
				{row: row, col: col + 1}
			]
		} else {
			return [
				{row: row - 1, col: col + 1},
				{row: row, col: col + 1},
				{row: row + 1, col: col + 1},
				{row: row - 1, col: col},
				{row: row + 1, col: col},
				{row: row, col: col - 1}
			]
		}
	}

	this.isCellInsideWorkspace = function(col, row) {  // ISO
		var colWidth=this.cellSize*sin60;
		var rowCount=(this.workspaceHeight-this.cellSize)/(this.cellSize/2 + this.cellSize/2*cos60);
		var colCount=this.workspaceWidth/colWidth;
		return col>=0 && col<colCount && row>=0 && row<rowCount;
	}

	this.specialPasteShift=function(cells, baseCol, baseRow, pasteCol, pasteRow) {  // ISO ???
		var shiftRow=pasteRow-baseRow;
		var shiftCol=pasteCol-baseCol;
		var result=[];

		var baseCellLeft=(baseRow % 2) == 0;
		var pasteCellLeft=(pasteRow % 2) == 0;
		var colAddition=0;
		if (baseCellLeft && !pasteCellLeft) {
			colAddition=1;
		} else if (!baseCellLeft && pasteCellLeft) {
			colAddition=-1;
		}

		for (var i=0; i<cells.length; i++) {
			var cc=cells[i];

			var shiftedRow=cc.row+shiftRow;
			var shiftedCol=cc.col+shiftCol+((cc.row+shiftRow-pasteRow)%2)*colAddition;
			if (shiftedCol>=0) {
				result.push({
					row: shiftedRow,
					col: shiftedCol,
					shapeName: cc.shapeName,
					color: cc.color
				})
			}
		}

		return result;
	}

	this.shapes={
		// "empty": new GridHex_ShapeEmpty(this),
		"flat": new GridIsoHex_ShapeFlat(this),
		"diamond": new GridIsoHex_ShapeDiamond(this),
		"jewel": new GridIsoHex_ShapeJewel(this),
		"cube": new GridIsoHex_ShapeCube(this),
		'frame4u': new GridIsoHex_ShapeFramedLight(this),
		'frame4d': new GridIsoHex_ShapeFramedDark(this)
	};

	this.shapesToolbar = [
		// ['empty'],
		['flat', 'diamond', 'jewel', 'cube'],
		['frame4u', 'frame4d']
	]

	this.internalShapes={
	    "selected": new GridIsoHex_ShapeSelected(this)
	}

	this.shiftLeft={  // ISO
	    cell_dy:0,
	    cell_dx:-1,
	    dy: 0,
	    dx: -this.cellSize*sin60
	}

	this.shiftRight={  // ISO
	    cell_dy:0,
	    cell_dx:1,
	    dy:0,
	    dx: this.cellSize*sin60
	}

	this.shiftUp={  // ISO
	    cell_dy:-2,
	    cell_dx:0,
	    dy: -this.cellSize-this.cellSize*cos60,
	    dx: 0
	}

	this.shiftDown={  // ISO
	    cell_dy:2,
	    cell_dx:0,
	    dy: this.cellSize+this.cellSize*cos60,
	    dx: 0
	}
}

// Register grid
gridFactory["iso-hex"]=function() {
	return new GridIsoHex();
}

