/*
 * Diamond grid
 */


function GridDiamond_Points(col, row, cellSize) {
    var dSub = row * 2;
    var dSum = col;
    if (dSum % 2 != 0) {
        dSub += 1;
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

function GridDiamond_ShapeDiamond(parent) {
	this.name = "diamond";
	this.parent = parent;
	this.paint = function(paper, col, row, color, dx, dy) {
		var points = GridDiamond_Points(col, row, parent.cellSize);
		var cx = points[0].x;
		var cy = points[1].y;
		var c=hexToHsl(color);

		paper.setStart();
				
		var c1 = hslToHex(c.h, c.s, c.l+0.2);
		var e1 = paper.path([
			"M", points[0].x + dx, points[0].y + dy,
			"L", cx + dx, cy + dy,
			"L", points[3].x + dx, points[3].y + dy,
			"Z"]);
		e1.attr({"fill":c1, "stroke-width":0});
				
		var c2 = hslToHex(c.h, c.s, c.l+0.1);
		var e2 = paper.path([
			"M", points[0].x + dx, points[0].y + dy,
			"L", cx + dx, cy + dy,
			"L", points[1].x + dx, points[1].y + dy,
			"Z"])
		e2.attr({"fill":c2, "stroke-width":0});
				
		var c3 = hslToHex(c.h, c.s, c.l-0.1);
		var e3 = paper.path([
			"M", points[2].x + dx, points[2].y + dy,
			"L", cx + dx, cy + dy,
			"L", points[3].x + dx, points[3].y + dy,
			"Z"])
		e3.attr({"fill":c3, "stroke-width":0});
				
		var c4 = hslToHex(c.h, c.s, c.l-0.2);
		var e4 = paper.path([
			"M", points[1].x + dx, points[1].y + dy,
			"L", cx + dx, cy + dy,
			"L", points[2].x + dx, points[2].y + dy,
			"Z"])
		e4.attr({"fill":c4, "stroke-width":0});
		return paper.setFinish();
	}
}

function GridDiamond_ShapeJewel(parent) {
	this.name = "jewel";
	this.parent = parent;
	this.paint = function(paper, col, row, color, dx, dy) {
		var points = GridDiamond_Points(col, row, parent.cellSize);
		var facet = parent.cellSize / 4;
		var points2 = [
			{x: points[0].x, y: points[0].y + facet},
			{x: points[1].x - facet, y: points[1].y},
			{x: points[2].x, y: points[2].y - facet},
			{x: points[3].x + facet, y: points[3].y}
		]
		var c=hexToHsl(color);

		paper.setStart();
				
		var c1=hslToHex(c.h, c.s, c.l+0.2);
		var e1=paper.path([
			"M", points[0].x + dx, points[0].y + dy,
			"L", points2[0].x + dx, points2[0].y + dy,
			"L", points2[3].x + dx, points2[3].y + dy,
			"L", points[3].x + dx, points[3].y + dy,
			"Z"]);
		e1.attr({"fill":c1, "stroke-width":0});
				
		var c2=hslToHex(c.h, c.s, c.l+0.1);
		var e2=paper.path([
			"M", points[0].x + dx, points[0].y + dy,
			"L", points2[0].x + dx, points2[0].y + dy,
			"L", points2[1].x + dx, points2[1].y + dy,
			"L", points[1].x + dx, points[1].y + dy,
			"Z"])
		e2.attr({"fill":c2, "stroke-width":0});
				
		var c3=hslToHex(c.h, c.s, c.l-0.1);
		var e3=paper.path([
			"M", points[2].x + dx, points[2].y + dy,
			"L", points2[2].x + dx, points2[2].y + dy,
			"L", points2[3].x + dx, points2[3].y + dy,
			"L", points[3].x + dx, points[3].y + dy,
			"Z"])
		e3.attr({"fill":c3, "stroke-width":0});
				
		var c4=hslToHex(c.h, c.s, c.l-0.2);
		var e4=paper.path([
			"M", points[1].x + dx, points[1].y + dy,
			"L", points2[1].x + dx, points2[1].y + dy,
			"L", points2[2].x + dx, points2[2].y + dy,
			"L", points[2].x + dx, points[2].y + dy,
			"Z"])
		e4.attr({"fill":c4, "stroke-width":0});

		var e5=paper.path([
			"M", points2[0].x + dx, points2[0].y + dy,
			"L", points2[1].x + dx, points2[1].y + dy,
			"L", points2[2].x + dx, points2[2].y + dy,
			"L", points2[3].x + dx, points2[3].y + dy,
			"Z"])
		e5.attr({"fill":color, "stroke-width":0});

		return paper.setFinish();
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

function GridDiamond_BasicShapeFramed(parent) {
	this.parent = parent;
	this.frameLight = 0;
	this.paint=function(paper, col, row, color, dx, dy) {
		var points = GridDiamond_Points(col, row, parent.cellSize);
		var c = hexToHsl(color);
		paper.setStart();

        var c1 = hslToHex(c.h, c.s, c.l+this.frameLight);
        var e1 = paper.path(createSvgDiamondPath(points, dx, dy));
		e1.attr({"fill":c1, "stroke-width":0})
		
		var frame = this.parent.cellSize * 0.1;
		var points2 = [
			{x: points[0].x, y: points[0].y + frame},
			{x: points[1].x - frame, y: points[1].y},
			{x: points[2].x, y: points[2].y - frame},
			{x: points[3].x + frame, y: points[3].y}
		]

        var e4=paper.path(createSvgDiamondPath(points2, dx, dy))
        e4.attr({"fill":color, "stroke-width":0})

        return paper.setFinish();
	}
}

function GridDiamond_ShapeFramedDark(parent) {
    this.super = GridDiamond_BasicShapeFramed;
    this.super(parent);
    this.frameLight = - 0.15;
}

function GridDiamond_ShapeFramedLight(parent) {
    this.super = GridDiamond_BasicShapeFramed;
    this.super(parent);
    this.frameLight = 0.15;
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
		
		var col = d1 + d2;
		var row = Math.floor((d1 - d2) / 2);

        return {
            col: col, 
            row: row
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
		if (col % 2 == 0) {
			return [
				{col: col - 1, row: row - 1},
				{col: col + 1, row: row - 1},
				{col: col - 1, row: row},
				{col: col + 1, row: row}
			]
		} else {
			return [
				{col: col - 1, row: row},
				{col: col + 1, row: row},
				{col: col - 1, row: row + 1},
				{col: col + 1, row: row + 1}
			]
		}
	}

	this.isCellInsideWorkspace = function(col, row) {
		var cellRect = this.getCellRect(col, row);
		return cellRect.left >= 0 && cellRect.top >= 0 &&
			cellRect.left + cellRect.width < this.workspaceWidth &&
			cellRect.top + cellRect.height < this.workspaceHeight;
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
		"flat": new GridDiamond_ShapeFlat(this),
		"diamond": new GridDiamond_ShapeDiamond(this),
		"jewel": new GridDiamond_ShapeJewel(this),
		"frame10d": new GridDiamond_ShapeFramedDark(this),
		"frame10u": new GridDiamond_ShapeFramedLight(this)
	}

	this.shapesToolbar = [
		[/* 'empty', */ 'flat', 'jewel', 'diamond'],
		['frame10d', 'frame10u']
	]
	
	this.internalShapes={
	    "selected": new GridDiamond_ShapeSelected(this)
	}
	
	this.shiftLeft={
	    cell_dx:-2,
	    cell_dy:0,
	    dx: -this.cellSize,
	    dy: 0
	}

	this.shiftRight={
	    cell_dx:2,
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
}

// Register grid
gridFactory["diamond"]=function() {
	return new GridDiamond();
}

