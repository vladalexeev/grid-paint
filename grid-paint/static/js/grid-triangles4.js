/*
 * 4 triangle grid
 */

function GridTriangles4_TrianglePoints(col, row, cellSize) {
	var squareCol=Math.floor(col/4);
	var innerTriangle=col % 4;
	
	var squareTop=row*cellSize;
	var squareLeft=squareCol*cellSize;
	var centerX=squareLeft+cellSize/2;
	var centerY=squareTop+cellSize/2;
	
	if (innerTriangle==0) {
		return [
			{x: squareLeft, y: squareTop},
			{x: squareLeft+cellSize, y: squareTop},
			{x: centerX, y: centerY}];
	} else if (innerTriangle==1) {
		return [
			{x: squareLeft, y: squareTop+cellSize},
			{x: squareLeft, y: squareTop},
			{x: centerX, y: centerY}];

	} else if (innerTriangle==2) {
		return [
			{x: squareLeft+cellSize, y: squareTop},
			{x: squareLeft+cellSize, y: squareTop+cellSize},
			{x: centerX, y: centerY}];
	} else { //innerTriangle==3
		return [
			{x: squareLeft+cellSize, y: squareTop+cellSize},
			{x: squareLeft, y: squareTop+cellSize},
			{x: centerX, y: centerY}];
	}
}

function GridTriangles4_ShapeEmpty(parent) {
	this.name="empty";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var points=GridTriangles4_TrianglePoints(col, row, parent.cellSize);
		var element=paper.path(createSvgTrianglePath(points, dx, dy));
	    element.attr({"stroke":"#808080"});
	    return element;
	}   
}

function GridTriangles4_ShapeFlat(parent) {
	this.name="flat";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var points=GridTriangles4_TrianglePoints(col, row, parent.cellSize);
		var element=paper.path(createSvgTrianglePath(points, dx, dy))
		element.attr({"fill":color, "stroke-width":0})
		return element;
	}
}

function GridTriangles4_ShapeSelected(parent) {
	this.name="selected";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var points=GridTriangles4_TrianglePoints(col, row, parent.cellSize);
		var element=paper.path(createSvgTrianglePath(points, dx, dy))
		element.attr({
			"fill":"url('/img/selection-hatch.png')", 
			"fill-opacity": 0.5,
			"stroke-width":0})
		return element;
	}
}

function GridTriangles4() {
	this.cellSize=24;
	this.gridThickness=1;
	this.gridColor=gridLineColor;
	this.name="triangles4";
	
	this._createGridLine=function(paper, pathArray) {
		var path=paper.path(pathArray);
        path.attr({
			"stroke":this.gridColor,
			"stroke-width": this.gridThickness
        })
	}
	
	this.paintGrid=function (paper) {
		for (var y=0; y<paper.height; y+=this.cellSize) {
			this._createGridLine(paper,["M",0,y,"L",paper.width,y]);
		}
		
		for (var x=0; x<paper.width; x+=this.cellSize) {
			this._createGridLine(paper,["M",x,0,"L",x,paper.height]);
		}
		
		for (x=this.cellSize; x<paper.width+paper.height; x+=this.cellSize) {
			this._createGridLine(paper,["M", x, 0, "L", x-paper.height, paper.height]);
		}
		
		for (x=-Math.floor(paper.height/this.cellSize)*this.cellSize; x<paper.width; x+=this.cellSize) {
			this._createGridLine(paper,["M", x, 0, x+paper.height, paper.height]);
		}
	}
	
	this.pointToCell=function(x,y) {
        var squareCol=Math.floor(x/this.cellSize);
        var squareRow=Math.floor(y/this.cellSize);
        
        var xx=x-squareCol*this.cellSize;
        var yy=y-squareRow*this.cellSize;
        
        var mainDiagPos=xx-yy;
        var subDiagPos=xx-(this.cellSize-yy);
        
        if (mainDiagPos>=0 && subDiagPos<0) {
        	return {col: squareCol*4, row: squareRow};	
        } else if (mainDiagPos>=0 && subDiagPos>=0) {
        	return {col: squareCol*4+2, row: squareRow};
        } else if (mainDiagPos<0 && subDiagPos>=0) {
        	return {col: squareCol*4+3, row: squareRow};
        } else { //mainDiagPos<0 && subDiagPos<0
        	return {col: squareCol*4+1, row: squareRow};
        }
        	    
        
	}
	
	this.getCellRect=function(col, row) {
	    return {
	        left: Math.floor(col/4)*this.cellSize,
	        top: row*this.cellSize,
	        width: this.cellSize,
	        height: this.cellSize
	    }
	}
	
	this.nearestSameCell=function(col, row, nearCol, nearRow) {
		return {
			col: Math.floor(nearCol / 4)*4 + (col % 4),
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
	    // "empty": new GridTriangles4_ShapeEmpty(this),
		"flat": new GridTriangles4_ShapeFlat(this)
	}

	this.shapesToolbar = [
		[/* 'empty', */ 'flat']
	]
	
	this.internalShapes={
	    "selected": new GridTriangles4_ShapeSelected(this)
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
gridFactory["triangles4"]=function() {
	return new GridTriangles4();
}

