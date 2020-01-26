/*
 * Diamond grid
 */

function GridDiamond_Points(col, row, cellSize) {
    var dSub = row;
    var dSum = col * 2;
    if (dSub % 2 != 0) {
        dSum += 1;
    }

    var d2 = (dSum - dSub) / 2;
    var d1 = dSub + d2;

    var x1 = d1 * cellSize + cellSize / 2;
    var x2 = d2 * cellSize + cellSize / 2;

    var x = (x1 + x2) / 2;
    var y = x1 - x;

    var halfCell = cellSize / 2;

    return [
        {x: x, y: y},
        {x: x + halfCell, y: y + halfCell},
        {x: x, y: y + cellSize},
        {x: x - halfCell, y: y + halfCell}
    ]
}

function createSvgDiamondPath(pathPoints, dx, dy) {
    return [
		"M", pathPoints[0].x+dx, pathPoints[0].y+dy,
		"L", pathPoints[1].x+dx, pathPoints[1].y+dy,
        "L", pathPoints[2].x+dx, pathPoints[2].y+dy, 
        "L", pathPoints[3].x+dx, pathPoints[3].y+dy, 
        "Z"
	]
}

function GridDiamond_ShapeEmpty(parent) {
	this.name="empty";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var points=GridDiamond_Points(col, row, parent.cellSize);
		var element=paper.path(createSvgDiamondPath(points, dx, dy));
	    element.attr({"stroke":"#808080"});
	    return element;
	}   
}

function GridDiamond_ShapeFlat(parent) {
	this.name="flat";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var points=GridDiamond_Points(col, row, parent.cellSize);
		var element=paper.path(createSvgDiamondPath(points, dx, dy))
		element.attr({"fill":color, "stroke-width":0})
		return element;
	}
}

function GridDiamond_ShapeSelected(parent) {
	this.name="selected";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var points=GridDiamond_Points(col, row, parent.cellSize);
		var element=paper.path(createSvgDiamondPath(points, dx, dy))
		element.attr({
			"fill":"url('/img/selection-hatch.png')", 
			"fill-opacity": 0.5,
			"stroke-width":0})
		return element;
	}
}

function GridDiamond() {
	this.cellSize=24;
	this.name="diamond";
	
	this._createGridLine=function(paper, pathArray) {
		var path=paper.path(pathArray);
        path.attr({
            "stroke":gridLineColor,
        })
	}
	
	this.paintGrid=function (paper) {
		for (x=this.cellSize/2; x<paper.width+paper.height; x+=this.cellSize) {
			this._createGridLine(paper,["M", x, 0, "L", x-paper.height, paper.height]);
		}
		
		for (x=this.cellSize/2-Math.floor(paper.height/this.cellSize)*this.cellSize; x<paper.width; x+=this.cellSize) {
			this._createGridLine(paper,["M", x, 0, x+paper.height, paper.height]);
		}
	}
	
	this.pointToCell=function(x,y) {
        var d1 = Math.floor((x + y - this.cellSize / 2) / this.cellSize);
        var d2 = Math.floor((x - y - this.cellSize / 2) / this.cellSize + 1);

        return {
            col: Math.floor((d1 + d2) / 2), 
            row: d1 - d2
        }
	}
	
	this.getCellRect=function(col, row) {
        var points = GridDiamond_Points(col, row, this.cellSize);
	    return {
	        left: points[3].x,
	        top: points[0].y,
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
	    var cellType = col % 4;
	    if (cellType==0) {
	        return [
	            {col: col+3, row: row-1},
	            {col: col+1, row: row},
	            {col: col+2, row: row}
	        ]
	    } else if (cellType==1) {
            return [
            	{col: col-3, row: row},
	            {col: col-1, row: row},
	            {col: col+2, row: row}
            ]
	    } else if (cellType==2) {
            return [
            	{col: col+3, row: row},
	            {col: col-2, row: row},
	            {col: col+1, row: row}
            ]
	    } else if (cellType==3) {
            return [
            	{col: col-3, row: row+1},
	            {col: col-2, row: row},
	            {col: col-1, row: row}
            ]
	    }
	}

	this.isCellInsideWorkspace = function(col, row) {
		var colCount=this.workspaceWidth/this.cellSize*4;
		var rowCount=this.workspaceHeight/this.cellSize;
		return col>=0 && col<colCount && row>=0 && row<rowCount;
	}
		
	this.shapes={
		"flat": new GridDiamond_ShapeFlat(this)
	}

	this.shapesToolbar = [
		[/* 'empty', */ 'flat']
	]
	
	this.internalShapes={
	    "selected": new GridDiamond_ShapeSelected(this)
	}
	
	this.shiftLeft={
	    cell_dx:-4,
	    cell_dy:0,
	    dx: -this.cellSize,
	    dy: 0
	}
	
	this.shiftRight={
	    cell_dx:4,
	    cell_dy:0,
	    dx: this.cellSize,
	    dy: 0
	}
	
	this.shiftUp={
	    cell_dx:0,
	    cell_dy:-4,
	    dx: 0,
	    dy: -this.cellSize
	}
	
	this.shiftDown={
	    cell_dx:0,
	    cell_dy:4,
	    dx:0,
	    dy: this.cellSize
	}
}

// Register grid
gridFactory["diamond"]=function() {
	return new GridDiamond();
}

